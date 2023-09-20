#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/streamtools.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_3 32



// defines for network parameters
#define InWidth_str_dwc_3 32 
#define OutWidth_str_dwc_3 8 
#define NumInWords_str_dwc_3 196 
#define numReps_str_dwc_3 1

void str_dwc_3(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<8> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3, OutWidth_str_dwc_3, NumInWords_str_dwc_3>(in0, out, numReps_str_dwc_3);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_2 8



// defines for network parameters
#define ConvKernelDim1_conv_2 3
#define IFMChannels1_conv_2 32
#define Input_precision1_conv_2 1
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
        hls::stream<ap_uint<32>> & Input_1,
        hls::stream<ap_uint<8>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<8>> out_str_dwc_3("out_str_dwc_3");

#pragma HLS dataflow
    str_dwc_3(Input_1, out_str_dwc_3);
    conv_2(out_str_dwc_3, Output_1);

}
