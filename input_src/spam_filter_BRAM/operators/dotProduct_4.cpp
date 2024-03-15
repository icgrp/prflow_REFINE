#include "../host/typedefs.h"

#define NUM_OPS 4 // should divide PAR_FACTOR defined in typedefs.h
#define PAR_FACTOR_DEC (PAR_FACTOR/NUM_OPS)

void dotProduct_4(
	hls::stream<ap_uint<64> > & Input_1, // from data_in_redir
	hls::stream<ap_uint<32> > & Input_2, // from sigmoid
	hls::stream<ap_uint<32> > & Output_1, // to sigmoid
	hls::stream<ap_uint<32> > & Output_2 // to data_2_1
	)
{

#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Input_2
#pragma HLS INTERFACE axis register port=Output_1
#pragma HLS INTERFACE axis register port=Output_2


  const int unroll_factor = PAR_FACTOR_DEC;
  static FeatureType param[NUM_FEATURES];
  FeatureType grad[NUM_FEATURES];
  static DataType feature[NUM_FEATURES];
  FeatureType scale;
  FeatureType prob;

	#pragma HLS bind_storage variable=param type=RAM_1P impl=BRAM
	#pragma HLS bind_storage variable=feature type=RAM_1P impl=BRAM
	#pragma HLS bind_storage variable=grad type=RAM_1P impl=BRAM

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
	  //printf("label: 0x%08x,\n", training_label.to_int());

	  READ_TRAINING_DATA: for (int i = 0; i < NUM_FEATURES / D_VECTOR_SIZE / NUM_OPS; i ++ )
	  //                                      2400           1
	  {
#pragma HLS PIPELINE off
		VectorFeatureType tmp_data;
		tmp_data = Input_1.read();
		READ_TRAINING_DATA_INNER: for (int j = 0; j < D_VECTOR_SIZE; j ++ )
		{
			feature[i * D_VECTOR_SIZE + j](DTYPE_TWIDTH-1, 0) = tmp_data((j+1)*DTYPE_TWIDTH-1, j*DTYPE_TWIDTH);
		}

	  }


	  FeatureType result = 0;
	  DOT: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++)
	  {
		#pragma HLS PIPELINE off
		DOT_INNER: for(int j = 0; j < PAR_FACTOR_DEC; j++)
		{
		  FeatureType term = param[i*PAR_FACTOR_DEC+j] * ((FeatureType)feature[i*PAR_FACTOR_DEC+j]);
		  result = result + term;
		}
	  }
          out_tmp(31, 0) = result(31, 0); 
	  Output_1.write(out_tmp);
	  //printf("0x%08x,\n", (unsigned int) result(31,0));
	  odd_even = 1;
	  return;

  }else{
	  prob(31,0) = Input_2.read();
	  //printf("0x%08x,\n", (unsigned int) prob(31,0));
	  scale = prob - ((FeatureType)training_label);

	  GRAD: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++)
	  {
		#pragma HLS PIPELINE off
		GRAD_INNER: for (int j = 0; j < PAR_FACTOR_DEC; j++)
		  grad[i*PAR_FACTOR_DEC+j] = (scale * ((FeatureType) feature[i*PAR_FACTOR_DEC+j]));
	  }

	  FeatureType step = STEP_SIZE;
	  UPDATE: for (int i = 0; i < NUM_FEATURES / PAR_FACTOR_DEC / NUM_OPS; i++)
	  {
		#pragma HLS PIPELINE off
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
		  STREAM_OUT: for (int i = 0; i < NUM_FEATURES / F_VECTOR_SIZE / NUM_OPS; i ++ )
		  {
			#pragma HLS pipeline off
			bit32 tmp_data1;
			bit32 tmp_data2;
			tmp_data1(31,0) = param[i * F_VECTOR_SIZE + 0](FTYPE_TWIDTH-1, 0);
			tmp_data2(31,0) = param[i * F_VECTOR_SIZE + 1](FTYPE_TWIDTH-1, 0);
			Output_2.write(tmp_data1);
			Output_2.write(tmp_data2);
		  }
	  }
	  odd_even = 0;
	  return;
  }

}