#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/maxpool.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_2 72



// defines for network parameters
#define InWidth_str_dwc_2 32 
#define OutWidth_str_dwc_2 72 
#define NumInWords_str_dwc_2 7056 
#define numReps_str_dwc_2 1
#define LCMWidth_str_dwc_2 288
#define NumLCMToOut_str_dwc_2 784

void str_dwc_2(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<288>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_2, LCMWidth_str_dwc_2, NumInWords_str_dwc_2>(in0, intermediate, numReps_str_dwc_2);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_2, OutWidth_str_dwc_2, NumLCMToOut_str_dwc_2>(intermediate, out, numReps_str_dwc_2);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_1 72


#include "mva_1_thresh.h"

// defines for network parameters
#define MW1_mva_1 288
#define MH1_mva_1 32
#define SIMD1_mva_1 72
#define PE1_mva_1 32
#define WMEM1_mva_1 4
#define TMEM1_mva_1 1
#define numReps_mva_1 784

void mva_1(hls::stream<ap_uint<72>> &in0,
                    hls::stream<ap_uint<32>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_1_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_1_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_1_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_1, MH1_mva_1, SIMD1_mva_1, PE1_mva_1, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_1_weights, mva_1_threshs, numReps_mva_1, ap_resource_lut());
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_mp_batch_0 32



// defines for network parameters
#define ImgDim_str_mp_batch_0 28
#define PoolDim_str_mp_batch_0 2
#define NumChannels_str_mp_batch_0 32
#define numReps_str_mp_batch_0 1

void str_mp_batch_0(hls::stream<ap_uint<32>> &in0, 
                       hls::stream<ap_uint<32>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim_str_mp_batch_0, PoolDim_str_mp_batch_0, NumChannels_str_mp_batch_0>(in0, out);
}

// ------------------------------------------------------------------------

void layer_1_1 (
        hls::stream<ap_uint<32>> & Input_1,
        hls::stream<ap_uint<32>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<72>> out_str_dwc_2("out_str_dwc_2");
    static hls::stream<ap_uint<32>> out_mva_1("out_mva_1");

#pragma HLS dataflow
    str_dwc_2(Input_1, out_str_dwc_2);
    mva_1(out_str_dwc_2, out_mva_1);
    str_mp_batch_0(out_mva_1, Output_1);

}
