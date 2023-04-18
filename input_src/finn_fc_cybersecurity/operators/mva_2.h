#include "../host/finn-hlslib/bnn-library.h"

void mva_2(hls::stream<ap_uint<128>> &Input_1,
            hls::stream<ap_uint<2>> &Output_1);
#pragma map_target = HW