
#define AP_INT_MAX_W_thr_batch_0 8

#include "bnn-library.h"

// includes for network parameters
#include "activations.hpp"
#include "thr_batch_0_thresh.h"

// defines for network parameters
#define NumChannels1_thr_batch_0 3
#define PE1_thr_batch_0 1
#define numReps_thr_batch_0 1
#define ImgDim1_thr_batch_0 1024

void thr_batch_0(hls::stream<ap_uint<8>> &in0,
                    hls::stream<ap_uint<8>> &out
                    )
{
#pragma HLS INTERFACE axis register port=in0
#pragma HLS INTERFACE axis register port=out
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=1
#pragma HLS ARRAY_PARTITION variable=thr_batch_0_threshs.m_thresholds complete dim=3
#pragma HLS RESOURCE variable=thr_batch_0_threshs.m_thresholds core=ROM_2P_LUTRAM
Thresholding_Batch<ImgDim1_thr_batch_0, NumChannels1_thr_batch_0, PE1_thr_batch_0, Slice<ap_uint<8>>, Slice<ap_int<8>>>
                (in0, out, thr_batch_0_threshs, numReps_thr_batch_0);
}
