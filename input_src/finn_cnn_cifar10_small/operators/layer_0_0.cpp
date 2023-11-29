#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/streamtools.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_thr_batch_0 8


#include "thr_batch_0_thresh.h"

// defines for network parameters
#define NumChannels1_thr_batch_0 3
#define PE1_thr_batch_0 1
#define numReps_thr_batch_0 1
#define ImgDim1_thr_batch_0 1024

void thr_batch_0(hls::stream<ap_uint<8>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=3
#pragma HLS RESOURCE variable=thr_batch_0_threshs.m_thresholds core=ROM_2P_LUTRAM
Thresholding_Batch<ImgDim1_thr_batch_0, NumChannels1_thr_batch_0, PE1_thr_batch_0, Slice<ap_uint<8>>, Slice<ap_int<8>>>
                (in0, out, thr_batch_0_threshs, numReps_thr_batch_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_0 24



// defines for network parameters
#define InWidth_str_dwc_0 8 
#define OutWidth_str_dwc_0 24 
#define NumInWords_str_dwc_0 3072 
#define numReps_str_dwc_0 1

void str_dwc_0(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<24> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_0, OutWidth_str_dwc_0, NumInWords_str_dwc_0>(in0, out, numReps_str_dwc_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_0 24



// defines for network parameters
#define ConvKernelDim1_conv_0 3
#define IFMChannels1_conv_0 3
#define Input_precision1_conv_0 8
#define IFMDim1_conv_0 32
#define OFMDim1_conv_0 30
#define SIMD1_conv_0 3
#define Stride1_conv_0 1
#define numReps_conv_0 1

void conv_0(hls::stream<ap_uint<SIMD1_conv_0*Input_precision1_conv_0>> &in0,
                hls::stream<ap_uint<SIMD1_conv_0*Input_precision1_conv_0>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_0, IFMChannels1_conv_0, Input_precision1_conv_0, IFMDim1_conv_0,
                    OFMDim1_conv_0, SIMD1_conv_0, Stride1_conv_0> (in0, out, numReps_conv_0, ap_resource_lutram());
}

// ------------------------------------------------------------------------

void layer_0_0 (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<24> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<8>> out_thr_batch("out_thr_batch");
    static hls::stream<ap_uint<24>> out_str_dwc_0("out_str_dwc_0");

#pragma HLS dataflow
    thr_batch_0(Input_1, out_thr_batch);
    str_dwc_0(out_thr_batch, out_str_dwc_0);
    conv_0(out_str_dwc_0, Output_1);

}