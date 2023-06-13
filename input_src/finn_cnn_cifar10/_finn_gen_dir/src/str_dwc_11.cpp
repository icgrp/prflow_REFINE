
#define AP_INT_MAX_W_str_dwc_11 8

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_11 8 
#define OutWidth_str_dwc_11 1 
#define NumInWords_str_dwc_11 288 
#define numReps_str_dwc_11 1

void str_dwc_11(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<1> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_11, OutWidth_str_dwc_11, NumInWords_str_dwc_11>(in0, out, numReps_str_dwc_11);
}
