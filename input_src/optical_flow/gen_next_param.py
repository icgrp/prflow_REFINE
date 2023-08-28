import json, math, os
import argparse

# Based on the search space (params.json), update ./host/typedefs.h, ./operators/specs.json and cur_param.json.
# Generate ./operators/*.cpp if necessary => this file is benchmark-specific


def gen_outer_product_func(outer_width, par_factor):
    output_width = math.ceil(6/par_factor * outer_width/32) * 32

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

    func_str_list.append('      ap_uint<' + str(output_width) + '> out_tmp;')
    for i in range(par_factor):
        max_width = 0
        for j in range(6//par_factor):
            max_width += outer_width
            func_str_list.append('      out_tmp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ') = out.val[' + \
                                                    str(j + 6//par_factor *i) + '].range(' + str(outer_width-1) + ',0);')
        if max_width != output_width: # needs to send some blank vals
            func_str_list.append('      out_tmp(' + str(output_width-1) + ',' + str(max_width) + ') = 0;')
        func_str_list.append('      Output_' + str(i+1) + '.write(out_tmp);')
        func_str_list.append('')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    return 'outer_product', "\n".join(func_str_list)


def gen_outer_product_header(outer_width, par_factor):
    output_width = math.ceil(6/par_factor * outer_width/32) * 32

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
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void tensor_weight_y_' + str(idx_par_factor + 1) + '(')
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
    func_str_list.append('        ap_uint<' + str(outer_product_width) + '> in_tmp;')
    func_str_list.append('        in_tmp = Input_1.read();')
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
    func_str_list.append('        ap_uint<' + str(outer_product_width) + '> widetemp;')
    max_width = 0
    for j in range(6//par_factor):
        max_width += outer_width
        func_str_list.append('        widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ')  = acc.val[' + str(j) + '](' + str(outer_width-1) + ', 0);')

    if max_width != outer_product_width: # needs to send some blank vals
        func_str_list.append('        widetemp(' + str(outer_product_width-1) + ',' + str(max_width) + ') = 0;')
    func_str_list.append('        Output_1.write(widetemp);')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'tensor_weight_y_' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_y_header(outer_width, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('void tensor_weight_y_' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_y_' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_x_func(outer_width, par_factor, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void tensor_weight_x_' + str(idx_par_factor + 1) + '(')
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
    func_str_list.append('        ap_uint<' + str(outer_product_width) + '> widetemp;')
    func_str_list.append('        widetemp = Input_1.read();')
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
    func_str_list.append('        ap_uint<' + str(outer_product_width) + '> widetemp;')
    max_width = 0
    for j in range(6//par_factor):
        max_width += outer_width
        func_str_list.append('        widetemp(' + str(outer_width*(j+1)-1) + ',' + str(outer_width*j) + ')  = acc.val[' + str(j) + '](' + str(outer_width-1) + ', 0);')

    if max_width != outer_product_width: # needs to send some blank vals
        func_str_list.append('        widetemp(' + str(outer_product_width-1) + ',' + str(max_width) + ') = 0;')

    func_str_list.append('        Output_1.write(widetemp);')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    return 'tensor_weight_x_' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_x_header(outer_width, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('void tensor_weight_x_' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_x_' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_flow_calc_func(outer_width, par_factor, cast_float):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32
    func_str_list = []

    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void flow_calc(')
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
    func_str_list.append('      ap_uint<' + str(outer_product_width) + '> widetemp;')
    func_str_list.append('')

    for i in range(par_factor):
        func_str_list.append('      widetemp = Input_' + str(i + 1) + '.read();')
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
    func_str_list.append('')
    return 'flow_calc', "\n".join(func_str_list)


def gen_flow_calc_header(outer_width, par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('void flow_calc(')
    for idx_par_factor in range(par_factor):
        func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_' + str(idx_par_factor+1) + ',')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> &Output_2')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'flow_calc', "\n".join(func_str_list)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # args = parser.parse_args()
    # bottleneck = args.bottleneck

    # TODO: Create tuner
    op_dir = './operators'
    os.system('rm ./operators/outer_product*')
    os.system('rm ./operators/tensor_weight*')
    os.system('rm ./operators/flow_calc*')

    # 1, 16, False => +777, GOOD (161.651)
    # 2, 16, False => +777, GOOD (161.651)
    # 1, 16, True => +775, GOOD (161.651)
    # 2, 16, True => +775, GOOD (161.651)

    # 1, 32, False => +781, GOOD (150.083)
    # 2, 32, False => +781, GOOD (150.083)
    # 1, 32, True => +774, GOOD (150.083)
    # 2, 32, True => +774, GOOD (150.083)

    # 1, 48, False => flow_calc 50K Luts
    # 2, 48, False => flow_calc 50K Luts
    # 1, 48, True => +774, GOOD (32.058)
    # 2, 48, True => +774, GOOD (32.058)


    par_factor = 2 # 1, 2
    outer_width = 32 # 16, 32, 48
    dummy_len = 774
    outer_width_int = 27
    calc_width_int = 56
    cast_float = True

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
        elif line.startswith('#define CAST_FLOAT'):
            if cast_float:
                line = '#define CAST_FLOAT true\n'
            else:
                line = '#define CAST_FLOAT false\n'
        filedata += line
    with open('./host/typedefs.h', 'w') as outfile:
        outfile.write(filedata)


    # unchanged operators
    func_name_list =["data_transfer", "gradient_xyz_calc", "gradient_weight_x", "gradient_weight_y", "output_data"]

    func_name, filedata = gen_outer_product_func(outer_width, par_factor)
    func_name_list.append(func_name)
    with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
        outfile.write(filedata)

    func_name, filedata_header = gen_outer_product_header(outer_width, par_factor)
    with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
        outfile.write(filedata_header)

    for idx_par_factor in range(par_factor):
        func_name, filedata = gen_tensor_weight_y_func(outer_width, par_factor, idx_par_factor)
        func_name_list.append(func_name)
        with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
            outfile.write(filedata)

        func_name, filedata_header = gen_tensor_weight_y_header(outer_width, idx_par_factor)
        with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
            outfile.write(filedata_header)

        func_name, filedata = gen_tensor_weight_x_func(outer_width, par_factor, idx_par_factor)
        func_name_list.append(func_name)
        with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
            outfile.write(filedata)

        func_name, filedata_header = gen_tensor_weight_x_header(outer_width, idx_par_factor)
        with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
            outfile.write(filedata_header)


    func_name, filedata = gen_flow_calc_func(outer_width, par_factor, cast_float)
    func_name_list.append(func_name)
    with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
        outfile.write(filedata)

    func_name, filedata_header = gen_flow_calc_header(outer_width, par_factor)
    with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
        outfile.write(filedata_header)

    # For now, all run in 200 and num leaf interface is 1
    spec_dict = {}
    for func_name in func_name_list:
        spec_dict[func_name] = {"kernel_clk": 200, "num_leaf_interface": 1}
    with open(op_dir + '/specs.json', 'w') as outfile:
        json.dump(spec_dict, outfile, sort_keys=True, indent=4)

    # top.cpp
    top_str_list = ['data_transfer(Input_1, data_transfer_out);',
                    'gradient_xyz_calc(data_transfer_out, gradient_x, gradient_y, gradient_z);',
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
                tensor_weight_y_str = 'tensor_weight_y_' + str(idx_par_factor + 1) + '(outer_product_out_' + str(idx_par_factor + 1) + ', '
                tensor_weight_y_str += 'tensor_weight_y_out_' + str(idx_par_factor + 1) + ');'
                top_str_list.append(tensor_weight_y_str)
        elif func_name.startswith('tensor_weight_x'):
            for idx_par_factor in range(par_factor):
                tensor_weight_x_str = 'tensor_weight_x_' + str(idx_par_factor + 1) + '(tensor_weight_y_out_' + str(idx_par_factor + 1) + ', '
                tensor_weight_x_str += 'tensor_weight_x_out_' + str(idx_par_factor + 1) + ');'
                top_str_list.append(tensor_weight_x_str)
        elif func_name.startswith('flow_calc'):
            flow_calc_str = 'flow_calc('
            for idx_par_factor in range(par_factor):
                flow_calc_str += 'tensor_weight_x_out_' + str(idx_par_factor + 1) + ', '
            flow_calc_str += ' flow_calc_1, flow_calc_2);'
            top_str_list.append(flow_calc_str)

    output_data_str = 'output_data(flow_calc_1, flow_calc_2, Output_1);'
    top_str_list.append(output_data_str)
    with open('./host/top.cpp', 'w') as outfile:
        outfile.write("\n".join(top_str_list))

    
    # Check all the functions are instantiated in top.cpp
    top_func_name_list = []
    with open('./host/top.cpp', 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            func_name = line.split('(')[0]
            top_func_name_list.append(func_name)


    assert(top_func_name_list.sort() == func_name_list.sort())

