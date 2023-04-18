
#define AP_INT_MAX_W 216

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "mva_0_thresh.h"

// defines for network parameters
#define MW1 27
#define MH1 64
#define SIMD1 27
#define PE1 8
#define WMEM1 8
#define TMEM1 8
#define numReps 900

void mva_0(hls::stream<ap_uint<216>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_0_params.h"
#pragma HLS ARRAY_PARTITION variable=weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1, MH1, SIMD1, PE1, 1, Slice<ap_int<8>>, Slice<ap_uint<1>>, Recast<Binary>>
                (in0, out, weights, threshs, numReps, ap_resource_lut());
}
