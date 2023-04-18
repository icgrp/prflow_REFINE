#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_11 8

// defines for network parameters
#define InWidth_str_dwc_11 8 
#define OutWidth_str_dwc_11 1 
#define NumInWords_str_dwc_11 288 
#define numReps_str_dwc_11 1

void str_dwc_11(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<1> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_11, OutWidth_str_dwc_11, NumInWords_str_dwc_11>(in0, out, numReps_str_dwc_11);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_conv_5 1

// defines for network parameters
#define ConvKernelDim1_conv_5 3
#define IFMChannels1_conv_5 256
#define Input_precision1_conv_5 1
#define IFMDim1_conv_5 3
#define OFMDim1_conv_5 1
#define SIMD1_conv_5 1
#define Stride1_conv_5 1
#define numReps_conv_5 1

void conv_5(hls::stream<ap_uint<SIMD1_conv_5*Input_precision1_conv_5>> &in0,
                hls::stream<ap_uint<SIMD1_conv_5*Input_precision1_conv_5>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_5, IFMChannels1_conv_5, Input_precision1_conv_5, IFMDim1_conv_5,
                    OFMDim1_conv_5, SIMD1_conv_5, Stride1_conv_5> (in0, out, numReps_conv_5, ap_resource_lutram());
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_12 72

// defines for network parameters
#define InWidth_str_dwc_12 1 
#define OutWidth_str_dwc_12 72 
#define NumInWords_str_dwc_12 2304 
#define numReps_str_dwc_12 1

void str_dwc_12(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_12, OutWidth_str_dwc_12, NumInWords_str_dwc_12>(in0, out, numReps_str_dwc_12);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_mva_5 72

// includes for network parameters
#include "mva_5_thresh.h"

// defines for network parameters
#define MW1_mva_5 2304
#define MH1_mva_5 256
#define SIMD1_mva_5 72
#define PE1_mva_5 1
#define WMEM1mva_5 8192
#define TMEM1mva_5 256
#define numReps_mva_5 1

void mva_5(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_5_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_5_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_thresh.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_5_thresh.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_5, MH1_mva_5, SIMD1_mva_5, PE1_mva_5, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_5_weights, mva_5_thresh, numReps_mva_5, ap_resource_lut());
}

// -------------------------------------------------------------------------------------------------


void layer_5 (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<1> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<1>> out_str_dwc_11("out_str_dwc_11");
    static hls::stream<ap_uint<1>> out_conv_5("out_conv_5");
    static hls::stream<ap_uint<72>> out_str_dwc_12("out_str_dwc_12");

#pragma HLS dataflow
    str_dwc_11(Input_1, out_str_dwc_11);
    conv_5(out_str_dwc_11, out_conv_5);
    str_dwc_12(out_conv_5, out_str_dwc_12);
    mva_5(out_str_dwc_12, Output_1);

}
