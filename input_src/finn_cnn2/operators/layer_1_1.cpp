#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/maxpool.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_1_1_0 144



// defines for network parameters
#define InWidth_str_dwc_1_1_0 64 
#define OutWidth_str_dwc_1_1_0 144 
#define NumInWords_str_dwc_1_1_0 7056 
#define numReps_str_dwc_1_1_0 1
#define LCMWidth_str_dwc_1_1_0 576
#define NumLCMToOut_str_dwc_1_1_0 784

void str_dwc_1_1_0(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<144> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<576>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_1_1_0, LCMWidth_str_dwc_1_1_0, NumInWords_str_dwc_1_1_0>(in0, intermediate, numReps_str_dwc_1_1_0);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_1_1_0, OutWidth_str_dwc_1_1_0, NumLCMToOut_str_dwc_1_1_0>(intermediate, out, numReps_str_dwc_1_1_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_1 144


#include "mva_1_thresh.h"

// defines for network parameters
#define MW1_mva_1 288
#define MH1_mva_1 32
#define SIMD1_mva_1 72
#define PE1_mva_1 32
#define WMEM1_mva_1 4
#define TMEM1_mva_1 1
#define numReps_mva_1 784

void mva_1(hls::stream<ap_uint<144>> &in0,
                    hls::stream<ap_uint<64>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_1_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_1_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_1, MH1_mva_1, SIMD1_mva_1, PE1_mva_1, 1, Slice<ap_int<2>>, Slice<ap_int<2>>, Recast<Binary>>
                (in0, out, mva_1_weights, mva_1_threshs, numReps_mva_1, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_mp_batch_0 64



// defines for network parameters
#define ImgDim_str_mp_batch_0 28
#define PoolDim_str_mp_batch_0 2
#define NumChannels_str_mp_batch_0 32
#define numReps_str_mp_batch_0 1

void str_mp_batch_0(hls::stream<ap_uint<64>> &in0, 
                       hls::stream<ap_uint<64>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool_Precision<ImgDim_str_mp_batch_0, PoolDim_str_mp_batch_0, NumChannels_str_mp_batch_0, ap_int<2>, -2>(in0, out);
}

// ------------------------------------------------------------------------

void layer_1_1 (
        hls::stream<ap_uint<64>> & Input_1,
        hls::stream<ap_uint<64>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<144>> out_str_dwc_1_1_0("out_str_dwc_1_1_0");
    static hls::stream<ap_uint<64>> out_mva_1("out_mva_1");

#pragma HLS dataflow
    str_dwc_1_1_0(Input_1, out_str_dwc_1_1_0);
    mva_1(out_str_dwc_1_1_0, out_mva_1);
    str_mp_batch_0(out_mva_1, Output_1);

}
