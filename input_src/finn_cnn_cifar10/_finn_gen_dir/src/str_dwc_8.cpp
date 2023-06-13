
#define AP_INT_MAX_W_str_dwc_8 128

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth_str_dwc_8 32 
#define OutWidth_str_dwc_8 128 
#define NumInWords_str_dwc_8 400 
#define numReps_str_dwc_8 1

void str_dwc_8(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<128> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth_str_dwc_8, OutWidth_str_dwc_8, NumInWords_str_dwc_8>(in0, out, numReps_str_dwc_8);
}
