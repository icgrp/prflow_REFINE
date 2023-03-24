/*===============================================================*/
/*                                                               */
/*                          typedefs.h                           */
/*                                                               */
/*           Constant definitions and typedefs for host.         */
/*                                                               */
/*===============================================================*/
#ifndef __TYPEDEFS_H__
#define __TYPEDEFS_H__

// dataset information
#define NUM_TRAINING  18000
#define CLASS_SIZE    1800
#define NUM_TEST      2000
#define DIGIT_WIDTH   4
#define NUM_OPS 10
#define PAR_FACTOR_OP PAR_FACTOR/NUM_OPS
// typedefs
typedef unsigned long long DigitType;
typedef unsigned char      LabelType;


#include "ap_int.h"
typedef ap_uint<512> bit512;
typedef ap_uint<128> bit128;
typedef ap_uint<64> bit64;
typedef ap_uint<32> bit32;
// sdsoc wide vector type
typedef ap_uint<256>  WholeDigitType;

// parameters
#define K_CONST 5
#define OutputTmpWidth 32*K_CONST
typedef ap_uint<OutputTmpWidth> OutputTmpType;
#define PAR_FACTOR 40
#include <hls_stream.h>
#endif
