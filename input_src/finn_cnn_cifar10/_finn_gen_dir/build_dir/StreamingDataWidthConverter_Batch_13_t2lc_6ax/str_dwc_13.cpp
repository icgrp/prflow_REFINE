
#define AP_INT_MAX_W_str_dwc_13 16

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_13 1 
#define OutWidth_str_dwc_13 16 
#define NumInWords_str_dwc_13 256 
#define numReps_str_dwc_13 1

void str_dwc_13(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_13, OutWidth_str_dwc_13, NumInWords_str_dwc_13>(in0, out, numReps_str_dwc_13);
}
