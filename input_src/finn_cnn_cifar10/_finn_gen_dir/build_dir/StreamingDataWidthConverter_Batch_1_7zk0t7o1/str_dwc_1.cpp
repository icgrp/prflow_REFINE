
#define AP_INT_MAX_W_str_dwc_1 216

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_1 24 
#define OutWidth_str_dwc_1 216 
#define NumInWords_str_dwc_1 8100 
#define numReps_str_dwc_1 1

void str_dwc_1(hls::stream<ap_uint<24> > &in0, hls::stream<ap_uint<216> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_1, OutWidth_str_dwc_1, NumInWords_str_dwc_1>(in0, out, numReps_str_dwc_1);
}
