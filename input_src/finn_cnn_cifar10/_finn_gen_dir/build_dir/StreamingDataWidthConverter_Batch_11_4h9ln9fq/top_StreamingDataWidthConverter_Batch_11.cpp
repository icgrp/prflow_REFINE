
#define AP_INT_MAX_W 8

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 8 
#define OutWidth 1 
#define NumInWords 288 
#define numReps 1

void StreamingDataWidthConverter_Batch_11(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<1> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
