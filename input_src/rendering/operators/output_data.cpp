#include "../host/typedefs.h"

void output_data(
    hls::stream<ap_uint<32>> & Input_1,
    hls::stream<ap_uint<256>> & Output_1)

{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
  #pragma HLS INLINE off

  for (int i=0; i<MAX_X; i++){

    for(int j=0; j<MAX_Y/4; j+=8){ // MAX_Y/4 => 4 = 32/8, 8 = 256/32
      ap_uint<256> out_tmp;
      ap_uint<32> tmp;
#pragma HLS PIPELINE II=1
      for(int l = 0; l < 8; l++){ // 8 = 256/32
        tmp = Input_1.read();
        out_tmp(l*32+31, l*32) = tmp;
      }
      Output_1.write(out_tmp);
    }


  }
}
