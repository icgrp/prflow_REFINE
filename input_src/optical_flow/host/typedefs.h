/*===============================================================*/
/*                                                               */
/*                          kernel.h                             */
/*                                                               */
/*        Defines types and constants for host function          */
/*                                                               */
/*===============================================================*/

#ifndef __TYPEDEFS_H__
#define __TYPEDEFS_H__
//#include "ap_fixed.h"
const int MAX_HEIGHT = 436;
const int MAX_WIDTH = 1024;
// const int MAX_HEIGHT = 109;
// const int MAX_WIDTH = 64;

#include "ap_fixed.h"
//#include <hls_video.h>
#include "hls_stream.h"
#include <cassert>

// #include "/tools/Xilinx/Vivado/2021.1/include/multimediaIps/xf_video_mem.hpp"

#ifndef RISCV
  #include "/tools/Xilinx/Vivado/2022.1/include/multimediaIps/xf_video_mem.hpp"
#endif

typedef ap_uint<32> databus_t;
typedef ap_uint<128> bit128;
typedef ap_uint<512> bit512;
typedef ap_uint<64>  bit64;
typedef ap_uint<32>  bit32;
typedef ap_uint<160> bit160;
typedef ap_uint<96> bit96;

// define these constants so they can be used in pragma
const int max_width = MAX_WIDTH;
const int default_depth = MAX_WIDTH;

#define SDSOC


// User parameter
#define PAR_FACTOR 1
#define OUTER_WIDTH 16
#define OUTER_WIDTH_INT 11
#define CALC_WIDTH_INT 24
#define DUMMY_LEN 785


#include "ap_fixed.h"
typedef ap_fixed<17,9> input_t;
typedef ap_fixed<32,13> pixel_t;
// typedef ap_fixed<48,27> outer_pixel_t;
// typedef ap_fixed<96,56> calc_pixel_t;

typedef ap_fixed<OUTER_WIDTH, OUTER_WIDTH_INT> outer_pixel_t;
typedef ap_fixed<OUTER_WIDTH*2, CALC_WIDTH_INT> calc_pixel_t;

typedef ap_fixed<32,13> vel_pixel_t;
	
#ifdef OCL
	#include "ap_fixed.h"
	typedef ap_fixed<48,40> pixel_t;
#endif
#ifdef SW
	typedef float pixel_t;
#endif

typedef struct{
	pixel_t x;
	pixel_t y;
	pixel_t z;
}gradient_t;

typedef struct{
    outer_pixel_t val[6];
}outer_6_t; 

typedef struct{
    outer_pixel_t val[3];
}outer_3_t;

typedef struct{
    outer_pixel_t val[2];
}outer_2_t;

typedef struct{
    outer_pixel_t val[6];
}tensor_6_t;

typedef struct{
    outer_pixel_t val[3];
}tensor_3_t;

typedef struct{
    outer_pixel_t val[2];
}tensor_2_t;

typedef struct{
    vel_pixel_t x;
    vel_pixel_t y;
}velocity_t;

#include "ap_int.h"
// for data packing
typedef ap_uint<64> frames_t;
typedef ap_uint<32> stdio_t;


#endif