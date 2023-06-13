
#define AP_INT_MAX_W 128

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 32 
#define OutWidth 128 
#define NumInWords 400 
#define numReps 1

void StreamingDataWidthConverter_Batch_8(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<128> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}