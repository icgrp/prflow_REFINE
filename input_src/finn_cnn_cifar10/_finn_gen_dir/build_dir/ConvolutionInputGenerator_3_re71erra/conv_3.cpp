
#define AP_INT_MAX_W_conv_3 16

#include "bnn-library.h"

// includes for network parameters
#include "slidingwindow.h"

// defines for network parameters
#define ConvKernelDim1_conv_3 3
#define IFMChannels1_conv_3 128
#define Input_precision1_conv_3 1
#define IFMDim1_conv_3 12
#define OFMDim1_conv_3 10
#define SIMD1_conv_3 16
#define Stride1_conv_3 1
#define numReps_conv_3 1

void conv_3(hls::stream<ap_uint<SIMD1_conv_3*Input_precision1_conv_3>> &in0,
                hls::stream<ap_uint<SIMD1_conv_3*Input_precision1_conv_3>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_3, IFMChannels1_conv_3, Input_precision1_conv_3, IFMDim1_conv_3,
                    OFMDim1_conv_3, SIMD1_conv_3, Stride1_conv_3> (in0, out, numReps_conv_3, ap_resource_lutram());
}
