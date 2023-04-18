#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"


void out_data_collect (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<512> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    ap_uint<8> in_tmp;
    ap_uint<512> out_tmp;


    int out_idx = 0;
    for (int i=0; i < 10; i++){ // total 640 tests
        for (int j = 0; j < 64; j++){ // 64 data fits in 512bits
            in_tmp = Input_1.read();
            out_tmp(8*j+7, 8*j) = in_tmp;
        }
        Output_1.write(out_tmp);
    }

}

