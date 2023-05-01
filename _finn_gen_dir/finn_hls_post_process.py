# Below information should be pre-known
CNV_OUT_CH_POOL = [(64, False), (64, True), (128, False), (128, True), (256, False), (256, False)]
INTERMEDIATE_FC_FEATURES = [(256, 512), (512, 512)]
LAST_FC_IN_FEATURES = 512
LAST_FC_PER_OUT_CH_SCALING = False
POOL_SIZE = 2
KERNEL_SIZE = 3

import os


src_dir = "./src/"
dst_dir = src_dir + "operators/"
build_dir = "./build_dir/"
prefix_dict = {"thr_batch" : "Thresholding_Batch_",
               "str_dwc" : "StreamingDataWidthConverter_Batch_",
               "conv" : "ConvolutionInputGenerator_",
               "mva" : "MatrixVectorActivation_",
               "str_mp_batch" : "StreamingMaxPool_Batch_",
               "lab_sel" : "LabelSelect_Batch_"}
os.system('rm -rf ' + src_dir)
os.system('mkdir -p ' + dst_dir)
# print(os.listdir(build_dir))
thr_batch_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["thr_batch"])]
str_dwc_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["str_dwc"])]
conv_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["conv"])]
mva_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["mva"])]
str_mp_batch_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith(prefix_dict["str_mp_batch"])]
lab_sel_dirs = [build_dir + f for f in os.listdir(build_dir) if f.startswith('LabelSelect_Batch_')]



def replace_vars(line, def_list, op_type, idx):
    for def_var in def_list:
        line = line.replace(def_var, def_var + "_" + op_type + "_" + idx)
    return line


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





# layer_0:    thr_batch - str_dwc - conv - str_dwc - mva 
def create_wrapper_layer_0(src_dir, count_str_dwc, layer_num):

    thr_batch_in = get_input_stream_width(src_dir + 'thr_batch_' + str(layer_num) + '.cpp')
    thr_batch_out = get_output_stream_width(src_dir + 'thr_batch_' + str(layer_num) + '.cpp')

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')


    new_filedata_include = ['#include "../host/typedefs.h"\n']
    new_filedata = []

    # thr_batch
    with open(src_dir + 'thr_batch_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if thr_batch_out != conv_in:
        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1

    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if conv_out != mva_in:
        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1

    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    layer_filedata = [
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<8> > & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '> > & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    layer_filedata.append('    static hls::stream<ap_uint<' + str(thr_batch_out) + '>> out_thr_batch("out_thr_batch");\n')
    if thr_batch_out != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_out) + '>> out_conv("out_conv");\n')
    if conv_out != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_1("out_str_dwc_1");\n')
    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')
    layer_filedata.append('    thr_batch_' + str(layer_num) + '(Input_1, out_thr_batch);\n')
    if thr_batch_out != conv_in:
        layer_filedata.append('    str_dwc_0(out_thr_batch, out_str_dwc_0);\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_0, out_conv);\n')
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(out_thr_batch, out_conv);\n')
    if conv_out != mva_in:
        layer_filedata.append('    str_dwc_1(out_conv, out_str_dwc_1);\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_1, Output_1);\n')
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(out_conv, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')


    new_filedata_include = list(set(new_filedata_include))
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')
    new_filedata = new_filedata_include + new_filedata + layer_filedata

    with open(src_dir + 'layer_' + str(layer_num) + '.cpp' , 'w') as outfile:
        outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<8>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    with open(src_dir + 'layer_' + str(layer_num) + '.h' , 'w') as outfile:
        outfile.writelines(layer_h_filedata)

    return count_str_dwc, mva_out



# layer_1:                str_dwc - conv - str_dwc - mva - str_dwc - str_mp_batch
def create_wrapper_layer_1(src_dir, count_str_dwc, prev_out_width, layer_num):

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    str_mp_batch_in = get_input_stream_width(src_dir + "str_mp_batch_0.cpp")
    str_mp_batch_out = get_output_stream_width(src_dir + "str_mp_batch_0.cpp")


    layer_filedata = [
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_out) + '>> out_conv("out_conv");\n')
    if conv_out != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_1("out_str_dwc_1");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_out) + '>> out_mva("out_mva");\n')
    if mva_out != str_mp_batch_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(str_mp_batch_in) + '>> out_str_dwc_2("out_str_dwc_2");\n')
    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')


    new_filedata_include = []
    new_filedata = []


    if prev_out_width != conv_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_0);\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_0, out_conv);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(Input, out_conv);\n')


    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if conv_out != mva_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_conv, out_str_dwc_1);\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_1, out_mva);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(out_conv, out_mva);\n')


    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if mva_out != str_mp_batch_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_mva, out_str_dwc_2);\n')
        layer_filedata.append('    str_mp_batch_0(out_str_dwc_2, Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    str_mp_batch_0(out_mva, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')

    # str_mp_batch
    with open(src_dir + 'str_mp_batch_0.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')



    new_filedata_include = list(set(new_filedata_include))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"'] + new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    with open(src_dir + 'layer_' + str(layer_num) + '.cpp' , 'w') as outfile:
        outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    with open(src_dir + 'layer_' + str(layer_num) + '.h' , 'w') as outfile:
        outfile.writelines(layer_h_filedata)

    return count_str_dwc, str_mp_batch_out


# layer_2:                str_dwc - conv - str_dwc - mva 
def create_wrapper_layer_2(src_dir, count_str_dwc, prev_out_width, layer_num):

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')



    layer_filedata = [
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_out) + '>> out_conv("out_conv");\n')
    if conv_out != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_1("out_str_dwc_1");\n')

    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')


    new_filedata_include = []
    new_filedata = []


    if prev_out_width != conv_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_0);\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_0, out_conv);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith("_thresh.h"):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(Input, out_conv);\n')


    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if conv_out != mva_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_conv, out_str_dwc_1);\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_1, Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(out_conv, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')

    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')



    new_filedata_include = list(set(new_filedata_include))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"'] + new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    with open(src_dir + 'layer_' + str(layer_num) + '.cpp' , 'w') as outfile:
        outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(mva_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    with open(src_dir + 'layer_' + str(layer_num) + '.h' , 'w') as outfile:
        outfile.writelines(layer_h_filedata)

    return count_str_dwc, mva_out


# layer_3:                str_dwc - conv - str_dwc - mva - str_dwc - str_mp_batch
def create_wrapper_layer_3(src_dir, count_str_dwc, prev_out_width, layer_num):

    conv_in = get_input_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')
    conv_out = get_output_stream_width(src_dir + 'conv_' + str(layer_num) + '.cpp')

    mva_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    str_mp_batch_in = get_input_stream_width(src_dir + "/str_mp_batch_1.cpp")
    str_mp_batch_out = get_output_stream_width(src_dir + "/str_mp_batch_1.cpp")


    layer_filedata = [
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != conv_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(conv_out) + '>> out_conv("out_conv");\n')
    if conv_out != mva_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_in) + '>> out_str_dwc_1("out_str_dwc_1");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_out) + '>> out_mva("out_mva");\n')
    if mva_out != str_mp_batch_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(str_mp_batch_in) + '>> out_str_dwc_2("out_str_dwc_2");\n')
    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')




    new_filedata_include = []
    new_filedata = []


    if prev_out_width != conv_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_0);\n')
        layer_filedata.append('    conv_' + str(layer_num) + '(out_str_dwc_0, out_conv);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    conv_' + str(layer_num) + '(Input, out_conv);\n')


    # conv
    with open(src_dir + 'conv_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if conv_out != mva_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_conv, out_str_dwc_1);\n')
        layer_filedata.append('    mva_' + str(layer_num) + '(out_str_dwc_1, out_mva);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num) + '(out_conv, out_mva);\n')


    # mva
    with open(src_dir + 'mva_' + str(layer_num) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')

    if mva_out != str_mp_batch_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_mva, out_str_dwc_2);\n')
        layer_filedata.append('    str_mp_batch_1(out_str_dwc_2, Output_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    str_mp_batch_0(out_mva, Output_1);\n')
    layer_filedata.append('\n')
    layer_filedata.append('}\n')

    # str_mp_batch
    with open(src_dir + 'str_mp_batch_1.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')


    new_filedata_include = list(set(new_filedata_include))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"'] + new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    with open(src_dir + 'layer_' + str(layer_num) + '.cpp' , 'w') as outfile:
        outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_' + str(layer_num) + ' (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<' + str(str_mp_batch_out) + '>> & Output_1\n',
        '        );\n',
        '#pragma map_target = HW\n']
    with open(src_dir + 'layer_' + str(layer_num) + '.h' , 'w') as outfile:
        outfile.writelines(layer_h_filedata)

    return count_str_dwc, str_mp_batch_out


# layer_last:             str_dwc - mva - str_dwc - mva - mva - lab_sel
def create_wrapper_layer_last(src_dir, count_str_dwc, prev_out_width, layer_num):

    mva_0_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')
    mva_0_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num) + '.cpp')

    layer_num_new = layer_num + 1
    mva_1_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num_new) + '.cpp')
    mva_1_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num_new) + '.cpp')

    layer_num_new = layer_num_new + 1
    mva_2_in = get_input_stream_width(src_dir + 'mva_' + str(layer_num_new) + '.cpp')
    mva_2_out = get_output_stream_width(src_dir + 'mva_' + str(layer_num_new) + '.cpp')


    layer_filedata = [
        'void layer_last (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<8>> & Output_1\n',
        '        )\n',
        '{\n',
        '#pragma HLS INTERFACE axis register port=Input_1\n',
        '#pragma HLS INTERFACE axis register port=Output_1\n',
        '\n']

    if prev_out_width != mva_0_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_0_in) + '>> out_str_dwc_0("out_str_dwc_0");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_0_out) + '>> out_mva_0("out_mva_0");\n')
    if mva_0_out != mva_1_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_1_in) + '>> out_str_dwc_1("out_str_dwc_1");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_1_out) + '>> out_mva_1("out_mva_1");\n')
    if mva_1_out != mva_2_in:
        layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_2_in) + '>> out_str_dwc_2("out_str_dwc_2");\n')
    layer_filedata.append('    static hls::stream<ap_uint<' + str(mva_2_out) + '>> out_mva_2("out_mva_2");\n')

    layer_filedata.append('\n')
    layer_filedata.append('#pragma HLS dataflow\n')
    # Let's assume that mva_2_out==1 and input width of labelselect is 1


    new_filedata_include = []
    new_filedata = []


    layer_num_new = layer_num
    if prev_out_width != mva_0_in:

        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(Input_1, out_str_dwc_0);\n')
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_str_dwc_0, out_mva_0);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num_new) + '(Input, out_mva_0);\n')

    # mva
    with open(src_dir + 'mva_' + str(layer_num_new) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')
    layer_num_new = layer_num_new + 1


    if mva_0_out != mva_1_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_mva_0, out_str_dwc_1);\n')
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_str_dwc_1, out_mva_1);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_mva_0, out_mva_1);\n')

    # mva
    with open(src_dir + 'mva_' + str(layer_num_new) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')
    layer_num_new = layer_num_new + 1


    if mva_1_out != mva_2_in:
        layer_filedata.append('    str_dwc_' + str(count_str_dwc) + '(out_mva_1, out_str_dwc_2);\n')
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_str_dwc_2, out_mva_2);\n')

        with open(src_dir + 'str_dwc_' + str(count_str_dwc) + '.cpp', 'r') as infile:
            filedata = infile.readlines()
            for line in filedata:
                if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                    line = line.replace('#include "', '#include "../host/finn-hlslib/')
                    new_filedata_include.append(line)
                else:
                    if not line.startswith("// includes"):
                        new_filedata.append(line)
            new_filedata.append('\n')
            new_filedata.append('// ------------------------------------------------------------------------\n')
            new_filedata.append('\n')
        count_str_dwc = count_str_dwc + 1
    else:
        layer_filedata.append('    mva_' + str(layer_num_new) + '(out_mva_1, out_mva_2);\n')
    # mva
    with open(src_dir + 'mva_' + str(layer_num_new) + '.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')


    # label_sel, assume that input width of label_sel is fixed to 16
    layer_filedata.append('    lab_sel_0(out_mva_2, Output_1);\n')
    with open(src_dir + 'lab_sel_0.cpp', 'r') as infile:
        filedata = infile.readlines()
        for line in filedata:
            if line.startswith("#include") and not line.endswith('_thresh.h"\n') and not line.endswith('_params.h"\n'):
                line = line.replace('#include "', '#include "../host/finn-hlslib/')
                new_filedata_include.append(line)
            else:
                if not line.startswith("// includes"):
                    new_filedata.append(line)
        new_filedata.append('\n')
        new_filedata.append('// ------------------------------------------------------------------------\n')
        new_filedata.append('\n')



    layer_filedata.append('\n')
    layer_filedata.append('}\n')


    new_filedata_include = list(set(new_filedata_include))
    new_filedata_include = ['#include "../host/typedefs.h"\n','#include "../host/finn-hlslib/bnn-library.h"'] + new_filedata_include
    new_filedata_include.append('\n')
    new_filedata_include.append('// ------------------------------------------------------------------------\n')
    new_filedata_include.append('\n')

    new_filedata = new_filedata_include + new_filedata + layer_filedata

    with open(src_dir + 'layer_last.cpp' , 'w') as outfile:
        outfile.writelines(new_filedata)

    layer_h_filedata = [
        '#include "../host/finn-hlslib/bnn-library.h"\n',
        '\n',
        'void layer_last (\n',
        '        hls::stream<ap_uint<' + str(prev_out_width) + '>> & Input_1,\n',
        '        hls::stream<ap_uint<8>> & Output_1\n', # fixed to 8
        '        );\n',
        '#pragma map_target = HW\n']
    with open(src_dir + 'layer_last.h' , 'w') as outfile:
        outfile.writelines(layer_h_filedata)

    return count_str_dwc, 8




# create_wrapper_layer_0(src_dir, 0)

print(thr_batch_dirs)
print(str_dwc_dirs)
print(conv_dirs)
print(mva_dirs)
print(str_mp_batch_dirs)
print(lab_sel_dirs)


post_process("thr_batch", thr_batch_dirs, src_dir)
post_process("str_dwc", str_dwc_dirs, src_dir)
post_process("conv", conv_dirs, src_dir)
post_process("mva", mva_dirs, src_dir)
post_process("str_mp_batch", str_mp_batch_dirs, src_dir)
post_process("lab_sel", lab_sel_dirs, src_dir)


# Note that str_dwc is always optional, depending on the stream width
# layer_0:    thr_batch - str_dwc - conv - str_dwc - mva 
# layer_1:                str_dwc - conv - str_dwc - mva - str_dwc - str_mp_batch
# layer_2:                str_dwc - conv - str_dwc - mva 
# layer_3:                str_dwc - conv - str_dwc - mva - str_dwc - str_mp_batch
# layer_4:                str_dwc - conv - str_dwc - mva 
# layer_5:                str_dwc - conv - str_dwc - mva 
# layer_last:             str_dwc - mva - str_dwc - mva - mva - lab_sel

# print(get_input_stream_width(src_dir + "/conv_0.cpp"))
count_str_dwc = 0
layer_num = 0
count_str_dwc, prev_out_width = create_wrapper_layer_0(src_dir, count_str_dwc, layer_num)
layer_num = 1
count_str_dwc, prev_out_width = create_wrapper_layer_1(src_dir, count_str_dwc, prev_out_width, layer_num)
layer_num = 2
count_str_dwc, prev_out_width = create_wrapper_layer_2(src_dir, count_str_dwc, prev_out_width, layer_num)
layer_num = 3
count_str_dwc, prev_out_width = create_wrapper_layer_3(src_dir, count_str_dwc, prev_out_width, layer_num)
layer_num = 4 # exactly same as layer_2
count_str_dwc, prev_out_width = create_wrapper_layer_2(src_dir, count_str_dwc, prev_out_width, layer_num)
layer_num = 5 # exactly same as layer_2
count_str_dwc, prev_out_width = create_wrapper_layer_2(src_dir, count_str_dwc, prev_out_width, layer_num)
layer_num = 6
count_str_dwc, _ = create_wrapper_layer_last(src_dir, count_str_dwc, prev_out_width, layer_num)

# cp necessary files, data_transfer.cpp and out_data_collect.cpp should be the same all the time 
os.system('cp ' + src_dir + '*.h '  + dst_dir)
os.system('cp ' + src_dir + 'layer_*.cpp '  + dst_dir)