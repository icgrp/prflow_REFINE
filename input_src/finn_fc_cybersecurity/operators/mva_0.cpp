
#define AP_INT_MAX_W 64

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "thresh_0.h"

// defines for network parameters
#define MW1 608
#define MH1 64
#define SIMD1 32
#define PE1 16
#define WMEM1 76
#define TMEM1 4
#define numReps 1

void mva_0(hls::stream<ap_uint<32>> &Input_1,
                    hls::stream<ap_uint<32>> &Output_1
                    )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
#include "params_0.h"
#pragma HLS ARRAY_PARTITION variable=weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1, MH1, SIMD1, PE1, 1, Recast<Binary>, Slice<ap_uint<2>>, Identity>
                (Input_1, Output_1, weights, threshs, numReps, ap_resource_lut());
}
