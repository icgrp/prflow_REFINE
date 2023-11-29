#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_6_0_0 4



// defines for network parameters
#define InWidth_str_dwc_6_0_0 1 
#define OutWidth_str_dwc_6_0_0 4 
#define NumInWords_str_dwc_6_0_0 128 
#define numReps_str_dwc_6_0_0 1

void str_dwc_6_0_0(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<4> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_6_0_0, OutWidth_str_dwc_6_0_0, NumInWords_str_dwc_6_0_0>(in0, out, numReps_str_dwc_6_0_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_6 4


#include "mva_6_thresh.h"

// defines for network parameters
#define MW1_mva_6 128
#define MH1_mva_6 256
#define SIMD1_mva_6 4
#define PE1_mva_6 1
#define WMEM1_mva_6 8192
#define TMEM1_mva_6 256
#define numReps_mva_6 1

void mva_6(hls::stream<ap_uint<4>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_6_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_6_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_6, MH1_mva_6, SIMD1_mva_6, PE1_mva_6, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_6_weights, mva_6_threshs, numReps_mva_6, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_last_0 (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<4>> out_str_dwc_6_0_0("out_str_dwc_6_0_0");

#pragma HLS dataflow
    str_dwc_6_0_0(Input_1, out_str_dwc_6_0_0);
    mva_6(out_str_dwc_6_0_0, Output_1);

}
