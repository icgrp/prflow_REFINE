
#define AP_INT_MAX_W_str_mp_batch_0 64

#include "bnn-library.h"

// includes for network parameters
#include "maxpool.h"

// defines for network parameters
#define ImgDim_str_mp_batch_0 28
#define PoolDim_str_mp_batch_0 2
#define NumChannels_str_mp_batch_0 64
#define numReps_str_mp_batch_0 1

void str_mp_batch_0(hls::stream<ap_uint<64>> &in0, 
                       hls::stream<ap_uint<64>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim_str_mp_batch_0, PoolDim_str_mp_batch_0, NumChannels_str_mp_batch_0>(in0, out);
}
