#include "../host/typedefs.h"


void dotProduct_i7(
  hls::stream<ap_uint<64> > & Input_1, // from data_in_redir
  hls::stream<ap_uint<32> > & Input_2, // from sigmoid
  hls::stream<ap_uint<32> > & Output_1, // to sigmoid
  hls::stream<ap_uint<64> > & Output_2 // to data_2_1
)
{

#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Input_2
#pragma HLS INTERFACE axis register port=Output_1
#pragma HLS INTERFACE axis register port=Output_2


  const int unroll_factor = PAR_FACTOR_DEC;
  static FeatureType param[NUM_FEATURES/NUM_OPS];
  FeatureType grad[NUM_FEATURES/NUM_OPS];
  static DataType feature[NUM_FEATURES/NUM_OPS];
  FeatureType scale;
  FeatureType prob;
  #pragma HLS array_partition variable=param cyclic factor=unroll_factor
  #pragma HLS array_partition variable=feature cyclic factor=unroll_factor
  #pragma HLS array_partition variable=grad cyclic factor=unroll_factor
  static int odd_even = 0;
  static int num_train = 0;
  static int epoch;
  static int sb = 0;
  static LabelType training_label;
  bit64 in_tmp;
  bit32 out_tmp;

  if(odd_even == 0){
    in_tmp = Input_1.read();
    training_label(7,0) = in_tmp(7,0);

   READ_TRAINING_DATA: for (int i = 0; i < NUM_FEATURES / D_VECTOR_SIZE / NUM_OPS; i ++ ){
   //                                      1024           4
#pragma HLS PIPELINE II=1
  VectorFeatureType tmp_data;
  tmp_data = Input_1.read();
   READ_TRAINING_DATA_INNER: for (int j = 0; j < D_VECTOR_SIZE; j ++ ){
    feature[i * D_VECTOR_SIZE + j](DTYPE_TWIDTH-1, 0) = tmp_data((j+1)*DTYPE_TWIDTH-1, j*DTYPE_TWIDTH);
   }
   }

   FeatureType result = 0;
   DOT: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++){
#pragma HLS PIPELINE II=1
   DOT_INNER: for(int j = 0; j < PAR_FACTOR_DEC; j++){
     FeatureType term = param[i*PAR_FACTOR_DEC+j] * ((FeatureType)feature[i*PAR_FACTOR_DEC+j]);
     result = result + term;
   }
   }
    out_tmp(31, 0) = result(31, 0); 
   Output_1.write(out_tmp);
   odd_even = 1;
   return;
  }
  else{
   prob(31,0) = Input_2.read();
   scale = prob - ((FeatureType)training_label);

   GRAD: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++){
#pragma HLS PIPELINE II=1
   GRAD_INNER: for (int j = 0; j < PAR_FACTOR_DEC; j++){
     grad[i*PAR_FACTOR_DEC+j] = (scale * ((FeatureType) feature[i*PAR_FACTOR_DEC+j]));
   }
   }

   FeatureType step = STEP_SIZE;
   UPDATE: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++){
#pragma HLS PIPELINE II=1
   UPDATE_INNER: for (int j = 0; j < PAR_FACTOR_DEC; j++){
    FeatureType tmp;
    tmp = (-step) * grad[i*PAR_FACTOR_DEC+j];
    param[i*PAR_FACTOR_DEC+j] = param[i*PAR_FACTOR_DEC+j] + tmp;
   }
   }

   num_train++;
   if(num_train==NUM_TRAINING){
    num_train = 0;
    epoch++;
   }
   if(epoch==5){
    STREAM_OUT: for (int i = 0; i < NUM_FEATURES / F_VECTOR_SIZE / NUM_OPS; i ++ ){
#pragma HLS pipeline II=1
   bit64 tmp_data1;
   tmp_data1(31,0) = param[i * F_VECTOR_SIZE + 0](FTYPE_TWIDTH-1, 0);
   tmp_data1(63,32) = param[i * F_VECTOR_SIZE + 1](FTYPE_TWIDTH-1, 0);
   Output_2.write(tmp_data1);

    }
   }
   odd_even = 0;
   return;
  }
}