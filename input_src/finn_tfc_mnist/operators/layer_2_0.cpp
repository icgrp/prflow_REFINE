#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_1 64



// defines for network parameters
#define InWidth_str_dwc_1 1 
#define OutWidth_str_dwc_1 64 
#define NumInWords_str_dwc_1 64 
#define numReps_str_dwc_1 1

void str_dwc_1(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_1, OutWidth_str_dwc_1, NumInWords_str_dwc_1>(in0, out, numReps_str_dwc_1);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_2 64


#include "mva_2_thresh.h"

// defines for network parameters
#define MW1_mva_2 64
#define MH1_mva_2 64
#define SIMD1_mva_2 64
#define PE1_mva_2 1
#define WMEM1_mva_2 64
#define TMEM1_mva_2 64
#define numReps_mva_2 1

void mva_2(hls::stream<ap_uint<64>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_2_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_2_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_2, MH1_mva_2, SIMD1_mva_2, PE1_mva_2, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_2_weights, mva_2_threshs, numReps_mva_2, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_2_0 (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<64>> out_str_dwc_1("out_str_dwc_1");

#pragma HLS dataflow
    str_dwc_1(Input_1, out_str_dwc_1);
    mva_2(out_str_dwc_1, Output_1);

}
