#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_2 64



// defines for network parameters
#define InWidth_str_dwc_2 1 
#define OutWidth_str_dwc_2 64 
#define NumInWords_str_dwc_2 64 
#define numReps_str_dwc_2 1

void str_dwc_2(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_2, OutWidth_str_dwc_2, NumInWords_str_dwc_2>(in0, out, numReps_str_dwc_2);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_3 64


#include "mva_3_thresh.h"

// defines for network parameters
#define MW1_mva_3 64
#define MH1_mva_3 64
#define SIMD1_mva_3 64
#define PE1_mva_3 1
#define WMEM1_mva_3 64
#define TMEM1_mva_3 64
#define numReps_mva_3 1

void mva_3(hls::stream<ap_uint<64>> &in0,
                    hls::stream<ap_uint<1>> &out
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

void layer_3_0 (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<1>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<64>> out_str_dwc_2("out_str_dwc_2");

#pragma HLS dataflow
    str_dwc_2(Input_1, out_str_dwc_2);
    mva_3(out_str_dwc_2, Output_1);

}
