#include "../host/finn-hlslib/bnn-library.h"

void out_data_collect (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<512> > & Output_1
        );
#pragma map_target = HW