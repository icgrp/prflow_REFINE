#include "../host/typedefs.h"
#include "../host/finn-hlslib/bnn-library.h"
#include "../host/finn-hlslib/maxpool.h"

// ------------------------------------------------------------------------


#define AP_INT_MAX_W_lab_sel_0 8



// defines for network parameters


void lab_sel_0(hls::stream<ap_uint<1*8>> &in0,
                hls::stream<ap_uint<8> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
LabelSelect_Batch<10, 1, 1, ap_int<8>, ap_uint<8> > (in0, out, 1);
}

// ------------------------------------------------------------------------

void layer_last_0 (
        hls::stream<ap_uint<8>> & Input_1,
        hls::stream<ap_uint<8>> & Output_1
        )
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1


#pragma HLS dataflow
    lab_sel_0(Input_1, Output_1);

}
