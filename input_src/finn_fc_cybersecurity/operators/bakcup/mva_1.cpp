
#define AP_INT_MAX_W 128

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "thresh.h"

// defines for network parameters
#define MW1 64
 #define MH1 64

            #define SIMD1 64
 #define PE1 1
 #define WMEM1 64

            #define TMEM1 64
 #define numReps 1
#define WP1 2


void mva_1(
                    hls::stream<ap_uint<128>> &in0,
                    hls::stream<ap_uint<128>> &weights,
                    hls::stream<ap_uint<2>> &out
                    )
{
#pragma HLS INTERFACE axis port=in0 name=in0_V
#pragma HLS INTERFACE axis port=out name=out_V
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE axis port=weights name=weights_V
#pragma HLS stream depth=8 variable=weights
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Stream_Batch<MW1, MH1, SIMD1, PE1, Slice<ap_uint<2>>, Slice<ap_uint<2>>, Identity, ap_int<2> >
                (in0, out, weights, threshs, numReps, ap_resource_lut());
}
