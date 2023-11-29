#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_0_1_0 216



// defines for network parameters
#define InWidth_str_dwc_0_1_0 24 
#define OutWidth_str_dwc_0_1_0 216 
#define NumInWords_str_dwc_0_1_0 8100 
#define numReps_str_dwc_0_1_0 1

void str_dwc_0_1_0(hls::stream<ap_uint<24> > &in0, hls::stream<ap_uint<216> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_0_1_0, OutWidth_str_dwc_0_1_0, NumInWords_str_dwc_0_1_0>(in0, out, numReps_str_dwc_0_1_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_0 216


#include "mva_0_thresh.h"

// defines for network parameters
#define MW1_mva_0 27
#define MH1_mva_0 32
#define SIMD1_mva_0 27
#define PE1_mva_0 32
#define WMEM1_mva_0 1
#define TMEM1_mva_0 1
#define numReps_mva_0 900

void mva_0(hls::stream<ap_uint<216>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_0_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_0_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_0, MH1_mva_0, SIMD1_mva_0, PE1_mva_0, 1, Slice<ap_int<8>>, Slice<ap_uint<1>>, Recast<Binary>>
                (in0, out, mva_0_weights, mva_0_threshs, numReps_mva_0, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_0_1 (
        hls::stream<ap_uint<24>> & Input_1,
        hls::stream<ap_uint<32>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<216>> out_str_dwc_0_1_0("out_str_dwc_0_1_0");

#pragma HLS dataflow
    str_dwc_0_1_0(Input_1, out_str_dwc_0_1_0);
    mva_0(out_str_dwc_0_1_0, Output_1);

}
