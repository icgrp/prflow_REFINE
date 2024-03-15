#include "../host/typedefs.h"

static void tensor_weight_x_i1(
    hls::stream<ap_uint<256>> &Input_1,
    hls::stream<ap_uint<256>> &Output_1)
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
        ap_uint<256> widetemp;
        widetemp(255,0) = Input_1.read();
        tmp.val[0](47,0)  = widetemp(47,0);
        tmp.val[1](47,0)  = widetemp(95,48);
        tmp.val[2](47,0)  = widetemp(143,96);
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
        ap_uint<256> widetemp;
        widetemp(47,0)  = acc.val[0](47, 0);
        widetemp(95,48)  = acc.val[1](47, 0);
        widetemp(143,96)  = acc.val[2](47, 0);
        widetemp(255,144) = 0;
        Output_1.write(widetemp(255,0));
      }
    }
  }
}


static void tensor_weight_x_i2(
    hls::stream<ap_uint<256>> &Input_1,
    hls::stream<ap_uint<256>> &Output_1)
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
        ap_uint<256> widetemp;
        widetemp(255,0) = Input_1.read();
        tmp.val[0](47,0)  = widetemp(47,0);
        tmp.val[1](47,0)  = widetemp(95,48);
        tmp.val[2](47,0)  = widetemp(143,96);
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
        ap_uint<256> widetemp;
        widetemp(47,0)  = acc.val[0](47, 0);
        widetemp(95,48)  = acc.val[1](47, 0);
        widetemp(143,96)  = acc.val[2](47, 0);
        widetemp(255,144) = 0;
        Output_1.write(widetemp(255,0));
      }
    }
  }
}


static void output_data(
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


static void f_c_module(
    hls::stream<ap_uint<256>> &Input_1,
    hls::stream<ap_uint<256>> &Input_2,
    hls::stream<ap_uint<32>> &Output_1,
    hls::stream<ap_uint<32>> &Output_2)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Input_2
#pragma HLS interface axis register port=Output_1
#pragma HLS interface axis register port=Output_2

  static float buf[2];

  FLOW_OUTER: for(int r=0; r<MAX_HEIGHT; r++)
  {
    FLOW_INNER: for(int c=0; c<MAX_WIDTH; c++)
    {
      #pragma HLS pipeline II=1
      tensor_6_t tmp_tensor;
      ap_uint<256> widetemp;

      widetemp(255,0) = Input_1.read();
      tmp_tensor.val[0](47,0)  = widetemp(47,0);
      tmp_tensor.val[1](47,0)  = widetemp(95,48);
      tmp_tensor.val[2](47,0)  = widetemp(143,96);
      widetemp(255,0) = Input_2.read();
      tmp_tensor.val[3](47,0)  = widetemp(47,0);
      tmp_tensor.val[4](47,0)  = widetemp(95,48);
      tmp_tensor.val[5](47,0)  = widetemp(143,96);

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

static void flow_calc_body(
    hls::stream<ap_uint<256>> &Input_1,
    hls::stream<ap_uint<256>> &Input_2,
    hls::stream<ap_uint<256>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Input_2
#pragma HLS interface axis register port=Output_1

    static hls::stream<ap_uint<32>> f_c_module_out_1("f_c_module_out_1_stream");
    static hls::stream<ap_uint<32>> f_c_module_out_2("f_c_module_out_2_stream");

#pragma HLS dataflow

    f_c_module(Input_1, Input_2, f_c_module_out_1, f_c_module_out_2);
    output_data(f_c_module_out_1, f_c_module_out_2, Output_1);

}


void flow_calc_1(
    hls::stream<ap_uint<256>> &Input_1,
    hls::stream<ap_uint<256>> &Input_2,
    hls::stream<ap_uint<256>> &Output_1)
{
#pragma HLS interface axis register port=Input_1
#pragma HLS interface axis register port=Input_2
#pragma HLS interface axis register port=Output_1

    static hls::stream<ap_uint<256>> tensor_weight_x_out_1("tensor_weight_x_out_1_stream");
    static hls::stream<ap_uint<256>> tensor_weight_x_out_2("tensor_weight_x_out_2_stream");

#pragma HLS dataflow
    tensor_weight_x_i1(Input_1, tensor_weight_x_out_1);
    tensor_weight_x_i2(Input_2, tensor_weight_x_out_2);
    flow_calc_body(tensor_weight_x_out_1, tensor_weight_x_out_2,  Output_1);
}
