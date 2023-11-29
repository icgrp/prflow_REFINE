#include "../host/finn-hlslib/bnn-library.h"

void layer_2_1 (
        hls::stream<ap_uint<16>> & Input_1,
        hls::stream<ap_uint<16>> & Output_1
        );
#pragma map_target = HW
