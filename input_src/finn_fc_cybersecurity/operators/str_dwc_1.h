#include "../host/finn-hlslib/bnn-library.h"

void str_dwc_1 (
        hls::stream<ap_uint<2> > & Input_1,
        hls::stream<ap_uint<128> > & Output_1
        );
#pragma map_target = HW