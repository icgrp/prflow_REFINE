import json
from pr_flow.p23_pblock import pblock_page_dict
import argparse
import sys, os
import re



# Helper functions stolen from runtime.py
def return_operator_io_argument_dict_local(operator_list, benchmark, is_no_merge=False):
    # operator_list = operators.split()
    operator_arg_dict = {}
    for operator in operator_list:
        if is_no_merge:
            with open('./input_src/'+benchmark+'/operators/no_merge/'+operator+'.h', 'r') as infile:
                file_list = infile.readlines()
        else:
            with open('./input_src/'+benchmark+'/operators/'+operator+'.h', 'r') as infile:
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
def return_operator_inst_dict_local(operator_list, benchmark, top_file):
    # operator_list = operators.split()
    operator_var_dict = {}
    with open('./input_src/'+benchmark+'/host/' + top_file, 'r') as infile:
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

def return_io_num(self, io_pattern, file_list):
    max_num = 0
    for line in file_list:
        num_list = re.findall(r""+io_pattern+"\d*", line)
        if(len(num_list)>0 and int(num_list[0].replace(io_pattern,''))): max_num = int(num_list[0].replace(io_pattern,''))
    return max_num
 
def return_operator_connect_list_local(operator_arg_dict, operator_var_dict):
    connection_list = []
    for key_a in operator_var_dict:
        operator = key_a
        # src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
        with open('./input_src/'+benchmark+'/operators/'+operator+'.h', 'r') as infile:
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


def get_port_num(operator, io_port, pblock_assign_dict):
    leaf_interface_mapping_dict = pblock_assign_dict[operator]['leaf_interface']
    io_port_dict = {}
    # e.g. {'Input_1': 2, 'Output_1': 9, 'Input_2': 2, 'Output_2': 9}
    for leaf_interface_idx, io_ports in pblock_assign_dict[operator]['leaf_interface'].items():
        input_port_idx = 2 # gets reset for different leaf_interface_idx
        output_port_idx = 9 # gets reset for different leaf_interface_idx
        for io in io_ports:
            if io.startswith('Input_'):
                io_port_dict[io] = input_port_idx
                input_port_idx += 1
            else:
                io_port_dict[io] = output_port_idx
                output_port_idx += 1

    return io_port_dict[io_port]
    # if io_port.startswith('Input_'):
    #     idx = int(io_port.split('_')[1]) + 1
    #     return idx
    # else:
    #     assert(io_port.startswith('Output_'))
    #     idx = int(io_port.split('_')[1]) + 8
    #     return idx

def get_page_num(operator, io_port, pblock_assign_dict):
    leaf_interface_mapping_dict = pblock_assign_dict[operator]['leaf_interface']
    li_idx = 0
    for leaf_interface_idx in pblock_assign_dict[operator]['leaf_interface'].keys():
        if io_port in pblock_assign_dict[operator]['leaf_interface'][leaf_interface_idx]:
            li_idx = int(leaf_interface_idx)
    return li_idx + pblock_assign_dict[operator]['page_num']



def get_page_assign_dict(pblock_assign_dict):
    page_assign_dict = {}
    for op in pblock_assign_dict:
        num_leaf_interface = len(pblock_assign_dict[op]['leaf_interface'])
        page_num = pblock_assign_dict[op]['page_num']
        page_num_list = []
        for i in range(num_leaf_interface):
            page_num_list.append(page_num + i)
        page_assign_dict[op] = page_num_list
    return page_assign_dict

def get_counter_type_str(counter_type):
    if counter_type == 3:
        return "full"
    elif counter_type == 2:
        return "empty"
    elif counter_type == 1:
        return "read"
    else:
        return "stall"

def get_op_name(page_num, page_assign_dict):
    for op in page_assign_dict:
        if page_num in page_assign_dict[op]:
            return op
    return None

def get_best_latency(best_latency):
    if not os.path.isfile('./input_src/' + benchmark + '/params/best.txt'):
        os.system('cp ./input_src/' + benchmark + '/params/best_init.txt ' + './input_src/' + benchmark + '/params/best.txt')

    with open('./input_src/' + benchmark + '/params/best.txt', 'r') as infile:
        best_latency = float(infile.read())
    return best_latency


# Returns operator that matches the input idx
def mono_op_from_idx(mono_counter_idx_dict, idx):
    for elem in mono_counter_idx_dict:
        if idx == mono_counter_idx_dict[elem]:
            assert('->' not in elem)
            return elem
    raise Exception('Invalid idx for operator, mono_counter_idx_dict')

# Returns connection that matches the input idx
# idx 1,2,3 => mono_counter_idx_dict's connection whose item is 0
# idx 4,5,6 => mono_counter_idx_dict's connection whose item is 1
# ...
def mono_connection_from_idx(mono_counter_idx_dict, idx):
    for elem in mono_counter_idx_dict:
        connection_index = mono_counter_idx_dict[elem]
        if connection_index*3 < idx and idx <= connection_index*3+3:
            assert('->' in elem)
            return elem
    raise Exception('Invalid idx for connection, mono_counter_idx_dict')



# Returns counter dictionary for the benchmark
# e.g. cnt_dict = coloringFB_1 : {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                 0: {'stall': 117130}, 
#                                 9: {'full': 16735, 'empty': 210347}}
# ...
def counter_mono_dict(benchmark, mono_counter_idx_dict, cur_param_dict):
    cnt_dict = {}
    accuracy = -1

    total_len = len(mono_counter_idx_dict)
    num_connection = 0
    for elem in mono_counter_idx_dict:
        if ('->' in elem): # connection
            num_connection += 1
        else: # operator
            cnt_dict[elem] = {}
    num_ops = total_len-num_connection # excludes DMA
    first_stall_idx = 3*num_connection + 1 # each connection has full, empty, read cnt


    with open("./_bi_results/" + benchmark + "/results.txt", "r") as infile:
        lines = infile.readlines()

        # Parse results
        for line in lines:

            # Ignore first out1[0] data
            # full/empty counters are not used... but still have them for debugging
            if line.startswith('out1[') and not line.startswith('out1[0] '):

                idx = int(line.split(']')[0].split('[')[1])
                # print(idx)
                # print(line)
                hex_cnt = line.split()[2]
                counter_val = int(hex_cnt, 16)
                # print(counter_val)

                if idx < first_stall_idx:
                    if idx % 3 == 1:
                        counter_type = 'full'
                    elif idx % 3 == 2:
                        counter_type = 'empty'
                    else:
                        counter_type = 'read'

                    connection = mono_connection_from_idx(mono_counter_idx_dict, idx)
                    sender_op = connection.split('->')[0].split('.')[0]
                    sender_output_port = connection.split('->')[0].split('.')[1]
                    sender_output_port_num = int(sender_output_port.split('_')[1]) + 8 # output port starts from 9

                    receiver_op = connection.split('->')[1].split('.')[0]
                    receiver_input_port = connection.split('->')[1].split('.')[1]
                    receiver_input_port_num = int(receiver_input_port.split('_')[1]) + 1 # input port starts from 2

                    if sender_op != 'DMA':
                        if sender_output_port_num not in cnt_dict[sender_op].keys():
                            cnt_dict[sender_op][sender_output_port_num] = {}
                        cnt_dict[sender_op][sender_output_port_num][counter_type] = counter_val
                    if receiver_op != 'DMA':
                        if receiver_input_port_num not in cnt_dict[receiver_op].keys():
                            cnt_dict[receiver_op][receiver_input_port_num] = {}
                        cnt_dict[receiver_op][receiver_input_port_num][counter_type] = counter_val

                # stall counters are sent last
                else: 
                    print(mono_counter_idx_dict)
                    print(idx)
                    op = mono_op_from_idx(mono_counter_idx_dict, idx)
                    kernel_clk = cur_param_dict[op]['kernel_clk']
                    cnt_dict[op][0] = {'stall': counter_val / kernel_clk} # stall counter

            # if line.startswith('elapsed time: '):
            #     latency = int(line.split()[2])
            if line.startswith('accuracy: '):
                accuracy = float(line.split()[1])

    with open("./_bi_results/" + benchmark + "/summary.csv", "r") as infile:
        lines = infile.readlines()

        next_line = False
        # Parse results
        for line in lines:
            if line.startswith('Kernel,Number Of Enqueues'):
                next_line = True
            elif next_line == True:
                kernel_name, num_enqueue, latency, _, _, _, _ = line.split(',') 
                break

    latency = float(latency)
    print(">> accuracy: " + str(accuracy))
    print(">> latency: " + str(latency))
    for op_name in sorted(cnt_dict):
        print(op_name, end=' ')
        print(sorted(cnt_dict[op_name].items()))

    assert(int(num_enqueue) == 1)

    return latency, accuracy, cnt_dict


# Returns counter dictionary for the benchmark
# e.g. cnt_dict = coloringFB_1 : 0: {'stall': 117130}, 
#                                3: {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                    9: {'full': 16735, 'empty': 210347}}
#                                4: {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                    9: {'full': 16735, 'empty': 210347}}
# ... 3 and 4 are page_num
def counter_dict(benchmark, pblock_assign_dict, cur_param_dict):
    cnt_dict = {}
    accuracy = -1

    page_assign_dict = get_page_assign_dict(pblock_assign_dict)
    print(page_assign_dict)

    with open("./_bi_results/" + benchmark + "/results.txt", "r") as infile:
        lines = infile.readlines()

        # Parse results
        for line in lines:
            if line.startswith('out1['):
                hex_cnt = line.split()[2]
                # print(int(hex_cnt, 16))
                # print(bin(int(hex_cnt, 16)))
                # print(bin(int(hex_cnt, 16))[2:])
                cnt = bin(int(hex_cnt, 16))[2:].zfill(64) # 64b hex -> 64b binary
                # print(cnt)
                # print(len(cnt))
                cnt = cnt[15:] # remove padding
                cnt = cnt[1:] # remove valid bit

                # How the is_done packet is composed
                dst_leaf, dst_port, self_leaf, self_port, counter, counter_val =\
                    int(cnt[0:5],2), int(cnt[5:9],2), int(cnt[9:14],2), int(cnt[14:18],2), int(cnt[18:20],2), int(cnt[20:],2)
                # print(dst_leaf)
                # print(line)
                assert(dst_leaf == 1)
                assert(dst_port == 2)

                counter_type = get_counter_type_str(counter)
                op_name = get_op_name(self_leaf, page_assign_dict)

                if op_name == None:
                    print("####### error: " + str(self_leaf))
                    print("####### error: " + str(line))
                    print(counter)
                    print(self_leaf)
                    print(op_name)
                    print(counter_val)
                    print(line)

                kernel_clk = cur_param_dict[op_name]['kernel_clk']
                if op_name not in cnt_dict:
                    
                    if self_port == 0:
                        cnt_dict[op_name] = {}
                        cnt_dict[op_name][0] = {}
                        cnt_dict[op_name][0]['stall'] = counter_val / kernel_clk
                    else:
                        cnt_dict[op_name] = {}
                        cnt_dict[op_name][self_leaf] = {}
                        cnt_dict[op_name][self_leaf][self_port] = {}
                        cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val / kernel_clk
                        # print(cnt_dict)

                else:
                    if self_port == 0: # stall_cnt
                        cnt_dict[op_name][0] = {}
                        cnt_dict[op_name][0]['stall'] = counter_val / kernel_clk
                    else:
                        if self_leaf not in cnt_dict[op_name]:
                            cnt_dict[op_name][self_leaf] = {}
                            cnt_dict[op_name][self_leaf][self_port] = {}
                            cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val / kernel_clk
                        else:
                            if self_port not in cnt_dict[op_name][self_leaf]:
                                cnt_dict[op_name][self_leaf][self_port] = {}
                                cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val / kernel_clk
                            else:
                                cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val / kernel_clk

            # if line.startswith('elapsed time: '):
            #     latency = int(line.split()[2])
            if line.startswith('accuracy: '):
                accuracy = float(line.split()[1])

    with open("./_bi_results/" + benchmark + "/summary.csv", "r") as infile:
        lines = infile.readlines()

        next_line = False
        # Parse results
        for line in lines:
            if line.startswith('Kernel,Number Of Enqueues'):
                next_line = True
            elif next_line == True:
                kernel_name, num_enqueue, latency, _, _, _, _ = line.split(',') 
                break

    latency = float(latency)
    print(">> accuracy: " + str(accuracy))
    print(">> latency: " + str(latency))
    for op_name in sorted(cnt_dict):
        print(op_name)
        for page_num in sorted(cnt_dict[op_name]):
            if page_num != 0: # not stall
                print(page_num, end=' ')
                for port_num in sorted(cnt_dict[op_name][page_num]):
                    print(port_num, end=' ')
                    for cnt in sorted(cnt_dict[op_name][page_num][port_num]):
                        print(cnt, end=' ')
                        print(cnt_dict[op_name][page_num][port_num][cnt], end=' ')
                print()

    assert(int(num_enqueue) == 1)

    return latency, accuracy, cnt_dict


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

# E.g.: A->B->C
#       connection_list = [DMA.Output_1.->A.Input_1, A.Output_1->B.Input_1, B.Output_1->C.Input_1, C.Output_1->DMA.Input_1]
#       Returns [B.Output_1->C.Input_1, A.Output_1->B.Input_1,]
def sort_connection_list_backward(connection_list, sorted_backward_op_list):
    connection_list_copy = connection_list

    # Start from backward
    sorted_backward_connection_list = []
    for sublist in sorted_backward_op_list:

        # target_op.Output_*->
        connection_list_priority = []
        for target_op in sublist:
            for connection in connection_list:
                if target_op + '.Output_'  in connection and \
                   connection not in connection_list_priority and \
                   'DMA' not in connection:
                    connection_list_priority.append(connection)

            tmp_list = []
            for connection in connection_list:
                if connection not in connection_list_priority:
                    tmp_list.append(connection)
            connection_list = tmp_list

        # sort connection_list_priority
        sorted_connection_list_priority = []
        for connected_op in get_flat_list(sorted_backward_op_list):
            for connection in connection_list_priority:
                if connected_op + '.Input_' in connection and \
                   connection not in sorted_connection_list_priority:
                    sorted_connection_list_priority.append(connection)
        sorted_backward_connection_list += [sorted_connection_list_priority]
        # print("sorted_connection_list_priority:")
        # print(sorted_connection_list_priority)

        # ->target_op.Input_*
        connection_list_priority = []
        for target_op in sublist:
            for connection in connection_list:
                if target_op + '.Input_'  in connection and \
                   connection not in connection_list_priority and \
                   'DMA' not in connection:
                    connection_list_priority.append(connection)

            tmp_list = []
            for connection in connection_list:
                if connection not in connection_list_priority:
                    tmp_list.append(connection)
            connection_list = tmp_list

        # sort connection_list_priority
        sorted_connection_list_priority = []
        for connected_op in get_flat_list(sorted_backward_op_list):
            for connection in connection_list_priority:
                if connected_op + '.Output_' in connection and \
                   connection not in sorted_connection_list_priority:
                    sorted_connection_list_priority.append(connection)
        sorted_backward_connection_list += [sorted_connection_list_priority]
        # print("sorted_connection_list_priority:")
        # print(sorted_connection_list_priority)

    # print(sorted_backward_connection_list)
    assert(len(get_flat_list(sorted_backward_connection_list)) == len(connection_list_copy) - 2)
    return sorted_backward_connection_list


def no_merge_op_list(benchmark):
    with open('./input_src/' + benchmark + '/host/top_no_merge.cpp', 'r') as infile:
        lines = infile.readlines()
    operator_list = []
    for line in lines:
        if ');' in line:
            op_name = line.split('(')[0]
            operator_list.append(op_name)
    return operator_list

def merge_op_list(benchmark):
    with open('./input_src/' + benchmark + '/host/top.cpp', 'r') as infile:
        lines = infile.readlines()
    operator_list = []
    for line in lines:
        if ');' in line:
            op_name = line.split('(')[0]
            operator_list.append(op_name)
    return operator_list


def update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, operator_list, cnt_dict, cur_idx_dict, params_search_space_dict, params_annotate_dict, error_margin):
    # For each link in the graph, full_diff = sender's full cnt - receiver's full cnt
    #     => if the link's full_diff is large, NoC could be bottleneck
    # For each link in the graph, empty_diff = receiver's empty_cnt - sender's empty_cnt
    #     => if the link's empty_diff is large, NoC could be bottleneck

    # operator_list = list(prev_page_assign_dict.keys())
    # # print(operator_list)

    operator_arg_dict = return_operator_io_argument_dict_local(operator_list, benchmark, is_no_merge=False)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': ['Input_1', 'Output_1' .. }

    operator_var_dict = return_operator_inst_dict_local(operator_list, benchmark, 'top.cpp')
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...
    # print(operator_arg_dict)
    # print(operator_var_dict)

    connection_list = return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    # print(connection_list)

    connection_diff_dict = {}
    # 'data_transfer.Output_1->prj_rast1.Input_1': (full_diff, empty_diff)

    # print("cnt_dict:")
    # print(cnt_dict)
    # cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val


    for connection in connection_list:
        if 'DMA.' not in connection:
            # print(connection)
            sender_op = connection.split('->')[0].split('.')[0]
            sender_output_port = connection.split('->')[0].split('.')[1]
            receiver_op = connection.split('->')[1].split('.')[0]
            receiver_input_port = connection.split('->')[1].split('.')[1]

            sender_output_port_num = get_port_num(sender_op, sender_output_port, cur_idx_dict)
            sender_page_num = get_page_num(sender_op, sender_output_port, cur_idx_dict)
            # print(sender_op)
            # print(sender_page_num)
            # print(sender_output_port_num)
            sender_full_cnt = cnt_dict[sender_op][sender_page_num][sender_output_port_num]['full']

            receiver_input_port_num = get_port_num(receiver_op, receiver_input_port, cur_idx_dict)
            receiver_page_num = get_page_num(receiver_op, receiver_input_port, cur_idx_dict)
            receiver_full_cnt = cnt_dict[receiver_op][receiver_page_num][receiver_input_port_num]['full']
            # IMPORTANT: relax full difference
            if (sender_full_cnt*(1-error_margin) > receiver_full_cnt) and (sender_full_cnt - receiver_full_cnt) > 5: # difference is large enough
                full_diff = sender_full_cnt - receiver_full_cnt
            else: # difference is negligible
                full_diff = 0
            full_diff_original = sender_full_cnt - receiver_full_cnt # debugging purpose

            sender_empty_cnt = cnt_dict[sender_op][sender_page_num][sender_output_port_num]['empty']
            receiver_empty_cnt = cnt_dict[receiver_op][receiver_page_num][receiver_input_port_num]['empty']
            empty_diff = receiver_empty_cnt - sender_empty_cnt

            connection_diff_dict[connection] = (full_diff_original, full_diff, empty_diff)

    # print()
    # print("connection_diff_dict: ")
    # for connection in sorted(connection_diff_dict):
    #     print(str(connection) + ': ' + str(connection_diff_dict[connection]))

    operator_list_no_merge = no_merge_op_list(benchmark)
    operator_arg_dict_no_merge = return_operator_io_argument_dict_local(operator_list_no_merge, benchmark, is_no_merge=True)
    operator_var_dict_no_merge = return_operator_inst_dict_local(operator_list_no_merge, benchmark, 'top_no_merge.cpp')
    connection_list_no_merge = return_operator_connect_list_local(operator_arg_dict_no_merge, operator_var_dict_no_merge)
    # sorted_backward_op_list is all operators without merge
    sorted_backward_op_list = sorted_op_list_backward(operator_list_no_merge, connection_list_no_merge)
    # print()
    # print("sorted_backward_op_list: ")
    # print(sorted_backward_op_list)
    connection_list_sorted = sort_connection_list_backward(connection_list, sorted_backward_op_list)
    # print()
    # print("connection_list_sorted: ")
    # print(connection_list_sorted)

    print()
    print("potential erroneous connections with NoC bottleneck:")
    for connection_list in connection_list_sorted:
        for connection in connection_list:
            full_diff_original, full_diff, empty_diff = connection_diff_dict[connection]
            # if (full_diff > 0 or empty_diff > 0): # NoC bandwidth could be bottleneck
            if (full_diff_original > 0): # NoC bandwidth could be bottleneck
                print("> " + str(connection) + ": " + str((full_diff_original, full_diff, empty_diff)))
    print()

    return None, None



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',         '--benchmark',                       required = True)
    parser.add_argument('-s',         '--NoC_success',                     action='store_true')
    parser.add_argument('-t',         '--NoC_timing_violate',              action='store_true')
    parser.add_argument('-ms',        '--monolithic_success',              action='store_true')
    parser.add_argument('-mf',        '--monolithic_fail',                 action='store_true')
    # parser.add_argument('-a',         '--minimum_accuracy',                default = -1)

    args = parser.parse_args()
    benchmark = args.benchmark
    is_NoC_success = args.NoC_success
    is_NoC_timing_violate = args.NoC_timing_violate
    is_monolithic_success = args.monolithic_success
    is_monolithic_fail = args.monolithic_fail
    # minimum_accuracy = args.minimum_accuracy
    error_margin = 0.10
    os.system('mkdir -p ./input_src/' + benchmark + '/params/visited')


    with open('./input_src/' + benchmark + '/params/cur_param.json', 'r') as infile:
        prev_param_dict = json.load(infile)
    # Whether it succeeded or failed, always save prev_param. This will be used to determine whether to recompile the operator or not
    os.system('cp ./input_src/' + benchmark + '/params/cur_param.json ./input_src/' + benchmark + '/params/prev_param.json')


    best_latency = get_best_latency(benchmark)
    # print(best_latency)
    # print(latency)

    if is_NoC_success: 
        overlay_type = 'NoC'
        with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
            prev_idx_dict = json.load(infile)
        latency, accuracy, cnt_dict = counter_dict(benchmark, prev_idx_dict, prev_param_dict)
    else:
        assert(is_monolithic_success == True)
        overlay_type = 'mono'
        with open("./workspace/F007_mono_" + benchmark + "/mono_counter_idx_dict.json", "r") as infile:
            prev_idx_dict = json.load(infile)
        latency, accuracy, cnt_dict = counter_mono_dict(benchmark, prev_idx_dict, prev_param_dict) 

    print(latency, accuracy)
    print(cnt_dict)
    print(prev_param_dict)

    min_stall = sys.maxsize
    bottleneck_op = None
    bottleneck_op_list = []

    print()
    print('Normalized stalls:')
    for op_name in sorted(cnt_dict.keys()):
        stall_cnt = cnt_dict[op_name][0]['stall']
        print(op_name, str(stall_cnt))

        if stall_cnt < min_stall:
            min_stall = stall_cnt
            bottleneck_op = op_name
    print()
    print("bottleneck_op: ")
    print(bottleneck_op, min_stall)

    # The idea of having a bottleneck_op_list instead of a single bottleneck_op is to 
    # explore more in NoC ver. as the compile time is shorter.
    for op_name in cnt_dict:
        stall_cnt = cnt_dict[op_name][0]['stall']

        if stall_cnt*(1-error_margin) <= min_stall:
            bottleneck_op_list.append((op_name,stall_cnt))
    print()
    print("bottleneck_op_list: ")
    print(sorted(bottleneck_op_list, key=lambda x: x[1]))


    if overlay_type == 'NoC':
        cur_param_dict = prev_param_dict
        cur_idx_dict = prev_idx_dict
        operator_list = merge_op_list(benchmark)
        params_search_space_dict = None
        params_annotate_dict = None

        cur_param_dict, is_NoC_bot_addressed = update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, operator_list, cnt_dict, cur_idx_dict, \
                                                                               params_search_space_dict, params_annotate_dict, error_margin)
