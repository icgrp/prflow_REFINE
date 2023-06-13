
#define AP_INT_MAX_W_lab_sel_0 16

#include "bnn-library.h"

// includes for network parameters
#include "maxpool.h"

// defines for network parameters


void lab_sel_0(hls::stream<ap_uint<1*16>> &in0,
                hls::stream<ap_uint<8> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
LabelSelect_Batch<10, 1, 1, ap_int<16>, ap_uint<8> > (in0, out, 1);
}
