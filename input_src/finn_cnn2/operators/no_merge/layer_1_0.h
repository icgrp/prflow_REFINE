#include "../host/finn-hlslib/bnn-library.h"

void layer_1_0 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<64>> & Output_1
        );
#pragma map_target = HW
