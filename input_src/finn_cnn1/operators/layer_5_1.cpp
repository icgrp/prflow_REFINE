#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_5_1_0 36



// defines for network parameters
#define InWidth_str_dwc_5_1_0 1 
#define OutWidth_str_dwc_5_1_0 36 
#define NumInWords_str_dwc_5_1_0 1152 
#define numReps_str_dwc_5_1_0 1

void str_dwc_5_1_0(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<36> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_5_1_0, OutWidth_str_dwc_5_1_0, NumInWords_str_dwc_5_1_0>(in0, out, numReps_str_dwc_5_1_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_5 36


#include "mva_5_thresh.h"

// defines for network parameters
#define MW1_mva_5 1152
#define MH1_mva_5 128
#define SIMD1_mva_5 36
#define PE1_mva_5 1
#define WMEM1_mva_5 4096
#define TMEM1_mva_5 128
#define numReps_mva_5 1

void mva_5(hls::stream<ap_uint<36>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_5_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_5_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_5, MH1_mva_5, SIMD1_mva_5, PE1_mva_5, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_5_weights, mva_5_threshs, numReps_mva_5, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_5_1 (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<36>> out_str_dwc_5_1_0("out_str_dwc_5_1_0");

#pragma HLS dataflow
    str_dwc_5_1_0(Input_1, out_str_dwc_5_1_0);
    mva_5(out_str_dwc_5_1_0, Output_1);

}
