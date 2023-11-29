#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/slidingwindow.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_1 64



// defines for network parameters
#define ConvKernelDim1_conv_1 3
#define IFMChannels1_conv_1 32
#define Input_precision1_conv_1 2
#define IFMDim1_conv_1 30
#define OFMDim1_conv_1 28
#define SIMD1_conv_1 32
#define Stride1_conv_1 1
#define numReps_conv_1 1

void conv_1(hls::stream<ap_uint<SIMD1_conv_1*Input_precision1_conv_1>> &in0,
                hls::stream<ap_uint<SIMD1_conv_1*Input_precision1_conv_1>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_1, IFMChannels1_conv_1, Input_precision1_conv_1, IFMDim1_conv_1,
                    OFMDim1_conv_1, SIMD1_conv_1, Stride1_conv_1> (in0, out, numReps_conv_1, ap_resource_lutram());
}

// ------------------------------------------------------------------------

void layer_1_0 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<64>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1


#pragma HLS dataflow
    conv_1(Input_1, Output_1);

}
