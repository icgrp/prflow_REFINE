#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/weights.hpp"
#include "../host/finn-hlslib/maxpool.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_13 16



// defines for network parameters
#define InWidth_str_dwc_13 1 
#define OutWidth_str_dwc_13 16 
#define NumInWords_str_dwc_13 256 
#define numReps_str_dwc_13 1

void str_dwc_13(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_13, OutWidth_str_dwc_13, NumInWords_str_dwc_13>(in0, out, numReps_str_dwc_13);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_6 16


#include "mva_6_thresh.h"

// defines for network parameters
#define MW1_mva_6 256
#define MH1_mva_6 512
#define SIMD1_mva_6 16
#define PE1_mva_6 1
#define WMEM1_mva_6 8192
#define TMEM1_mva_6 512
#define numReps_mva_6 1

void mva_6(hls::stream<ap_uint<16>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_6_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_6_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_6_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_6, MH1_mva_6, SIMD1_mva_6, PE1_mva_6, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_6_weights, mva_6_threshs, numReps_mva_6, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_14 32



// defines for network parameters
#define InWidth_str_dwc_14 1 
#define OutWidth_str_dwc_14 32 
#define NumInWords_str_dwc_14 512 
#define numReps_str_dwc_14 1

void str_dwc_14(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<32> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_14, OutWidth_str_dwc_14, NumInWords_str_dwc_14>(in0, out, numReps_str_dwc_14);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_7 32


#include "mva_7_thresh.h"

// defines for network parameters
#define MW1_mva_7 512
#define MH1_mva_7 512
#define SIMD1_mva_7 32
#define PE1_mva_7 1
#define WMEM1_mva_7 8192
#define TMEM1_mva_7 512
#define numReps_mva_7 1

void mva_7(hls::stream<ap_uint<32>> &in0,
                    hls::stream<ap_uint<1>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_7_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_7_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_7_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_7_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_7, MH1_mva_7, SIMD1_mva_7, PE1_mva_7, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_7_weights, mva_7_threshs, numReps_mva_7, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_8 16



// defines for network parameters
#define MW1_mva_8 512
#define MH1_mva_8 10
#define SIMD1_mva_8 1
#define PE1_mva_8 1
#define WMEM1_mva_8 5120
#define TMEM1_mva_8 0
#define numReps_mva_8 1

void mva_8(hls::stream<ap_uint<1>> &in0,
                    hls::stream<ap_uint<16>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_8_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_8_weights.m_weights complete dim=1
Matrix_Vector_Activate_Batch<MW1_mva_8, MH1_mva_8, SIMD1_mva_8, PE1_mva_8, 1, Recast<XnorMul>, Slice<ap_int<16>>, Identity>
                (in0, out, mva_8_weights, PassThroughActivation<ap_int<16>>(), numReps_mva_8, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_lab_sel_0 16



// defines for network parameters


void lab_sel_0(hls::stream<ap_uint<1*16>> &in0,
                hls::stream<ap_uint<8> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
LabelSelect_Batch<10, 1, 1, ap_int<16>, ap_uint<8> > (in0, out, 1);
}

// ------------------------------------------------------------------------

void layer_last (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<8>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<16>> out_str_dwc_0("out_str_dwc_0");
    static hls::stream<ap_uint<1>> out_mva_0("out_mva_0");
    static hls::stream<ap_uint<32>> out_str_dwc_1("out_str_dwc_1");
    static hls::stream<ap_uint<1>> out_mva_1("out_mva_1");
    static hls::stream<ap_uint<16>> out_mva_2("out_mva_2");

#pragma HLS dataflow
    str_dwc_13(Input_1, out_str_dwc_0);
    mva_6(out_str_dwc_0, out_mva_0);
    str_dwc_14(out_mva_0, out_str_dwc_1);
    mva_7(out_str_dwc_1, out_mva_1);
    mva_8(out_mva_1, out_mva_2);
    lab_sel_0(out_mva_2, Output_1);

}
