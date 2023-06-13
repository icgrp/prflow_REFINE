
#define AP_INT_MAX_W_str_dwc_7 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_7 16 
#define OutWidth_str_dwc_7 72 
#define NumInWords_str_dwc_7 7200 
#define numReps_str_dwc_7 1
#define LCMWidth_str_dwc_7 144
#define NumLCMToOut_str_dwc_7 800

void str_dwc_7(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<144>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_7, LCMWidth_str_dwc_7, NumInWords_str_dwc_7>(in0, intermediate, numReps_str_dwc_7);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_7, OutWidth_str_dwc_7, NumLCMToOut_str_dwc_7>(intermediate, out, numReps_str_dwc_7);
}
