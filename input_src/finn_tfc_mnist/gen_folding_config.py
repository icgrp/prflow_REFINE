import json, re

def gen_orig_func_name(op_type):
    if op_type == 'thr_batch':
        return 'Thresholding_Batch'
    elif op_type == 'conv':
        return 'ConvolutionInputGenerator'
    elif op_type == 'mva':
        return 'MatrixVectorActivation'
    elif op_type == 'lab_sel':
        return 'LabelSelect_Batch'
    else:
        raise Exception('Invalid op_type')


def write_folding_config(cur_param_file, folding_config_file):

    folding_config_dict = {
        "Defaults": {},

        "Thresholding_Batch_0": {
            "PE": 8, # Fixed, should I?
            "ram_style": "distributed",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },

        "MatrixVectorActivation_0": {
            "PE": 1,
            "SIMD": 56, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },


        "MatrixVectorActivation_1": {
            "PE": 1,
            "SIMD": 64, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },

        "MatrixVectorActivation_2": {
            "PE": 1,
            "SIMD": 64, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },

        "MatrixVectorActivation_3": {
            "PE": 1,
            "SIMD": 64,  # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "StreamingMaxPool_Batch_1": {
            "PE": 1  # Fixed
        },

        "MatrixVectorActivation_4": {
            "PE": 1,
            "SIMD": 8, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },

        "LabelSelect_Batch_0": {
            "PE": 1
        }
    }

    with open(cur_param_file, 'r') as infile:
        cur_param_dict = json.load(infile)

    for op in cur_param_dict:
        if op != 'metric':
            params = cur_param_dict[op]
            for param in params:
                if param.startswith('PE') or param.startswith('SIMD'): 
                    # print(param)
                    param_FINN = param.split('_')[0].replace('1','')
                    assert(len(re.findall('_\d+$',param)) == 1)
                    idx_str = re.findall('_\d+$',param)[0]
                    op_type = param.replace(param_FINN + '1_', '').replace(idx_str,'')
                    idx = int(idx_str.replace('_',''))
                    orig_func_name = gen_orig_func_name(op_type)
                    orig_func_name += '_' + str(idx)
                    pram_val = cur_param_dict[op][param]

                    # Update
                    folding_config_dict[orig_func_name][param_FINN] = pram_val


    with open(folding_config_file, 'w') as outfile:
        json.dump(folding_config_dict, outfile, indent=4)