#include "../host/finn-hlslib/bnn-library.h"

void layer_5 (
        hls::stream<ap_uint<8>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        );
#pragma map_target = HW
