#include "../host/finn-hlslib/bnn-library.h"

void data_transfer (
        hls::stream<ap_uint<512> > & Input_1,
        hls::stream<ap_uint<32> > & Output_1
        );
#pragma map_target = HW