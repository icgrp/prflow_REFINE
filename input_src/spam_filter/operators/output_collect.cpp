#include "../host/typedefs.h"
void output_collect(
   hls::stream<ap_uint<64> > & Input_1,
   hls::stream<ap_uint<64> > & Input_2,
   hls::stream<ap_uint<64> > & Input_3,
   hls::stream<ap_uint<64> > & Input_4,
   hls::stream<ap_uint<256> > & Output_1
   )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Input_2
#pragma HLS INTERFACE axis register port=Input_3
#pragma HLS INTERFACE axis register port=Input_4
#pragma HLS INTERFACE axis register port=Output_1
ap_uint<256> out_tmp;

 static ap_uint<64> theta[NUM_FEATURES / 2];
  static ap_uint<32> counter=0;


 STREAM_IN_1: for (int i = 0; i < NUM_FEATURES / 8; i++){
#pragma HLS pipeline II=1
  theta[i] = Input_1.read();
 }
   
 STREAM_IN_2: for (int i = 0; i < NUM_FEATURES / 8; i++){
#pragma HLS pipeline II=1
  theta[i + NUM_FEATURES / 8] = Input_2.read();
 }

 STREAM_IN_3: for (int i = 0; i < NUM_FEATURES / 8; i++){
#pragma HLS pipeline II=1
  theta[i + (NUM_FEATURES / 8)*2] = Input_3.read();
 }

 STREAM_IN_4: for (int i = 0; i < NUM_FEATURES / 8; i++){
#pragma HLS pipeline II=1
  theta[i + (NUM_FEATURES / 8)*3] = Input_4.read();
 }


 STREAM_OUT: for (int i = 0; i < NUM_FEATURES / 2 / 4; i++){
#pragma HLS pipeline II=1
    for(int j=0; j<4; j++){
      out_tmp(j*64+63, j*64) = theta[4*i+j];
    }

    if (counter < NUM_FEATURES / 2/ 4){
      Output_1.write(out_tmp);

      counter++;
    }
 }
}
