
#define AP_INT_MAX_W_str_mp_batch_1 128

#include "bnn-library.h"

// includes for network parameters
#include "maxpool.h"

// defines for network parameters
#define ImgDim_str_mp_batch_1 10
#define PoolDim_str_mp_batch_1 2
#define NumChannels_str_mp_batch_1 128
#define numReps_str_mp_batch_1 1

void str_mp_batch_1(hls::stream<ap_uint<128>> &in0, 
                       hls::stream<ap_uint<128>> &out)
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
StreamingMaxPool<ImgDim_str_mp_batch_1, PoolDim_str_mp_batch_1, NumChannels_str_mp_batch_1>(in0, out);
}
