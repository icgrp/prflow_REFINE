#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/slidingwindow.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_3 16



// defines for network parameters
#define ConvKernelDim1_conv_3 3
#define IFMChannels1_conv_3 64
#define Input_precision1_conv_3 2
#define IFMDim1_conv_3 12
#define OFMDim1_conv_3 10
#define SIMD1_conv_3 8
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

// ------------------------------------------------------------------------

void layer_3_0 (
        hls::stream<ap_uint<16>> & Input_1,
        hls::stream<ap_uint<16>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1


#pragma HLS dataflow
    conv_3(Input_1, Output_1);

}
