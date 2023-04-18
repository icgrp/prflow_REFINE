
#define AP_INT_MAX_W 16

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"

// defines for network parameters
#define MW1 512
#define MH1 10
#define SIMD1 1
#define PE1 1
#define WMEM1 5120
#define TMEM1 0
#define numReps 1

void mva_8(hls::stream<ap_uint<1>> &in0,
                    hls::stream<ap_uint<16>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_8_params.h"
#pragma HLS ARRAY_PARTITION variable=weights.m_weights complete dim=1
Matrix_Vector_Activate_Batch<MW1, MH1, SIMD1, PE1, 1, Recast<XnorMul>, Slice<ap_int<16>>, Identity>
                (in0, out, weights, PassThroughActivation<ap_int<16>>(), numReps, ap_resource_lut());
}
