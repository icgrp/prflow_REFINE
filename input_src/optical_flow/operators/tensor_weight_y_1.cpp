#include "../host/typedefs.h"

void tensor_weight_y_1(
    hls::stream<ap_uint<96>> &Input_1,
    hls::stream<ap_uint<96>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Output_1
#ifdef RISCV
  hls::LineBuffer<3,MAX_WIDTH,outer_3_t> buf;
#else
  xf::cv::LineBuffer<3,MAX_WIDTH,outer_3_t> buf;
#endif
  const pixel_t TENSOR_FILTER[] = {0.3243, 0.3513, 0.3243};
  TENSOR_WEIGHT_Y_OUTER: for(int r=0; r<MAX_HEIGHT+1; r++)
  {
    TENSOR_WEIGHT_Y_INNER: for(int c=0; c<MAX_WIDTH; c++)
    {
#pragma HLS pipeline II=1

      outer_3_t tmp;
      #pragma HLS data_pack variable=tmp
      #pragma HLS data_pack variable=buf.val[0]
      buf.shift_pixels_up(c);
      if(r<MAX_HEIGHT)
      {
        ap_uint<96> in_tmp;
        in_tmp = Input_1.read();
        tmp.val[0](31,0)  = in_tmp(31,0);
        tmp.val[1](31,0)  = in_tmp(63,32);
        tmp.val[2](31,0)  = in_tmp(95,64);
      }
      else
      {
        TENSOR_WEIGHT_Y_TMP_INIT: for(int i=0; i<3; i++){
#pragma HLS UNROLL
         tmp.val[i] = 0;
        }
      }
      buf.insert_bottom_row(tmp,c);

      tensor_3_t acc;
      TENSOR_WEIGHT_Y_ACC_INIT: for(int k =0; k<3; k++){
#pragma HLS UNROLL
       acc.val[k] = 0;
      }

      if (r >= 2 && r < MAX_HEIGHT)
      {
        TENSOR_WEIGHT_Y_TMP_OUTER: for(int i=0; i<3; i++)
        {
#pragma HLS UNROLL
          tmp = buf.getval(i,c);
          pixel_t k = TENSOR_FILTER[i];
          TENSOR_WEIGHT_Y_TMP_INNER: for(int component=0; component<3; component++)
          {
#pragma HLS UNROLL
            acc.val[component] = acc.val[component] + tmp.val[component]*k;
          }
        }
      }
      if(r >= 1)
      {
        ap_uint<96> widetemp;
        widetemp(31,0)  = acc.val[0](31, 0);
        widetemp(63,32)  = acc.val[1](31, 0);
        widetemp(95,64)  = acc.val[2](31, 0);
        Output_1.write(widetemp);
      }
    }
  }
}
