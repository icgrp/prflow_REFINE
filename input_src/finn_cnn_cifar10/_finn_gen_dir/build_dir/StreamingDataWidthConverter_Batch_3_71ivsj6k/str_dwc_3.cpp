
#define AP_INT_MAX_W_str_dwc_3 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_3 64 
#define OutWidth_str_dwc_3 72 
#define NumInWords_str_dwc_3 7056 
#define numReps_str_dwc_3 1
#define LCMWidth_str_dwc_3 576
#define NumLCMToOut_str_dwc_3 784

void str_dwc_3(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<576>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth_str_dwc_3, LCMWidth_str_dwc_3, NumInWords_str_dwc_3>(in0, intermediate, numReps_str_dwc_3);
StreamingDataWidthConverter_Batch<LCMWidth_str_dwc_3, OutWidth_str_dwc_3, NumLCMToOut_str_dwc_3>(intermediate, out, numReps_str_dwc_3);
}
