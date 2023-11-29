#include "../host/typedefs.h"


static int popcount(WholeDigitType x)
{
  // most straightforward implementation
  // actually not bad on FPGA
  int cnt = 0;
  for (int i = 0; i < 256; i ++ )
  {
#pragma HLS unroll
    cnt = cnt + x(i, i);
  }
  return cnt;
}

static void update_knn( WholeDigitType test_inst, WholeDigitType train_inst, int min_distances[K_CONST] )
{
#pragma HLS inline
#pragma HLS array_partition variable=min_distances complete dim=0


  // Compute the difference using XOR
  WholeDigitType diff = test_inst ^ train_inst;

  int dist = 0;

  dist = popcount(diff);

  int max_dist = 0;
  int max_dist_id = 0;
  int k = 0;

  // Find the max distance
  FIND_MAX_DIST: for ( int k = 0; k < K_CONST; ++k )
  {
    if ( min_distances[k] > max_dist )
    {
      max_dist = min_distances[k];
      max_dist_id = k;
    }
  }

  // Replace the entry with the max distance
  if ( dist < max_dist )
    min_distances[max_dist_id] = dist;

  return;
}


static void knn_vote_small(int knn_set[OP_SIZE * K_CONST],
                           int min_distance_list[K_CONST],
                           int label_list[K_CONST],
                           LabelType label_in)
{
#pragma HLS inline
#pragma HLS array_partition variable=knn_set complete dim=0
// final K nearest neighbors
#pragma HLS array_partition variable=min_distance_list complete dim=0
// labels for the K nearest neighbors
#pragma HLS array_partition variable=label_list complete dim=0

  int pos = 1000;

  // go through all the lanes
  // do an insertion sort to keep a sorted neighbor list
  LANES: for (int i = 0; i < OP_SIZE; i ++ )
  {
    INSERTION_SORT_OUTER: for (int j = 0; j < K_CONST; j ++ )
    {
      #pragma HLS pipeline
      pos = 1000;
      INSERTION_SORT_INNER: for (int r = 0; r < K_CONST; r ++ )
      {
        #pragma HLS unroll
        pos = ((knn_set[i*K_CONST+j] < min_distance_list[r]) && (pos > K_CONST)) ? r : pos;
      }

      INSERT: for (int r = K_CONST ;r > 0; r -- )
      {
        #pragma HLS unroll
        if(r-1 > pos)
        {
          min_distance_list[r-1] = min_distance_list[r-2];
          label_list[r-1] = label_list[r-2];
        }
        else if (r-1 == pos)
        {
          min_distance_list[r-1] = knn_set[i*K_CONST+j];
          label_list[r-1] = label_in;
        }
      }
    }
  }
}


#define NUM8 8
void update_knn_i8(hls::stream<ap_uint<32> > & Input_1, hls::stream<ap_uint<32> > & Output_1)
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

static WholeDigitType training_set [NUM_TRAINING / NUM_OPS];
const int unroll_factor = OP_SIZE;
#pragma HLS array_partition variable=training_set block factor=unroll_factor dim=0

static WholeDigitType test_instance;


static int knn_set[K_CONST*OP_SIZE];
#pragma HLS array_partition variable=knn_set complete dim=0

WholeDigitType data_temp;
static int index = 0;
bit32 tmp;


  if (index == 0)
  {
    //Store the local training set
    STORE_LOCAL: for(int i = 0; i < NUM_TRAINING / NUM_OPS; i++)
    {
#pragma HLS pipeline
    for(int j=IMAGE_WIDTH-1; j>0; j=j-32){
      training_set[i](j,j-31) = Input_1.read();
    }
  }

  //Transit the training sets for other pages
  TRANSFER_LOOP: for(int i = 0; i < NUM_TRAINING / NUM_OPS * (NUM_OPS - NUM8); i++)
  {
#pragma HLS pipeline
    for(int j=IMAGE_WIDTH-1; j>0; j=j-32){
      data_temp(j,j-31) = Input_1.read();
    }

    bit32 tmp;
    for(int j=IMAGE_WIDTH-1; j>0; j=j-32){
      tmp(31, 0) = data_temp.range(j,j-31);
      Output_1.write(tmp);
    }
  }
    index = 1;
  }

  for(int i=IMAGE_WIDTH-1; i>0; i=i-32){
    test_instance(i,i-31) = Input_1.read();
  }
  for(int i=IMAGE_WIDTH-1; i>0; i=i-32){
    tmp(31, 0) = test_instance.range(i,i-31);
    Output_1.write(tmp);
  }

  int min_distance_list[K_CONST];
  int label_list[K_CONST];

  OutputTmpType input_tmp1, input_tmp2;

  for(int i=OutputTmpWidth-1; i>0; i=i-32){
    input_tmp1(i,i-31) = Input_1.read();
  }

  for(int i=OutputTmpWidth-1; i>0; i=i-32){
    input_tmp2(i,i-31) = Input_1.read();
  }


  for(int i=0; i<K_CONST; i++)
  {
#pragma HLS unroll
    min_distance_list[i] = (int) input_tmp1(i*32+31, i*32);
    label_list[i] = (int) input_tmp2(i*32+31, i*32);
  }

  // Initialize the knn set
  SET_KNN_SET: for ( int i = 0; i < K_CONST * OP_SIZE ; ++i )
  {
#pragma HLS unroll
    // Note that the max distance is 256
    knn_set[i] = 256;
  }

  TRAINING_LOOP : for ( int i = 0; i < NUM_TRAINING / PAR_FACTOR; ++i )
  {
#pragma HLS pipeline
    LANES : for ( int j = 0; j < OP_SIZE; j++ )
    {
#pragma HLS unroll
      WholeDigitType training_instance = training_set[j * NUM_TRAINING / PAR_FACTOR + i];
      update_knn( test_instance, training_instance, &knn_set[j * K_CONST] );
    }
  }

  //update min_distance_list and label_list according to the new knn_set
  LabelType label_in = 7;
  knn_vote_small(knn_set, min_distance_list, label_list, label_in);

  OutputTmpType output_tmp1, output_tmp2;

  for(int i=0; i<K_CONST; i++)
  {
#pragma HLS unroll
    output_tmp1(i*32+31, i*32) = min_distance_list[i];
    output_tmp2(i*32+31, i*32) = label_list[i];
  }

  for(int i=OutputTmpWidth-1; i>0; i=i-32){
    tmp(31,0) = output_tmp1(i,i-31);
    Output_1.write(tmp);
  }

  for(int i=OutputTmpWidth-1; i>0; i=i-32){
    tmp(31,0) = output_tmp2(i,i-31);
    Output_1.write(tmp);
  }

  return;
}