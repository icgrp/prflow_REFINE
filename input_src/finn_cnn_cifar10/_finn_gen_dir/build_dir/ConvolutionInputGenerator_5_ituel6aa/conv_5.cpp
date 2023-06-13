
#define AP_INT_MAX_W_conv_5 1

#include "bnn-library.h"

// includes for network parameters
#include "slidingwindow.h"

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
