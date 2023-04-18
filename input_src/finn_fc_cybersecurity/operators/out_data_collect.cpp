#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"


void out_data_collect (
        hls::stream<ap_uint<1> > & Input_1,
        hls::stream<ap_uint<512> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    ap_uint<32> in_tmp;
    ap_uint<512> out_tmp;

    // num of data is 1000
    int out_idx = 0;
    for (int i = 0; i < 1000; i++){
        in_tmp = Input_1.read();
        out_tmp(out_idx,out_idx) = in_tmp(0,0);
        if(out_idx == 511){
            Output_1.write(out_tmp);
            out_tmp = 0; // reset
            out_idx = 0; // reset
        }
        else{
            out_idx = out_idx + 1;            
        }
        std::cout << "i in output: " << i << std::endl;        
    }
    Output_1.write(out_tmp);
}

