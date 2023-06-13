
#define AP_INT_MAX_W 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 2 
#define OutWidth 72 
#define NumInWords 5184 
#define numReps 1

void StreamingDataWidthConverter_Batch_10(hls::stream<ap_uint<2> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
