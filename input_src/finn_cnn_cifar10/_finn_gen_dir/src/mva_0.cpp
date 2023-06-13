
#define AP_INT_MAX_W_mva_0 216

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_0_thresh.h"

// defines for network parameters
#define MW1_mva_0 27
#define MH1_mva_0 64
#define SIMD1_mva_0 27
#define PE1_mva_0 8
#define WMEM1_mva_0 8
#define TMEM1_mva_0 8
#define numReps_mva_0 900

void mva_0(hls::stream<ap_uint<216>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_0_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_0_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_0, MH1_mva_0, SIMD1_mva_0, PE1_mva_0, 1, Slice<ap_int<8>>, Slice<ap_uint<1>>, Recast<Binary>>
                (in0, out, mva_0_weights, mva_0_threshs, numReps_mva_0, ap_resource_lut());
}
