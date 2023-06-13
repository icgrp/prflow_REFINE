
#define AP_INT_MAX_W_mva_5 72

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"
#include "mva_5_thresh.h"

// defines for network parameters
#define MW1_mva_5 2304
#define MH1_mva_5 256
#define SIMD1_mva_5 72
#define PE1_mva_5 1
#define WMEM1_mva_5 8192
#define TMEM1_mva_5 256
#define numReps_mva_5 1

void mva_5(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_5_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_5_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_5, MH1_mva_5, SIMD1_mva_5, PE1_mva_5, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_5_weights, mva_5_threshs, numReps_mva_5, ap_resource_lut());
}
