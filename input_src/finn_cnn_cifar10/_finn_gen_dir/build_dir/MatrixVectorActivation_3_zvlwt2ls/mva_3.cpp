
#define AP_INT_MAX_W_mva_3 72

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_3_thresh.h"

// defines for network parameters
#define MW1_mva_3 1152
#define MH1_mva_3 128
#define SIMD1_mva_3 72
#define PE1_mva_3 32
#define WMEM1_mva_3 64
#define TMEM1_mva_3 4
#define numReps_mva_3 100

void mva_3(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_3_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_3_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_3, MH1_mva_3, SIMD1_mva_3, PE1_mva_3, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_3_weights, mva_3_threshs, numReps_mva_3, ap_resource_lut());
}
