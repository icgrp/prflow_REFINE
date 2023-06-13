
#define AP_INT_MAX_W_str_dwc_5 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_5 16 
#define OutWidth_str_dwc_5 72 
#define NumInWords_str_dwc_5 5184 
#define numReps_str_dwc_5 1
#define LCMWidth_str_dwc_5 144
#define NumLCMToOut_str_dwc_5 576

void str_dwc_5(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<144>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_5, LCMWidth_str_dwc_5, NumInWords_str_dwc_5>(in0, intermediate, numReps_str_dwc_5);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_5, OutWidth_str_dwc_5, NumLCMToOut_str_dwc_5>(intermediate, out, numReps_str_dwc_5);
}
