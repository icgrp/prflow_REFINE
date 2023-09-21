#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/streamtools.h"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_str_dwc_3 8



// defines for network parameters
#define InWidth_str_dwc_3 1 
#define OutWidth_str_dwc_3 8 
#define NumInWords_str_dwc_3 64 
#define numReps_str_dwc_3 1

void str_dwc_3(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<8> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3, OutWidth_str_dwc_3, NumInWords_str_dwc_3>(in0, out, numReps_str_dwc_3);
}

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_mva_4 8



// defines for network parameters
#define MW1_mva_4 64
#define MH1_mva_4 10
#define SIMD1_mva_4 8
#define PE1_mva_4 1
#define WMEM1_mva_4 80
#define TMEM1_mva_4 0
#define numReps_mva_4 1

void mva_4(hls::stream<ap_uint<8>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_4_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_4_weights.m_weights complete dim=1
Matrix_Vector_Activate_Batch<MW1_mva_4, MH1_mva_4, SIMD1_mva_4, PE1_mva_4, 1, Recast<XnorMul>, Slice<ap_int<8>>, Identity>
                (in0, out, mva_4_weights, PassThroughActivation<ap_int<8>>(), numReps_mva_4, ap_resource_lut());
}

// ------------------------------------------------------------------------

void layer_4_0 (
        hls::stream<ap_uint<1>> & Input_1,
        hls::stream<ap_uint<8>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<8>> out_str_dwc_3("out_str_dwc_3");

#pragma HLS dataflow
    str_dwc_3(Input_1, out_str_dwc_3);
    mva_4(out_str_dwc_3, Output_1);

}
