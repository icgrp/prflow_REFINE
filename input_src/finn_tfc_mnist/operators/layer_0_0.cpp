#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_thr_batch_0 64


#include "thr_batch_0_thresh.h"

// defines for network parameters
#define NumChannels1_thr_batch_0 784
#define PE1_thr_batch_0 8
#define numReps_thr_batch_0 1
#define ImgDim1_thr_batch_0 1

void thr_batch_0(hls::stream<ap_uint<64>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=3
#pragma HLS RESOURCE variable=thr_batch_0_threshs.m_thresholds core=ROM_2P_LUTRAM
Thresholding_Batch<ImgDim1_thr_batch_0, NumChannels1_thr_batch_0, PE1_thr_batch_0, Slice<ap_uint<8>>, Slice<ap_uint<1>>>
                (in0, out, thr_batch_0_threshs, numReps_thr_batch_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_0 56



// defines for network parameters
#define InWidth_str_dwc_0 8 
#define OutWidth_str_dwc_0 56 
#define NumInWords_str_dwc_0 98 
#define numReps_str_dwc_0 1

void str_dwc_0(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<56> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_0, OutWidth_str_dwc_0, NumInWords_str_dwc_0>(in0, out, numReps_str_dwc_0);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_0 64


#include "mva_0_thresh.h"

// defines for network parameters
#define MW1_mva_0 784
#define MH1_mva_0 64
#define SIMD1_mva_0 56
#define PE1_mva_0 64
#define WMEM1_mva_0 14
#define TMEM1_mva_0 1
#define numReps_mva_0 1

void mva_0(hls::stream<ap_uint<56>> &in0,
                    hls::stream<ap_uint<64>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_0_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_0_weights.m_weights complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=mva_0_threshs.m_thresholds complete dim=3
Matrix_Vector_Activate_Batch<MW1_mva_0, MH1_mva_0, SIMD1_mva_0, PE1_mva_0, 1, Recast<XnorMul>, Slice<ap_uint<1>>, Identity>
                (in0, out, mva_0_weights, mva_0_threshs, numReps_mva_0, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_0_0 (
        hls::stream<ap_uint<64> > & Input_1,
        hls::stream<ap_uint<64> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<8>> out_thr_batch("out_thr_batch");
    static hls::stream<ap_uint<56>> out_str_dwc_0("out_str_dwc_0");

#pragma HLS dataflow
    thr_batch_0(Input_1, out_thr_batch);
    str_dwc_0(out_thr_batch, out_str_dwc_0);
    mva_0(out_str_dwc_0, Output_1);

}
