/*===============================================================*/
/*                                                               */
/*                          typedefs.h                           */
/*                                                               */
/*           Constant definitions and typedefs for host.         */
/*                                                               */
/*===============================================================*/
#define SDSOC
#ifndef __TYPEDEFS_H__
#define __TYPEDEFS_H__

// dataset information
#define NUM_TRAINING  18000
#define CLASS_SIZE    1800
#define NUM_TEST      2000
#define DIGIT_WIDTH   4

// fixed to 10 operators
// #define NUM_OPS 10
// #define OP_SIZE PAR_FACTOR/NUM_OPS

// typedefs
typedef unsigned long long DigitType;
typedef unsigned char      LabelType;

#ifdef OCL
  #include <string>
  // target device
  // change here to map to a different device
  const std::string TARGET_DEVICE = "xilinx:aws-vu9p-f1:4ddr-xpr-2pr:4.0";
#endif

#ifdef SDSOC
  #include "ap_int.h"
  typedef ap_uint<512> bit512;
  typedef ap_uint<128> bit128;
  typedef ap_uint<64> bit64;
  typedef ap_uint<32> bit32;
  // sdsoc wide vector type
  typedef ap_uint<256>  WholeDigitType;
#endif

#include "hls_stream.h"


// User parameters - play around with params like K_CONST, IMAGE_SIZE, IMAGE_WIDTH to create different sizes of operators
#define K_CONST 2
#define IMAGE_SIZE 256
#define IMAGE_WIDTH 256 // multiple of 32 equal or greater than IMAGE_SIZE
#define OutputTmpWidth 32*K_CONST
typedef ap_uint<OutputTmpWidth> OutputTmpType;

#endif