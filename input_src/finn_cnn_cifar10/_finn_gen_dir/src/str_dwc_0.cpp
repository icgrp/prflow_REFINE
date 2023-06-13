
#define AP_INT_MAX_W_str_dwc_0 24

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_0 8 
#define OutWidth_str_dwc_0 24 
#define NumInWords_str_dwc_0 3072 
#define numReps_str_dwc_0 1

void str_dwc_0(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<24> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_0, OutWidth_str_dwc_0, NumInWords_str_dwc_0>(in0, out, numReps_str_dwc_0);
}
