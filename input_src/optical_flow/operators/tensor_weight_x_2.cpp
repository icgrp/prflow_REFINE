#include "../host/typedefs.h"

void tensor_weight_x_2(
    hls::stream<ap_uint<96>> &Input_1,
    hls::stream<ap_uint<96>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Output_1
#ifdef RISCV
  hls::Window<1,3,tensor_3_t> buf;
#else
  xf::cv::Window<1,3,tensor_3_t> buf;
#endif
  const pixel_t TENSOR_FILTER[] = {0.3243, 0.3513, 0.3243};
  TENSOR_WEIGHT_X_OUTER: for(int r=0; r<MAX_HEIGHT; r++)
  {
    TENSOR_WEIGHT_X_INNER: for(int c=0; c<MAX_WIDTH+1; c++)
    {
#pragma HLS pipeline II=1

      buf.shift_pixels_left();
      tensor_3_t tmp;
      if(c<MAX_WIDTH)
      {
        ap_uint<96> widetemp;
        widetemp = Input_1.read();
        tmp.val[0](31,0)  = widetemp(31,0);
        tmp.val[1](31,0)  = widetemp(63,32);
        tmp.val[2](31,0)  = widetemp(95,64);
      }
      else
      {
        TENSOR_WEIGHT_X_TMP_INIT: for(int i=0; i<3; i++)
#pragma HLS UNROLL
          tmp.val[i] = 0;
      }
      buf.insert_pixel(tmp,0,2);

      tensor_3_t acc;
      TENSOR_WEIGHT_X_ACC_INIT: for(int k =0; k<3; k++)
#pragma HLS UNROLL
        acc.val[k] = 0;
      if (c >= 2 && c < MAX_WIDTH)
      {
        TENSOR_WEIGHT_X_TMP_OUTER: for(int i=0; i<3; i++)
        {
#pragma HLS UNROLL
          tmp = buf.getval(0,i);
          TENSOR_WEIGHT_X_TMP_INNER: for(int component=0; component<3; component++)
          {
#pragma HLS UNROLL
            acc.val[component] = acc.val[component] + tmp.val[component]*TENSOR_FILTER[i];
          }
        }
      }
      if(c>=1)
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
