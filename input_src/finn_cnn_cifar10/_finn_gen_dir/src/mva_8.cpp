
#define AP_INT_MAX_W_mva_8 16

#include "bnn-library.h"

// includes for network parameters
#include "weights.hpp"
#include "activations.hpp"
#include "mvau.hpp"

// defines for network parameters
#define MW1_mva_8 512
#define MH1_mva_8 10
#define SIMD1_mva_8 1
#define PE1_mva_8 1
#define WMEM1_mva_8 5120
#define TMEM1_mva_8 0
#define numReps_mva_8 1

void mva_8(hls::stream<ap_uint<1>> &in0,
                    hls::stream<ap_uint<16>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_8_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_8_weights.m_weights complete dim=1
Matrix_Vector_Activate_Batch<MW1_mva_8, MH1_mva_8, SIMD1_mva_8, PE1_mva_8, 1, Recast<XnorMul>, Slice<ap_int<16>>, Identity>
                (in0, out, mva_8_weights, PassThroughActivation<ap_int<16>>(), numReps_mva_8, ap_resource_lut());
}
