#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/maxpool.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_3_1_0 144



// defines for network parameters
#define InWidth_str_dwc_3_1_0 16 
#define OutWidth_str_dwc_3_1_0 144 
#define NumInWords_str_dwc_3_1_0 7200 
#define numReps_str_dwc_3_1_0 1

void str_dwc_3_1_0(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<144> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3_1_0, OutWidth_str_dwc_3_1_0, NumInWords_str_dwc_3_1_0>(in0, out, numReps_str_dwc_3_1_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_3 144


#include "mva_3_thresh.h"

// defines for network parameters
#define MW1_mva_3 576
#define MH1_mva_3 64
#define SIMD1_mva_3 72
#define PE1_mva_3 8
#define WMEM1_mva_3 64
#define TMEM1_mva_3 8
#define numReps_mva_3 100

void mva_3(hls::stream<ap_uint<144>> &in0,
                    hls::stream<ap_uint<16>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_3_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_3_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_3_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_3, MH1_mva_3, SIMD1_mva_3, PE1_mva_3, 1, Slice<ap_int<2>>, Slice<ap_int<2>>, Recast<Binary>>
                (in0, out, mva_3_weights, mva_3_threshs, numReps_mva_3, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_3_1_1 128



// defines for network parameters
#define InWidth_str_dwc_3_1_1 16 
#define OutWidth_str_dwc_3_1_1 128 
#define NumInWords_str_dwc_3_1_1 800 
#define numReps_str_dwc_3_1_1 1

void str_dwc_3_1_1(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<128> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3_1_1, OutWidth_str_dwc_3_1_1, NumInWords_str_dwc_3_1_1>(in0, out, numReps_str_dwc_3_1_1);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_mp_batch_1 128



// defines for network parameters
#define ImgDim_str_mp_batch_1 10
#define PoolDim_str_mp_batch_1 2
#define NumChannels_str_mp_batch_1 64
#define numReps_str_mp_batch_1 1

void str_mp_batch_1(hls::stream<ap_uint<128>> &in0, 
                       hls::stream<ap_uint<128>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool_Precision<ImgDim_str_mp_batch_1, PoolDim_str_mp_batch_1, NumChannels_str_mp_batch_1, ap_int<2>, -2>(in0, out);
}

// ------------------------------------------------------------------------

void layer_3_1 (
        hls::stream<ap_uint<16>> & Input_1,
        hls::stream<ap_uint<128>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<144>> out_str_dwc_3_1_0("out_str_dwc_3_1_0");
    static hls::stream<ap_uint<16>> out_mva_3("out_mva_3");
    static hls::stream<ap_uint<128>> out_str_dwc_3_1_1("out_str_dwc_3_1_1");

#pragma HLS dataflow
    str_dwc_3_1_0(Input_1, out_str_dwc_3_1_0);
    mva_3(out_str_dwc_3_1_0, out_mva_3);
    str_dwc_3_1_1(out_mva_3, out_str_dwc_3_1_1);
    str_mp_batch_1(out_str_dwc_3_1_1, Output_1);

}
