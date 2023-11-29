#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/streamtools.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_2_0_0 64



// defines for network parameters
#define InWidth_str_dwc_2_0_0 64 
#define OutWidth_str_dwc_2_0_0 16 
#define NumInWords_str_dwc_2_0_0 196 
#define numReps_str_dwc_2_0_0 1

void str_dwc_2_0_0(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_2_0_0, OutWidth_str_dwc_2_0_0, NumInWords_str_dwc_2_0_0>(in0, out, numReps_str_dwc_2_0_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_2 16



// defines for network parameters
#define ConvKernelDim1_conv_2 3
#define IFMChannels1_conv_2 32
#define Input_precision1_conv_2 2
#define IFMDim1_conv_2 14
#define OFMDim1_conv_2 12
#define SIMD1_conv_2 8
#define Stride1_conv_2 1
#define numReps_conv_2 1

void conv_2(hls::stream<ap_uint<SIMD1_conv_2*Input_precision1_conv_2>> &in0,
                hls::stream<ap_uint<SIMD1_conv_2*Input_precision1_conv_2>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_2, IFMChannels1_conv_2, Input_precision1_conv_2, IFMDim1_conv_2,
                    OFMDim1_conv_2, SIMD1_conv_2, Stride1_conv_2> (in0, out, numReps_conv_2, ap_resource_lutram());
}

// ------------------------------------------------------------------------

void layer_2_0 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<16>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<16>> out_str_dwc_2_0_0("out_str_dwc_2_0_0");

#pragma HLS dataflow
    str_dwc_2_0_0(Input_1, out_str_dwc_2_0_0);
    conv_2(out_str_dwc_2_0_0, Output_1);

}
