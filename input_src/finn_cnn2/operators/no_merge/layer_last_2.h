#include "../host/finn-hlslib/bnn-library.h"

void layer_last_2 (
        hls::stream<ap_uint<2>> & Input_1,
        hls::stream<ap_uint<256>> & Output_1
        );
#pragma map_target = HW
