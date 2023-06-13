#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/slidingwindow.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/maxpool.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_6 32



// defines for network parameters
#define InWidth_str_dwc_6 32 
#define OutWidth_str_dwc_6 16 
#define NumInWords_str_dwc_6 576 
#define numReps_str_dwc_6 1

void str_dwc_6(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_6, OutWidth_str_dwc_6, NumInWords_str_dwc_6>(in0, out, numReps_str_dwc_6);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_conv_3 16



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

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_7 72



// defines for network parameters
#define InWidth_str_dwc_7 16 
#define OutWidth_str_dwc_7 72 
#define NumInWords_str_dwc_7 7200 
#define numReps_str_dwc_7 1
#define LCMWidth_str_dwc_7 144
#define NumLCMToOut_str_dwc_7 800

void str_dwc_7(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<144>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_7, LCMWidth_str_dwc_7, NumInWords_str_dwc_7>(in0, intermediate, numReps_str_dwc_7);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_7, OutWidth_str_dwc_7, NumLCMToOut_str_dwc_7>(intermediate, out, numReps_str_dwc_7);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_3 72


#include "mva_3_thresh.h"

// defines for network parameters
#define MW1_mva_3 1152
#define MH1_mva_3 128
#define SIMD1_mva_3 72
#define PE1_mva_3 32
#define WMEM1_mva_3 64
#define TMEM1_mva_3 4
#define numReps_mva_3 100

void mva_3(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_3_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_3_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_3, MH1_mva_3, SIMD1_mva_3, PE1_mva_3, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_3_weights, mva_3_threshs, numReps_mva_3, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_8 128



// defines for network parameters
#define InWidth_str_dwc_8 32 
#define OutWidth_str_dwc_8 128 
#define NumInWords_str_dwc_8 400 
#define numReps_str_dwc_8 1

void str_dwc_8(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<128> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_8, OutWidth_str_dwc_8, NumInWords_str_dwc_8>(in0, out, numReps_str_dwc_8);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_mp_batch_1 128



// defines for network parameters
#define ImgDim_str_mp_batch_1 10
#define PoolDim_str_mp_batch_1 2
#define NumChannels_str_mp_batch_1 128
#define numReps_str_mp_batch_1 1

void str_mp_batch_1(hls::stream<ap_uint<128>> &in0, 
                       hls::stream<ap_uint<128>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim_str_mp_batch_1, PoolDim_str_mp_batch_1, NumChannels_str_mp_batch_1>(in0, out);
}

// ------------------------------------------------------------------------

void layer_3 (
        hls::stream<ap_uint<32>> & Input_1,
        hls::stream<ap_uint<128>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<16>> out_str_dwc_0("out_str_dwc_0");
    static hls::stream<ap_uint<16>> out_conv("out_conv");
    static hls::stream<ap_uint<72>> out_str_dwc_1("out_str_dwc_1");
    static hls::stream<ap_uint<32>> out_mva("out_mva");
    static hls::stream<ap_uint<128>> out_str_dwc_2("out_str_dwc_2");

#pragma HLS dataflow
    str_dwc_6(Input_1, out_str_dwc_0);
    conv_3(out_str_dwc_0, out_conv);
    str_dwc_7(out_conv, out_str_dwc_1);
    mva_3(out_str_dwc_1, out_mva);
    str_dwc_8(out_mva, out_str_dwc_2);
    str_mp_batch_1(out_str_dwc_2, Output_1);

}
