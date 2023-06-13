#include "../host/finn-hlslib/bnn-library.h"

void layer_2 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<32>> & Output_1
        );
#pragma map_target = HW
