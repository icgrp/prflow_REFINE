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

def gen_projection_func(idx):
    func_str_list = []
    func_str_list.append('// project a 3D triangle to a 2D triangle')
    func_str_list.append('void projection_i' + str(idx) + ' (')
    func_str_list.append('    bit32 input_lo,')
    func_str_list.append('    bit32 input_mi,')
    func_str_list.append('    bit32 input_hi,')
    func_str_list.append('    Triangle_2D *triangle_2d')
    func_str_list.append('    )')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS INLINE off')
    func_str_list.append('  Triangle_3D triangle_3d;')
    func_str_list.append('  // Setting camera to (0,0,-1), the canvas at z=0 plane')
    func_str_list.append('  // The 3D model lies in z>0 space')
    func_str_list.append('  // The coordinate on canvas is proportional to the corresponding coordinate')
    func_str_list.append('  // on space')
    func_str_list.append('')
    func_str_list.append('  bit2 angle = 0;')
    func_str_list.append('  triangle_3d.x0(7, 0) = input_lo( 7,  0);')
    func_str_list.append('  triangle_3d.y0(7, 0) = input_lo(15,  8);')
    func_str_list.append('  triangle_3d.z0(7, 0) = input_lo(23, 16);')
    func_str_list.append('  triangle_3d.x1(7, 0) = input_lo(31, 24);')
    func_str_list.append('  triangle_3d.y1(7, 0) = input_mi( 7,  0);')
    func_str_list.append('  triangle_3d.z1(7, 0) = input_mi(15,  8);')
    func_str_list.append('  triangle_3d.x2(7, 0) = input_mi(23, 16);')
    func_str_list.append('  triangle_3d.y2(7, 0) = input_mi(31, 24);')
    func_str_list.append('  triangle_3d.z2(7, 0) = input_hi( 7,  0);')
    func_str_list.append('')
    func_str_list.append('  if(angle == 0)')
    func_str_list.append('  {')
    func_str_list.append('    triangle_2d->x0 = triangle_3d.x0;')
    func_str_list.append('    triangle_2d->y0 = triangle_3d.y0;')
    func_str_list.append('    triangle_2d->x1 = triangle_3d.x1;')
    func_str_list.append('    triangle_2d->y1 = triangle_3d.y1;')
    func_str_list.append('    triangle_2d->x2 = triangle_3d.x2;')
    func_str_list.append('    triangle_2d->y2 = triangle_3d.y2;')
    func_str_list.append('    triangle_2d->z  = triangle_3d.z0 / 3 + triangle_3d.z1 / 3 + triangle_3d.z2 / 3;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  else if(angle == 1)')
    func_str_list.append('  {')
    func_str_list.append('    triangle_2d->x0 = triangle_3d.x0;')
    func_str_list.append('    triangle_2d->y0 = triangle_3d.z0;')
    func_str_list.append('    triangle_2d->x1 = triangle_3d.x1;')
    func_str_list.append('    triangle_2d->y1 = triangle_3d.z1;')
    func_str_list.append('    triangle_2d->x2 = triangle_3d.x2;')
    func_str_list.append('    triangle_2d->y2 = triangle_3d.z2;')
    func_str_list.append('    triangle_2d->z  = triangle_3d.y0 / 3 + triangle_3d.y1 / 3 + triangle_3d.y2 / 3;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  else if(angle == 2)')
    func_str_list.append('  {')
    func_str_list.append('    triangle_2d->x0 = triangle_3d.z0;')
    func_str_list.append('    triangle_2d->y0 = triangle_3d.y0;')
    func_str_list.append('    triangle_2d->x1 = triangle_3d.z1;')
    func_str_list.append('    triangle_2d->y1 = triangle_3d.y1;')
    func_str_list.append('    triangle_2d->x2 = triangle_3d.z2;')
    func_str_list.append('    triangle_2d->y2 = triangle_3d.y2;')
    func_str_list.append('    triangle_2d->z  = triangle_3d.x0 / 3 + triangle_3d.x1 / 3 + triangle_3d.x2 / 3;')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    return func_str_list

def gen_rasterization1_func(idx):
    func_str_list = []
    func_str_list.append('// calculate bounding box for a 2D triangle')
    func_str_list.append('void rasterization1_i' + str(idx) + ' (')
    func_str_list.append('    Triangle_2D triangle_2d,')
    func_str_list.append('    hls::stream<ap_uint<32> > & Output_1)')
    func_str_list.append('{')
    func_str_list.append('  Triangle_2D triangle_2d_same;')
    func_str_list.append('  static bit8 max_min[5]={0, 0, 0, 0, 0};')
    func_str_list.append('  static bit16 max_index[1]={0};')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  #pragma HLS INLINE off')
    func_str_list.append('  // clockwise the vertices of input 2d triangle')
    func_str_list.append('  if ( check_clockwise( triangle_2d ) == 0 ){')
    func_str_list.append('    bit32 tmp;')
    func_str_list.append('    tmp(7,0) = 1;')
    func_str_list.append('    tmp(15, 8) = triangle_2d_same.x0;')
    func_str_list.append('    tmp(23,16) = triangle_2d_same.y0;')
    func_str_list.append('    tmp(31,24) = triangle_2d_same.x1;')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('    tmp(7,0) = triangle_2d_same.y1;')
    func_str_list.append('    tmp(15, 8) = triangle_2d_same.x2;')
    func_str_list.append('    tmp(23,16) = triangle_2d_same.y2;')
    func_str_list.append('    tmp(31,24) = triangle_2d_same.z;')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('    tmp(15,0) = max_index[0];')
    func_str_list.append('    tmp(23,16) = max_min[0];')
    func_str_list.append('    tmp(31,24) = max_min[1];')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('    tmp(7,0) = max_min[2];')
    func_str_list.append('    tmp(15, 8) = max_min[3];')
    func_str_list.append('    tmp(23,16) = max_min[4];')
    func_str_list.append('    tmp(31,24) = 0;')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('    return;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  if ( check_clockwise( triangle_2d ) < 0 )')
    func_str_list.append('    clockwise_vertices( &triangle_2d );')
    func_str_list.append('')
    func_str_list.append('  // copy the same 2D triangle')
    func_str_list.append('  triangle_2d_same.x0 = triangle_2d.x0;')
    func_str_list.append('  triangle_2d_same.y0 = triangle_2d.y0;')
    func_str_list.append('  triangle_2d_same.x1 = triangle_2d.x1;')
    func_str_list.append('  triangle_2d_same.y1 = triangle_2d.y1;')
    func_str_list.append('  triangle_2d_same.x2 = triangle_2d.x2;')
    func_str_list.append('  triangle_2d_same.y2 = triangle_2d.y2;')
    func_str_list.append('  triangle_2d_same.z  = triangle_2d.z ;')
    func_str_list.append('')
    func_str_list.append('  // find the rectangle bounds of 2D triangles')
    func_str_list.append('  max_min[0] = find_min( triangle_2d.x0, triangle_2d.x1, triangle_2d.x2 );')
    func_str_list.append('  max_min[1] = find_max( triangle_2d.x0, triangle_2d.x1, triangle_2d.x2 );')
    func_str_list.append('  max_min[2] = find_min( triangle_2d.y0, triangle_2d.y1, triangle_2d.y2 );')
    func_str_list.append('  max_min[3] = find_max( triangle_2d.y0, triangle_2d.y1, triangle_2d.y2 );')
    func_str_list.append('  max_min[4] = max_min[1] - max_min[0];')
    func_str_list.append('')
    func_str_list.append('  // calculate index for searching pixels')
    func_str_list.append('  max_index[0] = (max_min[1] - max_min[0]) * (max_min[3] - max_min[2]);')
    func_str_list.append('  bit32 tmp;')
    func_str_list.append('')
    func_str_list.append('  tmp(7,0) = 0;')
    func_str_list.append('  tmp(15,8) = triangle_2d_same.x0;')
    func_str_list.append('  tmp(23,16) = triangle_2d_same.y0;')
    func_str_list.append('  tmp(31,24) = triangle_2d_same.x1;')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  tmp(7,0) = triangle_2d_same.y1;')
    func_str_list.append('  tmp(15,8) = triangle_2d_same.x2;')
    func_str_list.append('  tmp(23,16) = triangle_2d_same.y2;')
    func_str_list.append('  tmp(31,24) = triangle_2d_same.z;')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  tmp(15,0) = max_index[0];')
    func_str_list.append('  tmp(23,16) = max_min[0];')
    func_str_list.append('  tmp(31,24) = max_min[1];')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  tmp(7,0) = max_min[2];')
    func_str_list.append('  tmp(15,8) = max_min[3];')
    func_str_list.append('  tmp(23, 16) = max_min[4];')
    func_str_list.append('  tmp(31, 24) = 0;')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    return func_str_list

def gen_prj_rast1_func(par_rast):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('int check_clockwise( Triangle_2D triangle_2d )')
    func_str_list.append('{')
    func_str_list.append('  int cw;')
    func_str_list.append('')
    func_str_list.append('  cw = (triangle_2d.x2 - triangle_2d.x0) * (triangle_2d.y1 - triangle_2d.y0)')
    func_str_list.append('       - (triangle_2d.y2 - triangle_2d.y0) * (triangle_2d.x1 - triangle_2d.x0);')
    func_str_list.append('')
    func_str_list.append('  return cw;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('// swap (x0, y0) (x1, y1) of a Triangle_2D')
    func_str_list.append('void clockwise_vertices( Triangle_2D *triangle_2d )')
    func_str_list.append('{')
    func_str_list.append('')
    func_str_list.append('  bit8 tmp_x, tmp_y;')
    func_str_list.append('')
    func_str_list.append('  tmp_x = triangle_2d->x0;')
    func_str_list.append('  tmp_y = triangle_2d->y0;')
    func_str_list.append('')
    func_str_list.append('  triangle_2d->x0 = triangle_2d->x1;')
    func_str_list.append('  triangle_2d->y0 = triangle_2d->y1;')
    func_str_list.append('')
    func_str_list.append('  triangle_2d->x1 = tmp_x;')
    func_str_list.append('  triangle_2d->y1 = tmp_y;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('bit8 find_min( bit8 in0, bit8 in1, bit8 in2 )')
    func_str_list.append('{')
    func_str_list.append('  if (in0 < in1)')
    func_str_list.append('  {')
    func_str_list.append('    if (in0 < in2)')
    func_str_list.append('      return in0;')
    func_str_list.append('    else')
    func_str_list.append('      return in2;')
    func_str_list.append('  }')
    func_str_list.append('  else')
    func_str_list.append('  {')
    func_str_list.append('    if (in1 < in2)')
    func_str_list.append('      return in1;')
    func_str_list.append('    else')
    func_str_list.append('      return in2;')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('// find the max from 3 integers')
    func_str_list.append('bit8 find_max( bit8 in0, bit8 in1, bit8 in2 )')
    func_str_list.append('{')
    func_str_list.append('  if (in0 > in1)')
    func_str_list.append('  {')
    func_str_list.append('    if (in0 > in2)')
    func_str_list.append('      return in0;')
    func_str_list.append('    else')
    func_str_list.append('      return in2;')
    func_str_list.append('  }')
    func_str_list.append('  else')
    func_str_list.append('  {')
    func_str_list.append('    if (in1 > in2)')
    func_str_list.append('      return in1;')
    func_str_list.append('    else')
    func_str_list.append('      return in2;')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')

    for idx in range(par_rast):
        func_str_list += gen_projection_func(idx + 1)
        func_str_list += gen_rasterization1_func(idx + 1)

    func_str_list.append('void prj_rast1 (')
    func_str_list.append('    hls::stream<ap_uint<128>> & Input_1,')
    for idx in range(par_rast):
        if idx != par_rast-1:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1))
    func_str_list.append('    )')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    for idx in range(par_rast):
        func_str_list.append('#pragma HLS INTERFACE axis register port=Output_' + str(idx + 1))
    func_str_list.append('')
    func_str_list.append('  bit32 input_lo;')
    func_str_list.append('  bit32 input_mi;')
    func_str_list.append('  bit32 input_hi;')
    func_str_list.append('  bit128 input_tmp;')
    func_str_list.append('')
    for idx in range(par_rast):
        func_str_list.append('  Triangle_2D triangle_2ds_' + str(idx + 1) + ';')
    func_str_list.append('')

    for idx in range(par_rast):
        func_str_list.append('  input_tmp = Input_1.read();')
        func_str_list.append('')
        func_str_list.append('  input_lo(31,0) = input_tmp(31,  0);')
        func_str_list.append('  input_mi(31,0) = input_tmp(63, 32);')
        func_str_list.append('  input_hi(31,0) = input_tmp(95, 64);')
        func_str_list.append('  projection_i' + str(idx + 1) + ' (')
        func_str_list.append('    input_lo,')
        func_str_list.append('    input_mi,')
        func_str_list.append('    input_hi,')
        func_str_list.append('    &triangle_2ds_' + str(idx + 1) + ');')
        func_str_list.append('')
        func_str_list.append('  rasterization1_i' + str(idx + 1) + ' (')
        func_str_list.append('    triangle_2ds_' + str(idx + 1) + ',')
        func_str_list.append('    Output_' + str(idx + 1) + ');')
        func_str_list.append('')

    func_str_list.append('}')
    return "prj_rast1", "\n".join(func_str_list)

def gen_prj_rast1_header(par_rast):
    func_str_list = []
    func_str_list.append('void prj_rast1 (')
    func_str_list.append('    hls::stream<ap_uint<128>> & Input_1,')
    for idx in range(par_rast):
        if idx != par_rast-1:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1))
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return "prj_rast1", "\n".join(func_str_list)


def gen_rast2_func(idx_par_rast, par_zculling):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('bit1 pixel_in_triangle( bit8 x, bit8 y, Triangle_2D triangle_2d )')
    func_str_list.append('{')
    func_str_list.append('')
    func_str_list.append('  int pi0, pi1, pi2;')
    func_str_list.append('')
    func_str_list.append('  pi0 = (x - triangle_2d.x0) * (triangle_2d.y1 - triangle_2d.y0) - (y - triangle_2d.y0) * (triangle_2d.x1 - triangle_2d.x0);')
    func_str_list.append('  pi1 = (x - triangle_2d.x1) * (triangle_2d.y2 - triangle_2d.y1) - (y - triangle_2d.y1) * (triangle_2d.x2 - triangle_2d.x1);')
    func_str_list.append('  pi2 = (x - triangle_2d.x2) * (triangle_2d.y0 - triangle_2d.y2) - (y - triangle_2d.y2) * (triangle_2d.x0 - triangle_2d.x2);')
    func_str_list.append('')
    func_str_list.append('  return (pi0 >= 0 && pi1 >= 0 && pi2 >= 0);')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('// find pixels in the triangles from the bounding box')
    func_str_list.append('void rasterization2 (')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    for idx in range(par_zculling):
        if idx != par_zculling-1:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1))
    func_str_list.append('    )')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE ap_hs port=Input_1')
    for idx in range(par_zculling):
        func_str_list.append('#pragma HLS INTERFACE ap_hs port=Output_' + str(idx + 1))
    func_str_list.append('')
    func_str_list.append('  #pragma HLS INLINE off')
    func_str_list.append('  bit16 i = 0;')
    for idx in range(par_zculling):
        if (par_zculling != 1):
            func_str_list.append('  bit16 i_' + str(idx + 1) + ' = 0;')
    func_str_list.append('  int y_tmp;')
    func_str_list.append('  int j;')
    func_str_list.append('  Triangle_2D triangle_2d_same;')
    func_str_list.append('  bit2 flag;')
    func_str_list.append('  bit8 max_min[5];')
    func_str_list.append('  bit16 max_index[1];')
    func_str_list.append('  bit32 out_tmp;')
    func_str_list.append('  static CandidatePixel fragment[500];')
    func_str_list.append('')
    func_str_list.append('  bit32 tmp = Input_1.read();')
    func_str_list.append('  flag = (bit2) tmp(1,0);')
    func_str_list.append('  triangle_2d_same.x0(7, 0)=tmp(15,8);')
    func_str_list.append('  triangle_2d_same.y0(7, 0)=tmp(23,16);')
    func_str_list.append('  triangle_2d_same.x1(7, 0)=tmp(31,24);')
    func_str_list.append('')
    func_str_list.append('  tmp = Input_1.read();')
    func_str_list.append('  triangle_2d_same.y1(7, 0)=tmp(7,0);')
    func_str_list.append('  triangle_2d_same.x2(7, 0)=tmp(15,8);')
    func_str_list.append('  triangle_2d_same.y2(7, 0)=tmp(23,16);')
    func_str_list.append('  triangle_2d_same.z(7, 0)=tmp(31,24);')
    func_str_list.append('')
    func_str_list.append('  tmp = Input_1.read();')
    func_str_list.append('  max_index[0](15, 0)=tmp(15,0);')
    func_str_list.append('  max_min[0](7, 0)=tmp(23,16);')
    func_str_list.append('  max_min[1](7, 0)=tmp(31,24);')
    func_str_list.append('')
    func_str_list.append('  tmp = Input_1.read();')
    func_str_list.append('  max_min[2](7, 0)=tmp(7,0);')
    func_str_list.append('  max_min[3](7, 0)=tmp(15,8);')
    func_str_list.append('  max_min[4](7, 0)=tmp(23, 16);')
    func_str_list.append('')
    func_str_list.append('  // clockwise the vertices of input 2d triangle')
    func_str_list.append('  if ( flag )')
    func_str_list.append('  {')
    if (par_zculling != 1):
        for idx in range(par_zculling):
            func_str_list.append('    Output_' + str(idx + 1) + '.write(i_' + str(idx + 1) + ');')
    else:
        func_str_list.append('    Output_1.write(i);')
    func_str_list.append('    return;')
    func_str_list.append('  }')
    func_str_list.append('  bit8 color = 100;')
    func_str_list.append('')
    func_str_list.append('  RAST2: for ( bit16 k = 0; k < max_index[0]; k++ )')
    func_str_list.append('  {')
    func_str_list.append('    #pragma HLS PIPELINE II=1')
    func_str_list.append('    bit8 x = max_min[0] + k%max_min[4];')
    func_str_list.append('    bit8 y = max_min[2] + k/max_min[4];')
    func_str_list.append('')
    func_str_list.append('    if( pixel_in_triangle( x, y, triangle_2d_same ) )')
    func_str_list.append('    {')
    func_str_list.append('      fragment[i].x = x;')
    func_str_list.append('      fragment[i].y = y;')
    func_str_list.append('      fragment[i].z = triangle_2d_same.z;')
    func_str_list.append('      fragment[i].color = color;')
    func_str_list.append('      i++;')

    for idx in range(par_zculling):
        if (par_zculling != 1):
            if idx == 0:
                func_str_list.append('      if (y > ' + str(int(256 - 256/par_zculling - 1)) + ') i_' + str(idx + 1) + '++;')
            elif idx == par_zculling-1:
                func_str_list.append('      else i_' + str(idx + 1) + '++;')
            else:
                func_str_list.append('      else if (y > ' + str(int(256 - (idx+1)*(256/par_zculling) - 1)) + ') i_' + str(idx + 1) + '++;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    if (par_zculling != 1):
        for idx in range(par_zculling):
            func_str_list.append('  Output_' + str(idx + 1) + '.write(i_' + str(idx + 1) + ');')
    else:
        func_str_list.append('  Output_1.write(i);')
    func_str_list.append('')
    func_str_list.append('  for(j=0; j<i; j++){')
    func_str_list.append('    #pragma HLS PIPELINE II=1')
    func_str_list.append('    out_tmp(7, 0) = fragment[j].x;')
    func_str_list.append('    out_tmp(15, 8) = fragment[j].y;')
    func_str_list.append('    y_tmp = (int) out_tmp(15, 8);')
    func_str_list.append('    out_tmp(23, 16) = fragment[j].z;')
    func_str_list.append('    out_tmp(31, 24) = fragment[j].color;')
    for idx in range(par_zculling):
        if (par_zculling != 1):
            if idx == 0:
                func_str_list.append('    if (y_tmp > ' + str(int(256 - 256/par_zculling - 1)) + ') Output_' + str(idx + 1) + '.write(out_tmp);')
            elif idx == par_zculling-1:
                func_str_list.append('    else Output_' + str(idx + 1) + '.write(out_tmp);')
            else:
                func_str_list.append('    else if (y_tmp > ' + str(int(256 - (idx+1)*(256/par_zculling) - 1)) + ') Output_' + str(idx + 1) + '.write(out_tmp);')
        else:
            func_str_list.append('    Output_1.write(out_tmp);')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('void rast2_i' + str(idx_par_rast + 1) + ' (')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    for idx in range(par_zculling):
        if idx != par_zculling-1:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1))
    func_str_list.append('    )')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    for idx in range(par_zculling):
        func_str_list.append('#pragma HLS INTERFACE axis register port=Output_' + str(idx + 1))
    func_str_list.append('')
    func_str_list.append('  rasterization2(')
    func_str_list.append('      Input_1,')
    for idx in range(par_zculling):
        if idx != par_zculling-1:
            func_str_list.append('      Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('      Output_' + str(idx + 1) + ');')
    func_str_list.append('')
    func_str_list.append('}')

    return 'rast2_i' + str(idx_par_rast + 1), "\n".join(func_str_list)

def gen_rast2_header(idx_par_rast):
    func_str_list = []
    func_str_list.append('void rast2_i' + str(idx_par_rast + 1) + ' (')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    for idx in range(par_zculling):
        if idx != par_zculling-1:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1) + ',')
        else:
            func_str_list.append('    hls::stream<ap_uint<32>> & Output_' + str(idx + 1))
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'rast2_i' + str(idx_par_rast + 1), "\n".join(func_str_list)


def gen_zculling_func(par_rast, idx_par_zculling, par_zculling):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('// filter hidden pixels')
    func_str_list.append('void zculling_i' + str(idx_par_zculling + 1) + ' (')
    for idx in range(par_rast):
        func_str_list.append('    hls::stream<ap_uint<32>> & Input_' + str(idx + 1) + ',')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1')
    func_str_list.append('    )')
    func_str_list.append('{')
    for idx in range(par_rast):
        func_str_list.append('#pragma HLS INTERFACE axis register port=Input_' + str(idx + 1))
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('  #pragma HLS INLINE off')
    func_str_list.append('  CandidatePixel fragment;')
    func_str_list.append('  static bit16 counter=0;')
    func_str_list.append('  int i, j;')
    func_str_list.append('  Pixel pixels[500];')
    func_str_list.append('  bit16 size;')
    func_str_list.append('  bit32 in_tmp;')
    func_str_list.append('  bit32 out_tmp;')
    if (par_rast != 1):
        func_str_list.append('  static bit' + str(int(math.log(par_rast, 2))) + ' cnt = 0;')

    for idx in range(par_rast):
        if (par_rast != 1):
            if idx == 0:
                func_str_list.append('  if (cnt == 0) size = Input_1.read();')
            elif idx == par_rast-1:
                func_str_list.append('  else size = Input_' + str(idx + 1) + '.read();')
            else:
                func_str_list.append('  else if (cnt == ' + str(idx) + ') size = Input_' + str(idx + 1) + '.read();')
        else:
            func_str_list.append('  size = Input_1.read();')

    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // initilize the z-buffer in rendering first triangle for an image')
    func_str_list.append('  static bit8 z_buffer[MAX_X/' + str(par_zculling) + '][MAX_Y];')
    func_str_list.append('  if (counter == 0)')
    func_str_list.append('  {')
    func_str_list.append('    ZCULLING_INIT_ROW: for ( bit16 i = 0; i < MAX_X/' + str(par_zculling) + '; i++)')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS PIPELINE II=1')
    func_str_list.append('      ZCULLING_INIT_COL: for ( bit16 j = 0; j < MAX_Y; j++)')
    func_str_list.append('      {')
    func_str_list.append('        z_buffer[i][j] = 255;')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // pixel counter')
    func_str_list.append('  bit16 pixel_cntr = 0;')
    func_str_list.append('')
    func_str_list.append('  // update z-buffer and pixels')
    func_str_list.append('  ZCULLING: for ( bit16 n = 0; n < size; n++ )')
    func_str_list.append('  {')
    func_str_list.append('  #pragma HLS PIPELINE II=1')
    for idx in range(par_rast):
        if (par_rast != 1):
            if idx == 0:
                func_str_list.append('    if (cnt == 0) in_tmp = Input_1.read();')
            elif idx == par_rast-1:
                func_str_list.append('    else in_tmp = Input_' + str(idx + 1) + '.read();')
            else:
                func_str_list.append('    else if (cnt == ' + str(idx) + ') in_tmp = Input_' + str(idx + 1) + '.read();')
        else:
            func_str_list.append('    in_tmp = Input_1.read();')

    func_str_list.append('    fragment.x(7,0) = in_tmp(7, 0);')
    func_str_list.append('    fragment.y(7,0) = in_tmp(15, 8);')
    func_str_list.append('    fragment.z(7,0) = in_tmp(23, 16);')
    func_str_list.append('    fragment.color(7,0) = in_tmp(31, 24);')

    if par_zculling == 1:
        func_str_list.append('    if( fragment.z < z_buffer[fragment.y][fragment.x])')
    else:
        func_str_list.append('    if( fragment.z < z_buffer[fragment.y-' + str(int(256 - ((256/par_zculling)*(idx_par_zculling+1)))) + '][fragment.x])')
    func_str_list.append('    {')
    func_str_list.append('      pixels[pixel_cntr].x     = fragment.x;')
    func_str_list.append('      pixels[pixel_cntr].y     = fragment.y;')
    func_str_list.append('      pixels[pixel_cntr].color = fragment.color;')
    func_str_list.append('      pixel_cntr++;')

    if par_zculling == 1:
        func_str_list.append('      z_buffer[fragment.y][fragment.x] = fragment.z;')
    else:
        func_str_list.append('      z_buffer[fragment.y-' + str(int(256 - ((256/par_zculling)*(idx_par_zculling+1)))) + '][fragment.x] = fragment.z;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  Output_1.write(pixel_cntr);')
    func_str_list.append('  for(j=0; j<pixel_cntr; j++){')
    func_str_list.append('  #pragma HLS PIPELINE II=1')
    func_str_list.append('    out_tmp(7,  0) = pixels[j].x;')
    func_str_list.append('    out_tmp(15, 8) = pixels[j].y;')
    func_str_list.append('    out_tmp(23, 16) = pixels[j].color;')
    func_str_list.append('    out_tmp(31, 24) = 0;')
    func_str_list.append('    Output_1.write(out_tmp);')
    func_str_list.append('  }')
    func_str_list.append('')
    if par_rast != 1:
        func_str_list.append('  if(cnt == ' + str(par_rast-1) + ') cnt = 0;')
        func_str_list.append('  else cnt++;')
        func_str_list.append('')
    func_str_list.append('  counter++;')
    func_str_list.append('  if(counter==NUM_3D_TRI){counter=0;}')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')

    return 'zculling_i' + str(idx_par_zculling + 1), "\n".join(func_str_list)

def gen_zculling_header(par_rast, idx_par_zculling):
    func_str_list = []
    func_str_list.append('void zculling_i' + str(idx_par_zculling + 1) + ' (')
    for idx in range(par_rast):
        func_str_list.append('    hls::stream<ap_uint<32>> & Input_' + str(idx + 1) + ',')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'zculling_i' + str(idx_par_zculling + 1), "\n".join(func_str_list)

def gen_coloring_func(par_zculling, idx_par_zculling):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('// color the frame buffer')
    func_str_list.append('void coloringFB_i' + str(idx_par_zculling + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<128>> & Output_1)')
    func_str_list.append('')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('  #pragma HLS INLINE off')
    func_str_list.append('  int i,j;')
    func_str_list.append('  static bit8 frame_buffer[MAX_X][MAX_Y/' + str(par_zculling) + '];')
    func_str_list.append('  Pixel pixels;')
    func_str_list.append('  static bit16 counter=0;')
    func_str_list.append('  bit16 size_pixels;')
    func_str_list.append('  bit32 in_tmp;')
    func_str_list.append('  size_pixels=Input_1.read();')
    func_str_list.append('  bit128 out_FB = 0;')
    func_str_list.append('')
    func_str_list.append('  if ( counter == 0 )')
    func_str_list.append('  {')
    func_str_list.append('    // initilize the framebuffer for a new image')
    func_str_list.append('    COLORING_FB_INIT_ROW: for ( bit16 i = 0; i < MAX_X; i++)')
    func_str_list.append('    {')
    func_str_list.append('#pragma HLS PIPELINE II=1')
    func_str_list.append('      COLORING_FB_INIT_COL: for ( bit16 j = 0; j < MAX_Y/' + str(par_zculling) + '; j++)')
    func_str_list.append('        frame_buffer[i][j] = 0;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // update the framebuffer')
    func_str_list.append('  COLORING_FB: for ( bit16 i = 0; i < size_pixels; i++)')
    func_str_list.append('  {')
    func_str_list.append('    #pragma HLS PIPELINE II=1')
    func_str_list.append('    in_tmp = Input_1.read();')
    func_str_list.append('    pixels.x(7, 0)=in_tmp(7, 0);')
    func_str_list.append('    pixels.y(7, 0)=in_tmp(15, 8);')
    func_str_list.append('    pixels.color(7, 0)=in_tmp(23, 16);')
    func_str_list.append('    frame_buffer[ pixels.x ][ pixels.y - ' + str(int(256 - (256/par_zculling)*(idx_par_zculling+1))) + '] = pixels.color;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  counter++;')
    func_str_list.append('  if(counter==NUM_3D_TRI){')
    func_str_list.append('    for (i=0; i<MAX_X; i++){')
    func_str_list.append('      for(j=0; j<MAX_Y/' + str(par_zculling) + '; j+=16){')
    func_str_list.append('#pragma HLS PIPELINE II=1')
    func_str_list.append('        for (int k=0; k<16; k++){')
    func_str_list.append('          out_FB( k*8+7,  k*8) = frame_buffer[i][j+k];')
    func_str_list.append('        }')
    func_str_list.append('        Output_1.write(out_FB);')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('    counter=0;')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')

    return 'coloringFB_i' + str(idx_par_zculling + 1), "\n".join(func_str_list)

def gen_coloring_header(idx_par_zculling):
    func_str_list = []
    func_str_list.append('void coloringFB_i' + str(idx_par_zculling + 1) + ' (')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<128>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'coloringFB_i' + str(idx_par_zculling + 1), "\n".join(func_str_list)

def gen_output_data_func(par_zculling):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void output_data(')
    for idx in range(par_zculling):    
        func_str_list.append('    hls::stream<ap_uint<128>> & Input_' + str(idx + 1) + ',')
    func_str_list.append('    hls::stream<ap_uint<512>> & Output_1)')
    func_str_list.append('')
    func_str_list.append('{')
    for idx in range(par_zculling):
        func_str_list.append('#pragma HLS INTERFACE axis register port=Input_' + str(idx + 1))
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('  #pragma HLS INLINE off')

    func_str_list.append('')
    func_str_list.append('  for (int i=0; i<MAX_X; i++){')
    func_str_list.append('')
    for idx in range(par_zculling-1,-1,-1):    
        func_str_list.append('    RECV_' + str(idx + 1) + ': for(int k=0; k<MAX_Y/' + str(4*par_zculling) + '; k+=16){')
        func_str_list.append('      bit512 out_tmp;')
        func_str_list.append('      bit128 tmp;')
        func_str_list.append('#pragma HLS PIPELINE II=1')
        func_str_list.append('      for(int l = 0; l < 4; l++){')
        func_str_list.append('        tmp = Input_' + str(idx + 1) + '.read();')
        func_str_list.append('        for(int out_i = 0; out_i < 4; out_i++){')
        func_str_list.append('          out_tmp(l*128+out_i*32+31, l*128+out_i*32) = tmp(out_i*32+31, out_i*32);')
        func_str_list.append('        }')
        func_str_list.append('      }')
        func_str_list.append('      Output_1.write(out_tmp);')
        func_str_list.append('    }')
        func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'output_data', "\n".join(func_str_list)

def gen_output_data_header(par_zculling):
    func_str_list = []
    func_str_list.append('void output_data (')
    for idx in range(par_zculling):    
        func_str_list.append('    hls::stream<ap_uint<128>> & Input_' + str(idx + 1) + ',')
    func_str_list.append('    hls::stream<ap_uint<512>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'output_data', "\n".join(func_str_list)


def gen_data_transfer_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void data_transfer (')
    func_str_list.append('    hls::stream<ap_uint<512>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<128>> & Output_1)')
    func_str_list.append('')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('    bit512 in_tmp;')
    func_str_list.append('    bit128 out_tmp;')
    func_str_list.append('')
    func_str_list.append('    for ( int i = 0; i < NUM_3D_TRI/4; i++) {')
    func_str_list.append('        in_tmp = Input_1.read();')
    func_str_list.append('')
    func_str_list.append('        for (int j=0; j<4; j++) {')
    func_str_list.append('#pragma HLS PIPELINE II=1')
    func_str_list.append('            for(int jj=0; jj<4; jj++){')
    func_str_list.append('                out_tmp(jj*32+31, jj*32) = in_tmp(j*128+jj*32+31, j*128+jj*32);')
    func_str_list.append('            }')
    func_str_list.append('            Output_1.write(out_tmp);')
    func_str_list.append('        }')
    func_str_list.append('    }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'data_transfer', "\n".join(func_str_list)

def gen_data_transfer_header():
    func_str_list = []
    func_str_list.append('void data_transfer (')
    func_str_list.append('    hls::stream<ap_uint<512>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<128>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'data_transfer', "\n".join(func_str_list)



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

    # Values for PAR_RAST, PAR_ZCULLING shuold be identical across all the ops
    for prev_op, param_dict in cur_param_dict.items():
        if prev_op != 'metric':
            # print(prev_op)
            # print(param_dict)
            if 'PAR_RAST' in param_dict:
                par_rast = param_dict['PAR_RAST']
            if 'PAR_ZCULLING' in param_dict:
                par_zculling = param_dict['PAR_ZCULLING']
    # par_rast = 4
    # par_zculling = 4
    print(par_rast)
    print(par_zculling)


    ###########################################
    ## Generate src files based on cur param ##
    ###########################################

    # cpp code gen
    func_name_list = []
    ops_to_compile_list = []
    filedata_dict = {}

    func_name, filedata = gen_data_transfer_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_data_transfer_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    func_name, filedata = gen_prj_rast1_func(par_rast)
    func_name_list.append(func_name)
    func_name, filedata_header = gen_prj_rast1_header(par_rast)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    for idx_par_rast in range(par_rast):
        func_name, filedata = gen_rast2_func(idx_par_rast, par_zculling)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_rast2_header(idx_par_rast)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

    for idx_par_zculling in range(par_zculling):
        func_name, filedata = gen_zculling_func(par_rast, idx_par_zculling, par_zculling)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_zculling_header(par_rast, idx_par_zculling)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

        func_name, filedata = gen_coloring_func(par_zculling, idx_par_zculling)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_coloring_header(idx_par_zculling)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

    func_name, filedata = gen_output_data_func(par_zculling)
    func_name_list.append(func_name)
    func_name, filedata_header = gen_output_data_header(par_zculling)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    print()

    #############################################
    ## Update cur_param.json for new operators ##
    #############################################
    for func_name in func_name_list:
        if func_name not in cur_param_dict.keys():
            base_function_name = func_name.split('_i')[0]
            represent_function_name = base_function_name + '_i1'
            # Assume that kernel_clk, num_leaf_interface, and par factor are identical
            cur_param_dict[func_name] = cur_param_dict[represent_function_name]


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


    # Modify typedefs.h
    # Nothing to do for Rendering


    #################################################
    ## Update application graph (top_no_merge.cpp) ##
    #################################################
    top_str_list = ["data_transfer(Input_1, data_transfer_out);"]
    # print(func_name_list)
    base_func_name_list = ["data_transfer", "prj_rast1", "rast2", "zculling", 'coloringFB', 'output_data']
    for func_name in base_func_name_list:
        if func_name.startswith('prj_rast1'):
            prj_rast1_str = 'prj_rast1(data_transfer_out'
            for idx_par_rast in range(par_rast):
                prj_rast1_str += ', prj_rast1_out_' + str(idx_par_rast + 1)
                if idx_par_rast == par_rast-1:
                    prj_rast1_str += ');'
            top_str_list.append(prj_rast1_str)
        elif func_name.startswith('rast2'):
            for idx_par_rast in range(par_rast):
                rast2_str = 'rast2_i' + str(idx_par_rast + 1) + '(prj_rast1_out_' + str(idx_par_rast + 1)
                for idx_par_zculling in range(par_zculling):
                    rast2_str += ', rast2_i' + str(idx_par_rast + 1) + '_out_' + str(idx_par_zculling + 1)
                    if idx_par_zculling == par_zculling-1:
                        rast2_str += ');'
                top_str_list.append(rast2_str)
        elif func_name.startswith('zculling'):
            for idx_par_zculling in range(par_zculling):
                zculling_str = 'zculling_i' + str(idx_par_zculling + 1) + '('
                for idx_par_rast in range(par_rast):
                    zculling_str += 'rast2_i' + str(idx_par_rast + 1) + '_out_' + str(idx_par_zculling + 1) + ', '
                zculling_str += 'zculling_i' + str(idx_par_zculling + 1) + '_out);'
                top_str_list.append(zculling_str)
        elif func_name.startswith('coloringFB'):
            for idx_par_zculling in range(par_zculling):
                coloringFB_str = 'coloringFB_i' + str(idx_par_zculling + 1) + \
                                 '(zculling_i' + str(idx_par_zculling + 1) + '_out, ' + \
                                 'coloringFB_i' + str(idx_par_zculling + 1) + '_out);'
                top_str_list.append(coloringFB_str)
        elif func_name.startswith('output_data'):
            output_data_str = 'output_data('
            for idx_par_zculling in range(par_zculling):
                output_data_str += 'coloringFB_i' + str(idx_par_zculling + 1) + '_out, '
            output_data_str += 'Output_1);'
            top_str_list.append(output_data_str)
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
    spec_dict = {}
    for func_name in func_name_list:
        spec_dict[func_name] = {}
        spec_dict[func_name]['kernel_clk'] = cur_param_dict[func_name]['kernel_clk']
        spec_dict[func_name]['num_leaf_interface'] = cur_param_dict[func_name]['num_leaf_interface']
    with open(op_dir + '/specs.json', 'w') as outfile:
        json.dump(spec_dict, outfile, sort_keys=True, indent=4)


    #################################
    ## Remove old src files if any ##
    #################################
    # cpp_file_list = [x for x in os.listdir('./operators/') if x.endswith('.cpp')]
    # for cpp_file in cpp_file_list:
    #     func_name = cpp_file.split('.')[0]
    #     if func_name not in func_name_list:
    #         os.system('rm ./operators/' + func_name + '.cpp')
    #         os.system('rm ./operators/' + func_name + '.h')
    # os.system('rm ./operators/prj_rast1*')
    # os.system('rm ./operators/rast2_*')
    # os.system('rm ./operators/zculling*')
    # os.system('rm ./operators/coloring*')
    # os.system('rm ./operators/output_data*')
