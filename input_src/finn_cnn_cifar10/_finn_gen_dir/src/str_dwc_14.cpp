
#define AP_INT_MAX_W_str_dwc_14 32

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_14 1 
#define OutWidth_str_dwc_14 32 
#define NumInWords_str_dwc_14 512 
#define numReps_str_dwc_14 1

void str_dwc_14(hls::stream<ap_uint<1> > &in0, hls::stream<ap_uint<32> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_14, OutWidth_str_dwc_14, NumInWords_str_dwc_14>(in0, out, numReps_str_dwc_14);
}
