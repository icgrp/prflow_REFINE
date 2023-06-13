
#define AP_INT_MAX_W 2

#include "bnn-library.h"

// includes for network parameters
#include "slidingwindow.h"

// defines for network parameters
#define ConvKernelDim1 3
#define IFMChannels1 128
#define Input_precision1 1
#define IFMDim1 5
#define OFMDim1 3
#define SIMD1 2
#define Stride1 1
#define numReps 1

void ConvolutionInputGenerator_4(hls::stream<ap_uint<SIMD1*Input_precision1>> &in0,
                hls::stream<ap_uint<SIMD1*Input_precision1>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1, IFMChannels1, Input_precision1, IFMDim1,
                    OFMDim1, SIMD1, Stride1> (in0, out, numReps, ap_resource_lutram());
}
