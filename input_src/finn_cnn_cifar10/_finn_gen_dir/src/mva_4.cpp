
#define AP_INT_MAX_W_mva_4 72

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_4_thresh.h"

// defines for network parameters
#define MW1_mva_4 1152
#define MH1_mva_4 256
#define SIMD1_mva_4 72
#define PE1_mva_4 8
#define WMEM1_mva_4 512
#define TMEM1_mva_4 32
#define numReps_mva_4 9

void mva_4(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_4_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_4_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_4, MH1_mva_4, SIMD1_mva_4, PE1_mva_4, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_4_weights, mva_4_threshs, numReps_mva_4, ap_resource_lut());
}
