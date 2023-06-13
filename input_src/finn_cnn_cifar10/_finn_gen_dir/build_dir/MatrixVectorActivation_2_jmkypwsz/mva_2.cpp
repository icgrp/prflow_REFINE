
#define AP_INT_MAX_W_mva_2 72

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_2_thresh.h"

// defines for network parameters
#define MW1_mva_2 576
#define MH1_mva_2 128
#define SIMD1_mva_2 72
#define PE1_mva_2 32
#define WMEM1_mva_2 32
#define TMEM1_mva_2 4
#define numReps_mva_2 144

void mva_2(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_2_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_2_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_2, MH1_mva_2, SIMD1_mva_2, PE1_mva_2, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_2_weights, mva_2_threshs, numReps_mva_2, ap_resource_lut());
}
