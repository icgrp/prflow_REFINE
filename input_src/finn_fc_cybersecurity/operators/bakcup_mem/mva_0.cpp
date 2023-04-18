
#define AP_INT_MAX_W 1280

#include "./finn-hlslib/bnn-library.h"

// includes for network parameters
#include "./finn-hlslib/weights.hpp"
#include "./finn-hlslib/activations.hpp"
#include "./finn-hlslib/mvau.hpp"
#include "thresh_0.h"

// defines for network parameters
#define MW1 600
 #define MH1 64

            #define SIMD1 40
 #define PE1 16
 #define WMEM1 60

            #define TMEM1 4
 #define numReps 1
#define WP1 2


void mva_0(
                    hls::stream<ap_uint<40>> &INPUT_1,
                    hls::stream<ap_uint<1280>> &weights,
                    hls::stream<ap_uint<32>> &OUTPUT_1
                    )
{
#pragma HLS INTERFACE axis register port=INPUT_1
#pragma HLS INTERFACE axis register port=OUTPUT_1
#pragma HLS INTERFACE axis port=weights
#pragma HLS stream depth=8 variable=weights
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Stream_Batch<MW1, MH1, SIMD1, PE1, Recast<Binary>, Slice<ap_uint<2>>, Identity, ap_int<2> >
                (INPUT_1, OUTPUT_1, weights, threshs, numReps, ap_resource_lut());
}
