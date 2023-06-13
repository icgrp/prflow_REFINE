#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_4 64



// defines for network parameters
#define InWidth_str_dwc_4 64 
#define OutWidth_str_dwc_4 16 
#define NumInWords_str_dwc_4 196 
#define numReps_str_dwc_4 1

void str_dwc_4(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_4, OutWidth_str_dwc_4, NumInWords_str_dwc_4>(in0, out, numReps_str_dwc_4);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_2 16



// defines for network parameters
#define ConvKernelDim1_conv_2 3
#define IFMChannels1_conv_2 64
#define Input_precision1_conv_2 1
#define IFMDim1_conv_2 14
#define OFMDim1_conv_2 12
#define SIMD1_conv_2 16
#define Stride1_conv_2 1
#define numReps_conv_2 1

void conv_2(hls::stream<ap_uint<SIMD1_conv_2*Input_precision1_conv_2>> &in0,
                hls::stream<ap_uint<SIMD1_conv_2*Input_precision1_conv_2>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
ConvolutionInputGenerator<ConvKernelDim1_conv_2, IFMChannels1_conv_2, Input_precision1_conv_2, IFMDim1_conv_2,
                    OFMDim1_conv_2, SIMD1_conv_2, Stride1_conv_2> (in0, out, numReps_conv_2, ap_resource_lutram());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_5 72



// defines for network parameters
#define InWidth_str_dwc_5 16 
#define OutWidth_str_dwc_5 72 
#define NumInWords_str_dwc_5 5184 
#define numReps_str_dwc_5 1
#define LCMWidth_str_dwc_5 144
#define NumLCMToOut_str_dwc_5 576

void str_dwc_5(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<144>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_5, LCMWidth_str_dwc_5, NumInWords_str_dwc_5>(in0, intermediate, numReps_str_dwc_5);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_5, OutWidth_str_dwc_5, NumLCMToOut_str_dwc_5>(intermediate, out, numReps_str_dwc_5);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_2 72


#include "mva_2_thresh.h"

// defines for network parameters
#define MW1_mva_2 576
#define MH1_mva_2 128
#define SIMD1_mva_2 72
#define PE1_mva_2 32
#define WMEM1_mva_2 32
#define TMEM1_mva_2 4
#define numReps_mva_2 144

void mva_2(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_2_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_2_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_2_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_2, MH1_mva_2, SIMD1_mva_2, PE1_mva_2, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_2_weights, mva_2_threshs, numReps_mva_2, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_2 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<32>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<16>> out_str_dwc_0("out_str_dwc_0");
    static hls::stream<ap_uint<16>> out_conv("out_conv");
    static hls::stream<ap_uint<72>> out_str_dwc_1("out_str_dwc_1");

#pragma HLS dataflow
    str_dwc_4(Input_1, out_str_dwc_0);
    conv_2(out_str_dwc_0, out_conv);
    str_dwc_5(out_conv, out_str_dwc_1);
    mva_2(out_str_dwc_1, Output_1);

}
