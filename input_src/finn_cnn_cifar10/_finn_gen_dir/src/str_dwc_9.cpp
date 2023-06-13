
#define AP_INT_MAX_W_str_dwc_9 128

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_9 128 
#define OutWidth_str_dwc_9 2 
#define NumInWords_str_dwc_9 25 
#define numReps_str_dwc_9 1

void str_dwc_9(hls::stream<ap_uint<128> > &in0, hls::stream<ap_uint<2> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_9, OutWidth_str_dwc_9, NumInWords_str_dwc_9>(in0, out, numReps_str_dwc_9);
}
