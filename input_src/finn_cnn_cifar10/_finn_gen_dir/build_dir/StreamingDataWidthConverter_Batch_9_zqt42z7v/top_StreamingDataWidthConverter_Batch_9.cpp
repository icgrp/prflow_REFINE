
#define AP_INT_MAX_W 128

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 128 
#define OutWidth 2 
#define NumInWords 25 
#define numReps 1

void StreamingDataWidthConverter_Batch_9(hls::stream<ap_uint<128> > &in0, hls::stream<ap_uint<2> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
