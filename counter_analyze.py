import json
from pr_flow.p23_pblock import pblock_page_dict
import argparse
import sys, os
import re

# num_cnt_read = 60

# Helper functions stolen from runtime.py
def return_operator_io_argument_dict_local(operator_list, benchmark):
    # operator_list = operators.split()
    operator_arg_dict = {}
    for operator in operator_list:
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

def check_visited(overlay_type, operator, param_to_tune, new_param_val):
    if overlay_type == 'NoC':
        param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/") \
                                if ( ( x.startswith('NoC_succ_param_') or \
                                       x.startswith('mono_succ_param_') or \
                                       x.startswith('NoC_timing_param_') ) \
                                and x.endswith('.json') )]
        # param_fail_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/") \
        #                         if ( x.startswith('NoC_timing_param_') and x.endswith('.json') )]
    else: # In monolithic ver., don't care about failed parameters in NoC ver.
        param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/") \
                                if ( ( x.startswith('NoC_succ_param_') or \
                                       x.startswith('mono_succ_param_') or \
                                       x.startswith('mono_fail_param_') ) \
                                and x.endswith('.json') )]
        # param_fail_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/") \
        #                         if ( x.startswith('mono_fail_param_') and x.endswith('.json') )]

    for param_file in param_file_list:
        with open("./input_src/" + benchmark + "/params/visited/" + param_file, "r") as infile:
            param_dict = json.load(infile)
        if param_to_tune == 'kernel_clk':
            if operator in param_dict.keys():
                # if param_dict[operator]['kernel_clk'] == new_param_val:
                if param_dict[operator]['kernel_clk'] == new_param_val: 
                    return True
        else:
            for operator in param_dict.keys():
                if operator != 'metric':
                    if param_to_tune in param_dict[operator].keys():
                        # The value of parameter variable is the same for all operators.
                        # For example, if rast2_i1's PAR_RAST == 1, rast2_i1's PAR_RAST should be 1 too.
                        # If they want different parameter, the variable name should differ, like PAR_RAST_1 or PAR_RAST_2.
                        # For this reason, for the given param_to_tune, for any operator, 
                        # if new_param_val is already tested, return True.
                        if param_dict[operator][param_to_tune] == new_param_val:
                            return True
    return False


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
def coutner_mono_dict(benchmark, mono_counter_idx_dict):
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

                else:
                    op = mono_op_from_idx(mono_counter_idx_dict, idx)
                    cnt_dict[op][0] = {'stall': counter_val} # stall counter

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
        print(op_name, cnt_dict[op_name])

    assert(int(num_enqueue) == 1)

    return latency, accuracy, cnt_dict


# Returns counter dictionary for the benchmark
# e.g. cnt_dict = coloringFB_1 : 0: {'stall': 117130}, 
#                                3: {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                    9: {'full': 16735, 'empty': 210347}}
#                                4: {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                    9: {'full': 16735, 'empty': 210347}}
# ... 3 and 4 are page_num
def coutner_dict(benchmark, pblock_assign_dict):
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
                if op_name not in cnt_dict:
                    if self_port == 0:
                        cnt_dict[op_name] = {}
                        cnt_dict[op_name][0] = {}
                        cnt_dict[op_name][0]['stall'] = counter_val
                    else:
                        cnt_dict[op_name] = {}
                        cnt_dict[op_name][self_leaf] = {}
                        cnt_dict[op_name][self_leaf][self_port] = {}
                        cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val
                        # print(cnt_dict)

                else:
                    if self_port == 0: # stall_cnt
                        cnt_dict[op_name][0] = {}
                        cnt_dict[op_name][0]['stall'] = counter_val
                    else:
                        if self_leaf not in cnt_dict[op_name]:
                            cnt_dict[op_name][self_leaf] = {}
                            cnt_dict[op_name][self_leaf][self_port] = {}
                            cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val
                        else:
                            if self_port not in cnt_dict[op_name][self_leaf]:
                                cnt_dict[op_name][self_leaf][self_port] = {}
                                cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val
                            else:
                                cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val

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
        print(op_name, cnt_dict[op_name])

    assert(int(num_enqueue) == 1)

    return latency, accuracy, cnt_dict



def prev_param_success_file_idx():
    # NoC_succ_param_*.json and mono_succ_param_*.json share index
    prev_param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/")\
                                 if (x.split('_')[1] == 'succ' and x.split('_')[2] == 'param' and x.endswith('.json'))]
    param_file = ''
    idx_most_recent = len(prev_param_file_list)-1

    for x in prev_param_file_list:
        idx = int(x.split('.')[0].split('_')[-1])
        if idx == idx_most_recent:
            param_file = x
    return param_file, idx_most_recent


def param_fail_file_idx(fail_type):
    prev_param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/")\
                                 if (x.startswith(fail_type + '_param_') and x.endswith('.json'))]
    if len(prev_param_file_list) != 0:
        most_recent_file_name = fail_type + '_param_' + str(len(prev_param_file_list)-1) + '.json'
    else:
        most_recent_file_name = None
    return  most_recent_file_name, len(prev_param_file_list)


# prev_param_dict didn't improve metric or caused timing violation
# Revert to the most recent prev_param and save the current parameter
def revert_cur_param(benchmark, prev_param_dict, prev_idx_dict, overlay_type = None, fail_type = None):
    if fail_type != None:
        # Save current parameters that failed
        if overlay_type == 'NoC':
            assert(fail_type == 'NoC_timing')
            param_file, idx = param_fail_file_idx(fail_type)
            with open('./input_src/' + benchmark + '/params/visited/NoC_timing_idx_dict_' + str(idx) + '.json', 'w') as outfile:
                json.dump(prev_idx_dict, outfile, sort_keys=True, indent=4)
        else:
            assert(overlay_type == 'mono')
            assert(fail_type == 'mono_fail')
            param_file, idx = param_fail_file_idx(fail_type)
            with open('./input_src/' + benchmark + '/params/visited/mono_fail_idx_dict_' + str(idx) + '.json', 'w') as outfile:
                json.dump(prev_idx_dict, outfile, sort_keys=True, indent=4)        

        with open('./input_src/' + benchmark + '/params/visited/' + fail_type + '_param_' + str(idx) + '.json', 'w') as outfile:
            json.dump(prev_param_dict, outfile, sort_keys=True, indent=4)


        # Revert
        param_success_file, idx_most_recent = prev_param_success_file_idx()
        if idx_most_recent != -1:
            if param_success_file.startswith('NoC_succ'):
                overlay_type_success = 'NoC'
            else:
                overlay_type_success = 'mono'

            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_idx_dict_' + str(idx_most_recent) + '.json', 'r') as infile:
                reverted_idx_dict = json.load(infile)
            os.system('rm ./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_idx_dict_' + str(idx_most_recent) + '.json')

            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_param_' + str(idx_most_recent) + '.json', 'r') as infile:
                reveretd_cur_param_dict = json.load(infile)
            os.system('rm ./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_param_' + str(idx_most_recent) + '.json')

            os.system('mv ./input_src/' + benchmark + '/params/visited/results_' + str(idx_most_recent) + '.txt ' + \
                         './_bi_results/' + benchmark + '/results.txt')
            os.system('mv ./input_src/' + benchmark + '/params/visited/summary_' + str(idx_most_recent) + '.csv ' + \
                         './_bi_results/' + benchmark + '/summary.csv')

            return reveretd_cur_param_dict, reverted_idx_dict, overlay_type_success
 
        else: # If the first NoC ver. failed in timing or if the first monolithic ver. failed in implementation
            print("First run failed")
            # pblock_assign_dict = None
            # if os.path.isfile("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json"):
            #     with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
            #         pblock_assign_dict = json.load(infile)
            return prev_param_dict, prev_idx_dict, overlay_type
    else:
        param_success_file, idx_most_recent = prev_param_success_file_idx()
        if idx_most_recent != -1:
            # Revert
            if param_success_file.startswith('NoC_succ'):
                overlay_type_success = 'NoC'
            else:
                assert(param_success_file.startswith('mono_succ'))
                overlay_type_success = 'mono'

            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_idx_dict_' + str(idx_most_recent) + '.json', 'r') as infile:
                reverted_idx_dict = json.load(infile)
            os.system('rm ./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_idx_dict_' + str(idx_most_recent) + '.json')

            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_param_' + str(idx_most_recent) + '.json', 'r') as infile:
                reveretd_cur_param_dict = json.load(infile)
            os.system('rm ./input_src/' + benchmark + '/params/visited/' + overlay_type_success + '_succ_param_' + str(idx_most_recent) + '.json')

            os.system('mv ./input_src/' + benchmark + '/params/visited/results_' + str(idx_most_recent) + '.txt ' + \
                         './_bi_results/' + benchmark + '/tmp_results.txt')
            os.system('mv ./input_src/' + benchmark + '/params/visited/summary_' + str(idx_most_recent) + '.csv ' + \
                         './_bi_results/' + benchmark + '/tmp_summary.csv')

            # Save current results, which were successful but didn't improve performance

            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type + '_succ_idx_dict_' + str(idx_most_recent) + '.json', 'w') as outfile:
                json.dump(prev_idx_dict, outfile, sort_keys=True, indent=4)
            with open('./input_src/' + benchmark + '/params/visited/' + overlay_type + '_succ_param_' + str(idx_most_recent) + '.json', 'w') as outfile:
                json.dump(prev_param_dict, outfile, sort_keys=True, indent=4)
            os.system('cp ./_bi_results/' + benchmark + '/results.txt ' + './input_src/' + benchmark + '/params/visited/results_' + str(idx_most_recent) + '.txt')
            os.system('cp ./_bi_results/' + benchmark + '/summary.csv ' + './input_src/' + benchmark + '/params/visited/summary_' + str(idx_most_recent) + '.csv')

            os.system('cp ./_bi_results/' + benchmark + '/tmp_results.txt ./_bi_results/' + benchmark + '/results.txt')
            os.system('cp ./_bi_results/' + benchmark + '/tmp_summary.csv ./_bi_results/' + benchmark + '/summary.csv')
            return reveretd_cur_param_dict, reverted_idx_dict, overlay_type_success
        else:
            raise Exception("The first run should be always better than the default fom value")

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

    print(sorted_backward_connection_list)
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


def update_for_idetical_op(cur_param_dict, bottleneck_op, param):
    if param == 'merged_to_try':
        sender_op, receiver_op = bottleneck_op
        # 1) when identical op is sender_op
        is_identical_op = (len(re.findall('_i\d+$',sender_op)) != 0) # operator name ends with _i{SOME_NUM}
        if is_identical_op:
            base_name = sender_op.replace(re.findall('_i\d+$',sender_op)[0],'')
            base_name = base_name + '_i'
            for op in cur_param_dict.keys():
                if op.startswith(base_name):
                    cur_param_dict[op][param] = receiver_op
        # 2) when identical op is receiver_op
        is_identical_op = (len(re.findall('_i\d+$',receiver_op)) != 0) # operator name ends with _i{SOME_NUM}
        if is_identical_op:
            base_name = receiver_op.replace(re.findall('_i\d+$',receiver_op)[0],'')
            base_name = base_name + '_i'
            for op in cur_param_dict.keys():
                if op.startswith(base_name) and op != receiver_op:
                    cur_param_dict[op][param] = receiver_op
    else:
        new_param_val = cur_param_dict[bottleneck_op][param]
        is_identical_op = (len(re.findall('_i\d+$',bottleneck_op)) != 0) # operator name ends with _i{SOME_NUM}
        if is_identical_op:
            base_name = bottleneck_op.replace(re.findall('_i\d+$',bottleneck_op)[0],'')
            base_name = base_name + '_i'
            for op in cur_param_dict.keys():
                # identical ops and not merged to anything
                if op.startswith(base_name) and 'merged_to' not in cur_param_dict[op].keys():
                    cur_param_dict[op][param] = new_param_val
    return cur_param_dict



def update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, operator_list, cnt_dict, cur_idx_dict, params_search_space_dict, params_annotate_dict):
    # For each link in the graph, full_diff = sender's full cnt - receiver's full cnt
    #     => if the link's full_diff is large, NoC could be bottleneck
    # For each link in the graph, empty_diff = receiver's empty_cnt - sender's empty_cnt
    #     => if the link's empty_diff is large, NoC could be bottleneck

    # operator_list = list(prev_page_assign_dict.keys())
    # # print(operator_list)

    operator_arg_dict = return_operator_io_argument_dict_local(operator_list, benchmark)
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

    print("cnt_dict:")
    print(cnt_dict)
    # cnt_dict[op_name][self_leaf][self_port][counter_type] = counter_val


    for connection in connection_list:
        if 'DMA.' not in connection:
            print(connection)
            sender_op = connection.split('->')[0].split('.')[0]
            sender_output_port = connection.split('->')[0].split('.')[1]
            receiver_op = connection.split('->')[1].split('.')[0]
            receiver_input_port = connection.split('->')[1].split('.')[1]

            sender_output_port_num = get_port_num(sender_op, sender_output_port, cur_idx_dict)
            sender_page_num = get_page_num(sender_op, sender_output_port, cur_idx_dict)
            sender_full_cnt = cnt_dict[sender_op][sender_page_num][sender_output_port_num]['full']

            receiver_input_port_num = get_port_num(receiver_op, receiver_input_port, cur_idx_dict)
            receiver_page_num = get_page_num(receiver_op, receiver_input_port, cur_idx_dict)
            receiver_full_cnt = cnt_dict[receiver_op][receiver_page_num][receiver_input_port_num]['full']
            full_diff = sender_full_cnt - receiver_full_cnt

            sender_empty_cnt = cnt_dict[sender_op][sender_page_num][sender_output_port_num]['empty']
            receiver_empty_cnt = cnt_dict[receiver_op][receiver_page_num][receiver_input_port_num]['empty']
            empty_diff = receiver_empty_cnt - sender_empty_cnt

            connection_diff_dict[connection] = (full_diff, empty_diff)

    print()
    print("connection_diff_dict: ")
    print(connection_diff_dict)

    operator_list_no_merge = no_merge_op_list(benchmark)
    operator_arg_dict_no_merge = return_operator_io_argument_dict_local(operator_list_no_merge, benchmark)
    operator_var_dict_no_merge = return_operator_inst_dict_local(operator_list_no_merge, benchmark, 'top_no_merge.cpp')
    connection_list_no_merge = return_operator_connect_list_local(operator_arg_dict_no_merge, operator_var_dict_no_merge)
    # sorted_backward_op_list is all operators without merge
    sorted_backward_op_list = sorted_op_list_backward(operator_list_no_merge, connection_list_no_merge)
    print()
    print("sorted_backward_op_list: ")
    print(sorted_backward_op_list)
    connection_list_sorted = sort_connection_list_backward(connection_list, sorted_backward_op_list)
    print()
    print("connection_list_sorted: ")
    print(connection_list_sorted)

    print()
    print("potential erroneous connections with NoC bottleneck:")
    for connection_list in connection_list_sorted:
        for connection in connection_list:
            full_diff, empty_diff = connection_diff_dict[connection]
            if (full_diff > 0 or empty_diff > 0): # NoC bandwidth could be bottleneck
                print("> " + str(connection))
    print()

    is_NoC_bot_addressed = False
    # If NoC is bottleneck, perform only one change at a time
    for connection_list in connection_list_sorted:
        for connection in connection_list:
            full_diff, empty_diff = connection_diff_dict[connection]
            if (full_diff > 0 or empty_diff > 0) and is_NoC_bot_addressed == False: # One step at a time when resolving NoC bottleneck

                print("fix this connection: " + str(connection))
                # Increase sender's num_leaf_interface
                sender_op = connection.split('->')[0].split('.')[0]
                num_sender_output = len([port for port in operator_arg_dict[sender_op] if port.startswith('Output_')])
                cur_sender_num_leaf_interface = cur_param_dict[sender_op]["num_leaf_interface"]
                if cur_sender_num_leaf_interface < 4 and num_sender_output > 2:
                    cur_param_dict[sender_op]["num_leaf_interface"] = 4 
                    cur_param_dict = update_for_idetical_op(cur_param_dict, sender_op, "num_leaf_interface")
                    is_NoC_bot_addressed = True
                if cur_sender_num_leaf_interface < 2 and num_sender_output > 1:
                    cur_param_dict[sender_op]["num_leaf_interface"] = 2 
                    cur_param_dict = update_for_idetical_op(cur_param_dict, sender_op, "num_leaf_interface")
                    is_NoC_bot_addressed = True

                # Increase receiver's num_leaf_interface
                receiver_op = connection.split('->')[1].split('.')[0]
                num_receiver_input = len([port for port in operator_arg_dict[receiver_op] if port.startswith('Input_')])
                cur_receiver_num_leaf_interface = cur_param_dict[receiver_op]["num_leaf_interface"]
                if cur_receiver_num_leaf_interface < 4 and num_receiver_input > 2:
                    cur_param_dict[receiver_op]["num_leaf_interface"] = 4 
                    cur_param_dict = update_for_idetical_op(cur_param_dict, receiver_op, "num_leaf_interface")
                    is_NoC_bot_addressed = True
                if cur_receiver_num_leaf_interface < 2 and num_receiver_input > 1:
                    cur_param_dict[receiver_op]["num_leaf_interface"] = 2 
                    cur_param_dict = update_for_idetical_op(cur_param_dict, receiver_op, "num_leaf_interface")
                    is_NoC_bot_addressed = True

                # NoC bottleneck exists, and 
                #   1) can't resolve it by increasing num_leaf_interface and
                #   2) the sender_op has not been merged to other ops yet
                #   3) the sender_op's param reached to max

                params_sender_op = cur_param_dict[sender_op].keys()
                param_for_lat_list = [] # list of sender_op's param that can improve latency
                for param in params_sender_op:
                    if param in params_annotate_dict: # except kernel_clk, num_leaf_interface, merged_to
                        effect_list = params_annotate_dict[param] # e.g. ["latency", "accuracy", ...]
                    else:
                        effect_list = []
                    if 'latency' in effect_list:
                        param_for_lat_list.append(param)

                is_reached_max = True
                for param in param_for_lat_list:
                    param_search_space = params_search_space_dict[param] # e.g. [1,2,4]
                    cur_param_val = cur_param_dict[sender_op][param] # e.g. 2
                    if cur_param_val != param_search_space[-1]:
                        is_reached_max = False

                if "merged_to" not in cur_param_dict[sender_op].keys() and is_reached_max and is_NoC_bot_addressed == False:
                    cur_param_dict[sender_op]["merged_to_try"] = receiver_op
                    cur_param_dict = update_for_idetical_op(cur_param_dict, (sender_op, receiver_op), "merged_to_try")
                    is_NoC_bot_addressed = True
    return cur_param_dict, is_NoC_bot_addressed



def update_cur_param(benchmark, overlay_type, prev_param_dict, cnt_dict, accuracy, error_margin, prev_idx_dict):
    # Load previous parameter dictionary and will update this
    cur_param_dict = prev_param_dict
    cur_idx_dict = prev_idx_dict
    operator_list = merge_op_list(benchmark)
    # operator_list is all ops without merging
    # operator_list = list(prev_param_dict.keys())
    # operator_list.remove("metric")

    with open('./input_src/' + benchmark + '/params_annotate.json', 'r') as infile:
        params_annotate_dict = json.load(infile)
    # e.g. params_annotate_dict = { "PAR_FACTOR": ["latency"],
    #                               "K_CONST": ["accuracy"]}

    with open('./input_src/' + benchmark + '/params.json', 'r') as infile:
        params_search_space_dict = json.load(infile)
    # print(params_search_space_dict)
    if "MIN_ACCURACY" in params_search_space_dict:
        minimum_accuracy = float(params_search_space_dict["MIN_ACCURACY"])
    else:
        minimum_accuracy = -1

    ###############################
    ## Bottleneck identification ##
    ###############################
    min_stall = sys.maxsize
    bottleneck_op = None
    bottleneck_op_list = []
    print()
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

        if stall_cnt*(1-error_margin) < min_stall:
            bottleneck_op_list.append((op_name,stall_cnt))
    print()
    print("bottleneck_op_list: ")
    print(sorted(bottleneck_op_list, key=lambda x: x[1]))


    #############################################
    ## Check whether NoC is bottleneck or not. ## ==> update cur_param_dict
    #############################################
    if overlay_type == 'NoC':
        cur_param_dict, is_NoC_bot_addressed = update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, operator_list, cnt_dict, cur_idx_dict, \
                                                                               params_search_space_dict, params_annotate_dict)
    else:
        is_NoC_bot_addressed = False
    # print(cur_param_dict)

    if minimum_accuracy != -1: # Benchmarks that have accuracy metric like Digit Recognition, Optical Flow, etc
        if accuracy < minimum_accuracy:
            metric = "accuracy"
        else:
            if is_NoC_bot_addressed: 
                metric = 'NoC_bottleneck'
            else: 
                metric = "latency"
    else:
        if is_NoC_bot_addressed: 
            metric = 'NoC_bottleneck'
        else: 
            metric = "latency"
    print()
    print("metric: " + metric)
    print()
    cur_param_dict['metric'] = metric

    ######################
    ## Parameter tuning ## ==> update cur_param_dict and save cur_param_dict.json
    ######################
    # - Explore parameter to improve accuracy first, and then improve other metrics like latency 
    # - Incrementally explore param like par factor first, and then increase kernel clk
    if metric == "accuracy":
        param_to_tune, new_param_val = None, None
        param_for_acc_list = []
        for param in params_annotate_dict.keys():
            effect_list = params_annotate_dict[param] # e.g. ["latency", "accuracy", ...]
            if "accuracy" in effect_list:
                param_for_acc_list.append(param)

        for param_acc in param_for_acc_list:
            if param_to_tune == None and new_param_val == None:
                op_accuracy = None
                found = False
                # Greedily increment this parameter for accuracy
                for op in cur_param_dict.keys():
                    if op != 'metric':
                        if (not found) and (param_acc in cur_param_dict[op].keys()):
                            op_accuracy = op # any operator that's holding this param_acc
                            cur_param_val = cur_param_dict[op_accuracy][param_acc]
                            found = True
                param_search_space = params_search_space_dict[param_acc]
                if cur_param_val != param_search_space[-1]:
                    # param_to_tune = param_acc
                    # new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
                    # if check_visited(op_accuracy, param_to_tune, new_param_val):
                    #     param_to_tune = None
                    #     new_param_val = None
                    idx = param_search_space.index(cur_param_val) + 1 # next param
                    found = False
                    while idx < len(param_search_space) and found == False:
                        param_to_tune = param_acc
                        new_param_val = param_search_space[idx]
                        if check_visited(overlay_type, op_accuracy, param_to_tune, new_param_val):
                            param_to_tune = None
                            new_param_val = None
                            idx = idx + 1
                        else:
                            found = True
        print(">> param_to_tune(accuracy): " + str(param_to_tune))
        print(">> new_param_val: " + str(new_param_val))
        print()
        # Update cur_param for the incremental refinement
        if param_to_tune != None and new_param_val != None:
            assert(param_to_tune != 'kernel_clk')
            assert(param_to_tune != 'num_leaf_interface')            
            # Update for all other ops if they have param_to_tune because
            # if param variable names are the same, the values are consistent accross operators
            for op in cur_param_dict.keys():
                if op != 'metric':
                    if param_to_tune in cur_param_dict[op]:
                        cur_param_dict[op][param_to_tune] = new_param_val
            print(cur_param_dict)

            with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
            return False, metric
        else:
            with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
            return True, metric

    else:
        # For now, we use one compile run just for resolving NoC bottleneck
        if is_NoC_bot_addressed:
            with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)            
            return False, metric
        else:
            assert(metric == "latency")
            param_to_tune, new_param_val = None, None
            param_for_lat_list = []
            for param in params_annotate_dict.keys():
                effect_list = params_annotate_dict[param] # e.g. ["latency", "accuracy", ...]
                if "latency" in effect_list:
                    param_for_lat_list.append(param)

            for bottleneck_op, stall_cnt in sorted(bottleneck_op_list, key=lambda x: x[1]):
                # Prioritize non-"kernel_clk" parameters
                for param in sorted(cur_param_dict[bottleneck_op].keys()): # sorted for deterministic refinement
                    if param in param_for_lat_list:
                    # if param != "num_leaf_interface" and param != "kernel_clk":
                        param_search_space = params_search_space_dict[param] # e.g. [1,2,4]
                        cur_param_val = cur_param_dict[bottleneck_op][param] # e.g. 2
                        # print(param)
                        # print(cur_param_val)
                        # print(param_search_space)
                        if cur_param_val != param_search_space[-1]:
                            idx = param_search_space.index(cur_param_val) + 1 # next param
                            found = False
                            while idx < len(param_search_space) and found == False:
                                param_to_tune = param
                                new_param_val = param_search_space[idx]
                                if check_visited(overlay_type, bottleneck_op, param_to_tune, new_param_val):
                                    param_to_tune = None
                                    new_param_val = None
                                    idx = idx + 1
                                else:
                                    found = True

                # Explore kernel_clk
                if param_to_tune == None and new_param_val == None:
                    param_search_space = params_search_space_dict["kernel_clk"] # [200, 250, 300, 350, 400]
                    cur_param_val = cur_param_dict[bottleneck_op]["kernel_clk"] # e.g. 200
                    if cur_param_val != param_search_space[-1]:
                        idx = param_search_space.index(cur_param_val) + 1 # next param
                        found = False
                        while idx < len(param_search_space) and found == False:
                            param_to_tune = 'kernel_clk'
                            new_param_val = param_search_space[idx]
                            if check_visited(overlay_type, bottleneck_op, param_to_tune, new_param_val):
                                param_to_tune = None
                                new_param_val = None
                                idx = idx + 1
                            else:
                                found = True

                if param_to_tune != None and new_param_val != None:
                    break

            print()
            print(">> bottleneck_op: " + str(bottleneck_op))
            print(">> param_to_tune: " + str(param_to_tune))
            print(">> new_param_val: " + str(new_param_val))
            print()
            # Update cur_param for the incremental refinement
            if param_to_tune != None and new_param_val != None:
                # For kernel_clk, update one operator at a time
                if param_to_tune == "kernel_clk":
                    cur_param_dict[bottleneck_op][param_to_tune] = new_param_val
                    cur_param_dict = update_for_idetical_op(cur_param_dict, bottleneck_op, 'kernel_clk')
                else:
                    # Update for all other ops if they have param_to_tune because
                    # if param variable names are the same, the values are consistent accross operators
                    for op in cur_param_dict.keys():
                        if op != 'metric':
                            if param_to_tune != "num_leaf_interface" and \
                               param_to_tune in cur_param_dict[op]:
                                cur_param_dict[op][param_to_tune] = new_param_val
                    print(cur_param_dict)

                with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                    json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
                return False, metric
            else:
                with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                    json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
                return True, metric


# Save cur_param.json, results.txt, summary.csv, pblock_assignment.json(if NoC ver.) / mono_counter_idx_dict.json(if mono ver.)
def save_prev_param(benchmark, prev_param_dict, prev_idx_dict, prev_overlay_type):
    param_success_file, idx_most_recent = prev_param_success_file_idx()
    idx = idx_most_recent + 1

    with open('./input_src/' + benchmark + '/params/visited/' + prev_overlay_type + '_succ_idx_dict_' + str(idx) + '.json', 'w') as outfile:
        json.dump(prev_idx_dict, outfile, sort_keys=True, indent=4)        

    with open('./input_src/' + benchmark + '/params/visited/' + prev_overlay_type + '_succ_param_' + str(idx) + '.json', 'w') as outfile:
        json.dump(prev_param_dict, outfile, sort_keys=True, indent=4)
    os.system('cp ./_bi_results/' + benchmark + '/results.txt ' + \
                 './input_src/' + benchmark + '/params/visited/results_' + str(idx) + '.txt')

    os.system('cp ./_bi_results/' + benchmark + '/summary.csv ' + \
                 './input_src/' + benchmark + '/params/visited/summary_' + str(idx) + '.csv')


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


    # Previous run failed
    if is_NoC_timing_violate or is_monolithic_fail:
        if is_NoC_timing_violate: 
            fail_type = 'NoC_timing'
            overlay_type = 'NoC'
            with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
                prev_idx_dict = json.load(infile)
        else:
            fail_type = 'mono_fail'
            overlay_type = 'mono'
            with open("./workspace/F007_mono_" + benchmark + "/mono_counter_idx_dict.json", "r") as infile:
                prev_idx_dict = json.load(infile)

        prev_param_dict, prev_idx_dict, prev_overlay_type = revert_cur_param(benchmark, prev_param_dict, prev_idx_dict,
                                                                             overlay_type = overlay_type, fail_type = fail_type)
        print("Param, reverted")
        print(prev_param_dict)

        save_prev_param(benchmark, prev_param_dict, prev_idx_dict, prev_overlay_type)

        if prev_overlay_type == 'NoC':
            latency, accuracy, cnt_dict = coutner_dict(benchmark, prev_idx_dict) # use reverted summary.csv
        else:
            latency, accuracy, cnt_dict = coutner_mono_dict(benchmark, prev_idx_dict) # use reverted summary.csv

        no_valid_param, metric = update_cur_param(benchmark, overlay_type, prev_param_dict, cnt_dict, accuracy, error_margin, prev_idx_dict)

    # Previous run was successful
    else:
        best_latency = get_best_latency(benchmark)
        # print(best_latency)
        # print(latency)

        if is_NoC_success: 
            overlay_type = 'NoC'
            with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
                prev_idx_dict = json.load(infile)
            latency, accuracy, cnt_dict = coutner_dict(benchmark, prev_idx_dict)
        else:
            assert(is_monolithic_success == True)
            overlay_type = 'mono'
            with open("./workspace/F007_mono_" + benchmark + "/mono_counter_idx_dict.json", "r") as infile:
                prev_idx_dict = json.load(infile)
            latency, accuracy, cnt_dict = coutner_mono_dict(benchmark, prev_idx_dict) 

        # print(latency, accuracy)
        # print(cnt_dict)


        min_stall = sys.maxsize
        bottleneck_op = None
        bottleneck_op_list = []
        print()
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

            if stall_cnt*(1-error_margin) < min_stall:
                bottleneck_op_list.append((op_name,stall_cnt))
        print()
        print("bottleneck_op_list: ")
        print(sorted(bottleneck_op_list, key=lambda x: x[1]))


        # If previous run didn't improve the latency, revert and save the previous param
        if prev_param_dict['metric'] == "latency" and latency*(1-error_margin) > best_latency:
            prev_param_dict, prev_idx_dict, prev_overlay_type = revert_cur_param(benchmark, prev_param_dict, prev_idx_dict,
                                                                                 overlay_type = overlay_type, fail_type = None)
            print("Param, reverted")
            print(prev_param_dict)
            save_prev_param(benchmark, prev_param_dict, prev_idx_dict, prev_overlay_type)

        # If previous run was to improve accuracy or
        # if previous run improved the latency, save the previous param
        else:
            save_prev_param(benchmark, prev_param_dict, prev_idx_dict, overlay_type)
            if latency < best_latency:
                # Update the best latency
                with open('./input_src/' + benchmark + '/params/best.txt', 'w') as outfile:
                    outfile.write(str(latency))

        no_valid_param, metric = update_cur_param(benchmark, overlay_type, prev_param_dict, cnt_dict, accuracy, error_margin, prev_idx_dict)


    # Touch status flag
    if overlay_type == 'NoC':
        if no_valid_param:
            print('Can not improve ' + str(metric) + ' anymore in NoC version. Move to monolithic!')
            os.system('touch ./input_src/' + benchmark + '/__NoC_done__')
        else:
            print('>> NoC version: Next parameter is generated!')
    else:
        assert(overlay_type == 'mono')
        if no_valid_param:
            print('Can not improve ' + str(metric) + ' anymore in monolithic version.')
            os.system('touch ./input_src/' + benchmark + '/__mono_done__')
        else:
            print('>> Monolithic version: Next parameter is generated!')