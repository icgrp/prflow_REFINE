
#define AP_INT_MAX_W 128

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/streamtools.h"

// defines for network parameters
#define InWidth 2 
#define OutWidth 128 
#define NumInWords 64 
#define numReps 1

void str_dwc_1(hls::stream<ap_uint<2> > &Input_1, 
               hls::stream<ap_uint<128> > &Output_1)
{
#pragma HLS INTERFACE axis register port=Input_1
#pragma HLS INTERFACE axis register port=Output_1
StreamingDataWidthConverter_Batch<InWidth, OutWidth, NumInWords>(Input_1, Output_1, numReps);
}
