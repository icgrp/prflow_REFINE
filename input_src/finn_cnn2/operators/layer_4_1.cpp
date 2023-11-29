#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_4_1_0 192



// defines for network parameters
#define InWidth_str_dwc_4_1_0 2 
#define OutWidth_str_dwc_4_1_0 192 
#define NumInWords_str_dwc_4_1_0 5184 
#define numReps_str_dwc_4_1_0 1

void str_dwc_4_1_0(hls::stream<ap_uint<2> > &in0, hls::stream<ap_uint<192> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_4_1_0, OutWidth_str_dwc_4_1_0, NumInWords_str_dwc_4_1_0>(in0, out, numReps_str_dwc_4_1_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_4 192


#include "mva_4_thresh.h"

// defines for network parameters
#define MW1_mva_4 576
#define MH1_mva_4 128
#define SIMD1_mva_4 96
#define PE1_mva_4 1
#define WMEM1_mva_4 768
#define TMEM1_mva_4 128
#define numReps_mva_4 9

void mva_4(hls::stream<ap_uint<192>> &in0,
                    hls::stream<ap_uint<2>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_4_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_4_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_4, MH1_mva_4, SIMD1_mva_4, PE1_mva_4, 1, Slice<ap_int<2>>, Slice<ap_int<2>>, Recast<Binary>>
                (in0, out, mva_4_weights, mva_4_threshs, numReps_mva_4, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_4_1 (
        hls::stream<ap_uint<2>> & Input_1,
        hls::stream<ap_uint<2>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<192>> out_str_dwc_4_1_0("out_str_dwc_4_1_0");

#pragma HLS dataflow
    str_dwc_4_1_0(Input_1, out_str_dwc_4_1_0);
    mva_4(out_str_dwc_4_1_0, Output_1);

}
