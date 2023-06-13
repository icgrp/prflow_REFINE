
#define AP_INT_MAX_W_str_dwc_12 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_12 1 
#define OutWidth_str_dwc_12 72 
#define NumInWords_str_dwc_12 2304 
#define numReps_str_dwc_12 1

void str_dwc_12(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_12, OutWidth_str_dwc_12, NumInWords_str_dwc_12>(in0, out, numReps_str_dwc_12);
}
