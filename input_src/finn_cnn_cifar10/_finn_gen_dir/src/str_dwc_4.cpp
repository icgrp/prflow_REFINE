
#define AP_INT_MAX_W_str_dwc_4 64

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_4 64 
#define OutWidth_str_dwc_4 16 
#define NumInWords_str_dwc_4 196 
#define numReps_str_dwc_4 1

void str_dwc_4(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_4, OutWidth_str_dwc_4, NumInWords_str_dwc_4>(in0, out, numReps_str_dwc_4);
}
