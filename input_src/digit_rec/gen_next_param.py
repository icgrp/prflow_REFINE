import json, math, os
import argparse

# Based on the search space (params.json), update ./host/typedefs.h, ./operators/specs.json and cur_param.json.
# Generate ./operators/*.cpp if necessary => this file is benchmark-specific

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # args = parser.parse_args()
    # bottleneck = args.bottleneck

    # TODO: Create tuner

    par_factor = 20 # 20, 40, 60, 80
    k_val = 1 # 1, 3, 5, 7

    # Modify typedefs.h
    filedata = ''
    with open('./host/typedefs.h', 'r') as infile:
        lines = infile.readlines()
    for line in lines:
        if line.startswith('#define PAR_FACTOR '):
            line = '#define PAR_FACTOR ' + str(par_factor) + '\n'
        elif line.startswith('#define K_CONST '):
            line = '#define K_CONST ' + str(k_val) + '\n'
        filedata += line
    with open('./host/typedefs.h', 'w') as outfile:
        outfile.write(filedata)


    # unchanged operators
    # Nothing needs to be changed

    # For now, all run in 200 and num leaf interface is 1
    # spec_dict = {}
    # for func_name in func_name_list:
    #     spec_dict[func_name] = {"kernel_clk": 200, "num_leaf_interface": 1}
    # with open(op_dir + '/specs.json', 'w') as outfile:
    #     json.dump(spec_dict, outfile, sort_keys=True, indent=4)

    # top.cpp
    # Nothing needs to be changed

    
    # Check all the functions are instantiated in top.cpp
    # Nothing needs to be changed

