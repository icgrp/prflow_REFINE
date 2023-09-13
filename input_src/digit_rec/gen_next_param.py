import json, math, os
import argparse
import re
from collections import Counter


##################
## Common field ## => TODO: code refactor later
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

def needs_write_filedata(func_name, filedata):
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
            if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata):
                with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
                    outfile.write(filedata)
                with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
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
        #     if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata):
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
            if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata):
                with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
                    outfile.write(filedata)
                with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
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
                    if needs_write_param(func_name, filedata) or needs_write_filedata(func_name, filedata):
                        with open(op_dir + '/' + func_name + '.cpp', 'w') as outfile:
                            outfile.write(filedata)
                        with open(op_dir + '/' + func_name + '.h', 'w') as outfile:
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


            if needs_write_param(represent_op, filedata_rep_op) or needs_write_filedata(represent_op, filedata_rep_op):
                with open(op_dir + '/' + represent_op + '.cpp', 'w') as outfile:
                    outfile.write(filedata_rep_op)
                with open(op_dir + '/' + represent_op + '.h', 'w') as outfile:
                    outfile.write(filedata_header_rep_op)
                if represent_op not in ops_to_compile_list:
                    ops_to_compile_list.append(represent_op)

        return top_str_dict


def merge_op_list():
    with open('./host/top.cpp', 'r') as infile:
        lines = infile.readlines()
    operator_list = []
    for line in lines:
        op_name = line.split('(')[0]
        operator_list.append(op_name)
    return operator_list



########################
## Benchmark-specific ##
########################


def gen_update_knn_i1_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static int popcount(WholeDigitType x)')
    func_str_list.append('{')
    func_str_list.append('  // most straightforward implementation')
    func_str_list.append('  // actually not bad on FPGA')
    func_str_list.append('  int cnt = 0;')
    func_str_list.append('  for (int i = 0; i < 256; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('    cnt = cnt + x(i,i);')
    func_str_list.append('  }')
    func_str_list.append('  return cnt;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('static void update_knn( WholeDigitType test_inst, WholeDigitType train_inst, int min_distances[K_CONST] )')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=min_distances complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // Compute the difference using XOR')
    func_str_list.append('  WholeDigitType diff = test_inst ^ train_inst;')
    func_str_list.append('')
    func_str_list.append('  int dist = 0;')
    func_str_list.append('')
    func_str_list.append('  dist = popcount(diff);')
    func_str_list.append('')
    func_str_list.append('  int max_dist = 0;')
    func_str_list.append('  int max_dist_id = 0;')
    func_str_list.append('  int k = 0;')
    func_str_list.append('')
    func_str_list.append('  // Find the max distance')
    func_str_list.append('  FIND_MAX_DIST: for ( int k = 0; k < K_CONST; ++k )')
    func_str_list.append('  {')
    func_str_list.append('    if ( min_distances[k] > max_dist )')
    func_str_list.append('    {')
    func_str_list.append('      max_dist = min_distances[k];')
    func_str_list.append('      max_dist_id = k;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Replace the entry with the max distance')
    func_str_list.append('  if ( dist < max_dist )')
    func_str_list.append('    min_distances[max_dist_id] = dist;')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static void knn_vote_small( int knn_set[OP_SIZE * K_CONST],')
    func_str_list.append('                    int min_distance_list[K_CONST],')
    func_str_list.append('        int label_list[K_CONST],')
    func_str_list.append('        LabelType label_in)')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('  // final K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=min_distance_list complete dim=0')
    func_str_list.append('  // labels for the K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=label_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  int pos = 1000;')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // go through all the lanes')
    func_str_list.append('  // do an insertion sort to keep a sorted neighbor list')
    func_str_list.append('  LANES: for (int i = 0; i < OP_SIZE; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    INSERTION_SORT_OUTER: for (int j = 0; j < K_CONST; j ++ )')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline')
    func_str_list.append('      pos = 1000;')
    func_str_list.append('      INSERTION_SORT_INNER: for (int r = 0; r < K_CONST; r ++ )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        pos = ((knn_set[i*K_CONST+j] < min_distance_list[r]) && (pos > K_CONST)) ? r : pos;')
    func_str_list.append('      }')
    func_str_list.append('')
    func_str_list.append('      INSERT: for (int r = K_CONST ;r > 0; r -- )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        if(r-1 > pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = min_distance_list[r-2];')
    func_str_list.append('          label_list[r-1] = label_list[r-2];')
    func_str_list.append('        }')
    func_str_list.append('        else if (r-1 == pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = knn_set[i*K_CONST+j];')
    func_str_list.append('          label_list[r-1] = label_in;')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('#define NUM1 1')
    func_str_list.append('void update_knn_i1(hls::stream<ap_uint<512> > & Input_1,')
    func_str_list.append('  hls::stream<ap_uint<32> > & Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType training_set [NUM_TRAINING / NUM_OPS];')
    func_str_list.append('const int unroll_factor = OP_SIZE;')
    func_str_list.append('#pragma HLS array_partition variable=training_set block factor=unroll_factor dim=0')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType test_instance;')
    func_str_list.append('bit32 tmp;')
    func_str_list.append('')
    func_str_list.append('static int knn_set[K_CONST*OP_SIZE];')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('')
    func_str_list.append('static bit512 in_tmp;')
    func_str_list.append('')
    func_str_list.append('WholeDigitType data_temp;')
    func_str_list.append('static int index = 0;')
    func_str_list.append('')
    func_str_list.append('  if (index == 0)')
    func_str_list.append('  {')
    func_str_list.append('   //Store the local training set')
    func_str_list.append('   STORE_LOCAL: for(int i = 0; i < NUM_TRAINING / NUM_OPS / 2; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS pipeline')
    func_str_list.append('                in_tmp = Input_1.read();')
    func_str_list.append('  training_set[2*i  ](255, 224) =in_tmp(31,    0);')
    func_str_list.append('  training_set[2*i  ](223, 192) =in_tmp(63,   32);')
    func_str_list.append('  training_set[2*i  ](191, 160) =in_tmp(95,   64);')
    func_str_list.append('  training_set[2*i  ](159, 128) =in_tmp(127,  96);')
    func_str_list.append('  training_set[2*i  ](127,  96) =in_tmp(159, 128);')
    func_str_list.append('  training_set[2*i  ](95,   64) =in_tmp(191, 160);')
    func_str_list.append('  training_set[2*i  ](63,   32) =in_tmp(223, 192);')
    func_str_list.append('  training_set[2*i  ](31,    0) =in_tmp(255, 224);')
    func_str_list.append('  training_set[2*i+1](255, 224) =in_tmp(287, 256);')
    func_str_list.append('  training_set[2*i+1](223, 192) =in_tmp(319, 288);')
    func_str_list.append('  training_set[2*i+1](191, 160) =in_tmp(351, 320);')
    func_str_list.append('  training_set[2*i+1](159, 128) =in_tmp(383, 352);')
    func_str_list.append('  training_set[2*i+1](127,  96) =in_tmp(415, 384);')
    func_str_list.append('  training_set[2*i+1](95,   64) =in_tmp(447, 416);')
    func_str_list.append('  training_set[2*i+1](63,   32) =in_tmp(479, 448);')
    func_str_list.append('  training_set[2*i+1](31,    0) =in_tmp(511, 480);')
    func_str_list.append('        ')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   //Transit the training sets for other pages')
    func_str_list.append('   TRANSFER_LOOP: for(int i = 0; i < NUM_TRAINING / NUM_OPS * (NUM_OPS - NUM1) / 2; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS pipeline')
    func_str_list.append('                in_tmp = Input_1.read();')
    func_str_list.append('  tmp(31, 0) = in_tmp(31,    0); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(63,   32); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(95,   64); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(127,  96); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(159, 128); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(191, 160); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(223, 192); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(255, 224); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(287, 256); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(319, 288); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(351, 320); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(383, 352); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(415, 384); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(447, 416); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(479, 448); Output_1.write(tmp);')
    func_str_list.append('  tmp(31, 0) = in_tmp(511, 480); Output_1.write(tmp);')
    func_str_list.append('   }')
    func_str_list.append('   index = 1;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  if(index%2 == 1){')
    func_str_list.append('    in_tmp = Input_1.read();')
    func_str_list.append('    test_instance(255, 224) = in_tmp(31,    0);')
    func_str_list.append('    test_instance(223, 192) = in_tmp(63,   32);')
    func_str_list.append('    test_instance(191, 160) = in_tmp(95,   64);')
    func_str_list.append('    test_instance(159, 128) = in_tmp(127,  96);')
    func_str_list.append('    test_instance(127,  96) = in_tmp(159, 128);')
    func_str_list.append('    test_instance(95,   64) = in_tmp(191, 160);')
    func_str_list.append('    test_instance(63,   32) = in_tmp(223, 192);')
    func_str_list.append('    test_instance(31,    0) = in_tmp(255, 224);')
    func_str_list.append('    tmp(31,0) = test_instance(255, 224);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(223, 192);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(191, 160);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(159, 128);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(127,  96);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(95,   64);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(63,   32);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(31,    0);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('  }else{')
    func_str_list.append('    test_instance(255, 224) = in_tmp(287,  256);')
    func_str_list.append('    test_instance(223, 192) = in_tmp(319,  288);')
    func_str_list.append('    test_instance(191, 160) = in_tmp(351,  320);')
    func_str_list.append('    test_instance(159, 128) = in_tmp(383, 352);')
    func_str_list.append('    test_instance(127,  96) = in_tmp(415, 384);')
    func_str_list.append('    test_instance(95,   64) = in_tmp(447, 416);')
    func_str_list.append('    test_instance(63,   32) = in_tmp(479, 448);')
    func_str_list.append('    test_instance(31,    0) = in_tmp(511, 480);')
    func_str_list.append('    tmp(31,0) = test_instance(255, 224);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(223, 192);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(191, 160);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(159, 128);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(127,  96);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(95,   64);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(63,   32);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('    tmp(31,0) = test_instance(31,    0);')
    func_str_list.append('    Output_1.write(tmp);')
    func_str_list.append('  }')
    func_str_list.append('  ')
    func_str_list.append('')
    func_str_list.append('  int min_distance_list[K_CONST];')
    func_str_list.append('#pragma HLS array_partition variable=min_distance_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('  int label_list[K_CONST];')
    func_str_list.append('#pragma HLS array_partition variable=label_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  for(int i=0; i<K_CONST; i++)')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('   min_distance_list[i] = 256;')
    func_str_list.append('   label_list[i] = 0;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Initialize the knn set')
    func_str_list.append('   SET_KNN_SET: for ( int i = 0; i < K_CONST * OP_SIZE ; ++i )')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('     // Note that the max distance is 256')
    func_str_list.append('     knn_set[i] = 256;')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   TRAINING_LOOP : for ( int i = 0; i < NUM_TRAINING / PAR_FACTOR; ++i )')
    func_str_list.append('   {')
    func_str_list.append('       #pragma HLS pipeline')
    func_str_list.append('       LANES : for ( int j = 0; j < OP_SIZE; j++ )')
    func_str_list.append('       {')
    func_str_list.append('         #pragma HLS unroll')
    func_str_list.append('         WholeDigitType training_instance = training_set[j * NUM_TRAINING / PAR_FACTOR + i];')
    func_str_list.append('         update_knn( test_instance, training_instance, &knn_set[j * K_CONST] );')
    func_str_list.append('       }')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   //update min_distance_list and label_list according to the new knn_set')
    func_str_list.append('   LabelType label_in = 0;')
    func_str_list.append('   knn_vote_small(knn_set, min_distance_list, label_list, label_in);')
    func_str_list.append('')
    func_str_list.append('   bit128 output_tmp1, output_tmp2;')
    func_str_list.append('')
    func_str_list.append('   for(int i=0; i<K_CONST; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('    output_tmp1(i*32+31, i*32) = min_distance_list[i];')
    func_str_list.append('    output_tmp2(i*32+31, i*32) = label_list[i];')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   tmp(31,0) = output_tmp1(127,96);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(95, 64);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(63, 32);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(31,  0);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(127,96);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(95, 64);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(63, 32);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(31,  0);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  index++;')
    func_str_list.append('  return;')
    func_str_list.append('}')
    return 'update_knn_i1', "\n".join(func_str_list)

def gen_update_knn_i1_header():
    func_str_list = []
    func_str_list.append('void update_knn_i1(')
    func_str_list.append('    hls::stream<ap_uint<512>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'update_knn_i1', "\n".join(func_str_list)

def gen_update_knn_iN_func(N):
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static int popcount(WholeDigitType x)')
    func_str_list.append('{')
    func_str_list.append('  // most straightforward implementation')
    func_str_list.append('  // actually not bad on FPGA')
    func_str_list.append('  int cnt = 0;')
    func_str_list.append('  for (int i = 0; i < 256; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('    cnt = cnt + x(i, i);')
    func_str_list.append('  }')
    func_str_list.append('  return cnt;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('static void update_knn( WholeDigitType test_inst, WholeDigitType train_inst, int min_distances[K_CONST] )')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=min_distances complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // Compute the difference using XOR')
    func_str_list.append('  WholeDigitType diff = test_inst ^ train_inst;')
    func_str_list.append('')
    func_str_list.append('  int dist = 0;')
    func_str_list.append('')
    func_str_list.append('  dist = popcount(diff);')
    func_str_list.append('')
    func_str_list.append('  int max_dist = 0;')
    func_str_list.append('  int max_dist_id = 0;')
    func_str_list.append('  int k = 0;')
    func_str_list.append('')
    func_str_list.append('  // Find the max distance')
    func_str_list.append('  FIND_MAX_DIST: for ( int k = 0; k < K_CONST; ++k )')
    func_str_list.append('  {')
    func_str_list.append('    if ( min_distances[k] > max_dist )')
    func_str_list.append('    {')
    func_str_list.append('      max_dist = min_distances[k];')
    func_str_list.append('      max_dist_id = k;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Replace the entry with the max distance')
    func_str_list.append('  if ( dist < max_dist )')
    func_str_list.append('    min_distances[max_dist_id] = dist;')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static void knn_vote_small( int knn_set[OP_SIZE * K_CONST],')
    func_str_list.append('                    int min_distance_list[K_CONST],')
    func_str_list.append('        int label_list[K_CONST],')
    func_str_list.append('        LabelType label_in)')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('  // final K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=min_distance_list complete dim=0')
    func_str_list.append('  // labels for the K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=label_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  int pos = 1000;')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // go through all the lanes')
    func_str_list.append('  // do an insertion sort to keep a sorted neighbor list')
    func_str_list.append('  LANES: for (int i = 0; i < OP_SIZE; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    INSERTION_SORT_OUTER: for (int j = 0; j < K_CONST; j ++ )')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline')
    func_str_list.append('      pos = 1000;')
    func_str_list.append('      INSERTION_SORT_INNER: for (int r = 0; r < K_CONST; r ++ )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        pos = ((knn_set[i*K_CONST+j] < min_distance_list[r]) && (pos > K_CONST)) ? r : pos;')
    func_str_list.append('      }')
    func_str_list.append('')
    func_str_list.append('      INSERT: for (int r = K_CONST ;r > 0; r -- )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        if(r-1 > pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = min_distance_list[r-2];')
    func_str_list.append('          label_list[r-1] = label_list[r-2];')
    func_str_list.append('        }')
    func_str_list.append('        else if (r-1 == pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = knn_set[i*K_CONST+j];')
    func_str_list.append('          label_list[r-1] = label_in;')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('#define NUM' + str(N) + ' ' + str(N))
    func_str_list.append('void update_knn_i' + str(N) + '(hls::stream<ap_uint<32> > & Input_1, hls::stream<ap_uint<32> > & Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType training_set [NUM_TRAINING / NUM_OPS];')
    func_str_list.append('const int unroll_factor = OP_SIZE;')
    func_str_list.append('#pragma HLS array_partition variable=training_set block factor=unroll_factor dim=0')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType test_instance;')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static int knn_set[K_CONST*OP_SIZE];')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('')
    func_str_list.append('WholeDigitType data_temp;')
    func_str_list.append('static int index = 0;')
    func_str_list.append('bit32 tmp;')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  if (index == 0)')
    func_str_list.append('  {')
    func_str_list.append('   //Store the local training set')
    func_str_list.append('   STORE_LOCAL: for(int i = 0; i < NUM_TRAINING / NUM_OPS; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS pipeline')
    func_str_list.append('   training_set[i](255, 224) =Input_1.read();')
    func_str_list.append('   training_set[i](223, 192) =Input_1.read();')
    func_str_list.append('   training_set[i](191, 160) =Input_1.read();')
    func_str_list.append('   training_set[i](159, 128) =Input_1.read();')
    func_str_list.append('   training_set[i](127,  96) =Input_1.read();')
    func_str_list.append('   training_set[i](95,   64) =Input_1.read();')
    func_str_list.append('   training_set[i](63,   32) =Input_1.read();')
    func_str_list.append('   training_set[i](31,    0) =Input_1.read();')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   //Transit the training sets for other pages')
    func_str_list.append('   TRANSFER_LOOP: for(int i = 0; i < NUM_TRAINING / NUM_OPS * (NUM_OPS - NUM' + str(N) + '); i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS pipeline')
    func_str_list.append('   data_temp(255, 224) =Input_1.read();')
    func_str_list.append('   data_temp(223, 192) =Input_1.read();')
    func_str_list.append('   data_temp(191, 160) =Input_1.read();')
    func_str_list.append('   data_temp(159, 128) =Input_1.read();')
    func_str_list.append('   data_temp(127,  96) =Input_1.read();')
    func_str_list.append('   data_temp(95,   64) =Input_1.read();')
    func_str_list.append('   data_temp(63,   32) =Input_1.read();')
    func_str_list.append('   data_temp(31,    0) =Input_1.read();')
    func_str_list.append('   bit32 tmp;')
    func_str_list.append('   tmp(31, 0) = data_temp.range(255, 224);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(223, 192);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(191, 160);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(159, 128);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(127,  96);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(95,   64);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(63,   32);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31, 0) = data_temp.range(31,    0);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   index = 1;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  test_instance(255, 224) = Input_1.read();')
    func_str_list.append('  test_instance(223, 192) = Input_1.read();')
    func_str_list.append('  test_instance(191, 160) = Input_1.read();')
    func_str_list.append('  test_instance(159, 128) = Input_1.read();')
    func_str_list.append('  test_instance(127,  96) = Input_1.read();')
    func_str_list.append('  test_instance(95,   64) = Input_1.read();')
    func_str_list.append('  test_instance(63,   32) = Input_1.read();')
    func_str_list.append('  test_instance(31,    0) = Input_1.read();')
    func_str_list.append('  tmp(31,0) = test_instance(255, 224);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(223, 192);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(191, 160);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(159, 128);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(127,  96);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(95,   64);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(63,   32);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('  tmp(31,0) = test_instance(31,    0);')
    func_str_list.append('  Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  int min_distance_list[K_CONST];')
    func_str_list.append('  int label_list[K_CONST];')
    func_str_list.append('')
    func_str_list.append('  bit128 input_tmp1, input_tmp2;')
    func_str_list.append('')
    func_str_list.append('  input_tmp1(127,  96) = Input_1.read();')
    func_str_list.append('  input_tmp1(95,   64) = Input_1.read();')
    func_str_list.append('  input_tmp1(63,   32) = Input_1.read();')
    func_str_list.append('  input_tmp1(31,    0) = Input_1.read();')
    func_str_list.append('  input_tmp2(127,  96) = Input_1.read();')
    func_str_list.append('  input_tmp2(95,   64) = Input_1.read();')
    func_str_list.append('  input_tmp2(63,   32) = Input_1.read();')
    func_str_list.append('  input_tmp2(31,    0) = Input_1.read();')
    func_str_list.append('')
    func_str_list.append('  for(int i=0; i<K_CONST; i++)')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('   min_distance_list[i] = (int) input_tmp1(i*32+31, i*32);')
    func_str_list.append('   label_list[i] = (int) input_tmp2(i*32+31, i*32);')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Initialize the knn set')
    func_str_list.append('   SET_KNN_SET: for ( int i = 0; i < K_CONST * OP_SIZE ; ++i )')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('     // Note that the max distance is 256')
    func_str_list.append('     knn_set[i] = 256;')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   TRAINING_LOOP : for ( int i = 0; i < NUM_TRAINING / PAR_FACTOR; ++i )')
    func_str_list.append('   {')
    func_str_list.append('       #pragma HLS pipeline')
    func_str_list.append('       LANES : for ( int j = 0; j < OP_SIZE; j++ )')
    func_str_list.append('       {')
    func_str_list.append('         #pragma HLS unroll')
    func_str_list.append('         WholeDigitType training_instance = training_set[j * NUM_TRAINING / PAR_FACTOR + i];')
    func_str_list.append('         update_knn( test_instance, training_instance, &knn_set[j * K_CONST] );')
    func_str_list.append('       }')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   //update min_distance_list and label_list according to the new knn_set')
    func_str_list.append('   LabelType label_in = ' + str(N-1) + ';')
    func_str_list.append('   knn_vote_small(knn_set, min_distance_list, label_list, label_in);')
    func_str_list.append('')
    func_str_list.append('   bit128 output_tmp1, output_tmp2;')
    func_str_list.append('')
    func_str_list.append('   for(int i=0; i<K_CONST; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('    output_tmp1(i*32+31, i*32) = min_distance_list[i];')
    func_str_list.append('    output_tmp2(i*32+31, i*32) = label_list[i];')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   tmp(31,0) = output_tmp1(127,96);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(95, 64);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(63, 32);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp1(31,  0);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(127,96);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(95, 64);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(63, 32);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('   tmp(31,0) = output_tmp2(31,  0);')
    func_str_list.append('   Output_1.write(tmp);')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    return 'update_knn_i'+str(N), "\n".join(func_str_list)

def gen_update_knn_iN_header(N):
    func_str_list = []
    func_str_list.append('void update_knn_i' + str(N) + '(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'update_knn_i'+str(N), "\n".join(func_str_list)


def gen_update_knn_i10_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('static int popcount(WholeDigitType x)')
    func_str_list.append('{')
    func_str_list.append('  // most straightforward implementation')
    func_str_list.append('  // actually not bad on FPGA')
    func_str_list.append('  int cnt = 0;')
    func_str_list.append('  for (int i = 0; i < 256; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('    cnt = cnt + x(i, i);')
    func_str_list.append('  }')
    func_str_list.append('  return cnt;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('static void update_knn( WholeDigitType test_inst, WholeDigitType train_inst, int min_distances[K_CONST] )')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=min_distances complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // Compute the difference using XOR')
    func_str_list.append('  WholeDigitType diff = test_inst ^ train_inst;')
    func_str_list.append('')
    func_str_list.append('  int dist = 0;')
    func_str_list.append('')
    func_str_list.append('  dist = popcount(diff);')
    func_str_list.append('')
    func_str_list.append('  int max_dist = 0;')
    func_str_list.append('  int max_dist_id = 0;')
    func_str_list.append('  int k = 0;')
    func_str_list.append('')
    func_str_list.append('  // Find the max distance')
    func_str_list.append('  FIND_MAX_DIST: for ( int k = 0; k < K_CONST; ++k )')
    func_str_list.append('  {')
    func_str_list.append('    if ( min_distances[k] > max_dist )')
    func_str_list.append('    {')
    func_str_list.append('      max_dist = min_distances[k];')
    func_str_list.append('      max_dist_id = k;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Replace the entry with the max distance')
    func_str_list.append('  if ( dist < max_dist )')
    func_str_list.append('    min_distances[max_dist_id] = dist;')
    func_str_list.append('')
    func_str_list.append('  return;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('static void knn_vote_small( int knn_set[OP_SIZE * K_CONST],')
    func_str_list.append('                    int min_distance_list[K_CONST],')
    func_str_list.append('        int label_list[K_CONST],')
    func_str_list.append('        LabelType label_in)')
    func_str_list.append('{')
    func_str_list.append('  #pragma HLS inline')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('  // final K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=min_distance_list complete dim=0')
    func_str_list.append('  // labels for the K nearest neighbors')
    func_str_list.append('  #pragma HLS array_partition variable=label_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  int pos = 1000;')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  // go through all the lanes')
    func_str_list.append('  // do an insertion sort to keep a sorted neighbor list')
    func_str_list.append('  LANES: for (int i = 0; i < OP_SIZE; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    INSERTION_SORT_OUTER: for (int j = 0; j < K_CONST; j ++ )')
    func_str_list.append('    {')
    func_str_list.append('      #pragma HLS pipeline')
    func_str_list.append('      pos = 1000;')
    func_str_list.append('      INSERTION_SORT_INNER: for (int r = 0; r < K_CONST; r ++ )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        pos = ((knn_set[i*K_CONST+j] < min_distance_list[r]) && (pos > K_CONST)) ? r : pos;')
    func_str_list.append('      }')
    func_str_list.append('')
    func_str_list.append('      INSERT: for (int r = K_CONST ;r > 0; r -- )')
    func_str_list.append('      {')
    func_str_list.append('        #pragma HLS unroll')
    func_str_list.append('        if(r-1 > pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = min_distance_list[r-2];')
    func_str_list.append('          label_list[r-1] = label_list[r-2];')
    func_str_list.append('        }')
    func_str_list.append('        else if (r-1 == pos)')
    func_str_list.append('        {')
    func_str_list.append('          min_distance_list[r-1] = knn_set[i*K_CONST+j];')
    func_str_list.append('          label_list[r-1] = label_in;')
    func_str_list.append('        }')
    func_str_list.append('      }')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('static LabelType knn_vote_final(int label_list[K_CONST])')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS array_partition variable=label_list complete dim=0')
    func_str_list.append('#pragma HLS inline')
    func_str_list.append('')
    func_str_list.append('  int vote_list[10];')
    func_str_list.append('#pragma HLS array_partition variable=vote_list complete dim=0')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  INIT_2: for (int i = 0;i < 10; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    #pragma HLS unroll')
    func_str_list.append('    vote_list[i] = 0;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // vote')
    func_str_list.append('  INCREMENT: for (int i = 0;i < K_CONST; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    #pragma HLS pipeline')
    func_str_list.append('    vote_list[label_list[i]] += 1;')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  LabelType max_vote;')
    func_str_list.append('  max_vote = 0;')
    func_str_list.append('')
    func_str_list.append('  // find the maximum value')
    func_str_list.append('  VOTE: for (int i = 0;i < 10; i ++ )')
    func_str_list.append('  {')
    func_str_list.append('    #pragma HLS unroll')
    func_str_list.append('    if(vote_list[i] >= vote_list[max_vote])')
    func_str_list.append('    {')
    func_str_list.append('      max_vote = i;')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  return max_vote;')
    func_str_list.append('')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('void update_knn_i10(hls::stream<ap_uint<32> > & Input_1, hls::stream<ap_uint<512> > & Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Input_1')
    func_str_list.append('#pragma HLS INTERFACE axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType training_set [NUM_TRAINING / NUM_OPS];')
    func_str_list.append('const int unroll_factor = OP_SIZE;')
    func_str_list.append('#pragma HLS array_partition variable=training_set block factor=unroll_factor dim=0')
    func_str_list.append('')
    func_str_list.append('static WholeDigitType test_instance;')
    func_str_list.append('static unsigned char results_holder[2048];')
    func_str_list.append('')
    func_str_list.append('static int knn_set[K_CONST*OP_SIZE];')
    func_str_list.append('#pragma HLS array_partition variable=knn_set complete dim=0')
    func_str_list.append('')
    func_str_list.append('WholeDigitType data_temp;')
    func_str_list.append('static int index = 0;')
    func_str_list.append('')
    func_str_list.append('if (index == 0)')
    func_str_list.append('{')
    func_str_list.append('   //Store the local training set')
    func_str_list.append('   STORE_LOCAL: for(int i = 0; i < NUM_TRAINING / NUM_OPS; i++)')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS pipeline')
    func_str_list.append('')
    func_str_list.append('  training_set[i](255, 224) =Input_1.read();')
    func_str_list.append('  training_set[i](223, 192) =Input_1.read();')
    func_str_list.append('  training_set[i](191, 160) =Input_1.read();')
    func_str_list.append('  training_set[i](159, 128) =Input_1.read();')
    func_str_list.append('  training_set[i](127,  96) =Input_1.read();')
    func_str_list.append('  training_set[i](95,   64) =Input_1.read();')
    func_str_list.append('  training_set[i](63,   32) =Input_1.read();')
    func_str_list.append('  training_set[i](31,    0) =Input_1.read();')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   //Output_1.write(2001);')
    func_str_list.append('   index = 1;')
    func_str_list.append('}')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  for(int j=255; j>0; j=j-32){')
    func_str_list.append('   test_instance(j, j-31) =Input_1.read();')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('  int min_distance_list[K_CONST];')
    func_str_list.append('  int label_list[K_CONST];')
    func_str_list.append('')
    func_str_list.append('  bit128 input_tmp1, input_tmp2;')
    func_str_list.append('')
    func_str_list.append('  for(int j=127; j>0; j=j-32){')
    func_str_list.append('   input_tmp1(j,  j-31) = Input_1.read();')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  for(int j=127; j>0; j=j-32){')
    func_str_list.append('   input_tmp2(j,  j-31) = Input_1.read();')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  for(int i=0; i<K_CONST; i++)')
    func_str_list.append('  {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('   min_distance_list[i] = (int) input_tmp1(i*32+31, i*32);')
    func_str_list.append('   label_list[i] = (int) input_tmp2(i*32+31, i*32);')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('  // Initialize the knn set')
    func_str_list.append('   SET_KNN_SET: for ( int i = 0; i < K_CONST * OP_SIZE ; ++i )')
    func_str_list.append('   {')
    func_str_list.append('#pragma HLS unroll')
    func_str_list.append('     // Note that the max distance is 256')
    func_str_list.append('     knn_set[i] = 256;')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('   TRAINING_LOOP : for ( int i = 0; i < NUM_TRAINING / PAR_FACTOR; ++i )')
    func_str_list.append('   {')
    func_str_list.append('       #pragma HLS pipeline')
    func_str_list.append('       LANES : for ( int j = 0; j < OP_SIZE; j++ )')
    func_str_list.append('       {')
    func_str_list.append('         #pragma HLS unroll')
    func_str_list.append('         WholeDigitType training_instance = training_set[j * NUM_TRAINING / PAR_FACTOR + i];')
    func_str_list.append('         update_knn( test_instance, training_instance, &knn_set[j * K_CONST] );')
    func_str_list.append('       }')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   //update min_distance_list and label_list according to the new knn_set')
    func_str_list.append('   LabelType label_in = 9;')
    func_str_list.append('   knn_vote_small(knn_set, min_distance_list, label_list, label_in);')
    func_str_list.append('')
    func_str_list.append('')
    func_str_list.append('   LabelType result = knn_vote_final(label_list);')
    func_str_list.append('')
    func_str_list.append('   bit512 out_tmp;')
    func_str_list.append('   results_holder[index-1] = result;')
    func_str_list.append('   if(index == 2000){')
    func_str_list.append('     for(int i=0; i<32; i++){')
    func_str_list.append('       for(int j=0; j<64; j++) {')
    func_str_list.append('         out_tmp(j*8+7, j*8) = results_holder[i*64+j];')
    func_str_list.append('       }')
    func_str_list.append('       Output_1.write(out_tmp);')
    func_str_list.append('     }')
    func_str_list.append('   }')
    func_str_list.append('')
    func_str_list.append('  index++;')
    func_str_list.append('  return;')
    func_str_list.append('}')
    return 'update_knn_i10', "\n".join(func_str_list)

def gen_update_knn_i10_header():
    func_str_list = []
    func_str_list.append('void update_knn_i10(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<512>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'update_knn_i10', "\n".join(func_str_list)



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

    # Values for PAR_FACTOR, K_CONST shuold be identical across all the ops
    for op, param_dict in cur_param_dict.items():
        if op != 'metric':
            if 'PAR_FACTOR' in param_dict:
                par_factor = param_dict['PAR_FACTOR']
            if 'K_CONST' in param_dict:
                k_val = param_dict['K_CONST']
    print(par_factor)
    print(k_val)


    ###########################################
    ## Generate src files based on cur param ##
    ###########################################

    # cpp code gen
    func_name_list = []
    ops_to_compile_list = []
    filedata_dict = {}

    func_name, filedata = gen_update_knn_i1_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_update_knn_i1_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    for i in range(2,10):
        func_name, filedata = gen_update_knn_iN_func(i)
        func_name_list.append(func_name)
        func_name, filedata_header = gen_update_knn_iN_header(i)
        filedata_dict[func_name] = (filedata, filedata_header)
        if needs_write_param(func_name, filedata):
            ops_to_compile_list.append(func_name)

    func_name, filedata = gen_update_knn_i10_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_update_knn_i10_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    print()
    #############################################
    ## Update cur_param.json for new operators ##
    #############################################
    # Nothing to do for this benchmark because no new operator is generated


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


    #################################################
    ## Update application graph (top_no_merge.cpp) ##
    #################################################
    # Doesn't change for this benchmark
    top_str_list = ['update_knn_i1(Input_1, knn_out1);',
                    'update_knn_i2(knn_out1, knn_out2);',
                    'update_knn_i3(knn_out2, knn_out3);',
                    'update_knn_i4(knn_out3, knn_out4);',
                    'update_knn_i5(knn_out4, knn_out5);',
                    'update_knn_i6(knn_out5, knn_out6);',
                    'update_knn_i7(knn_out6, knn_out7);',
                    'update_knn_i8(knn_out7, knn_out8);',
                    'update_knn_i9(knn_out8, knn_out9);',
                    'update_knn_i10(knn_out9, Output_1);']
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