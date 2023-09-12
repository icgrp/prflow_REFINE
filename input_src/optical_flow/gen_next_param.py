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
#   - divide ops with cur_param_dict's "merged_to" param and "merged_to_try" param
#   - assign representative operator to each group (the one with the last in the graph)
#   - write operators that are not merged with others
#   - write operators that are merged with others, the top level is representative op
#   - returns top_str_dict
#     e.g. {('flow_calc', 'tensor_weight_x_i1', 'tensor_weight_y_i1'): 'flow_calc(outer_product_out_1,flow_calc_1, flow_calc_2);\n'}
def perform_merging(operator_list, cur_param_dict, ops_to_compile_list, filedata_dict):
    top_str_dict = {}

    is_merged_to_exist = False
    for func_name in cur_param_dict:
        if func_name != 'metric':
            if 'merged_to' in cur_param_dict[func_name] or 'merged_to_try' in cur_param_dict[func_name]:
                is_merged_to_exist = True

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
                    non_io_stream_list.append(stream)
            # print(io_stream_list)
            # print(non_io_stream_list)

            op_io_type_and_width_dict = return_operator_io_type_and_width(operator_list, filedata_dict)
            # print("op_io_type_and_width_dict:")
            # print(op_io_type_and_width_dict)
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
            for sublist in sorted_forward_op_list:
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


def gen_data_transfer_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void data_transfer(')
    func_str_list.append('    hls::stream<ap_uint<512>>  &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<64>>  &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('')
    func_str_list.append('bit512 in_tmp;')
    func_str_list.append('bit64  out_tmp;')
    func_str_list.append('')
    func_str_list.append('  for(int i=0; i<MAX_HEIGHT*MAX_WIDTH/8; i++){')
    func_str_list.append('#pragma HLS PIPELINE')
    func_str_list.append('    in_tmp = Input_1.read();')
    func_str_list.append('    for(int j=0; j<8; j++){')
    func_str_list.append('      out_tmp(31, 0) = in_tmp((j<<6)+31, (j<<6)+0 );')
    func_str_list.append('      out_tmp(63,32) = in_tmp((j<<6)+63, (j<<6)+32);')
    func_str_list.append('      Output_1.write(out_tmp);')
    func_str_list.append('    }')
    func_str_list.append('  }')
    func_str_list.append('')
    func_str_list.append('}')
    func_str_list.append('  ')
    func_str_list.append('     ')
    return 'data_transfer', "\n".join(func_str_list)

def gen_data_transfer_header():
    func_str_list = []
    func_str_list.append('void data_transfer(')
    func_str_list.append('    hls::stream<ap_uint<512>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<64>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'data_transfer', "\n".join(func_str_list)


def gen_gradient_xyz_calc_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void gradient_xyz_calc(    ')
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
    func_str_list.append('            else {')
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
    return 'gradient_xyz_calc', "\n".join(func_str_list)

def gen_gradient_xyz_calc_header():
    func_str_list = []
    func_str_list.append('void gradient_xyz_calc(')
    func_str_list.append('    hls::stream<ap_uint<64>> & Input_1,')
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
    return 'tensor_weight_y_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_y_header(outer_width, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('void tensor_weight_y_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_y_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_x_func(outer_width, par_factor, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

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
    return 'tensor_weight_x_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


def gen_tensor_weight_x_header(outer_width, idx_par_factor):
    outer_product_width = math.ceil(6/par_factor * outer_width/32) * 32

    func_str_list = []
    func_str_list.append('void tensor_weight_x_i' + str(idx_par_factor + 1) + '(')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Input_1,')
    func_str_list.append('    hls::stream<ap_uint<' + str(outer_product_width) + '>> &Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'tensor_weight_x_i' + str(idx_par_factor + 1), "\n".join(func_str_list)


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


def gen_output_data_func():
    func_str_list = []
    func_str_list.append('#include "../host/typedefs.h"')
    func_str_list.append('')
    func_str_list.append('void output_data(')
    func_str_list.append(' hls::stream<ap_uint<32>> &Input_1,')
    func_str_list.append(' hls::stream<ap_uint<32>> &Input_2,')
    func_str_list.append(' hls::stream<ap_uint<512>> &Output_1)')
    func_str_list.append('{')
    func_str_list.append('#pragma HLS interface axis register port=Input_1')
    func_str_list.append('#pragma HLS interface axis register port=Output_1')
    func_str_list.append('#pragma HLS interface axis register port=Input_2')
    func_str_list.append('')
    func_str_list.append(' OUT_CONVERT: for (int i = 0; i < MAX_HEIGHT*MAX_WIDTH/8; i++)')
    func_str_list.append(' {')
    func_str_list.append('   bit512 tmpframe;')
    func_str_list.append('      #pragma HLS pipeline II = 4')
    func_str_list.append('   for(int j=0; j<8; j++){')
    func_str_list.append('    tmpframe(j*64+31, j*64   ) = Input_1.read();')
    func_str_list.append('    tmpframe(j*64+63, j*64+32) = Input_2.read();')
    func_str_list.append('   }')
    func_str_list.append('   Output_1.write(tmpframe);')
    func_str_list.append(' }')
    func_str_list.append('}')
    return 'output_data', "\n".join(func_str_list)

def gen_output_data_header():
    func_str_list = []
    func_str_list.append('void output_data(')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_1,')
    func_str_list.append('    hls::stream<ap_uint<32>> & Input_2,')
    func_str_list.append('    hls::stream<ap_uint<512>> & Output_1')
    func_str_list.append('    );')
    func_str_list.append('#pragma map_target = HW')
    return 'output_data', "\n".join(func_str_list)



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

    func_name, filedata = gen_data_transfer_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_data_transfer_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

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

    func_name, filedata = gen_output_data_func()
    func_name_list.append(func_name)
    func_name, filedata_header = gen_output_data_header()
    filedata_dict[func_name] = (filedata, filedata_header)
    if needs_write_param(func_name, filedata):
        ops_to_compile_list.append(func_name)

    print(filedata_dict.keys())
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



    # outer_width_int, calc_width_int values could be also design space, but
    # We fix these vals for each outer_width val
    # TODO: dummy_len is required to flush out all the outputs in optical_flow benchmark.
    #       This is a BUG in current decomposition of optical_flow benchmark.
    if outer_width == 16:
        outer_width_int, calc_width_int = 11, 24
        dummy_len = 775
    elif outer_width == 32:
        outer_width_int, calc_width_int = 27, 56
        dummy_len = 774
    elif outer_width == 48:
        outer_width_int, calc_width_int = 27, 56
        dummy_len = 774
        for op in cur_param_dict.keys():
            if op != 'metric':
                if (op.startswith('tensor_weight_x_i') and 'merged_to' in cur_param_dict[op].keys()) or\
                   (op.startswith('tensor_weight_y_i') and 'merged_to' in cur_param_dict[op].keys()) or\
                   (op.startswith('outer_product') and 'merged_to' in cur_param_dict[op].keys()):
                    dummy_len = 775
        if cur_param_dict['flow_calc']['kernel_clk'] == 250:
            dummy_len = 777
        elif cur_param_dict['flow_calc']['kernel_clk'] == 300:
            dummy_len = 777
        elif cur_param_dict['flow_calc']['kernel_clk'] == 350:
            dummy_len = 778
        elif cur_param_dict['flow_calc']['kernel_clk'] == 400:
            dummy_len = 779
        if cur_param_dict['gradient_xyz_calc']['kernel_clk'] == 250:
            dummy_len = 779            
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



    #################################################
    ## Update application graph (top_no_merge.cpp) ##
    #################################################
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
            flow_calc_str += ' flow_calc_1, flow_calc_2);'
            top_str_list.append(flow_calc_str)

    output_data_str = 'output_data(flow_calc_1, flow_calc_2, Output_1);'
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


    # TODO: specs.json and cur_param.json are redundant
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