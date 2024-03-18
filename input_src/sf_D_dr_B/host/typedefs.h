/*===============================================================*/
/*                                                               */
/*                          typedefs.h                           */
/*                                                               */
/*              Constant definitions and typedefs.               */
/*                                                               */
/*===============================================================*/

#ifndef __TYPEDEFS_H__
#define __TYPEDEFS_H__

#define SDSOC

////////////////////
// Spam Filtering //
////////////////////

// User parameters - play around with PAR_FACTOR and NUM_FEATURES to create different sizes of operators
#define PAR_FACTOR 32

// dataset information
const int NUM_FEATURES  = 1024;

const int NUM_SAMPLES   = 5000;
const int NUM_TRAINING  = 4500;
const int NUM_TESTING   = 500;
const int STEP_SIZE     = 60000; 
const int NUM_EPOCHS    = 5;
const int DATA_SET_SIZE = NUM_FEATURES * NUM_SAMPLES;
#include <hls_stream.h>


#ifdef SDSOC
  // embedded platforms have less off-chip bandwidth
  #define VFTYPE_WIDTH  64
  #define VDTYPE_WIDTH  64
#endif

// datatypes for accelerator

  #include "ap_int.h"
  #include "ap_fixed.h"
  // features / parameters
  typedef ap_uint<512> bit512;
  typedef ap_uint<128> bit128;
  typedef ap_uint<64> bit64;
  typedef ap_uint<32> bit32;
  #define FTYPE_TWIDTH 32
  #define FTYPE_IWIDTH 13
  typedef ap_fixed<FTYPE_TWIDTH,FTYPE_IWIDTH> FeatureType;
  typedef ap_uint<VFTYPE_WIDTH>               VectorFeatureType;
  const int F_VECTOR_SIZE = VFTYPE_WIDTH / FTYPE_TWIDTH;
  // training data
  #define DTYPE_TWIDTH 64 // changed
  #define DTYPE_IWIDTH 4
  typedef ap_fixed<DTYPE_TWIDTH,DTYPE_IWIDTH>  DataType;
  typedef ap_uint<VDTYPE_WIDTH>                VectorDataType;
  const int D_VECTOR_SIZE = VDTYPE_WIDTH / DTYPE_TWIDTH;
  // label
  #define LTYPE_WIDTH   8
  #define VLTYPE_WIDTH  32
  typedef ap_uint<LTYPE_WIDTH>                 LabelType;
  typedef ap_uint<VLTYPE_WIDTH>                VectorLabelType;
  const int L_VECTOR_SIZE = VLTYPE_WIDTH / LTYPE_WIDTH;
  
  // datatypes for the LUT
  #define LUTOUT_TWIDTH     16
  #define LUTOUT_IWIDTH     6
  #define LUTIN_TWIDTH      16
  #define LUTIN_IWIDTH      8
  //typedef ap_ufixed<32, 20> TmpFixed;
  typedef ap_fixed<32, 20> TmpFixed;
  typedef ap_uint<LUTIN_TWIDTH> IdxFixed; 
  typedef ap_fixed<LUTIN_TWIDTH, LUTIN_IWIDTH> LutInFixed;
  typedef ap_fixed<LUTOUT_TWIDTH, LUTOUT_IWIDTH> LutOutFixed;


///////////////////////
// Digit Recognition //
///////////////////////

// dataset information
#define NUM_TRAINING_DR  18000
#define CLASS_SIZE    1800
// #define NUM_TEST      2000
#define DIGIT_WIDTH   4

// typedefs
typedef unsigned long long DigitType;
typedef unsigned char      LabelType_DR;

typedef ap_uint<256>  WholeDigitType;

// User parameters - play around with params like K_CONST, IMAGE_SIZE, IMAGE_WIDTH to create different sizes of operators
#define K_CONST 2
#define IMAGE_SIZE 256
#define IMAGE_WIDTH 256 // multiple of 32 equal or greater than IMAGE_SIZE
#define OutputTmpWidth 32*K_CONST
typedef ap_uint<OutputTmpWidth> OutputTmpType;


#endif
