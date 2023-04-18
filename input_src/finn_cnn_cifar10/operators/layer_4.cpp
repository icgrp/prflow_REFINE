#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_9 128

// defines for network parameters
#define InWidth_str_dwc_9 128 
#define OutWidth_str_dwc_9 2 
#define NumInWords_str_dwc_9 25 
#define numReps_str_dwc_9 1

void str_dwc_9(hls::stream<ap_uint<128> > &in0, hls::stream<ap_uint<2> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_9, OutWidth_str_dwc_9, NumInWords_str_dwc_9>(in0, out, numReps_str_dwc_9);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_conv_4 2

// defines for network parameters
#define ConvKernelDim1_conv_4 3
#define IFMChannels1_conv_4 128
#define Input_precision1_conv_4 1
#define IFMDim1_conv_4 5
#define OFMDim1_conv_4 3
#define SIMD1_conv_4 2
#define Stride1_conv_4 1
#define numReps_conv_4 1

void conv_4(hls::stream<ap_uint<SIMD1_conv_4*Input_precision1_conv_4>> &in0,
                hls::stream<ap_uint<SIMD1_conv_4*Input_precision1_conv_4>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_4, IFMChannels1_conv_4, Input_precision1_conv_4, IFMDim1_conv_4,
                    OFMDim1_conv_4, SIMD1_conv_4, Stride1_conv_4> (in0, out, numReps_conv_4, ap_resource_lutram());
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_10 72

// defines for network parameters
#define InWidth_str_dwc_10 2 
#define OutWidth_str_dwc_10 72 
#define NumInWords_str_dwc_10 5184 
#define numReps_str_dwc_10 1

void str_dwc_10(hls::stream<ap_uint<2> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_10, OutWidth_str_dwc_10, NumInWords_str_dwc_10>(in0, out, numReps_str_dwc_10);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_mva_4 72

// includes for network parameters
#include "mva_4_thresh.h"

// defines for network parameters
#define MW1_mva_4 1152
#define MH1_mva_4 256
#define SIMD1_mva_4 72
#define PE1_mva_4 8
#define WMEM1_mva_4 512
#define TMEM1_mva_4 32
#define numReps_mva_4 9

void mva_4(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_4_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_4_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_thresh.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_4_thresh.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_4, MH1_mva_4, SIMD1_mva_4, PE1_mva_4, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_4_weights, mva_4_thresh, numReps_mva_4, ap_resource_lut());
}

// -------------------------------------------------------------------------------------------------

void layer_4 (
        hls::stream<ap_uint<128> > & Input_1,
        hls::stream<ap_uint<8> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<2>> out_str_dwc_9("out_str_dwc_9");
    static hls::stream<ap_uint<2>> out_conv_4("out_conv_4");
    static hls::stream<ap_uint<72>> out_str_dwc_10("out_str_dwc_10");

#pragma HLS dataflow
    str_dwc_9(Input_1, out_str_dwc_9);
    conv_4(out_str_dwc_9, out_conv_4);
    str_dwc_10(out_conv_4, out_str_dwc_10);
    mva_4(out_str_dwc_10, Output_1);

}
