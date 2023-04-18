#include "../host/finn-hlslib/bnn-library.h"

void mva_3(hls::stream<ap_uint<2>> &Input_1,
            hls::stream<ap_uint<1>> &Output_1);
#pragma map_target = HW