#include "../host/finn-hlslib/bnn-library.h"
#include "../host/typedefs.h"


void data_transfer (
        hls::stream<ap_uint<512> > & Input_1,
        hls::stream<ap_uint<8> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    bit512 in_tmp;
    ap_uint<8> out_tmp;

    // INPUT_SIZE = 30720
    for ( int i = 0; i < 30720; i++){
        in_tmp = Input_1.read();
        for (int j = 0; j < 64; j++){ // 64 = 512/8
            out_tmp = in_tmp(8*j+7, 8*j+0);
            Output_1.write(out_tmp);
        }
        std::cout << "i: " << i << std::endl;
    }
}

