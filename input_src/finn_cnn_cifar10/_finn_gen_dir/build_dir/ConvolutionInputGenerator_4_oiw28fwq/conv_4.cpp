
#define AP_INT_MAX_W_conv_4 2

#include "bnn-library.h"

// includes for network parameters
#include "slidingwindow.h"

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
