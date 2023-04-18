#include "../host/finn-hlslib/bnn-library.h"
#include "../host/typedefs.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/maxpool.h"


// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_2 64

// defines for network parameters
#define InWidth_str_dwc_2 8 
#define OutWidth_str_dwc_2 64 
#define NumInWords_str_dwc_2 7200 
#define numReps_str_dwc_2 1

void str_dwc_2(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_2, OutWidth_str_dwc_2, NumInWords_str_dwc_2>(in0, out, numReps_str_dwc_2);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_conv_1 64

// defines for network parameters
#define ConvKernelDim1_conv_1 3
#define IFMChannels1_conv_1 64
#define Input_precision1_conv_1 1
#define IFMDim1_conv_1 30
#define OFMDim1_conv_1 28
#define SIMD1_conv_1 64
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

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_3 72

// defines for network parameters
#define InWidth_str_dwc_3 64 
#define OutWidth_str_dwc_3 72 
#define NumInWords_str_dwc_3 7056 
#define numReps_str_dwc_3 1
#define LCMWidth_str_dwc_3 576
#define NumLCMToOut_str_dwc_3 784

void str_dwc_3(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<576>> intermediate_str_dwc_3 ("intermediate_str_dwc_3");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3, LCMWidth_str_dwc_3, NumInWords_str_dwc_3>(in0, intermediate_str_dwc_3, numReps_str_dwc_3);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_3, OutWidth_str_dwc_3, NumLCMToOut_str_dwc_3>(intermediate_str_dwc_3, out, numReps_str_dwc_3);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_mva_1 72


// includes for network parameters
#include "mva_1_thresh.h"

// defines for network parameters
#define MW1_mva_1 576
#define MH1_mva_1 64
#define SIMD1_mva_1 72
#define PE1_mva_1 64
#define WMEM1_mva_1 8
#define TMEM1_mva_1 1
#define numReps_mva_1 784

void mva_1(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<64>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_1_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_1_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_thresh.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_thresh.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_1, MH1_mva_1, SIMD1_mva_1, PE1_mva_1, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_1_weights, mva_1_thresh, numReps_mva_1, ap_resource_lut());
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_mp_batch_0 64

// defines for network parameters
#define ImgDim_str_mp_batch_0 28
#define PoolDim_str_mp_batch_0 2

#define NumChannels_str_mp_batch_0 64
#define numReps_str_mp_batch_0 1

void str_mp_batch_0(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim_str_mp_batch_0, PoolDim_str_mp_batch_0, NumChannels_str_mp_batch_0>(in0, out);
}

// -------------------------------------------------------------------------------------------------

void layer_1 (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<64> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<64>> out_str_dwc_2("out_str_dwc_2");
    static hls::stream<ap_uint<64>> out_conv_1("out_conv_1");
    static hls::stream<ap_uint<72>> out_str_dwc_3("out_str_dwc_3");
    static hls::stream<ap_uint<64>> out_mva_1("out_mva_1");

#pragma HLS dataflow
    str_dwc_2(Input_1, out_str_dwc_2);
    conv_1(out_str_dwc_2, out_conv_1);
    str_dwc_3(out_conv_1, out_str_dwc_3);
    mva_1(out_str_dwc_3, out_mva_1);
    str_mp_batch_0(out_mva_1, Output_1);
}

