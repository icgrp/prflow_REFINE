import json, math, os, sys
import argparse
import re
from collections import Counter
sys.path.append('../')
from code_gen_util import return_operator_io_argument_dict_local, return_operator_inst_dict_local, return_operator_connect_list_local,\
                          return_operator_io_type_and_width, needs_write_param, needs_write_filedata, sorted_op_list_backward, divide_ops,\
                          perform_merging, merge_op_list


########################
## Benchmark-specific ##
########################

def gen_gradient_xyz_calc_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void data_transfer(')
    func_str_list.append('    hls::stream<ap_uint<256>>  &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<64>>  &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('ap_uint<256> in_tmp;')
    func_str_list.append('ap_uint<64>  out_tmp;')
    func_str_list.append('')
    func_str_list.append('  for(int i=0; i<MAX_HEIGHT*MAX_WIDTH/4; i++){')
    func_str_list.append('#pragma HLS PIPELINE')
    func_str_list.append('    in_tmp = Input_1.read();')
    func_str_list.append('    for(int j=0; j<4; j++){ // 4 = 256/64')
    func_str_list.append('      out_tmp(31, 0) = in_tmp((j<<6)+31, (j<<6)+0 );')
    func_str_list.append('      out_tmp(63,32) = in_tmp((j<<6)+63, (j<<6)+32);')
    func_str_list.append('      Output_1.write(out_tmp);')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('void g_xyz_calc_module(    ')
    func_str_list.append('    hls::stream<ap_uint<64>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_3)')
    func_str_list.append('{')
    func_str_list.append('    #pragma HLS interface axis register port=Input_1')
    func_str_list.append('    #pragma HLS interface axis register port=Output_1')
    func_str_list.append('    #pragma HLS interface axis register port=Output_2')
    func_str_list.append('    #pragma HLS interface axis register port=Output_3')
    func_str_list.append('')
    func_str_list.append('    // our own line buffer')
    func_str_list.append('    // static pixel_t buf[5][MAX_WIDTH+2];')
    func_str_list.append('    static pixel_t buf[5][MAX_WIDTH];')
    func_str_list.append('    #pragma HLS array_partition variable=buf complete dim=1')
    func_str_list.append('')
    func_str_list.append('    // small buffer')
    func_str_list.append('    pixel_t smallbuf[5];')
    func_str_list.append('    #pragma HLS array_partition variable=smallbuf complete dim=0')
    func_str_list.append('')
    func_str_list.append('    // window buffer')
    func_str_list.append('    xf::cv::Window<5,5,input_t> window;')
    func_str_list.append('')
    func_str_list.append('    ap_fixed<17, 9> GRAD_WEIGHTS[] =  {1,-8,0,8,-1};')
    func_str_list.append('    hls::stream<databus_t> gradient_z;')
    func_str_list.append('    #pragma HLS STREAM variable=gradient_z depth=3*MAX_WIDTH')
    func_str_list.append('')
    func_str_list.append('    // compute gradient')
    func_str_list.append('    pixel_t x_grad = 0;')
    func_str_list.append('    pixel_t y_grad = 0;')
    func_str_list.append('    databus_t grad_z;')
    func_str_list.append('    databus_t temp1 = 0;')
    func_str_list.append('    databus_t temp2 = 0;')
    func_str_list.append('    databus_t temp3 = 0;')
    func_str_list.append('')
    func_str_list.append('    GRAD_XY_OUTER: for(int r=0; r<MAX_HEIGHT+2; r++){')
    func_str_list.append('')
    func_str_list.append('        GRAD_XY_INNER: for(int c=0; c<MAX_WIDTH+2; c++){')
    func_str_list.append('            #pragma HLS pipeline II=1')
    func_str_list.append('')
    func_str_list.append('            // read out values from current line buffer')
    func_str_list.append('            for (int i = 0; i < 4; i ++ ){ smallbuf[i] = buf[i+1][c]; }')
    func_str_list.append('')
    func_str_list.append('            // the new value is either 0 or read from frame')
    func_str_list.append('            if (r<MAX_HEIGHT && c<MAX_WIDTH){')
    func_str_list.append('                databus_t pixel1, pixel2, pixel3, pixel4, pixel5;')
    func_str_list.append('                ap_uint<64> in_tmp;')
    func_str_list.append('                in_tmp= Input_1.read();')
    func_str_list.append('                pixel1 = 0;')
    func_str_list.append('                pixel2 = 0;')
    func_str_list.append('                pixel3 = 0;')
    func_str_list.append('                pixel4 = 0;')
    func_str_list.append('                pixel5 = 0;')
    func_str_list.append('                pixel1(7,0) = in_tmp(7,0);')
    func_str_list.append('                pixel2(7,0) = in_tmp(15,8);')
    func_str_list.append('                pixel3(7,0) = in_tmp(23,16);')
    func_str_list.append('                pixel4(7,0) = in_tmp(31,24);')
    func_str_list.append('                pixel5(7,0) = in_tmp(39,32);')
    func_str_list.append('')
    func_str_list.append('                databus_t tmpread = pixel3;')
    func_str_list.append('                input_t tmpin = 0;')
    func_str_list.append('                tmpin(16,0) = tmpread(16,0);')
    func_str_list.append('                smallbuf[4] = (pixel_t)(tmpin);')
    func_str_list.append('                input_t frame1_tmp,frame2_tmp,frame3_tmp,frame4_tmp,frame5_tmp;')
    func_str_list.append('                frame1_tmp = 0;')
    func_str_list.append('                frame2_tmp = 0;')
    func_str_list.append('                frame3_tmp = 0;')
    func_str_list.append('                frame4_tmp = 0;')
    func_str_list.append('                frame5_tmp = 0;')
    func_str_list.append('                databus_t data = 0;')
    func_str_list.append('                pixel_t temp_z = 0;')
    func_str_list.append('                data = pixel1;')
    func_str_list.append('                frame1_tmp(16,0) = data(16,0);')
    func_str_list.append('                data = pixel2;;')
    func_str_list.append('                frame2_tmp(16,0) = data(16,0);')
    func_str_list.append('                data = pixel3;;')
    func_str_list.append('                frame3_tmp(16,0) = data(16,0);')
    func_str_list.append('                data = pixel4;')
    func_str_list.append('                frame4_tmp(16,0) = data(16,0);')
    func_str_list.append('                data = pixel5;')
    func_str_list.append('                frame5_tmp(16,0) = data(16,0);')
    func_str_list.append('                temp_z =((pixel_t)(frame1_tmp*GRAD_WEIGHTS[0]')
    func_str_list.append('                    + frame2_tmp*GRAD_WEIGHTS[1]')
    func_str_list.append('                    + frame3_tmp*GRAD_WEIGHTS[2]')
    func_str_list.append('                    + frame4_tmp*GRAD_WEIGHTS[3]')
    func_str_list.append('                    + frame5_tmp*GRAD_WEIGHTS[4]))/12;')
    func_str_list.append('                grad_z(31,0) = temp_z(31,0);')
    func_str_list.append('                gradient_z.write(grad_z);')
    func_str_list.append('   }')
    func_str_list.append('            else if (c < MAX_WIDTH) smallbuf[4] = 0;')
    func_str_list.append('')
    func_str_list.append('            // update line buffer')
    func_str_list.append('            if(r<MAX_HEIGHT && c<MAX_WIDTH){')
    func_str_list.append('                for (int i = 0; i < 4; i ++ ) { buf[i][c] = smallbuf[i]; }')
    func_str_list.append('                buf[4][c] = smallbuf[4];')
    func_str_list.append('            }')
    func_str_list.append('            else if(c<MAX_WIDTH){')
    func_str_list.append('                for (int i = 0; i < 4; i ++ ) { buf[i][c] = smallbuf[i]; }')
    func_str_list.append('                buf[4][c] = smallbuf[4];')
    func_str_list.append('            }')
    func_str_list.append('')
    func_str_list.append('   // manage window buffer')
    func_str_list.append('   if(r<MAX_HEIGHT && c<MAX_WIDTH){')
    func_str_list.append('    window.shift_pixels_left();')
    func_str_list.append('')
    func_str_list.append('    for (int i = 0; i < 5; i ++ )')
    func_str_list.append('    window.insert_pixel(smallbuf[i],i,4);')
    func_str_list.append('   } ')
    func_str_list.append('   else {')
    func_str_list.append('    window.shift_pixels_left();')
    func_str_list.append('    window.insert_pixel(0,0,4);')
    func_str_list.append('    window.insert_pixel(0,1,4);')
    func_str_list.append('    window.insert_pixel(0,2,4);')
    func_str_list.append('    window.insert_pixel(0,3,4);')
    func_str_list.append('    window.insert_pixel(0,4,4);')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   x_grad = 0;')
    func_str_list.append('   y_grad = 0;')
    func_str_list.append('   if(r>=4 && r<MAX_HEIGHT && c>=4 && c<MAX_WIDTH) {')
    func_str_list.append('    GRAD_XY_XYGRAD: for(int i=0; i<5; i++){')
    func_str_list.append('     x_grad = x_grad + window.getval(2,i)*GRAD_WEIGHTS[i];')
    func_str_list.append('     y_grad = y_grad + window.getval(i,2)*GRAD_WEIGHTS[i];')
    func_str_list.append('    }')
    func_str_list.append('    x_grad = x_grad/12;')
    func_str_list.append('    temp1(31,0) = x_grad(31,0);')
    func_str_list.append('    Output_1.write(temp1);')
    func_str_list.append('')
    func_str_list.append('    y_grad = y_grad/12;')
    func_str_list.append('    temp2(31,0) = y_grad(31,0);')
    func_str_list.append('    Output_2.write(temp2);')
    func_str_list.append('')
    func_str_list.append('    temp3 = gradient_z.read();')
    func_str_list.append('    Output_3.write(temp3);')
    func_str_list.append('   } ')
    func_str_list.append('            else if(r>=2 && c>=2) {')
    func_str_list.append('    Output_1.write(0);')
    func_str_list.append('    Output_2.write(0);')
    func_str_list.append('    temp3 = gradient_z.read();')
    func_str_list.append('    Output_3.write(temp3);')
    func_str_list.append('   }')
    func_str_list.append('  }')
    func_str_list.append(' }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('void gradient_xyz_calc(    ')
    func_str_list.append('    hls::stream<ap_uint<256>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_3)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_2')
    func_str_list.append('#pragma HLS interface axis register port=Output_3')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('    static hls::stream<ap_uint<64>> data_transfer_out("data_transfer_out_stream");')
    func_str_list.append('')
    func_str_list.append('#pragma HLS dataflow')
    func_str_list.append('    data_transfer(Input_1, data_transfer_out);')
    func_str_list.append('    g_xyz_calc_module(data_transfer_out, Output_1, Output_2, Output_3);')
    func_str_list.append('}')
    func_str_list.append('')
    return 'gradient_xyz_calc', "\n".join(func_str_list)

def gen_gradient_xyz_calc_header():
    func_str_list = []
    func_str_list.append('void gradient_xyz_calc(')
    func_str_list.append('    hls::stream<ap_uint<256>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_3')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'gradient_xyz_calc', "\n".join(func_str_list)


def gen_gradient_weight_x_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void gradient_weight_x(')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_3,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_3)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Input_2')
    func_str_list.append('#pragma HLS interface axis register port=Input_3')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_2')
    func_str_list.append('#pragma HLS interface axis register port=Output_3')
    func_str_list.append('#ifdef RISCV')
    func_str_list.append('  hls::Window<1,7,gradient_t> buf;')
    func_str_list.append('#else')
    func_str_list.append('  xf::cv::Window<1,7,gradient_t> buf;')
    func_str_list.append('#endif')
    func_str_list.append('  const pixel_t GRAD_FILTER[] = {0.0755, 0.133, 0.1869, 0.2903, 0.1869, 0.133, 0.0755};')
    func_str_list.append('  GRAD_WEIGHT_X_OUTER: for(int r=0; r<MAX_HEIGHT; r++)')
    func_str_list.append('  {')
    func_str_list.append('    GRAD_WEIGHT_X_INNER: for(int c=0; c<MAX_WIDTH+3; c++)')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline II=1')
    func_str_list.append('      buf.shift_pixels_left();')
    func_str_list.append('      gradient_t tmp;')
    func_str_list.append('      databus_t temp_x, temp_y, temp_z;')
    func_str_list.append('      if(c<MAX_WIDTH)')
    func_str_list.append('      {')
    func_str_list.append('      temp_x = Input_1.read();')
    func_str_list.append('        temp_y = Input_2.read();')
    func_str_list.append('        temp_z = Input_3.read();')
    func_str_list.append('      tmp.x(31,0) = temp_x.range(31,0);')
    func_str_list.append('        tmp.y(31,0) = temp_y.range(31,0);')
    func_str_list.append('        tmp.z(31,0) = temp_z.range(31,0);')
    func_str_list.append('      }')
    func_str_list.append('      else')
    func_str_list.append('      {')
    func_str_list.append('        tmp.x = 0;')
    func_str_list.append('        tmp.y = 0;')
    func_str_list.append('        tmp.z = 0;')
    func_str_list.append('      }')
    func_str_list.append('      buf.insert_pixel(tmp,0,6);')
    func_str_list.append('')
    func_str_list.append('      gradient_t acc;')
    func_str_list.append('      acc.x = 0;')
    func_str_list.append('      acc.y = 0;')
    func_str_list.append('      acc.z = 0;')
    func_str_list.append('      if(c >= 6 && c<MAX_WIDTH)')
    func_str_list.append('      {')
    func_str_list.append('        GRAD_WEIGHT_X_ACC: for(int i=0; i<7; i++)')
    func_str_list.append('        {')
    func_str_list.append('          acc.x = acc.x + buf.getval(0,i).x*GRAD_FILTER[i];')
    func_str_list.append('          acc.y = acc.y + buf.getval(0,i).y*GRAD_FILTER[i];')
    func_str_list.append('          acc.z = acc.z + buf.getval(0,i).z*GRAD_FILTER[i];')
    func_str_list.append('        }')
    func_str_list.append('        temp_x(31,0) = acc.x.range(31,0);')
    func_str_list.append('        temp_y(31,0) = acc.y.range(31,0);')
    func_str_list.append('        temp_z(31,0) = acc.z.range(31,0);')
    func_str_list.append('        Output_1.write(temp_x);')
    func_str_list.append('        Output_2.write(temp_y);')
    func_str_list.append('        Output_3.write(temp_z);')
    func_str_list.append('      }')
    func_str_list.append('      else if(c>=3)')
    func_str_list.append('      {')
    func_str_list.append('        temp_x(31,0) = acc.x.range(31,0);')
    func_str_list.append('        temp_y(31,0) = acc.y.range(31,0);')
    func_str_list.append('        temp_z(31,0) = acc.z.range(31,0);')
    func_str_list.append('        Output_1.write(temp_x);')
    func_str_list.append('        Output_2.write(temp_y);')
    func_str_list.append('        Output_3.write(temp_z);')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'gradient_weight_x', "\n".join(func_str_list)

def gen_gradient_weight_x_header():
    func_str_list = []
    func_str_list.append('void gradient_weight_x(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_3,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_3')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'gradient_weight_x', "\n".join(func_str_list)


def gen_gradient_weight_y_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void gradient_weight_y(')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_3,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_3)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Input_2')
    func_str_list.append('#pragma HLS interface axis register port=Input_3')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_2')
    func_str_list.append('#pragma HLS interface axis register port=Output_3')
    func_str_list.append('#ifdef RISCV')
    func_str_list.append('  hls::LineBuffer<7,MAX_WIDTH,gradient_t> buf;')
    func_str_list.append('#else')
    func_str_list.append('  xf::cv::LineBuffer<7,MAX_WIDTH,gradient_t> buf;')
    func_str_list.append('#endif')
    func_str_list.append('  const pixel_t GRAD_FILTER[] = {0.0755, 0.133, 0.1869, 0.2903, 0.1869, 0.133, 0.0755};')
    func_str_list.append('  GRAD_WEIGHT_Y_OUTER: for(int r=0; r<MAX_HEIGHT+3; r++)')
    func_str_list.append('  {')
    func_str_list.append('    GRAD_WEIGHT_Y_INNER: for(int c=0; c<MAX_WIDTH; c++)')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline II=1')
    func_str_list.append('      #pragma HLS dependence variable=buf inter false')
    func_str_list.append('')
    func_str_list.append('      if(r<MAX_HEIGHT)')
    func_str_list.append('      {')
    func_str_list.append('        buf.shift_pixels_up(c);')
    func_str_list.append('        databus_t temp_x, temp_y, temp_z;')
    func_str_list.append('        gradient_t tmp;')
    func_str_list.append('        // tmp.x = 0;')
    func_str_list.append('        // tmp.y = 0;')
    func_str_list.append('        // tmp.z = 0;')
    func_str_list.append('       temp_x = Input_1.read();')
    func_str_list.append('        temp_y = Input_2.read();')
    func_str_list.append('        temp_z = Input_3.read();')
    func_str_list.append('       tmp.x(31,0) = temp_x(31,0);')
    func_str_list.append('        tmp.y(31,0) = temp_y(31,0);')
    func_str_list.append('        tmp.z(31,0) = temp_z(31,0);')
    func_str_list.append('        buf.insert_bottom_row(tmp,c);')
    func_str_list.append('      }')
    func_str_list.append('      else')
    func_str_list.append('      {')
    func_str_list.append('        buf.shift_pixels_up(c);')
    func_str_list.append('        gradient_t tmp;')
    func_str_list.append('        tmp.x(31,0) = 0;')
    func_str_list.append('        tmp.y(31,0) = 0;')
    func_str_list.append('        tmp.z(31,0) = 0;')
    func_str_list.append('        buf.insert_bottom_row(tmp,c);')
    func_str_list.append('      }')
    func_str_list.append('')
    func_str_list.append('      gradient_t acc;')
    func_str_list.append('      acc.x = 0;')
    func_str_list.append('      acc.y = 0;')
    func_str_list.append('      acc.z = 0;')
    func_str_list.append('      databus_t temp_x, temp_y, temp_z;')
    func_str_list.append('      if(r >= 6 && r<MAX_HEIGHT)')
    func_str_list.append('      {')
    func_str_list.append('        GRAD_WEIGHT_Y_ACC: for(int i=0; i<7; i++)')
    func_str_list.append('        {')
    func_str_list.append('          acc.x =  acc.x + buf.getval(i,c).x*GRAD_FILTER[i];')
    func_str_list.append('          acc.y =  acc.y + buf.getval(i,c).y*GRAD_FILTER[i];')
    func_str_list.append('          acc.z =  acc.z + buf.getval(i,c).z*GRAD_FILTER[i];')
    func_str_list.append('        }')
    func_str_list.append('      temp_x(31,0) = acc.x.range(31,0);')
    func_str_list.append('        temp_y(31,0) = acc.y.range(31,0);')
    func_str_list.append('        temp_z(31,0) = acc.z.range(31,0);')
    func_str_list.append('      Output_1.write(temp_x);')
    func_str_list.append('        Output_2.write(temp_y);')
    func_str_list.append('        Output_3.write(temp_z);')
    func_str_list.append('      }')
    func_str_list.append('      else if(r>=3)')
    func_str_list.append('      {')
    func_str_list.append('        temp_x(31,0) = acc.x.range(31,0);')
    func_str_list.append('        temp_y(31,0) = acc.y.range(31,0);')
    func_str_list.append('        temp_z(31,0) = acc.z.range(31,0);')
    func_str_list.append('        Output_1.write(temp_x);')
    func_str_list.append('        Output_2.write(temp_y);')
    func_str_list.append('        Output_3.write(temp_z);')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'gradient_weight_y', "\n".join(func_str_list)

def gen_gradient_weight_y_header():
    func_str_list = []
    func_str_list.append('void gradient_weight_y(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_3,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_3')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'gradient_weight_y', "\n".join(func_str_list)

def nearestPowerOf2(N):
    a = int(math.log2(N))
    if 2**a == N:
        return N
    return 2**(a+1)

def gen_outer_product_func(outer_width, par_factor):
    num_send = 1
    # output_width = math.ceil(6/par_factor * outer_width/32) * 32
    output_width = nearestPowerOf2(6/par_factor * outer_width)
    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if output_width > 384:
    #     output_width = output_width // 4
    #     num_send = 4
    # elif output_width > 256:
    #     output_width = output_width // 3
    #     num_send = 3
    # elif output_width > 128: 
    #     output_width = output_width // 2
    #     num_send = 2
    if output_width > 256: 
        output_width = output_width // 2
        num_send = 2


    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('void outer_product(')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_3,')
    for i in range(par_factor):
        if i != par_factor-1:
            func_str_list.append('    hls::stream<ap_uint<' + str(output_width) + '>> &Output_' + str(i+1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<' + str(output_width) + '>> &Output_' + str(i+1))
    func_str_list.append('    )')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Input_2')
    func_str_list.append('#pragma HLS interface axis register port=Input_3')
    for i in range(par_factor):
        func_str_list.append('#pragma HLS interface axis register port=Output_' + str(i + 1))
    func_str_list.append('  OUTER_OUTER: for(int r=0; r<MAX_HEIGHT; r++)')
    func_str_list.append('  {')
    func_str_list.append('    OUTER_INNER: for(int c=0; c<MAX_WIDTH; c++)')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline II=1')
    func_str_list.append('      //gradient_t grad = gradient[r][c];')
    func_str_list.append('      gradient_t grad;')
    func_str_list.append('      databus_t temp_x,temp_y,temp_z;')
    func_str_list.append('      temp_x = Input_1.read();')
    func_str_list.append('      temp_y = Input_2.read();')
    func_str_list.append('      temp_z = Input_3.read();')
    func_str_list.append('      grad.x(31,0) = temp_x.range(31,0);')
    func_str_list.append('      grad.y(31,0) = temp_y.range(31,0);')
    func_str_list.append('      grad.z(31,0) = temp_z.range(31,0);')
    func_str_list.append('      outer_pixel_t x = (outer_pixel_t) grad.x;')
    func_str_list.append('      outer_pixel_t y = (outer_pixel_t) grad.y;')
    func_str_list.append('      outer_pixel_t z = (outer_pixel_t) grad.z;')
    func_str_list.append('      outer_6_t out;')
    func_str_list.append('')
    func_str_list.append('      out.val[0] = (x*x);')
    func_str_list.append('      out.val[1] = (y*y);')
    func_str_list.append('      out.val[2] = (z*z);')
    func_str_list.append('      out.val[3] = (x*y);')
    func_str_list.append('      out.val[4] = (x*z);')
    func_str_list.append('      out.val[5] = (y*z);')
    func_str_list.append('')

    func_str_list.append('      ap_uint<' + str(output_width*num_send) + '> out_tmp;')
    for i in range(par_factor):
        # Filling up out_tmp
        max_width = 0
        for j in range(6//par_factor):
            max_width += outer_width
            func_str_list.append('      out_tmp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ') = out.val[' + \
                                                    str(j + 6//par_factor *i) + '].range(' + str(outer_width-1) + ',0);')
        if max_width != output_width*num_send: # needs to send some blank vals
            func_str_list.append('      out_tmp(' + str(output_width*num_send-1) + ',' + str(max_width) + ') = 0;')

        # Multiplex
        for idx_send in range(num_send):
            func_str_list.append('      Output_' + str(i+1) + '.write(out_tmp(' + str(output_width*(idx_send+1)-1) + ',' + str(output_width*idx_send) + '));')
        func_str_list.append('')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    return 'outer_product', "\n".join(func_str_list)

def gen_outer_product_header(outer_width, par_factor):
    # output_width = math.ceil(6/par_factor * outer_width/32) * 32
    output_width = nearestPowerOf2(6/par_factor * outer_width)
    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if output_width > 384:
    #     output_width = output_width // 4
    # elif output_width > 256:
    #     output_width = output_width // 3
    # elif output_width > 128: 
    #     output_width = output_width // 2
    if output_width > 256: 
        output_width = output_width // 2

    func_str_list = []
    func_str_list.append('void outer_product(')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Input_3,')
    for i in range(par_factor):
        if i != par_factor-1:
            func_str_list.append('    hls::stream<ap_uint<' + str(output_width) + '>> &Output_' + str(i+1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<' + str(output_width) + '>> &Output_' + str(i+1))
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'outer_product', "\n".join(func_str_list)


def gen_tensor_weight_y_func(outer_width, par_factor, idx_par_factor):
    num_send = 1
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    #     num_send = 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    #     num_send = 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    #     num_send = 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2
        num_send = 2

    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void tensor_weight_y_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#ifdef RISCV')
    func_str_list.append('  hls::LineBuffer<3,MAX_WIDTH,outer_' + str(6//par_factor) + '_t> buf;')
    func_str_list.append('#else')
    func_str_list.append('  xf::cv::LineBuffer<3,MAX_WIDTH,outer_' + str(6//par_factor) + '_t> buf;')
    func_str_list.append('#endif')
    func_str_list.append('  const pixel_t TENSOR_FILTER[] = {0.3243, 0.3513, 0.3243};')
    func_str_list.append('  TENSOR_WEIGHT_Y_OUTER: for(int r=0; r<MAX_HEIGHT+1; r++)')
    func_str_list.append('  {')
    func_str_list.append('    TENSOR_WEIGHT_Y_INNER: for(int c=0; c<MAX_WIDTH; c++)')
    func_str_list.append('    {')
    func_str_list.append('#pragma HLS pipeline II=1')
    func_str_list.append('')
    func_str_list.append('      outer_' + str(6//par_factor) + '_t tmp;')
    func_str_list.append('      #pragma HLS data_pack variable=tmp')
    func_str_list.append('      #pragma HLS data_pack variable=buf.val[0]')
    func_str_list.append('      buf.shift_pixels_up(c);')
    func_str_list.append('      if(r<MAX_HEIGHT)')
    func_str_list.append('      {')
    func_str_list.append('        ap_uint<' + str(outer_product_width*num_send) + '> in_tmp;')

    for idx_send in range(num_send):
        func_str_list.append('        in_tmp(' + str(outer_product_width*(idx_send+1)-1) + ',' + str(outer_product_width*idx_send) + ') = Input_1.read();')
    max_width = 0
    for j in range(6//par_factor):
        max_width += outer_width
        func_str_list.append('        tmp.val[' + str(j) + '](' + str(outer_width-1) + ',0)  = in_tmp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ');')

    func_str_list.append('      }')
    func_str_list.append('      else')
    func_str_list.append('      {')
    func_str_list.append('        TENSOR_WEIGHT_Y_TMP_INIT: for(int i=0; i<' + str(6//par_factor) + '; i++){')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('         tmp.val[i] = 0;')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('      buf.insert_bottom_row(tmp,c);')
    func_str_list.append('')

    func_str_list.append('      tensor_' + str(6//par_factor) + '_t acc;')

    func_str_list.append('      TENSOR_WEIGHT_Y_ACC_INIT: for(int k =0; k<' + str(6//par_factor) + '; k++){')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('       acc.val[k] = 0;')
    func_str_list.append('      }')
    func_str_list.append('')
    func_str_list.append('      if (r >= 2 && r < MAX_HEIGHT)')
    func_str_list.append('      {')
    func_str_list.append('        TENSOR_WEIGHT_Y_TMP_OUTER: for(int i=0; i<3; i++)')
    func_str_list.append('        {')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('          tmp = buf.getval(i,c);')
    func_str_list.append('          pixel_t k = TENSOR_FILTER[i];')
    func_str_list.append('          TENSOR_WEIGHT_Y_TMP_INNER: for(int component=0; component<' + str(6//par_factor) + '; component++)')
    func_str_list.append('          {')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('            acc.val[component] = acc.val[component] + tmp.val[component]*k;')
    func_str_list.append('          }')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('      if(r >= 1)')
    func_str_list.append('      {')
    func_str_list.append('        ap_uint<' + str(outer_product_width*num_send) + '> widetemp;')
    max_width = 0
    for j in range(6//par_factor):
        max_width += outer_width
        func_str_list.append('        widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ')  = acc.val[' + str(j) + '](' + str(outer_width-1) + ', 0);')

    if max_width != outer_product_width*num_send: # needs to send some blank vals
        func_str_list.append('        widetemp(' + str(outer_product_width*num_send-1) + ',' + str(max_width) + ') = 0;')

    for idx_send in range(num_send):
        func_str_list.append('        Output_1.write(widetemp(' + str(outer_product_width*(idx_send+1)-1) + ',' + str(outer_product_width*idx_send) + '));')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'tensor_weight_y_i' + str(idx_par_factor + 1), "\n".join(func_str_list)

def gen_tensor_weight_y_header(outer_width, idx_par_factor):
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2

    func_str_list = []
    func_str_list.append('void tensor_weight_y_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_y_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_x_func(outer_width, par_factor, idx_par_factor):
    num_send = 1
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    #     num_send = 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    #     num_send = 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    #     num_send = 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2
        num_send = 2

    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void tensor_weight_x_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#ifdef RISCV')
    func_str_list.append('  hls::Window<1,3,' + 'tensor_' + str(6//par_factor) + '_t' + '> buf;')
    func_str_list.append('#else')
    func_str_list.append('  xf::cv::Window<1,3,' + 'tensor_' + str(6//par_factor) + '_t' + '> buf;')
    func_str_list.append('#endif')
    func_str_list.append('  const pixel_t TENSOR_FILTER[] = {0.3243, 0.3513, 0.3243};')
    func_str_list.append('  TENSOR_WEIGHT_X_OUTER: for(int r=0; r<MAX_HEIGHT; r++)')
    func_str_list.append('  {')
    func_str_list.append('    TENSOR_WEIGHT_X_INNER: for(int c=0; c<MAX_WIDTH+1; c++)')
    func_str_list.append('    {')
    func_str_list.append('#pragma HLS pipeline II=1')
    func_str_list.append('')
    func_str_list.append('      buf.shift_pixels_left();')
    func_str_list.append('      tensor_' + str(6//par_factor) + '_t tmp;')

    func_str_list.append('      if(c<MAX_WIDTH)')
    func_str_list.append('      {')

    func_str_list.append('        ap_uint<' + str(outer_product_width*num_send) + '> widetemp;')
    for idx_send in range(num_send):
        func_str_list.append('        widetemp(' + str(outer_product_width*(idx_send+1)-1) + ',' + str(outer_product_width*idx_send) + ') = Input_1.read();')
    for j in range(6//par_factor):
        func_str_list.append('        tmp.val[' + str(j) + '](' + str(outer_width-1) + ',0)  = widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ');')

    func_str_list.append('      }')
    func_str_list.append('      else')
    func_str_list.append('      {')
    func_str_list.append('        TENSOR_WEIGHT_X_TMP_INIT: for(int i=0; i<' + str(6//par_factor) + '; i++)')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('          tmp.val[i] = 0;')
    func_str_list.append('      }')
    func_str_list.append('      buf.insert_pixel(tmp,0,2);')
    func_str_list.append('')
    func_str_list.append('      tensor_' + str(6//par_factor) + '_t acc;')
    func_str_list.append('      TENSOR_WEIGHT_X_ACC_INIT: for(int k =0; k<' + str(6//par_factor) + '; k++)')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('        acc.val[k] = 0;')
    func_str_list.append('      if (c >= 2 && c < MAX_WIDTH)')
    func_str_list.append('      {')
    func_str_list.append('        TENSOR_WEIGHT_X_TMP_OUTER: for(int i=0; i<3; i++)')
    func_str_list.append('        {')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('          tmp = buf.getval(0,i);')
    func_str_list.append('          TENSOR_WEIGHT_X_TMP_INNER: for(int component=0; component<' + str(6//par_factor) + '; component++)')
    func_str_list.append('          {')
    func_str_list.append('#pragma HLS UNROLL')
    func_str_list.append('            acc.val[component] = acc.val[component] + tmp.val[component]*TENSOR_FILTER[i];')
    func_str_list.append('          }')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('      if(c>=1)')
    func_str_list.append('      {')
    func_str_list.append('        ap_uint<' + str(outer_product_width*num_send) + '> widetemp;')
    max_width = 0

    for j in range(6//par_factor):
        max_width += outer_width
        func_str_list.append('        widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ')  = acc.val[' + str(j) + '](' + str(outer_width-1) + ', 0);')

    if max_width != outer_product_width*num_send: # needs to send some blank vals
        func_str_list.append('        widetemp(' + str(outer_product_width*num_send-1) + ',' + str(max_width) + ') = 0;')

    for idx_send in range(num_send):
        func_str_list.append('        Output_1.write(widetemp(' + str(outer_product_width*(idx_send+1)-1) + ',' + str(outer_product_width*idx_send) + '));')

    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'tensor_weight_x_i' + str(idx_par_factor + 1), "\n".join(func_str_list)

def gen_tensor_weight_x_header(outer_width, idx_par_factor):
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2

    func_str_list = []
    func_str_list.append('void tensor_weight_x_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_x_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_flow_calc_func(outer_width, par_factor, cast_float):
    num_send = 1
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    #     num_send = 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    #     num_send = 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    #     num_send = 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2
        num_send = 2
    func_str_list = []

    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void output_data(')
    func_str_list.append('  hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append('  hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append('  hls::stream<ap_uint<256>> &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Input_2')
    func_str_list.append('')
    func_str_list.append('static ap_uint<32> counter=0;')
    func_str_list.append('  OUT_CONVERT: for (int i = 0; i < MAX_HEIGHT*MAX_WIDTH/4; i++)')
    func_str_list.append('  {')
    func_str_list.append('    ap_uint<256> tmpframe;')
    func_str_list.append('#pragma HLS pipeline II = 2')
    func_str_list.append('    for(int j=0; j<4; j++){')
    func_str_list.append('      tmpframe(j*64+31, j*64   ) = Input_1.read();')
    func_str_list.append('      tmpframe(j*64+63, j*64+32) = Input_2.read();')
    func_str_list.append('    }')
    func_str_list.append('    if (counter < MAX_HEIGHT*MAX_WIDTH/4){')
    func_str_list.append('      Output_1.write(tmpframe);')
    func_str_list.append('      counter++;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('void f_c_module(')
    for idx_par_factor in range(par_factor):
        func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_' + str(idx_par_factor+1) + ',')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2)')
    func_str_list.append('{')
    for i in range(par_factor):
        func_str_list.append('#pragma HLS interface axis register port=Input_' + str(i + 1))
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_2')
    func_str_list.append('')
    if cast_float:
        func_str_list.append('  static float buf[2];')
    else:
        func_str_list.append('  static outer_pixel_t buf[2];')
    func_str_list.append('')
    func_str_list.append('  FLOW_OUTER: for(int r=0; r<MAX_HEIGHT; r++)')
    func_str_list.append('  {')
    func_str_list.append('    FLOW_INNER: for(int c=0; c<MAX_WIDTH; c++)')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline II=1')
    func_str_list.append('      tensor_6_t tmp_tensor;')
    func_str_list.append('      ap_uint<' + str(outer_product_width*num_send) + '> widetemp;')
    func_str_list.append('')

    for i in range(par_factor):
        for idx_send in range(num_send):
            func_str_list.append('      widetemp(' + str(outer_product_width*(idx_send+1)-1) + ',' + str(outer_product_width*idx_send) + ') = Input_' + str(i + 1) + '.read();')

        for j in range(6//par_factor):
            func_str_list.append('      tmp_tensor.val[' + str(j + 6//par_factor *i) + '](' + str(outer_width-1) + ',0)  = widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ');')

    func_str_list.append('')
    func_str_list.append('      if(r>=2 && r<MAX_HEIGHT-2 && c>=2 && c<MAX_WIDTH-2)')
    func_str_list.append('      {')
    func_str_list.append('        calc_pixel_t t1 = (calc_pixel_t) tmp_tensor.val[0];')
    func_str_list.append('        calc_pixel_t t2 = (calc_pixel_t) tmp_tensor.val[1];')
    func_str_list.append('        calc_pixel_t t3 = (calc_pixel_t) tmp_tensor.val[2];')
    func_str_list.append('        calc_pixel_t t4 = (calc_pixel_t) tmp_tensor.val[3];')
    func_str_list.append('        calc_pixel_t t5 = (calc_pixel_t) tmp_tensor.val[4];')
    func_str_list.append('        calc_pixel_t t6 = (calc_pixel_t) tmp_tensor.val[5];')
    func_str_list.append('')
    func_str_list.append('        calc_pixel_t denom = t1*t2-t4*t4;')
    func_str_list.append('        calc_pixel_t numer0 = t6*t4-t5*t2;')
    func_str_list.append('        calc_pixel_t numer1 = t5*t4-t6*t1;')
    func_str_list.append('')
    func_str_list.append('        if(denom != 0)')
    func_str_list.append('        {')
    if cast_float:
        func_str_list.append('          buf[0] = (float) numer0 / (float) denom;')
        func_str_list.append('          buf[1] = (float) numer1 / (float) denom;')
    else:
        func_str_list.append('          buf[0] = numer0 / denom;')
        func_str_list.append('          buf[1] = numer1 / denom;')
    func_str_list.append('        }')
    func_str_list.append('        else')
    func_str_list.append('        {')
    func_str_list.append('          buf[0] = 0;')
    func_str_list.append('          buf[1] = 0;')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('      else')
    func_str_list.append('      {')
    func_str_list.append('        buf[0] = 0;')
    func_str_list.append('        buf[1] = 0;')
    func_str_list.append('      }')
    func_str_list.append('      stdio_t tmpframe_0, tmpframe_1;')
    func_str_list.append('      vel_pixel_t tmpvel_0, tmpvel_1;')
    func_str_list.append('')
    func_str_list.append('      tmpvel_0 = (vel_pixel_t)buf[0];')
    func_str_list.append('      tmpframe_0(31,0) = tmpvel_0(31,0);')
    func_str_list.append('')
    func_str_list.append('      tmpvel_1 = (vel_pixel_t)buf[1];')
    func_str_list.append('      tmpframe_1(31,0) = tmpvel_1(31,0);')
    func_str_list.append('')
    func_str_list.append('      Output_1.write(tmpframe_0);')
    func_str_list.append('      Output_2.write(tmpframe_1);')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('void flow_calc(')
    for idx_par_factor in range(par_factor):
        func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_' + str(idx_par_factor+1) + ',')
    func_str_list.append('    hls::stream<ap_uint<256>> &Output_1)')
    func_str_list.append('{')
    for i in range(par_factor):
        func_str_list.append('#pragma HLS interface axis register port=Input_' + str(i + 1))
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('    static hls::stream<ap_uint<32>> f_c_module_out_1("f_c_module_out_1_stream");')
    func_str_list.append('    static hls::stream<ap_uint<32>> f_c_module_out_2("f_c_module_out_2_stream");')
    func_str_list.append('')
    func_str_list.append('#pragma HLS dataflow')
    func_str_list.append('')
    input_str = ''
    for idx_par_factor in range(par_factor):
        if idx_par_factor == par_factor-1:
            input_str += 'Input_' + str(idx_par_factor+1)
        else:
            input_str += 'Input_' + str(idx_par_factor+1) + ', '

    func_str_list.append('    f_c_module(' + input_str + ', f_c_module_out_1, f_c_module_out_2);')
    func_str_list.append('    output_data(f_c_module_out_1, f_c_module_out_2, Output_1);')
    func_str_list.append('')
    func_str_list.append('}')
    func_str_list.append('')
    return 'flow_calc', "\n".join(func_str_list)

def gen_flow_calc_header(outer_width, par_factor):
    # outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    outer_product_width = nearestPowerOf2(6/par_factor * outer_width)

    # When NoC's payload is 32b, the max possible datawidth is 256 = 32*8
    # if outer_product_width > 384:
    #     outer_product_width = outer_product_width // 4
    # elif outer_product_width > 256:
    #     outer_product_width = outer_product_width // 3
    # elif outer_product_width > 128: 
    #     outer_product_width = outer_product_width // 2
    if outer_product_width > 256: 
        outer_product_width = outer_product_width // 2

    func_str_list = []
    func_str_list.append('void flow_calc(')
    for idx_par_factor in range(par_factor):
        func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_' + str(idx_par_factor+1) + ',')
    func_str_list.append('    hls::stream<ap_uint<256>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'flow_calc', "\n".join(func_str_list)



# Based on ./params/cur_param.json, this file 
# generates HLS source codes (if necessary)
# updates ./host/typedefs.h, ./operators/specs.json, cur_parm.json
if __name__ == '__main__':

    op_dir = './operators'

    #####################################
    ## Extract param from cur_par.json ##
    #####################################
    with open('./params/cur_param.json', 'r') as infile:
        cur_param_dict = json.load(infile)
    # print(cur_param_dict)

    # Values for PAR_FACTOR, OUTER_WIDTH shuold be identical across all the ops
    for prev_op, param_dict in cur_param_dict.items():
        if prev_op != 'metric':
            # print(prev_op)
            # print(param_dict)
            if 'PAR_FACTOR' in param_dict:
                par_factor = param_dict['PAR_FACTOR']
            if 'OUTER_WIDTH' in param_dict:
                outer_width = param_dict['OUTER_WIDTH']
            # if 'CAST_FLOAT' in param_dict:
            #     cast_float = param_dict['CAST_FLOAT']
    print(par_factor)
    print(outer_width)
    cast_float = True # fix to true
    print(cast_float)


    ###########################################
    ## Generate src files based on cur param ##
    ###########################################

    # cpp code gen
    func_name_list = []
    ops_to_compile_list = []
    filedata_dict = {}

    func_name, filedata = gen_gradient_xyz_calc_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_gradient_xyz_calc_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    func_name, filedata = gen_gradient_weight_y_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_gradient_weight_y_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    func_name, filedata = gen_gradient_weight_x_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_gradient_weight_x_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    #########

    func_name, filedata = gen_outer_product_func(outer_width, par_factor)
    func_name_list.append(func_name)
    func_name, filedata_header = gen_outer_product_header(outer_width, par_factor)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    for idx_par_factor in range(par_factor):
        func_name, filedata = gen_tensor_weight_y_func(outer_width, par_factor, idx_par_factor)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_tensor_weight_y_header(outer_width, idx_par_factor)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

        func_name, filedata = gen_tensor_weight_x_func(outer_width, par_factor, idx_par_factor)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_tensor_weight_x_header(outer_width, idx_par_factor)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

    func_name, filedata = gen_flow_calc_func(outer_width, par_factor, cast_float)
    func_name_list.append(func_name)
    func_name, filedata_header = gen_flow_calc_header(outer_width, par_factor)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    # print(filedata_dict.keys())
    print()

    tmp_cur_param_dict = cur_param_dict
    #############################################
    ## Update cur_param.json for new operators ##
    #############################################
    for func_name in func_name_list:
        if func_name not in cur_param_dict.keys():
            base_function_name = func_name.split('_i')[0]
            represent_function_name = base_function_name + '_i1'
            # Assume that kernel_clk, num_leaf_interface, and par factor are identical
            tmp_cur_param_dict[func_name] = cur_param_dict[represent_function_name].copy()

            for op in cur_param_dict.keys():
                if op != 'metric':
                    if 'merged_to' in cur_param_dict[op].keys():
                        if cur_param_dict[op]['merged_to'].startswith(base_function_name):
                            tmp_cur_param_dict[func_name]['merged_to'] = cur_param_dict[op]['merged_to']

    cur_param_dict = tmp_cur_param_dict
    print(cur_param_dict)

    #################################################
    ## Update application graph (top_no_merge.cpp) ##
    #################################################
    top_str_list = ['gradient_xyz_calc(Input_1, gradient_x, gradient_y, gradient_z);',
                    'gradient_weight_y(gradient_x, gradient_y, gradient_z, y_filtered_x, y_filtered_y, y_filtered_z);',
                    'gradient_weight_x(y_filtered_x, y_filtered_y, y_filtered_z, filtered_gradient_x, filtered_gradient_y, filtered_gradient_z);',
                    ]
    # print(func_name_list)
    base_func_name_list = ["outer_product", "tensor_weight_y", "tensor_weight_x", "flow_calc"]
    for func_name in base_func_name_list:
        if func_name.startswith('outer_product'):
            outer_product_str = 'outer_product(filtered_gradient_x, filtered_gradient_y, filtered_gradient_z'
            for idx_par_factor in range(par_factor):
                outer_product_str += ', outer_product_out_' + str(idx_par_factor + 1)
                if idx_par_factor == par_factor-1:
                    outer_product_str += ');'
            top_str_list.append(outer_product_str)
        elif func_name.startswith('tensor_weight_y'):
            for idx_par_factor in range(par_factor):
                tensor_weight_y_str = 'tensor_weight_y_i' + str(idx_par_factor + 1) + '(outer_product_out_' + str(idx_par_factor + 1) + ', '
                tensor_weight_y_str += 'tensor_weight_y_out_' + str(idx_par_factor + 1) + ');'
                top_str_list.append(tensor_weight_y_str)
        elif func_name.startswith('tensor_weight_x'):
            for idx_par_factor in range(par_factor):
                tensor_weight_x_str = 'tensor_weight_x_i' + str(idx_par_factor + 1) + '(tensor_weight_y_out_' + str(idx_par_factor + 1) + ', '
                tensor_weight_x_str += 'tensor_weight_x_out_' + str(idx_par_factor + 1) + ');'
                top_str_list.append(tensor_weight_x_str)
        elif func_name.startswith('flow_calc'):
            flow_calc_str = 'flow_calc('
            for idx_par_factor in range(par_factor):
                flow_calc_str += 'tensor_weight_x_out_' + str(idx_par_factor + 1) + ', '
            flow_calc_str += ' Output_1);'
            top_str_list.append(flow_calc_str)

    with open('./host/top_no_merge.cpp', 'w') as outfile:
        outfile.write("\n".join(top_str_list))

    
    # Check all the functions are instantiated in top_no_merge.cpp
    top_func_name_list = []
    with open('./host/top_no_merge.cpp', 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            func_name = line.split('(')[0]
            top_func_name_list.append(func_name)
    assert(top_func_name_list.sort() == func_name_list.sort())


    #####################
    ## Perform merging ##
    #####################
    operator_list = list(cur_param_dict.keys())
    operator_list.remove("metric")
    # operator_list = merge_op_list()

    # Modify cur_param_dict, ops_to_compile_list and WRITE .cpp files
    merged_top_str_dict = perform_merging(operator_list, cur_param_dict, ops_to_compile_list, filedata_dict)


    # Save cur_param_dict updated by perform_merging
    with open('./params/cur_param.json', 'w') as outfile:
        json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)

    # Save ops_to_compile.json, used to record compile time
    with open('./params/ops_to_compile.json', 'w') as outfile:
        json.dump(ops_to_compile_list, outfile, sort_keys=True, indent=4)

    # outer_width_int, calc_width_int values could be also design space, but
    # We fix these vals for each outer_width val
    # TODO: dummy_len is required to flush out all the outputs in optical_flow benchmark.
    dummy_len = 785
    if outer_width == 16:
        outer_width_int, calc_width_int = 11, 24
    elif outer_width == 32:
        outer_width_int, calc_width_int = 27, 56
    elif outer_width == 48:
        outer_width_int, calc_width_int = 27, 56

    # For monolithic ver., dummy_len = 1024 is fine
    if os.path.isfile('./__NoC_done__'):
        dummy_len = 1024


    # Modify typedefs.h
    filedata = ''
    with open('./host/typedefs.h', 'r') as infile:
        lines = infile.readlines()
    for line in lines:
        if line.startswith('#define PAR_FACTOR'):
            line = '#define PAR_FACTOR ' + str(par_factor) + '\n'
        elif line.startswith('#define OUTER_WIDTH '):
            line = '#define OUTER_WIDTH ' + str(outer_width) + '\n'
        elif line.startswith('#define OUTER_WIDTH_INT '):
            line = '#define OUTER_WIDTH_INT ' + str(outer_width_int) + '\n'
        elif line.startswith('#define CALC_WIDTH_INT '):
            line = '#define CALC_WIDTH_INT ' + str(calc_width_int) + '\n'
        elif line.startswith('#define DUMMY_LEN '):
            line = '#define DUMMY_LEN ' + str(dummy_len) + '\n'
        # elif line.startswith('#define CAST_FLOAT'):
        #     if cast_float:
        #         line = '#define CAST_FLOAT true\n'
        #     else:
        #         line = '#define CAST_FLOAT false\n'
        filedata += line
    with open('./host/typedefs.h', 'w') as outfile:
        outfile.write(filedata)




    #######################################################
    ## Update application graph (top.cpp) - post merging ##
    #######################################################
    post_merging_top_str_list = top_str_list
    for op_tup in merged_top_str_dict:
        for op in op_tup:
            for line in top_str_list:
                if line.startswith(op + '('):
                    post_merging_top_str_list.remove(line)

    for op_tup in merged_top_str_dict:
        merged_top_str = merged_top_str_dict[op_tup]
        post_merging_top_str_list.append(merged_top_str)

    with open('./host/top.cpp', 'w') as outfile:
        outfile.write("\n".join(post_merging_top_str_list))


    ###############################################
    ## Update specs.json -- may be removed later ##
    ###############################################
    post_merging_func_name_list = []
    for line in post_merging_top_str_list:
        func_name = line.split('(')[0]
        post_merging_func_name_list.append(func_name)

    spec_dict = {}
    for func_name in post_merging_func_name_list:
        spec_dict[func_name] = {}
        spec_dict[func_name]['kernel_clk'] = cur_param_dict[func_name]['kernel_clk']
        spec_dict[func_name]['num_leaf_interface'] = cur_param_dict[func_name]['num_leaf_interface']
    with open(op_dir + '/specs.json', 'w') as outfile:
        json.dump(spec_dict, outfile, sort_keys=True, indent=4)

