/*===============================================================*/
/*                                                               */
/*                          sgd.cpp                              */
/*                                                               */
/*             Hardware function for spam filtering.             */
/*                                                               */
/*===============================================================*/

#include "../host/typedefs.h"
#include "../operators/data_in_redir.h"
#include "../operators/dotProduct_i1.h"
#include "../operators/dotProduct_i3.h"
#include "../operators/dotProduct_i5.h"
#include "../operators/dotProduct_i7.h"
#include "../operators/sigmoid.h"
#include "../operators/output_collect.h"


  // top-level function
  void top(
    hls::stream<ap_uint<256> > & Input_1,
  	hls::stream<ap_uint<256> > & Output_1
  )
  {
  #pragma HLS INTERFACE ap_hs port=Input_1
  #pragma HLS INTERFACE ap_hs port=Output_1


  	hls::stream<ap_uint<64>>  Output_1_redir("Output_1_redir");
  	hls::stream<ap_uint<64>>  Output_2_redir("Output_2_redir");
    hls::stream<ap_uint<64>>  Output_3_redir("Output_3_redir");
    hls::stream<ap_uint<64>>  Output_4_redir("Output_4_redir");

    hls::stream<ap_uint<32>>  Output_1_sigmoid("Output_1_sigmoid");
    hls::stream<ap_uint<32>>  Output_2_sigmoid("Output_2_sigmoid");
    hls::stream<ap_uint<32>>  Output_3_sigmoid("Output_3_sigmoid");
    hls::stream<ap_uint<32>>  Output_4_sigmoid("Output_4_sigmoid");

    hls::stream<ap_uint<32>>  Output_1_dot_1("Output_1_dot_1");
    hls::stream<ap_uint<64>>  Output_2_dot_1("Output_2_dot_1");

    hls::stream<ap_uint<32>>  Output_1_dot_3("Output_1_dot_3");
    hls::stream<ap_uint<64>>  Output_2_dot_3("Output_2_dot_3");

    hls::stream<ap_uint<32>>  Output_1_dot_5("Output_1_dot_5");
    hls::stream<ap_uint<64>>  Output_2_dot_5("Output_2_dot_5");

    hls::stream<ap_uint<32>>  Output_1_dot_7("Output_1_dot_7");
    hls::stream<ap_uint<64>>  Output_2_dot_7("Output_2_dot_7");


    for(int epoch = 0; epoch<NUM_EPOCHS; epoch++){
      printf("epoch = %d\n", epoch);
      data_in_redir(Input_1, Output_1_redir, Output_2_redir, Output_3_redir, Output_4_redir);

      TRAINING_INST: for( int training_id = 0; training_id < NUM_TRAINING; training_id ++ ){
        dotProduct_i1(Output_1_redir, Output_1_sigmoid, Output_1_dot_1, Output_2_dot_1);
        dotProduct_i3(Output_2_redir, Output_2_sigmoid, Output_1_dot_3, Output_2_dot_3);
        dotProduct_i5(Output_3_redir, Output_3_sigmoid, Output_1_dot_5, Output_2_dot_5);
        dotProduct_i7(Output_4_redir, Output_4_sigmoid, Output_1_dot_7, Output_2_dot_7);

        sigmoid(Output_1_dot_1, Output_1_dot_3, Output_1_dot_5, Output_1_dot_7, Output_1_sigmoid, Output_2_sigmoid, Output_3_sigmoid, Output_4_sigmoid);

        dotProduct_i1(Output_1_redir, Output_1_sigmoid, Output_1_dot_1, Output_2_dot_1);
        dotProduct_i3(Output_2_redir, Output_2_sigmoid, Output_1_dot_3, Output_2_dot_3);
        dotProduct_i5(Output_3_redir, Output_3_sigmoid, Output_1_dot_5, Output_2_dot_5);
        dotProduct_i7(Output_4_redir, Output_4_sigmoid, Output_1_dot_7, Output_2_dot_7);

        printf("training_id = %d\n", training_id);
      }
      if(epoch==4){
        output_collect(Output_2_dot_1, Output_2_dot_3, Output_2_dot_5, Output_2_dot_7, Output_1);
      }
    }
 }

  extern "C" {
  	void ydma (
  			bit64 * input1,
  			bit512 * input2,
  			bit64 * output1,
  			bit512 * output2,
  			int config_size,
  			int input_size,
  			int output_size,
        int num_total_cnt
  			)
  	{
  #pragma HLS INTERFACE m_axi port=input1 bundle=aximm1
  #pragma HLS INTERFACE m_axi port=input2 bundle=aximm2
  #pragma HLS INTERFACE m_axi port=output1 bundle=aximm1
  #pragma HLS INTERFACE m_axi port=output2 bundle=aximm2
  	#pragma HLS DATAFLOW

  	  bit64 v1_buffer[256];    //Local memory to store vector1
  	  #pragma HLS STREAM variable=v1_buffer depth=256

            hls::stream<ap_uint<256> > Input_1("Input_1_str");
            hls::stream<ap_uint<256> > Output_1("Output_str");

            for(int i=0; i<config_size; i++){
              v1_buffer[i] = input1[i];
              printf("input1[%d]\n", i);
            }
            for(int i=0; i<config_size; i++){ output1[i] = v1_buffer[i]; }


      	    for(int i=0; i<input_size;  i++){
              bit512 in_tmp = input2[i];
              Input_1.write(in_tmp(255,0));
              Input_1.write(in_tmp(511,256));
            }

            top(Input_1, Output_1);

            for(int i=0; i<output_size; i++){
              bit512 out_tmp;
              out_tmp(255,0) = Output_1.read();
              out_tmp(511,256) = Output_1.read();
              output2[i] = out_tmp;
            }
  	}

  }



