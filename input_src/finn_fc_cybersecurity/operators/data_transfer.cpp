#include "../host/finn-hlslib/bnn-library.h"
#include "../host/typedefs.h"


void data_transfer (
        hls::stream<ap_uint<512> > & Input_1,
        hls::stream<ap_uint<32> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    bit512 in_tmp;
    ap_uint<608> out_tmp;

    // num of data is 1000
    for ( int i = 0; i < 1000; i++){
        in_tmp = Input_1.read();
        out_tmp(511,0) = in_tmp(511,0);
        in_tmp = Input_1.read();
        out_tmp(607,512) = in_tmp(95,0);

        for (int j = 0; j < 19; j++){
            Output_1.write(out_tmp(32*j+31,32*j));
        }

        std::cout << "i: " << i << std::endl;

    }
}

