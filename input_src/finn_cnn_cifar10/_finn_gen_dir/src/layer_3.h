#include "../host/finn-hlslib/bnn-library.h"

void layer_3 (
        hls::stream<ap_uint<32>> & Input_1,
        hls::stream<ap_uint<128>> & Output_1
        );
#pragma map_target = HW
