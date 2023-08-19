#include "../host/typedefs.h"

void output_data(
    hls::stream<ap_uint<128>> & Input_1,
    hls::stream<ap_uint<128>> & Input_2,
    hls::stream<ap_uint<128>> & Input_3,
    hls::stream<ap_uint<128>> & Input_4,
    hls::stream<ap_uint<512>> & Output_1)

{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Input_2
#pragma HLS INTERFACE axis register port=Input_3
#pragma HLS INTERFACE axis register port=Input_4
#pragma HLS INTERFACE axis register port=Output_1
  #pragma HLS INLINE off

  for (int i=0; i<MAX_X; i++){

    RECV_4: for(int k=0; k<MAX_Y/16; k+=16){
      bit512 out_tmp;
      bit128 tmp;
#pragma HLS PIPELINE II=1
      for(int l = 0; l < 4; l++){
        tmp = Input_4.read();
        for(int out_i = 0; out_i < 4; out_i++){
          out_tmp(l*128+out_i*32+31, l*128+out_i*32) = tmp(out_i*32+31, out_i*32);
        }
      }
      Output_1.write(out_tmp);
    }

    RECV_3: for(int k=0; k<MAX_Y/16; k+=16){
      bit512 out_tmp;
      bit128 tmp;
#pragma HLS PIPELINE II=1
      for(int l = 0; l < 4; l++){
        tmp = Input_3.read();
        for(int out_i = 0; out_i < 4; out_i++){
          out_tmp(l*128+out_i*32+31, l*128+out_i*32) = tmp(out_i*32+31, out_i*32);
        }
      }
      Output_1.write(out_tmp);
    }

    RECV_2: for(int k=0; k<MAX_Y/16; k+=16){
      bit512 out_tmp;
      bit128 tmp;
#pragma HLS PIPELINE II=1
      for(int l = 0; l < 4; l++){
        tmp = Input_2.read();
        for(int out_i = 0; out_i < 4; out_i++){
          out_tmp(l*128+out_i*32+31, l*128+out_i*32) = tmp(out_i*32+31, out_i*32);
        }
      }
      Output_1.write(out_tmp);
    }

    RECV_1: for(int k=0; k<MAX_Y/16; k+=16){
      bit512 out_tmp;
      bit128 tmp;
#pragma HLS PIPELINE II=1
      for(int l = 0; l < 4; l++){
        tmp = Input_1.read();
        for(int out_i = 0; out_i < 4; out_i++){
          out_tmp(l*128+out_i*32+31, l*128+out_i*32) = tmp(out_i*32+31, out_i*32);
        }
      }
      Output_1.write(out_tmp);
    }


  }
}
