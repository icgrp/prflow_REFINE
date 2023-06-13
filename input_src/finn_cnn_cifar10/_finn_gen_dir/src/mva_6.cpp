
#define AP_INT_MAX_W_mva_6 16

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_6_thresh.h"

// defines for network parameters
#define MW1_mva_6 256
#define MH1_mva_6 512
#define SIMD1_mva_6 16
#define PE1_mva_6 1
#define WMEM1_mva_6 8192
#define TMEM1_mva_6 512
#define numReps_mva_6 1

void mva_6(hls::stream<ap_uint<16>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_6_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_6_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_6, MH1_mva_6, SIMD1_mva_6, PE1_mva_6, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_6_weights, mva_6_threshs, numReps_mva_6, ap_resource_lut());
}
