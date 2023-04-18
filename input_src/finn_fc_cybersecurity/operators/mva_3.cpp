
#define AP_INT_MAX_W 2

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "thresh_3.h"

// defines for network parameters
#define MW1 64
#define MH1 1
#define SIMD1 1
#define PE1 1
#define WMEM1 64
#define TMEM1 1
#define numReps 1

void mva_3(hls::stream<ap_uint<2>> &Input_1,
                    hls::stream<ap_uint<1>> &Output_1
                    )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
#include "params_3.h"
#pragma HLS ARRAY_PARTITION variable=weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1, MH1, SIMD1, PE1, 1, Slice<ap_uint<2>>, Slice<ap_int<1>>, Identity>
                (Input_1, Output_1, weights, threshs, numReps, ap_resource_lut());
}
