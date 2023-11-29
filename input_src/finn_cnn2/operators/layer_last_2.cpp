#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/activations.hpp"
#include "../host/finn-hlslib/maxpool.h"
#include "../host/finn-hlslib/mvau.hpp"
#include "../host/finn-hlslib/weights.hpp"

// ------------------------------------------------------------------------


void out_data_collect (
        hls::stream<ap_uint<8> > & Input_1,
        hls::stream<ap_uint<256> > & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
    ap_uint<8> in_tmp;
    static ap_uint<256> out_tmp;
    static ap_uint<16> counter = 0;

    in_tmp = Input_1.read();
    out_tmp(8*counter+7, 8*counter) = in_tmp;
    if(counter == 31){ // 32 data fits in 256bits
        Output_1.write(out_tmp);
        counter = 0;
    }
    else{
        counter++;
    }
}

// ------------------------------------------------------------------------

#define AP_INT_MAX_W_mva_8 16



// defines for network parameters
#define MW1_mva_8 256
#define MH1_mva_8 10
#define SIMD1_mva_8 1
#define PE1_mva_8 1
#define WMEM1_mva_8 2560
#define TMEM1_mva_8 0
#define numReps_mva_8 1

void mva_8(hls::stream<ap_uint<2>> &in0,
                    hls::stream<ap_uint<16>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#include "mva_8_params.h"
#pragma HLS ARRAY_PARTITION variable=mva_8_weights.m_weights complete dim=1
Matrix_Vector_Activate_Batch<MW1_mva_8, MH1_mva_8, SIMD1_mva_8, PE1_mva_8, 1, Slice<ap_int<2>>, Slice<ap_int<16>>, Recast<Binary>>
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

void layer_last_2 (
        hls::stream<ap_uint<2>> & Input_1,
        hls::stream<ap_uint<256>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1

    static hls::stream<ap_uint<16>> out_mva_8("out_mva_8");
    static hls::stream<ap_uint<8>> out_lab_sel_0("out_lab_sel_0");

#pragma HLS dataflow
    mva_8(Input_1, out_mva_8);
    lab_sel_0(out_mva_8, out_lab_sel_0);
    out_data_collect(out_lab_sel_0, Output_1);

}
