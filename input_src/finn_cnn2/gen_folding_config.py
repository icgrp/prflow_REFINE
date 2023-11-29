import json

def gen_orig_func_name(op_type):
    if op_type == 'thr_batch':
        return 'Thresholding_Batch'
    elif op_type == 'conv':
        return 'ConvolutionInputGenerator'
    elif op_type == 'mva':
        return 'MatrixVectorActivation'
    else:
        raise Exception('Invalid op_type')


def write_folding_config(cur_param_file, folding_config_file):

    folding_config_dict = {
        "Defaults": {},

        "Thresholding_Batch_0": {
            "PE": 1, # Fixed
            "ram_style": "distributed",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "ConvolutionInputGenerator_0": {
            "SIMD": 3, # Fixed
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_0": {
            "PE": 1,
            "SIMD": 27, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },


        "ConvolutionInputGenerator_1": {
            "SIMD": 1,
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_1": {
            "PE": 1,
            "SIMD": 72, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "StreamingMaxPool_Batch_0": {
            "PE": 1 # Fixed
        },


        "ConvolutionInputGenerator_2": {
            "SIMD": 1,
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_2": {
            "PE": 1,
            "SIMD": 72, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },


        "ConvolutionInputGenerator_3": {
            "SIMD": 1,
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_3": {
            "PE": 1,
            "SIMD": 72,  # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "StreamingMaxPool_Batch_1": {
            "PE": 1  # Fixed
        },


        "ConvolutionInputGenerator_4": {
            "SIMD": 1, 
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_4": {
            "PE": 1,
            "SIMD": 96, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },


        "ConvolutionInputGenerator_5": {
            "SIMD": 1,
            "ram_style": "distributed"
        },
        "MatrixVectorActivation_5": {
            "PE": 1,
            "SIMD": 36, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },


        "MatrixVectorActivation_6": {
            "PE": 1,
            "SIMD": 4, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "MatrixVectorActivation_7": {
            "PE": 1,
            "SIMD": 8, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "MatrixVectorActivation_8": {
            "PE": 1,  # Fixed
            "SIMD": 1, # Fixed
            "ram_style": "auto",
            "resType": "lut",
            "mem_mode": "const",
            "runtime_writeable_weights": 0
        },
        "LabelSelect_Batch_0": {
            "PE": 1  # Fixed
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
                    op_type = param.split('_')[1]
                    idx = param.split('_')[2]
                    orig_func_name = gen_orig_func_name(op_type)
                    orig_func_name += '_' + str(idx)
                    pram_val = cur_param_dict[op][param]

                    # Update
                    folding_config_dict[orig_func_name][param_FINN] = pram_val


    with open(folding_config_file, 'w') as outfile:
        json.dump(folding_config_dict, outfile, indent=4)