#include "../host/typedefs.h"

void output_data(
  hls::stream<ap_uint<32>> &Input_1,
  hls::stream<ap_uint<32>> &Input_2,
  hls::stream<ap_uint<256>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Output_1
#pragma HLS interface axis register port=Input_2

static ap_uint<32> counter=0;
  OUT_CONVERT: for (int i = 0; i < MAX_HEIGHT*MAX_WIDTH/4; i++)
  {
    ap_uint<256> tmpframe;
#pragma HLS pipeline II = 2
    for(int j=0; j<4; j++){
      tmpframe(j*64+31, j*64   ) = Input_1.read();
      tmpframe(j*64+63, j*64+32) = Input_2.read();
    }
    if (counter < MAX_HEIGHT*MAX_WIDTH/4){
      Output_1.write(tmpframe);
      counter++;
    }
  }
}


void f_c_module(
    hls::stream<ap_uint<128>> &Input_1,
    hls::stream<ap_uint<32>> &Output_1,
    hls::stream<ap_uint<32>> &Output_2)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Output_1
#pragma HLS interface axis register port=Output_2

  static float buf[2];

  FLOW_OUTER: for(int r=0; r<MAX_HEIGHT; r++)
  {
    FLOW_INNER: for(int c=0; c<MAX_WIDTH; c++)
    {
      #pragma HLS pipeline II=1
      tensor_6_t tmp_tensor;
      ap_uint<128> widetemp;

      widetemp(127,0) = Input_1.read();
      tmp_tensor.val[0](15,0)  = widetemp(15,0);
      tmp_tensor.val[1](15,0)  = widetemp(31,16);
      tmp_tensor.val[2](15,0)  = widetemp(47,32);
      tmp_tensor.val[3](15,0)  = widetemp(63,48);
      tmp_tensor.val[4](15,0)  = widetemp(79,64);
      tmp_tensor.val[5](15,0)  = widetemp(95,80);

      if(r>=2 && r<MAX_HEIGHT-2 && c>=2 && c<MAX_WIDTH-2)
      {
        calc_pixel_t t1 = (calc_pixel_t) tmp_tensor.val[0];
        calc_pixel_t t2 = (calc_pixel_t) tmp_tensor.val[1];
        calc_pixel_t t3 = (calc_pixel_t) tmp_tensor.val[2];
        calc_pixel_t t4 = (calc_pixel_t) tmp_tensor.val[3];
        calc_pixel_t t5 = (calc_pixel_t) tmp_tensor.val[4];
        calc_pixel_t t6 = (calc_pixel_t) tmp_tensor.val[5];

        calc_pixel_t denom = t1*t2-t4*t4;
        calc_pixel_t numer0 = t6*t4-t5*t2;
        calc_pixel_t numer1 = t5*t4-t6*t1;

        if(denom != 0)
        {
          buf[0] = (float) numer0 / (float) denom;
          buf[1] = (float) numer1 / (float) denom;
        }
        else
        {
          buf[0] = 0;
          buf[1] = 0;
        }
      }
      else
      {
        buf[0] = 0;
        buf[1] = 0;
      }
      stdio_t tmpframe_0, tmpframe_1;
      vel_pixel_t tmpvel_0, tmpvel_1;

      tmpvel_0 = (vel_pixel_t)buf[0];
      tmpframe_0(31,0) = tmpvel_0(31,0);

      tmpvel_1 = (vel_pixel_t)buf[1];
      tmpframe_1(31,0) = tmpvel_1(31,0);

      Output_1.write(tmpframe_0);
      Output_2.write(tmpframe_1);
    }
  }
}

void flow_calc(
    hls::stream<ap_uint<128>> &Input_1,
    hls::stream<ap_uint<256>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Output_1

    static hls::stream<ap_uint<32>> f_c_module_out_1("f_c_module_out_1_stream");
    static hls::stream<ap_uint<32>> f_c_module_out_2("f_c_module_out_2_stream");

#pragma HLS dataflow

    f_c_module(Input_1, f_c_module_out_1, f_c_module_out_2);
    output_data(f_c_module_out_1, f_c_module_out_2, Output_1);

}
