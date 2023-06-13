
#define AP_INT_MAX_W 64

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 8 
#define OutWidth 64 
#define NumInWords 7200 
#define numReps 1

void StreamingDataWidthConverter_Batch_2(hls::stream<ap_uint<8> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
