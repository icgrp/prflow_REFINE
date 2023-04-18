#include "../host/finn-hlslib/bnn-library.h"

void layer_last (
        hls::stream<ap_uint<1> > & Input_1,
        hls::stream<ap_uint<8> > & Output_1
        );
#pragma map_target = HW