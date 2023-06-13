
#define AP_INT_MAX_W 64

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 64 
#define OutWidth 16 
#define NumInWords 196 
#define numReps 1

void StreamingDataWidthConverter_Batch_4(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
