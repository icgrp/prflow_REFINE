#include "../host/finn-hlslib/bnn-library.h"
#include "../host/typedefs.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/mvau.hpp"


// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_thr_batch_0 8

// includes for network parameters
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
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_thresh.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_thresh.m_thresholds complete dim=3
#pragma HLS RESOURCE variable=thr_batch_0_thresh.m_thresholds core=ROM_2P_LUTRAM
Thresholding_Batch<ImgDim1_thr_batch_0, NumChannels1_thr_batch_0, PE1_thr_batch_0, Slice<ap_uint<8>>, Slice<ap_int<8>>>
                (in0, out, thr_batch_0_thresh, numReps_thr_batch_0);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_Wstr_dwc_0 24

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

// -------------------------------------------------------------------------------------------------

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

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_str_dwc_1 216

// defines for network parameters
#define InWidth_str_dwc_1 24 
#define OutWidth_str_dwc_1 216 
#define NumInWords_str_dwc_1 8100 
#define numReps_str_dwc_1 1

void str_dwc_1(hls::stream<ap_uint<24> > &in0, hls::stream<ap_uint<216> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_1, OutWidth_str_dwc_1, NumInWords_str_dwc_1>(in0, out, numReps_str_dwc_1);
}

// -------------------------------------------------------------------------------------------------

#define AP_INT_MAX_W_mva_0 216

// includes for network parameters
#include "mva_0_thresh.h"

// defines for network parameters
#define MW1_mva_0 27
#define MH1_mva_0 64
#define SIMD1_mva_0 27
#define PE1_mva_0 8
#define WMEM1_mva_0 8
#define TMEM1_mva_0 8
#define numReps_mva_0 900

void mva_0(hls::stream<ap_uint<216>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_0_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_0_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_thresh.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_thresh.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_0, MH1_mva_0, SIMD1_mva_0, PE1_mva_0, 1, Slice<ap_int<8>>, Slice<ap_uint<1>>, Recast<Binary>>
                (in0, out, mva_0_weights, mva_0_thresh, numReps_mva_0, ap_resource_lut());
}

// -------------------------------------------------------------------------------------------------

void layer_0 (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<8> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<8>> out_thr_batch_0("out_thr_batch_0");
    static hls::stream<ap_uint<24>> out_str_dwc_0("out_str_dwc_0");
    static hls::stream<ap_uint<24>> out_conv_0("out_conv_0");
    static hls::stream<ap_uint<216>> out_str_dwc_1("out_str_dwc_1");


#pragma HLS dataflow
    thr_batch_0(Input_1, out_thr_batch_0);
    str_dwc_0(out_thr_batch_0, out_str_dwc_0);
    conv_0(out_str_dwc_0, out_conv_0);
    str_dwc_1(out_conv_0, out_str_dwc_1);
    mva_0(out_str_dwc_1, Output_1);

}

