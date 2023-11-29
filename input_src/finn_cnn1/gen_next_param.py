import json, math, os, sys
import argparse
import re
from collections import Counter
sys.path.append('../')
from code_gen_util import return_operator_io_argument_dict_local, return_operator_inst_dict_local, return_operator_connect_list_local,\
                          return_operator_io_type_and_width, needs_write_param, needs_write_filedata, sorted_op_list_backward, divide_ops,\
                          perform_merging, merge_op_list

from gen_folding_config import write_folding_config

########################
## Benchmark-specific ##
########################

def replace_idx(lines, base_idx = ''):
    # prefix_list = ['thr_batch', 'str_dwc', 'conv', 'mva', 'str_mp_batch', 'lab_sel']
    # If prefix_list is the list above, we need to change the name of header files too, like mva_1_params.h => mva_1_1_params.h
    prefix_list = ['str_dwc']

    func_name_list = []

    for line in lines:
        for prefix in prefix_list:
            if ('void ' + prefix + '_') in line:
                func_name = line.split('(')[0].replace('void ', '')
                func_name_list.append(func_name)

    for i, func_name in enumerate(func_name_list):
        prev_idx = func_name.split('_')[-1]
        new_func_name = func_name.replace('_' + prev_idx, '')
        new_func_name = new_func_name + '_' + base_idx + '_' + str(i)
        # print(func_name)
        # print(new_func_name)
        new_lines = []
        for line in lines:
            if func_name in line:
                line = line.replace(func_name, new_func_name)
            new_lines.append(line)
        lines = new_lines

    return "".join(lines)

def replace_vars(line, def_list, op_type, idx):
    for def_var in def_list:
        line = line.replace(def_var, def_var + "_" + op_type + "_" + idx)
    return line

# Add appropriate indices and copy files to src_dir
# op_type = 'thr_batch' or 'str_dwc' or 'conv' or 'mva' or 'str_mp_batch' or 'lab_sel' 
def post_process(op_type, file_dirs, src_dir):
    prefix = prefix_dict[op_type]

    for d in file_dirs:
        idx = d.split(build_dir)[1].split(prefix)[1].split('_')[0]
        # print(idx)
        # print(idx)

        # main hls function
        new_filedata = []
        with open(d + "/top_" + prefix + idx + '.cpp' , 'r') as infile:
            filedata = infile.readlines()
        
        def_list = []
        for line in filedata:
            if line.startswith("#define"):
                def_var = line.split()[1]
                new_def_var = def_var + "_" + op_type + "_" + idx
                line = line.replace(def_var, new_def_var)
                def_list.append(def_var)
            else:
                line = line.replace(prefix, op_type + "_") # module name
                line = line.replace("thresh.h", op_type + "_" + idx + "_thresh.h") # thresh.h
                line = line.replace("threshs", op_type + "_" + idx + "_threshs") # threshs if exists
                line = line.replace("params.h", op_type + "_" + idx + "_params.h") # thresh.h
                line = line.replace("=weights", "=" + op_type + "_" + idx + "_weights") # weights variable if exists
                line = line.replace("weights,", op_type + "_" + idx + "_weights,") # weights variable if exists
                line = replace_vars(line, def_list, op_type, idx)
            new_filedata.append(line)

        with open(d + "/" + op_type + "_" + idx + '.cpp' , 'w') as outfile:
            outfile.writelines(new_filedata)
        os.system('cp ' + d + "/" + op_type + "_" + idx + '.cpp ' + src_dir)

        # thresh file
        if os.path.isfile(d + "/thresh.h"):
            new_filedata = []
            with open(d + "/thresh.h" , 'r') as infile:
                filedata = infile.readlines()

            for line in filedata:
                if "threshs" in line:
                    line = line.replace("threshs", op_type + "_" + idx + "_threshs")
                new_filedata.append(line)

            with open(d + "/" + op_type + "_" + idx + '_thresh.h' , 'w') as outfile:
                outfile.writelines(new_filedata)
            os.system('cp ' + d + "/" + op_type + "_" + idx + '_thresh.h ' + src_dir)

        # params file
        if os.path.isfile(d + "/params.h"):
            new_filedata = []
            with open(d + "/params.h" , 'r') as infile:
                filedata = infile.readlines()

            for line in filedata:
                if "weights" in line:
                    line = line.replace("weights", op_type + "_" + idx + "_weights")
                new_filedata.append(line)

            with open(d + "/" + op_type + "_" + idx + '_params.h' , 'w') as outfile:
                outfile.writelines(new_filedata)
            os.system('cp ' + d + "/" + op_type + "_" + idx + '_params.h ' + src_dir)


def get_input_stream_width(src_file):
    with open(src_file , 'r') as infile:
        filedata = infile.readlines()
        SIMD_val = -1 # for conv only
        Input_precision_val = -1 # for conv only
        for line in filedata:
            if line.startswith('#define SIMD1'):
                SIMD_val = int(line.split()[2])
            if line.startswith('#define Input_precision1'):
                Input_precision_val = int(line.split()[2])
            if '&in0' in line:
                if 'SIMD1' in line and 'Input_precision1' in line:
                    input_stream_width = SIMD_val * Input_precision_val
                else:
                    input_stream_width = int(line.split('<ap_uint<')[1].split('>>')[0])
    return input_stream_width

def get_output_stream_width(src_file):
    with open(src_file , 'r') as infile:
        filedata = infile.readlines()
        SIMD_val = -1 # for conv only
        Input_precision_val = -1 # for conv only
        for line in filedata:
            if line.startswith('#define SIMD1'):
                SIMD_val = int(line.split()[2])
            if line.startswith('#define Input_precision1'):
                Input_precision_val = int(line.split()[2])
            if '&out' in line:
                if 'SIMD1' in line and 'Input_precision1' in line:
                    output_stream_width = SIMD_val * Input_precision_val
                else:
                    output_stream_width = int(line.split('<ap_uint<')[1].split('>>')[0])
    return output_stream_width


# def gen_data_transfer_func():
#     func_str_list = []
#     func_str_list.append('#include "../host/finn-hlslib/bnn-library.h"')
#     func_str_list.append('#include "../host/typedefs.h"')
#     func_str_list.append('')
#     func_str_list.append('')
#     func_str_list.append('void data_transfer (')
#     func_str_list.append('        hls::stream<ap_uint<512> > & Input_1,')
#     func_str_list.append('        hls::stream<ap_uint<8> > & Output_1')
#     func_str_list.append('        )')
#     func_str_list.append('{')
#     func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
#     func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
#     func_str_list.append('    bit512 in_tmp;')
#     func_str_list.append('    ap_uint<8> out_tmp;')
#     func_str_list.append('')
#     func_str_list.append('    // INPUT_SIZE = 30720')
#     func_str_list.append('    for ( int i = 0; i < 30720; i++){')
#     func_str_list.append('    // for ( int i = 0; i < 384; i++){ // 8(BATCH_SIZE) * 32*32*3/64')
#     func_str_list.append('        in_tmp = Input_1.read();')
#     func_str_list.append('        for (int j = 0; j < 64; j++){ // 64 = 512/8')
#     func_str_list.append('            out_tmp = in_tmp(8*j+7, 8*j+0);')
#     func_str_list.append('            Output_1.write(out_tmp);')
#     func_str_list.append('        }')
#     func_str_list.append('        std::cout << "i: " << i << std::endl;')
#     func_str_list.append('    }')
#     func_str_list.append('}')
#     func_str_list.append('')
#     return 'data_transfer', "\n".join(func_str_list)

# def gen_data_transfer_header():
#     func_str_list = []
#     func_str_list.append('void data_transfer (')
#     func_str_list.append('    hls::stream<ap_uint<512>> & Input_1,')
#     func_str_list.append('    hls::stream<ap_uint<8>> & Output_1')
#     func_str_list.append('    );')
#     func_str_list.append('#pragma map_target = HW')
#     return 'data_transfer', "\n".join(func_str_list)



# def gen_out_data_collect_func():
#     func_str_list = []
#     func_str_list.append('#include "../host/typedefs.h"')
#     func_str_list.append('#include "../host/finn-hlslib/bnn-library.h"')
#     func_str_list.append('')
#     func_str_list.append('')
#     func_str_list.append('void out_data_collect (')
#     func_str_list.append('        hls::stream<ap_uint<8> > & Input_1,')
#     func_str_list.append('        hls::stream<ap_uint<512> > & Output_1')
#     func_str_list.append('        )')
#     func_str_list.append('{')
#     func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
#     func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
#     func_str_list.append('    ap_uint<8> in_tmp;')
#     func_str_list.append('    ap_uint<512> out_tmp;')
#     func_str_list.append('')
#     func_str_list.append('    int out_idx = 0;')
#     func_str_list.append('    for (int i=0; i < 10; i++){ // total 640 tests')
#     func_str_list.append('        for (int j = 0; j < 64; j++){ // 64 data fits in 512bits')
#     func_str_list.append('            in_tmp = Input_1.read();')
#     func_str_list.append('            out_tmp(8*j+7, 8*j) = in_tmp;')
#     func_str_list.append('        }')
#     func_str_list.append('        Output_1.write(out_tmp);')
#     func_str_list.append('    }')
#     func_str_list.append('}')
#     func_str_list.append('')
#     return 'out_data_collect', "\n".join(func_str_list)

# def gen_out_data_collect_header():
#     func_str_list = []
#     func_str_list.append('void out_data_collect (')
#     func_str_list.append('    hls::stream<ap_uint<8>> & Input_1,')
#     func_str_list.append('    hls::stream<ap_uint<512>> & Output_1')
#     func_str_list.append('    );')
#     func_str_list.append('#pragma map_target = HW')
#     return 'out_data_collect', "\n".join(func_str_list)





# layer_0_0:    thr_batch - str_dwc - conv 
def gen_layer_0_0(src_dir, count_str_dwc, layer_num, layer_index):

    thr_batch_in = get_input_stream_width(src_dir + 'thr_batch_' + str(layer_num) + '.cpp')
    thr_batch_out = get_output_stream_width(src_dir + 'thr_batch_' + str(layer_num) + '.cpp')

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')


    new_filedata_include = []
    new_filedata = []
    new_filedata.append('\n')
    new_filedata.append('void data_transfer (\n')
    new_filedata.append('        hls::stream<ap_uint<256> > & Input_1,\n')
    new_filedata.append('        hls::stream<ap_uint<8> > & Output_1\n')
    new_filedata.append('        )\n')
    new_filedata.append('{\n')
    new_filedata.append('#pragma HLS INTERFACE axis register port=Input_1\n')
    new_filedata.append('#pragma HLS INTERFACE axis register port=Output_1\n')
    new_filedata.append('    ap_uint<256> in_tmp;\n')
    new_filedata.append('    ap_uint<8> out_tmp;\n')
    new_filedata.append('\n')
    new_filedata.append('    // 32 = 256/8\n')
    new_filedata.append('    // Thresholding_Batch reads reps(1) * ImgDim(1024) * NF(3)\n')
    new_filedata.append('    // => 1024*3/32 = 96\n')
    new_filedata.append('    for ( int i = 0; i < 96; i++){\n')
    new_filedata.append('        in_tmp = Input_1.read();\n')
    new_filedata.append('        for (int j = 0; j < 32; j++){ // 32 = 256/8\n')
    new_filedata.append('            out_tmp = in_tmp(8*j+7, 8*j+0);\n')
    new_filedata.append('            Output_1.write(out_tmp);\n')
    new_filedata.append('        }\n')
    new_filedata.append('    }\n')
    new_filedata.append('}\n')
    new_filedata.append('\n')
    new_filedata.append('// ------------------------------------------------------------------------\n')


    # thr_batch
    with open(src_dir + 'thr_batch_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if thr_batch_out != conv_in:
        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1

    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')


    layer_filedata = [
        'void layer_' + str(layer_num) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<256> > & Input_1,\n',
        '        hls::stream<ap_uint<' + str(conv_out) + '> > & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    layer_filedata.append('    static hls::stream<ap_uint<8>> out_data_transfer("out_data_transfer");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(thr_batch_out) + '>> out_thr_batch("out_thr_batch");\n')
    if thr_batch_out != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')
    layer_filedata.append('    data_transfer(Input_1, out_data_transfer);\n')
    layer_filedata.append('    thr_batch_' + str(layer_num) + '(out_data_transfer, out_thr_batch);\n')
    if thr_batch_out != conv_in:
        layer_filedata.append('    str_dwc_0(out_thr_batch, out_str_dwc_0);\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_0, Output_1);\n')
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(out_thr_batch, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')


    new_filedata_include = sorted(list(set(new_filedata_include)))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"\n'] + \
                            new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')
    new_filedata = new_filedata_include + new_filedata + layer_filedata


    # with open(src_dir + 'layer_' + str(layer_num) + '_' + str(layer_index) + '.cpp' , 'w') as outfile:
    #     outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<256>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(conv_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    # with open(src_dir + 'layer_' + str(layer_num) + '_' + str(layer_index) + '.h' , 'w') as outfile:
    #     outfile.writelines(layer_h_filedata)

    # count_str_dwc, prev_out_width, func_name, filedata, filedata_header
    return count_str_dwc, conv_out, 'layer_' + str(layer_num) + '_' + str(layer_index), new_filedata, "".join(layer_h_filedata)





# layer:    str_dwc - mva 
def gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, layer_name):

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    layer_filedata = [
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_' + str(count_str_dwc) +\
                                 '("out_str_dwc_' + str(count_str_dwc) + '");\n')

    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')

    new_filedata_include = []
    new_filedata = []

    if prev_out_width != mva_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_' + str(count_str_dwc) + ');\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_' + str(count_str_dwc) + ', Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(Input_1, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')

    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')


    new_filedata_include = sorted(list(set(new_filedata_include)))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"\n'] +\
                             new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) + '.cpp' , 'w') as outfile:
    #     outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) + '.h' , 'w') as outfile:
    #     outfile.writelines(layer_h_filedata)

    return count_str_dwc, mva_out,  'layer_' + str(layer_name) + '_' + str(layer_index),  new_filedata, "".join(layer_h_filedata)



# layer:                str_dwc - conv
def gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index):

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')

    layer_filedata = [
        'void layer_' + str(layer_num) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(conv_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_' +\
                                 str(count_str_dwc) + '("out_str_dwc_' + str(count_str_dwc) +  '");\n')

    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')

    new_filedata_include = []
    new_filedata = []

    if prev_out_width != conv_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_' +\
                             str(count_str_dwc) + ');\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_' +\
                             str(count_str_dwc) + ', Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(Input_1, Output_1);\n')


    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    layer_filedata.append('\n')
    layer_filedata.append('}\n')


    new_filedata_include = sorted(list(set(new_filedata_include)))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"\n'] +\
                             new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    # with open(src_dir + 'layer_' + str(layer_num) + '_' + str(layer_index) + '.cpp' , 'w') as outfile:
    #     outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(conv_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    # with open(src_dir + 'layer_' + str(layer_num) + '_' + str(layer_index) + '.h' , 'w') as outfile:
    #     outfile.writelines(layer_h_filedata)

    return count_str_dwc, conv_out, 'layer_' + str(layer_num) + '_' + str(layer_index),  new_filedata, "".join(layer_h_filedata)




# layer:                str_dwc - mva - str_dwc - str_mp_batch
def gen_layer_mva_mp(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, mp_index, layer_name):

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    str_mp_batch_in = get_input_stream_width(src_dir + 'str_mp_batch_' + str(mp_index) + '.cpp')
    str_mp_batch_out = get_output_stream_width(src_dir + 'str_mp_batch_' + str(mp_index) + '.cpp')

    layer_filedata = [
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_' + str(count_str_dwc) +\
                                 '("out_str_dwc_' + str(count_str_dwc) + '");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_out) + '>> out_mva_' + str(layer_num) +\
                                 '("out_mva_' + str(layer_num) + '");\n')
    if mva_out != str_mp_batch_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(str_mp_batch_in) + '>> out_str_dwc_' + str(count_str_dwc+1) +\
                                 '("out_str_dwc_' + str(count_str_dwc+1) + '");\n')
    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')

    new_filedata_include = []
    new_filedata = []

    if prev_out_width != mva_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_' + str(count_str_dwc) + ');\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_' + str(count_str_dwc) + ', out_mva_' + str(layer_num) + ');\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(Input_1, out_mva_' + str(layer_num) + ');\n')


    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if mva_out != str_mp_batch_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_mva_' + str(layer_num) + ', out_str_dwc_' + str(count_str_dwc) + ');\n')
        layer_filedata.append('    str_mp_batch_' + str(mp_index) + '(out_str_dwc_' + str(count_str_dwc) + ', Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    str_mp_batch_' + str(mp_index) + '(out_mva_' + str(layer_num) + ', Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')

    # str_mp_batch
    with open(src_dir + 'str_mp_batch_' + str(mp_index) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    new_filedata_include = sorted(list(set(new_filedata_include)))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"\n'] +\
                             new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) + '.cpp' , 'w') as outfile:
    #     outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) + '.h' , 'w') as outfile:
    #     outfile.writelines(layer_h_filedata)

    return count_str_dwc, str_mp_batch_out, 'layer_' + str(layer_name) + '_' + str(layer_index),  new_filedata, "".join(layer_h_filedata)



# layer_last:             str_dwc - mva - lab_sel
def gen_layer_last(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, layer_name):

    mva_0_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_0_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    layer_filedata = [
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<256>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != mva_0_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_0_in) + '>> out_str_dwc_' + str(count_str_dwc) +\
                                 '("out_str_dwc_' + str(count_str_dwc) + '");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_0_out) + '>> out_mva_' + str(layer_num) +\
                                '("out_mva_' + str(layer_num) + '");\n')
    layer_filedata.append('    static hls::stream<ap_uint<8>> out_lab_sel_0("out_lab_sel_0");\n')

    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')
    # Let's assume that mva_2_out==1 and input width of labelselect is 1

    new_filedata_include = []
    new_filedata = []
    new_filedata.append('\n')
    new_filedata.append('void out_data_collect (\n')
    new_filedata.append('        hls::stream<ap_uint<8> > & Input_1,\n')
    new_filedata.append('        hls::stream<ap_uint<256> > & Output_1\n')
    new_filedata.append('        )\n')
    new_filedata.append('{\n')
    new_filedata.append('#pragma HLS INTERFACE axis register port=Input_1\n')
    new_filedata.append('#pragma HLS INTERFACE axis register port=Output_1\n')
    new_filedata.append('    ap_uint<8> in_tmp;\n')
    new_filedata.append('    static ap_uint<256> out_tmp;\n')
    new_filedata.append('    static ap_uint<16> counter = 0;\n')
    new_filedata.append('\n')
    new_filedata.append('    in_tmp = Input_1.read();\n')
    new_filedata.append('    out_tmp(8*counter+7, 8*counter) = in_tmp;\n')
    new_filedata.append('    if(counter == 31){ // 32 data fits in 256bits\n') 
    new_filedata.append('        Output_1.write(out_tmp);\n')
    new_filedata.append('        counter = 0;\n')
    new_filedata.append('    }\n')
    new_filedata.append('    else{\n')
    new_filedata.append('        counter++;\n')
    new_filedata.append('    }\n')
    new_filedata.append('}\n')
    new_filedata.append('\n')
    new_filedata.append('// ------------------------------------------------------------------------\n')


    layer_num_new = layer_num
    if prev_out_width != mva_0_in:

        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_' + str(count_str_dwc) + ');\n')
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_str_dwc_' + str(count_str_dwc) + ', out_mva_' + str(layer_num) + ');\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and \
                    not line.endswith('_thresh.h"\n') and \
                    not line.endswith('_params.h"\n') and \
                    not line.endswith('bnn-library.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes") and \
                        not line.startswith('#include "bnn-library.h"'):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num_new) + '(Input_1, out_mva_' + str(layer_num) + ');\n')

    # mva
    with open(src_dir + 'mva_' + str(layer_num_new) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    # label_sel, assume that input width of label_sel is fixed to 16
    layer_filedata.append('    lab_sel_0(out_mva_' + str(layer_num) + ', out_lab_sel_0);\n')
    with open(src_dir + 'lab_sel_0.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and \
                not line.endswith('_thresh.h"\n') and \
                not line.endswith('_params.h"\n') and \
                not line.endswith('bnn-library.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes") and \
                    not line.startswith('#include "bnn-library.h"'):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    layer_filedata.append('    out_data_collect(out_lab_sel_0, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')


    new_filedata_include = sorted(list(set(new_filedata_include)))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"\n'] + \
                            new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) + '.cpp' , 'w') as outfile:
    #     outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_name) + '_' + str(layer_index) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<256>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    # with open(src_dir + 'layer_' + str(layer_name) + '_' + str(layer_index) +'.h' , 'w') as outfile:
    #     outfile.writelines(layer_h_filedata)

    return count_str_dwc, 8, 'layer_' + str(layer_name) + '_' + str(layer_index),  new_filedata, "".join(layer_h_filedata)



# Based on ./params/cur_param.json, this file 
# generates HLS source codes (if necessary)
# updates ./host/typedefs.h, ./operators/specs.json, cur_parm.json
if __name__ == '__main__':


    # Generate folding_config.json from cur_param.json
    cur_param_file = './params/cur_param.json'
    folding_config_file = './folding_config.json'
    write_folding_config(cur_param_file, folding_config_file)

    # ./build_dataflow.sh will generate cpp source files based on folding_config.json
    # Default output dir: ./_finn_gen_dir/build_dir/
    os.system('source ./build_dataflow.sh')


    # Based on the generated source files in ./_finn_gen_dir/build_dir/,
    # create wrapper source files in ./operators/
    op_dir = './operators'

    #####################################
    ## Extract param from cur_par.json ##
    #####################################
    with open('./params/cur_param.json', 'r') as infile:
        cur_param_dict = json.load(infile)

    # Extract param from cur_param_dict
    # Nothing to do for this benchmark


    ###########################################
    ## Generate src files based on cur param ##
    ###########################################

    # cpp code gen
    func_name_list = []
    ops_to_compile_list = []
    filedata_dict = {}

    src_dir = "./_finn_gen_dir/src/"
    build_dir = "./_finn_gen_dir/build_dir/"
    prefix_dict = {"thr_batch" : "Thresholding_Batch_",
                   "str_dwc" : "StreamingDataWidthConverter_Batch_",
                   "conv" : "ConvolutionInputGenerator_",
                   "mva" : "MatrixVectorActivation_",
                   "str_mp_batch" : "StreamingMaxPool_Batch_",
                   "lab_sel" : "LabelSelect_Batch_"}
    thr_batch_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["thr_batch"])]
    str_dwc_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["str_dwc"])]
    conv_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["conv"])]
    mva_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["mva"])]
    str_mp_batch_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["str_mp_batch"])]
    lab_sel_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith('LabelSelect_Batch_')]
    # print(thr_batch_dirs)
    # print(str_dwc_dirs)
    # print(conv_dirs)
    # print(mva_dirs)
    # print(str_mp_batch_dirs)
    # print(lab_sel_dirs)

    # Write to intermediate files to src_dir
    post_process("thr_batch", thr_batch_dirs, src_dir)
    post_process("str_dwc", str_dwc_dirs, src_dir)
    post_process("conv", conv_dirs, src_dir)
    post_process("mva", mva_dirs, src_dir)
    post_process("str_mp_batch", str_mp_batch_dirs, src_dir)
    post_process("lab_sel", lab_sel_dirs, src_dir)
    os.system('cp ' + src_dir + '*.h '  + op_dir) # weight files

    # Note that str_dwc is always optional, depending on the stream width
    # layer_0_0:    thr_batch - str_dwc - conv 
    # layer_0_1:    str_dwc - mva 
    # layer_1_0:    str_dwc - conv 
    # layer_1_1:    str_dwc - mva - str_dwc - str_mp_batch
    # layer_2_0:    str_dwc - conv 
    # layer_2_1:    str_dwc - mva 
    # layer_3_0:    str_dwc - conv 
    # layer_3_1:    str_dwc - mva - str_dwc - str_mp_batch
    # layer_4_0:    str_dwc - conv 
    # layer_4_1:    str_dwc - mva 
    # layer_5_0:    str_dwc - conv 
    # layer_5_1:    str_dwc - mva 
    # layer_last_0: str_dwc - mva 
    # layer_last_1: str_dwc - mva 
    # layer_last_2: mva - lab_sel

    # func_name, filedata = gen_data_transfer_func()
    # func_name_list.append(func_name)
    # func_name, filedata_header = gen_data_transfer_header()
    # filedata_dict[func_name] = (filedata, filedata_header)
    # if needs_write_param(func_name, filedata):
    #     ops_to_compile_list.append(func_name)

    # Network starts
    count_str_dwc = 0
    layer_num, layer_index = 0, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_0_0(src_dir, count_str_dwc, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '0_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 0, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, '0')
    filedata = replace_idx(filedata, base_idx = '0_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 1, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '1_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 1, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva_mp(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, 0, '1')
    filedata = replace_idx(filedata, base_idx = '1_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 2, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '2_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 2, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, '2')
    filedata = replace_idx(filedata, base_idx = '2_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 3, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '3_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 3, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva_mp(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, 1, '3')
    filedata = replace_idx(filedata, base_idx = '3_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 4, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '4_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 4, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, '4')
    filedata = replace_idx(filedata, base_idx = '4_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 5, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_conv(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index)
    filedata = replace_idx(filedata, base_idx = '5_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 5, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, '5')
    filedata = replace_idx(filedata, base_idx = '5_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 6, 0
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, 'last')
    filedata = replace_idx(filedata, base_idx = '6_0')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 7, 1
    count_str_dwc, prev_out_width, func_name, filedata, filedata_header = gen_layer_mva(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, 'last')
    filedata = replace_idx(filedata, base_idx = '7_1')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    layer_num, layer_index = 8, 2
    _, _, func_name, filedata, filedata_header = gen_layer_last(src_dir, count_str_dwc, prev_out_width, layer_num, layer_index, 'last')
    filedata = replace_idx(filedata, base_idx = '8_2')
    func_name_list.append(func_name)
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    # Network ends

    # func_name, filedata = gen_out_data_collect_func()
    # func_name_list.append(func_name)
    # func_name, filedata_header = gen_out_data_collect_header()
    # filedata_dict[func_name] = (filedata, filedata_header)
    # if needs_write_param(func_name, filedata):
    #     ops_to_compile_list.append(func_name)

    print()

    #############################################
    ## Update cur_param.json for new operators ##
    #############################################
    # Nothing to do for this benchmark because no new operator is generated

    #################################################
    ## Update application graph (top_no_merge.cpp) ##
    #################################################
    # Doesn't change for this benchmark
    top_str_list = ['layer_0_0(Input_1, layer_0_0_OUT_1);',
                    'layer_0_1(layer_0_0_OUT_1, layer_0_1_OUT_1);',
                    'layer_1_0(layer_0_1_OUT_1, layer_1_0_OUT_1);',
                    'layer_1_1(layer_1_0_OUT_1, layer_1_1_OUT_1);',
                    'layer_2_0(layer_1_1_OUT_1, layer_2_0_OUT_1);',
                    'layer_2_1(layer_2_0_OUT_1, layer_2_1_OUT_1);',
                    'layer_3_0(layer_2_1_OUT_1, layer_3_0_OUT_1);',
                    'layer_3_1(layer_3_0_OUT_1, layer_3_1_OUT_1);',
                    'layer_4_0(layer_3_1_OUT_1, layer_4_0_OUT_1);',
                    'layer_4_1(layer_4_0_OUT_1, layer_4_1_OUT_1);',
                    'layer_5_0(layer_4_1_OUT_1, layer_5_0_OUT_1);',
                    'layer_5_1(layer_5_0_OUT_1, layer_5_1_OUT_1);',
                    'layer_last_0(layer_5_1_OUT_1, layer_last_0_OUT_1);',
                    'layer_last_1(layer_last_0_OUT_1, layer_last_1_OUT_1);',
                    'layer_last_2(layer_last_1_OUT_1, Output_1);']
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


    # Modify typedefs.h
    # Nothing to do


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

    #################################
    ## Remove old src files if any ##
    #################################
    # cpp_file_list = [x for x in os.listdir('./operators/') if x.endswith('.cpp')]
    # for cpp_file in cpp_file_list:
    #     func_name = cpp_file.split('.')[0]
    #     if func_name not in post_merging_func_name_list:
    #         os.system('rm ./operators/' + func_name + '.cpp')
    #         os.system('rm ./operators/' + func_name + '.h')