#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_1 64


#include "mva_1_thresh.h"

// defines for network parameters
#define MW1_mva_1 64
#define MH1_mva_1 64
#define SIMD1_mva_1 64
#define PE1_mva_1 1
#define WMEM1_mva_1 64
#define TMEM1_mva_1 64
#define numReps_mva_1 1

void mva_1(hls::stream<ap_uint<64>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_1_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_1_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_1, MH1_mva_1, SIMD1_mva_1, PE1_mva_1, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_1_weights, mva_1_threshs, numReps_mva_1, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_1_0 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1


#pragma HLS dataflow
    mva_1(Input_1, Output_1);

}
