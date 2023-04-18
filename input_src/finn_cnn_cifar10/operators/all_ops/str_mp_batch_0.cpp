
#define AP_INT_MAX_W 64

#include "../host/finn-hlslib/bnn-library.h"

// includes for network parameters
#include "../host/finn-hlslib/maxpool.h"

// defines for network parameters
#define ImgDim 28
 #define PoolDim 2

                #define NumChannels 64
 #define numReps 1

void str_mp_batch_0(hls::stream<ap_uint<64> > &in0, hls::stream<ap_uint<64> > &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim, PoolDim, NumChannels>(in0, out);
}
