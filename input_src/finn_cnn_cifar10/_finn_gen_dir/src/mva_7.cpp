
#define AP_INT_MAX_W_mva_7 32

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_7_thresh.h"

// defines for network parameters
#define MW1_mva_7 512
#define MH1_mva_7 512
#define SIMD1_mva_7 32
#define PE1_mva_7 1
#define WMEM1_mva_7 8192
#define TMEM1_mva_7 512
#define numReps_mva_7 1

void mva_7(hls::stream<ap_uint<32>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_7_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_7_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_7_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_7_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_7, MH1_mva_7, SIMD1_mva_7, PE1_mva_7, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_7_weights, mva_7_threshs, numReps_mva_7, ap_resource_lut());
}
