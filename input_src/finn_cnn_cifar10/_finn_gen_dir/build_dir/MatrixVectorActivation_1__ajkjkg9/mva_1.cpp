
#define AP_INT_MAX_W_mva_1 72

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_1_thresh.h"

// defines for network parameters
#define MW1_mva_1 576
#define MH1_mva_1 64
#define SIMD1_mva_1 72
#define PE1_mva_1 64
#define WMEM1_mva_1 8
#define TMEM1_mva_1 1
#define numReps_mva_1 784

void mva_1(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<64>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_1_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_1_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_1, MH1_mva_1, SIMD1_mva_1, PE1_mva_1, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_1_weights, mva_1_threshs, numReps_mva_1, ap_resource_lut());
}
