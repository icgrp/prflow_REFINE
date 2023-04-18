
#define AP_INT_MAX_W 72

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/streamtools.h"

// defines for network parameters
#define InWidth 16 
#define OutWidth 72 
#define NumInWords 7200 
#define numReps 1
#define LCMWidth 144
#define NumLCMToOut 800

void str_dwc_7(hls::stream<ap_uint<16> > &in0, hls::stream<ap_uint<72> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS DATAFLOW disable_start_propagation
hls::stream<ap_uint<144>> intermediate ("intermediate");
StreamingDataWidthConverter_Batch<InWidth, LCMWidth, NumInWords>(in0, intermediate, numReps);
StreamingDataWidthConverter_Batch<LCMWidth, OutWidth, NumLCMToOut>(intermediate, out, numReps);
}
