#include "../host/finn-hlslib/bnn-library.h"
#include "../host/typedefs.h"


void data_transfer (
        hls::stream<ap_uint<512> > & Input_1,
        hls::stream<ap_uint<64> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    bit512 in_tmp;
    ap_uint<64> out_tmp;

    // INPUT_SIZE = 7840
    for ( int i = 0; i < 7840; i++){
        in_tmp = Input_1.read();
        for (int j = 0; j < 8; j++){ // 8 = 512/64
            out_tmp = in_tmp(64*j+63, 64*j+0);
            Output_1.write(out_tmp);
        }
    }
}
