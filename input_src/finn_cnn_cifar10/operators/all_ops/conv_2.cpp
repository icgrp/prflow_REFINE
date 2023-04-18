
#define AP_INT_MAX_W 16

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/slidingwindow.h"

// defines for network parameters
#define ConvKernelDim1 3
#define IFMChannels1 64
#define Input_precision1 1
#define IFMDim1 14
#define OFMDim1 12
#define SIMD1 16
#define Stride1 1
#define numReps 1

void conv_2(hls::stream<ap_uint<SIMD1*Input_precision1>> &in0,
                hls::stream<ap_uint<SIMD1*Input_precision1>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1, IFMChannels1, Input_precision1, IFMDim1,
                    OFMDim1, SIMD1, Stride1> (in0, out, numReps, ap_resource_lutram());
}
