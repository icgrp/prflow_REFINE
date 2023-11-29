#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/streamtools.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_4_0_0 64



// defines for network parameters
#define InWidth_str_dwc_4_0_0 64 
#define OutWidth_str_dwc_4_0_0 1 
#define NumInWords_str_dwc_4_0_0 25 
#define numReps_str_dwc_4_0_0 1

void str_dwc_4_0_0(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<1> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_4_0_0, OutWidth_str_dwc_4_0_0, NumInWords_str_dwc_4_0_0>(in0, out, numReps_str_dwc_4_0_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_4 1



// defines for network parameters
#define ConvKernelDim1_conv_4 3
#define IFMChannels1_conv_4 64
#define Input_precision1_conv_4 1
#define IFMDim1_conv_4 5
#define OFMDim1_conv_4 3
#define SIMD1_conv_4 1
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

// ------------------------------------------------------------------------

void layer_4_0 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<1>> out_str_dwc_4_0_0("out_str_dwc_4_0_0");

#pragma HLS dataflow
    str_dwc_4_0_0(Input_1, out_str_dwc_4_0_0);
    conv_4(out_str_dwc_4_0_0, Output_1);

}
