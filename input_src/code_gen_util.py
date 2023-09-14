import json, math, os
import argparse
import re
from collections import Counter


##################
## Common field ##
##################

# Helper functions stolen from runtime.py
def return_operator_io_argument_dict_local(operator_list, benchmark):
    # operator_list = operators.split()
    operator_arg_dict = {}
    for operator in operator_list:
        with open('./operators/'+operator+'.h', 'r') as infile:
            file_list = infile.readlines()
        # file_list = self.shell.file_to_list()
        arguments_list = [] 
        def_valid = False # Ture if function definition begins
        def_str = ''
        for line in file_list:
            if '(' in line: def_valid = True
            if def_valid: 
                line_str=re.sub('\s+', '', line)
                line_str=re.sub('\t+', '', line_str)
                def_str=def_str+line_str
            if ')' in line: def_valid = False

        # a list for the stream arguments functions
        arg_str_list = def_str.split(',')
        for arg_str in arg_str_list:
            input_str_list = re.findall(r"Input_\d+", arg_str)
            output_str_list = re.findall(r"Output_\d+", arg_str)
            input_str_list.extend(output_str_list)
            io_str = input_str_list
            arguments_list.append(io_str[0])

        operator_arg_dict[operator] = arguments_list
    return operator_arg_dict 

# find all the operators instantiation in the top function
def return_operator_inst_dict_local(operator_list, benchmark):
    # operator_list = operators.split()
    operator_var_dict = {}
    with open('./host/top_no_merge.cpp', 'r') as infile:
        file_list = infile.readlines()

    for operator in operator_list:
        arguments_list = [] 

        # 1 when detect the start of operation instantiation
        # 2 when detect the end of operation instantiation
        inst_cnt = 0 
        inst_str = ''
        for line in file_list:
            if operator+'(' in line: inst_cnt = inst_cnt + 1
            if inst_cnt == 1: 
                line_str=re.sub('\s+', '', line)
                line_str=re.sub('\t+', '', line_str)
                line_str=re.sub('//.*', '', line_str)
                inst_str=inst_str+line_str
            if (')' in line) and inst_cnt == 1: inst_cnt = 2
        inst_str = inst_str.replace(operator+'(','')
        inst_str = inst_str.replace(');','')
        var_str_list = inst_str.split(',')
        operator_var_dict[operator] = var_str_list
    
    return operator_var_dict 
 
def return_operator_connect_list_local(operator_arg_dict, operator_var_dict):
    connection_list = []
    for key_a in operator_var_dict:
        operator = key_a
        # src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
        with open('./operators/'+operator+'.h', 'r') as infile:
            src_list = infile.readlines()

        for i_a, var_value_a in enumerate(operator_var_dict[key_a]):
            if var_value_a == 'Input_1': 
                tmp_str='DMA.Output_1->'+key_a+'.Input_1' 
                connection_list.append(tmp_str)
            if var_value_a == 'Input_2': 
                tmp_str='DMA2.Output_1->'+key_a+'.Input_1' 
                connection_list.append(tmp_str)
            if var_value_a == 'Output_1': 
                tmp_str=key_a+'.'+operator_arg_dict[key_a][i_a] + '->'+'DMA.Input_1' # not necessarily Output_1
                # tmp_str=key_a+'.Output_1->'+'DMA.Input_1'
                connection_list.append(tmp_str)
            for key_b in operator_var_dict:
                for i_b, var_value_b in enumerate(operator_var_dict[key_b]):
                    if var_value_a==var_value_b and key_a!=key_b:
                        if 'Input' in operator_arg_dict[key_a][i_a]:
                            tmp_str = key_b+'.'+operator_arg_dict[key_b][i_b]+'->'+key_a+'.'+operator_arg_dict[key_a][i_a]
                        else:
                            tmp_str = key_a+'.'+operator_arg_dict[key_a][i_a]+'->'+key_b+'.'+operator_arg_dict[key_b][i_b]
                        connection_list.append(tmp_str)

    connection_list = set(connection_list)
    return connection_list



# e.g.  e.g. {'zculling_bot': {0: (Input, 32),
#                              1: (Input, 32),
#                              2: (Output, 32)}, ...
def return_operator_io_type_and_width(operator_list, filedata_dict):
    # operator_list = operators.split()
    # operator_io_type_and_width_dict = {}
    # for operator in operator_list:
    #     io_type_and_width_dict = {}
    #     with open('./operators/'+operator+'.h', 'r') as infile:
    #         file_list = infile.readlines()
    #     index = 0
    #     for line in file_list:
    #         if 'Input_' in line or 'Output_' in line:
    #             if 'Input_' in line:
    #                 io_type = 'Input'
    #             else:
    #                 io_type = 'Output'
    #             ap_uint_str = re.findall(r"ap_uint\<\d+\>", line)[0]
    #             # print(ap_uint_str)
    #             width = int(ap_uint_str.split('<')[1].split('>')[0])
    #             io_type_and_width_dict[index] = (io_type, width)
    #             index += 1
    #     operator_io_type_and_width_dict[operator] = io_type_and_width_dict
    operator_io_type_and_width_dict = {}
    for operator in operator_list:
        io_type_and_width_dict = {}
        filedata, filedata_header = filedata_dict[operator]
        index = 0
        lines = filedata_header.split('\n')
        for line in lines:
            if 'Input_' in line or 'Output_' in line:
                if 'Input_' in line:
                    io_type = 'Input'
                else:
                    io_type = 'Output'
                ap_uint_str = re.findall(r"ap_uint\<\d+\>", line)[0]
                # print(ap_uint_str)
                width = int(ap_uint_str.split('<')[1].split('>')[0])
                io_type_and_width_dict[index] = (io_type, width)
                index += 1
        operator_io_type_and_width_dict[operator] = io_type_and_width_dict

    return operator_io_type_and_width_dict 

# Determine whether we need to write new src code
def needs_write_param(func_name, filedata):
    with open('./params/cur_param.json', 'r') as infile:
        cur_param_dict = json.load(infile)

    # 1) if new operator
    if not os.path.isfile('./operators/' + func_name + '.cpp') or func_name not in cur_param_dict: 
        print('NEEDS WRITE: new operator ' + func_name)
        return True
    else:
        # # 2) if function contents changed (filedata)
        # with open('./operators/' + func_name + '.cpp', 'r') as infile:
        #     prev_filedata = infile.read()
        #     # print(filedata)
        #     # print(prev_filedata)
        #     if filedata != prev_filedata:
        #         print('NEEDS WRITE: ' + func_name + ' file contents changed')
        #         # print(filedata_header)
        #         # print(prev_filedata_header)
        #         return True

        if os.path.isfile('./params/prev_param.json'):
            with open('./params/prev_param.json', 'r') as infile:
                prev_param_dict = json.load(infile)

            # 3) if param/kernel_clk/num_leaf_interface changed
            for param in cur_param_dict[func_name].keys():
                # if param != "num_leaf_interface" and param != "merged_to_try":
                if param != "merged_to_try":
                    if cur_param_dict[func_name][param] != prev_param_dict[func_name][param]:
                        print('NEEDS WRITE: ' + param + ' changed for ' + func_name)
                        return True

        return False

def needs_write_filedata(func_name, filedata, cur_param_dict):
    if not os.path.isfile('./operators/' + func_name + '.cpp') or func_name not in cur_param_dict: 
        print('NEEDS WRITE: new operator ' + func_name)
        return True
    else:
        # 2) if function contents changed (filedata)
        with open('./operators/' + func_name + '.cpp', 'r') as infile:
            prev_filedata = infile.read()
            # print(filedata)
            # print(prev_filedata)
            if filedata != prev_filedata:
                print('NEEDS WRITE: ' + func_name + ' file contents changed')
                # print(filedata_header)
                # print(prev_filedata_header)
                return True
    return False


# E.g.: [[A,B],[C]] => [A,B,C]
def get_flat_list(nested_list):
    flat_list = []
    for sublist in nested_list:
        for op in sublist:
            flat_list.append(op)
    return flat_list

# E.g.: A->B->  D
#        ->C->
#       Returns [[D],[B,C],[A]]
def sorted_op_list_backward(operator_list, connection_list):
    # List of operators, starting from backward
    sorted_backward_op_list = []
    for connection in connection_list:
        if 'DMA.Input_' in connection:
            start_op = connection.split('->')[0].split('.')[0]

    sorted_backward_op_list.append([start_op])
    for i in range(len(operator_list)-1):
        sublist = sorted_backward_op_list[-1]
        flat_list = get_flat_list(sorted_backward_op_list)
        new_sublist = [] # list of operators
        for op in sublist:
            for connection in connection_list:
                if op + '.Input_' in connection:
                    sender_op = connection.split('->')[0].split('.')[0]
                    if sender_op not in flat_list and sender_op not in new_sublist:
                        new_sublist.append(sender_op)
        sorted_backward_op_list.append(sorted(new_sublist))

        flat_list = get_flat_list(sorted_backward_op_list)
        if sorted(flat_list) == sorted(operator_list):
            break
    return sorted_backward_op_list

# Based on 'merged_to' or 'merged_to_try', it creates "clusters" of operators (independent_op_list). 
# E.g.: [[A,F,G],[X,Y],C,D] when A,F,G are merged and X,Y are merged.
def divide_ops(cur_param_dict, ops_to_compile_list):
    independent_op_list = []
    operator_list = list(cur_param_dict.keys())
    operator_list.remove("metric")
    # When multiple clusters are merged
    represent_op_list = []
    for func_name in operator_list:
        if 'merged_to' in cur_param_dict[func_name].keys():
            if cur_param_dict[func_name]['merged_to'] not in represent_op_list:
                represent_op_list.append(cur_param_dict[func_name]['merged_to'])
    for represent_op in represent_op_list:
        if 'merged_to_try' in cur_param_dict[represent_op].keys():
            new_represent_op = cur_param_dict[represent_op]['merged_to_try']
            for func_name in operator_list:
                if 'merged_to' in cur_param_dict[func_name].keys():
                    if cur_param_dict[func_name]['merged_to'] == represent_op:
                        del cur_param_dict[func_name]['merged_to']
                        cur_param_dict[func_name]['merged_to_try'] = new_represent_op

    for func_name in operator_list:
        # Already merged
        if 'merged_to' in cur_param_dict[func_name].keys():
            receiver_op = cur_param_dict[func_name]['merged_to']
            found = False
            for sub_list in independent_op_list:
                if receiver_op in sub_list:
                    found = True
                    sub_list.append(func_name)
                elif func_name in sub_list:
                    found = True
                    sub_list.append(receiver_op)
            if not found:
                independent_op_list.append([func_name, receiver_op])
        elif 'merged_to_try' in cur_param_dict[func_name].keys():
            receiver_op = cur_param_dict[func_name]['merged_to_try']
            # Let's merge!
            if func_name not in ops_to_compile_list and receiver_op not in ops_to_compile_list:
                found = False
                for sub_list in independent_op_list:
                    if receiver_op in sub_list:
                        found = True
                        print(func_name)
                        del cur_param_dict[func_name]['merged_to_try']
                        cur_param_dict[func_name]['merged_to'] = receiver_op
                        sub_list.append(func_name)
                    elif func_name in sub_list:
                        found = True
                        print(func_name)
                        del cur_param_dict[func_name]['merged_to_try']
                        cur_param_dict[func_name]['merged_to'] = receiver_op
                        sub_list.append(receiver_op)
                if not found:
                    del cur_param_dict[func_name]['merged_to_try']
                    cur_param_dict[func_name]['merged_to'] = receiver_op
                    independent_op_list.append([func_name, receiver_op])
            # Can't merge this time, TODO: outdated
            else: 
                del cur_param_dict[func_name]['merged_to_try']
                found = False
                for sub_list in independent_op_list:
                    if func_name in sub_list:
                        found = True
                if not found:
                    independent_op_list.append([func_name])
        else:
            found = False
            for sub_list in independent_op_list:
                if func_name in sub_list:
                    found = True
            if not found:
                independent_op_list.append([func_name])

    # Reflect the represent_op's kernel_clk to all children ops
    for func_name in operator_list:
        if 'merged_to' in cur_param_dict[func_name].keys():
            represent_op = cur_param_dict[func_name]['merged_to']
            cur_param_dict[func_name]['kernel_clk'] = cur_param_dict[represent_op]['kernel_clk']

    return independent_op_list, cur_param_dict


# cur_param_dict, ops_to_compile_list are updated
# Does followings:
#   - Divide ops with cur_param_dict's "merged_to" param and "merged_to_try" param
#   - Assign representative operator to each group (the one with the last in the graph)
#   - Write cpp codes for operators that are not merged with others
#   - Write cpp codes for operators that are merged with others, the top level is representative op
#   - Returns top_str_dict (used to write graph file, top.cpp)
#             e.g. {('flow_calc', 'tensor_weight_x_i1', 'tensor_weight_y_i1'): 'flow_calc(outer_product_out_1,flow_calc_1, flow_calc_2);\n'}
def perform_merging(operator_list, cur_param_dict, ops_to_compile_list, filedata_dict):
    top_str_dict = {}

    is_merged_to_exist = False
    for func_name in cur_param_dict:
        if func_name != 'metric':
            if 'merged_to' in cur_param_dict[func_name] or 'merged_to_try' in cur_param_dict[func_name]:
                is_merged_to_exist = True

    # No 'merged_to' or 'merged_to_try' because NoC bottleneck does not exist
    if not is_merged_to_exist:
        # Write operators that are not merged with other ops
        for func_name in operator_list:
            filedata, filedata_header = filedata_dict[func_name]
            if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata, cur_param_dict):
                with open('./operators/' + func_name + '.cpp', 'w') as outfile:
                    outfile.write(filedata)
                with open('./operators/' + func_name + '.h', 'w') as outfile:
                    outfile.write(filedata_header)
                if func_name not in ops_to_compile_list:
                    ops_to_compile_list.append(func_name)
        return top_str_dict

    else:
        operator_arg_dict = return_operator_io_argument_dict_local(operator_list, None)
        operator_var_dict = return_operator_inst_dict_local(operator_list, None)
        connection_list = return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
        # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
        # print(connection_list)
        sorted_backward_op_list = sorted_op_list_backward(operator_list, connection_list)
        # print(sorted_backward_op_list)
        sorted_forward_op_list = sorted_backward_op_list[::-1]

        independent_op_list, cur_param_dict = divide_ops(cur_param_dict, ops_to_compile_list)
        # print(independent_op_list)

        independent_op_dict = {} # key is list of merged ops, item is representative op
        for merged_ops in independent_op_list:
            found = False
            for op_list in sorted_backward_op_list:
                if not found:
                    for op in op_list:
                        if op in merged_ops:
                            represent_op = op
                            found = True
                            independent_op_dict[tuple(merged_ops)] = represent_op
                            break
        # print(independent_op_dict)

        with open('./host/top_no_merge.cpp', 'r') as infile:
            lines = infile.readlines()
        non_merged_ops = []
        merged_ops = []
        for op_tup, represent_op in independent_op_dict.items():
            inst_lines = []
            if len(op_tup) !=1:
                for op in op_tup:
                    merged_ops.append(op)
                    for line in lines:
                        if op+'(' in line:
                            inst_lines.append(line)
            else:
                non_merged_ops.append(op_tup[0])
            independent_op_dict[op_tup] = (represent_op, inst_lines)

        # # Write operators that are merged with other ops, not used in compile though
        # for func_name in merged_ops:
        #     filedata, filedata_header = filedata_dict[func_name]
        #     if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata, cur_param_dict):
        #         with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
        #             outfile.write(filedata)
        #         with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
        #             outfile.write(filedata_header)
        #         # if func_name not in ops_to_compile_list:
        #         #     ops_to_compile_list.append(func_name)

        # Write operators that are not merged with other ops
        for func_name in non_merged_ops:
            del independent_op_dict[tuple([func_name])]
            filedata, filedata_header = filedata_dict[func_name]
            if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata, cur_param_dict):
                with open('./operators/' + func_name + '.cpp', 'w') as outfile:
                    outfile.write(filedata)
                with open('./operators/' + func_name + '.h', 'w') as outfile:
                    outfile.write(filedata_header)
                if func_name not in ops_to_compile_list:
                    ops_to_compile_list.append(func_name)

        # Write operators that are merged with other ops
        # print("independent_op_dict")
        # print(independent_op_dict)
        for op_tup in independent_op_dict:
            represent_op, inst_lines = independent_op_dict[op_tup]

            # Update "merged_to" in cur_param_dict
            for func_name in op_tup:
                cur_param_dict[func_name]['merged_to'] = represent_op
            if 'merged_to' in cur_param_dict[represent_op]: # like tensor_weight_y_i1...
                del cur_param_dict[represent_op]['merged_to']

            # Write operators that are merged with other ops, not used in compile though
            for func_name in op_tup:
                if func_name != represent_op:
                    filedata, filedata_header = filedata_dict[func_name]
                    if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata, cur_param_dict):
                        with open('./operators/' + func_name + '.cpp', 'w') as outfile:
                            outfile.write(filedata)
                        with open('./operators/' + func_name + '.h', 'w') as outfile:
                            outfile.write(filedata_header)

            # From here, write merged operator
            stream_list = []
            # print()
            # print("inst_lines:")
            # print(inst_lines)
            for line in inst_lines:
                streams = line.split('(')[1].split(')')[0].replace(' ','').split(',')
                stream_list += streams

            # print(stream_list)
            counter = Counter(stream_list)
            # print(counter)

            io_stream_list = []
            non_io_stream_list = []
            for stream in counter:
                if counter[stream] == 1:
                    io_stream_list.append(stream)
                else:
                    non_io_stream_list.append(stream) # Counter val for internal stream is 2
            # print(io_stream_list)
            # print(non_io_stream_list)

            op_io_type_and_width_dict = return_operator_io_type_and_width(operator_list, filedata_dict)
            # print("op_io_type_and_width_dict:")
            # print(op_io_type_and_width_dict)
            #       e.g. {'zculling_bot': {0: (Input, 32),
            #                              1: (Input, 32),
            #                              2: (Output, 32)}, ...
            input_index = 1
            output_index = 1

            input_stream_dict = {}
            output_stream_dict = {}
            for io_straem in io_stream_list:
                for line in inst_lines:
                    if io_straem in line:
                        func_name = line.split('(')[0]
                        streams = line.split('(')[1].split(')')[0].replace(' ','').split(',')
                        stream_num = streams.index(io_straem)
                        # print(io_straem)
                        # print(stream_num)
                        if op_io_type_and_width_dict[func_name][stream_num][0] == 'Input':
                            width = op_io_type_and_width_dict[func_name][stream_num][1]
                            # print(io_straem, 'Input_' + str(input_index), str(width))
                            input_stream_dict[io_straem] = ('Input_' + str(input_index), width)
                            input_index += 1
                        elif op_io_type_and_width_dict[func_name][stream_num][0] == 'Output':
                            width = op_io_type_and_width_dict[func_name][stream_num][1]
                            # print(io_straem, 'Output_' + str(output_index), str(width))
                            output_stream_dict[io_straem] = ('Output_' + str(output_index), width)
                            output_index += 1

            non_io_stream_dict = {}
            for non_io_stream in non_io_stream_list:
                for line in inst_lines:
                    if non_io_stream in line:
                        func_name = line.split('(')[0]
                        streams = line.split('(')[1].split(')')[0].replace(' ','').split(',')
                        stream_num = streams.index(non_io_stream)
                        # print(io_straem)
                        # print(stream_num)

                        width = op_io_type_and_width_dict[func_name][stream_num][1]
                        non_io_stream_dict[non_io_stream] = (None, width)

            # Merge filedata
            filedata_rep_op, filedata_header_rep_op = filedata_dict[represent_op]
            filedata_rep_op = filedata_rep_op.replace('void ' + represent_op, 'static void ' + represent_op + '_body')
            # filedata_header_rep_op = filedata_header_rep_op.replace('void ' + represent_op, 'void ' + represent_op + '_body')
            # print(filedata_rep_op)

            for func_name in list(op_tup):
                if func_name != represent_op:
                    filedata, filedata_header = filedata_dict[func_name]
                    filedata = filedata.replace('void ' + func_name, 'static void ' + func_name)
                    filedata_rep_op += filedata

            # Add top level - io streams
            filedata_rep_op += '\n'
            filedata_rep_op += 'void ' + represent_op + '(\n'
            input_stream_dict = dict(sorted(input_stream_dict.items(), key=lambda x:int(x[1][0].split('_')[1])))
            # print("input_stream_dict:")
            # print(input_stream_dict)
            output_stream_dict = dict(sorted(output_stream_dict.items(), key=lambda x:int(x[1][0].split('_')[1])))
            # print("output_stream_dict:")
            # print(output_stream_dict)
            # print("non_io_stream_dict:")
            # print(non_io_stream_dict)

            top_str = represent_op + '('
            for stream in input_stream_dict:
                top_str += stream + ','
                io_name = input_stream_dict[stream][0] # e.g. Input_1
                width = input_stream_dict[stream][1]
                filedata_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ',\n'
            for i, stream in enumerate(output_stream_dict):
                io_name = output_stream_dict[stream][0] # e.g. Output_1
                width = output_stream_dict[stream][1]
                if i == len(output_stream_dict)-1:
                    top_str += stream + ');\n'
                    filedata_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ')\n'
                else:
                    top_str += stream + ', '
                    filedata_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ',\n'
            filedata_rep_op += '{\n'
            for stream in input_stream_dict:
                io_name = input_stream_dict[stream][0]
                filedata_rep_op += '#pragma HLS interface axis register port=' + str(io_name) + '\n'
            for stream in output_stream_dict:
                io_name = output_stream_dict[stream][0]
                filedata_rep_op += '#pragma HLS interface axis register port=' + str(io_name) + '\n'
            filedata_rep_op += '\n'


            top_str_dict[op_tup] = top_str

            # Add top level - non_io streams
            for non_io_stream in non_io_stream_dict:
                width = non_io_stream_dict[non_io_stream][1]
                filedata_rep_op += '    static hls::stream<ap_uint<' + str(width) + '>> ' + str(non_io_stream) + '("' + str(non_io_stream) + '_stream");\n'

            filedata_rep_op += '\n'
            filedata_rep_op += '#pragma HLS dataflow\n'


            # Modify stream name with Input_* and Output_* 
            new_inst_lines = []
            for line in inst_lines:
                for stream in input_stream_dict:
                    if stream in line:
                        io_name = input_stream_dict[stream][0]
                        line = line.replace(stream, io_name)
                for stream in output_stream_dict:
                    if stream in line:
                        io_name = output_stream_dict[stream][0]
                        line = line.replace(stream, io_name)
                if represent_op + '(' in line:
                    line = line.replace(represent_op + '(', represent_op + '_body' + '(')
                new_inst_lines.append(line)

            ordered_inst_lines = []
            # Reorder function instantiation
            print("sorted_forward_op_list:")
            print(sorted_forward_op_list)
            for sublist in sorted_forward_op_list: # Dataflow pragma requires correct order
                for op in sublist:
                    for line in new_inst_lines:
                        if line.startswith(op + '(') or line.startswith(op + '_body' + '('):
                            ordered_inst_lines.append(line)

            for line in ordered_inst_lines:
                filedata_rep_op += '    ' + line
            filedata_rep_op += '}\n'

            # filedata_header_rep_op
            filedata_header_rep_op = ''
            filedata_header_rep_op += 'void ' + represent_op + '(\n'
            for stream in input_stream_dict:
                io_name = input_stream_dict[stream][0] # e.g. Input_1
                width = input_stream_dict[stream][1]
                filedata_header_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ',\n'
            for i, stream in enumerate(output_stream_dict):
                io_name = output_stream_dict[stream][0] # e.g. Output_1
                width = output_stream_dict[stream][1]
                if i == len(output_stream_dict)-1:
                    filedata_header_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ');\n'
                else:
                    filedata_header_rep_op += '    hls::stream<ap_uint<' + str(width) + '>> &' + str(io_name) + ',\n'
            filedata_header_rep_op += '#pragma map_target = HW\n'


            if needs_write_param(represent_op, filedata_rep_op) or needs_write_filedata(represent_op, filedata_rep_op, cur_param_dict):
                with open('./operators/' + represent_op + '.cpp', 'w') as outfile:
                    outfile.write(filedata_rep_op)
                with open('./operators/' + represent_op + '.h', 'w') as outfile:
                    outfile.write(filedata_header_rep_op)
                if represent_op not in ops_to_compile_list:
                    ops_to_compile_list.append(represent_op)

            for op in op_tup:
                if op != represent_op and op in ops_to_compile_list:
                    ops_to_compile_list.remove(op)

        return top_str_dict


def merge_op_list():
    with open('./host/top.cpp', 'r') as infile:
        lines = infile.readlines()
    operator_list = []
    for line in lines:
        op_name = line.split('(')[0]
        operator_list.append(op_name)
    return operator_list