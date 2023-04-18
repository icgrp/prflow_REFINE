
#define AP_INT_MAX_W 216

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/streamtools.h"

// defines for network parameters
#define InWidth 24 
#define OutWidth 216 
#define NumInWords 8100 
#define numReps 1

void str_dwc_1(hls::stream<ap_uint<24> > &in0, hls::stream<ap_uint<216> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
