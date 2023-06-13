
#define AP_INT_MAX_W 32

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 32 
#define OutWidth 16 
#define NumInWords 576 
#define numReps 1

void StreamingDataWidthConverter_Batch_6(hls::stream<ap_uint<32> > &in0, hls::stream<ap_uint<16> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(in0, out, numReps);
}
