
#define AP_INT_MAX_W 72

#include "bnn-library.h"

// includes for network parameters
#include "streamtools.h"

// defines for network parameters
#define InWidth 64 
#define OutWidth 72 
#define NumInWords 7056 
#define numReps 1
#define LCMWidth 576
#define NumLCMToOut 784

void StreamingDataWidthConverter_Batch_3(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<576>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth, LCMWidth, NumInWords>(in0, intermediate, numReps);
StreamingDataWidthConverter_Batch<LCMWidth, OutWidth, NumLCMToOut>(intermediate, out, numReps);
}
