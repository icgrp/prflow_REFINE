
#define AP_INT_MAX_W 32

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "mva_7_thresh.h"

// defines for network parameters
#define MW1 512
#define MH1 512
#define SIMD1 32
#define PE1 1
#define WMEM1 8192
#define TMEM1 512
#define numReps 1

void mva_7(hls::stream<ap_uint<32>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_7_params.h"
#pragma HLS ARRAY_PARTITION variable=weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1, MH1, SIMD1, PE1, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, weights, threshs, numReps, ap_resource_lut());
}
