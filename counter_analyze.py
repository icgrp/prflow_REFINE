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
def return_operator_inst_dict_local(operator_list, benchmark):
    # operator_list = operators.split()
    operator_var_dict = {}
    with open('./input_src/'+benchmark+'/host/top.cpp', 'r') as infile:
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


def get_port_num(io_port):
    if io_port.startswith('Input_'):
        idx = int(io_port.split('_')[1]) + 1
        return idx
    else:
        assert(io_port.startswith('Output_'))
        idx = int(io_port.split('_')[1]) + 8
        return idx


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

def checked_visited(operator, param_to_tune, new_param_val):
    param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/") if x.endswith('.json')]
    for param_file in param_file_list:
        with open("./input_src/" + benchmark + "/params/visited/" + param_file, "r") as infile:
            param_dict = json.load(infile)
        if param_to_tune == 'kernel_clk':
            if operator in param_dict.keys():
                if param_dict[operator]['kernel_clk'] == new_param_val:
                    return True
        else:
            for operator in param_dict.keys():
                # The value of parameter variable is the same for all operators.
                # For example, if rast2_i1's PAR_RAST == 1, rast2_i1's PAR_RAST should be 1 too.
                # If they want different parameter, the variable name should differ, like PAR_RAST_1 or PAR_RAST_2.
                # For this reason, for the given param_to_tune, for any operator, 
                # if new_param_val is already tested, return True.
                if param_dict[operator][param_to_tune] == new_param_val:
                    return True
    return False


def prev_param_idx():
    prev_param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/")\
                                 if (x.startswith('prev_param_') and x.endswith('.json'))]
    return len(prev_param_file_list)

def timing_prev_param_idx():
    prev_param_file_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/")\
                                 if (x.startswith('timing_prev_param_') and x.endswith('.json'))]
    return len(prev_param_file_list)

# Returns counter dictionary for the benchmark
# e.g. cnt_dict = coloringFB_1 : {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
#                                 0: {'stall': 117130}, 
#                                 9: {'full': 16735, 'empty': 210347}}
# ...
def coutner_dict(benchmark, result_file, page_assign_dict):
    cnt_dict = {}
    accuracy = 0

    with open("./_bi_results/" + benchmark + "/" + result_file, "r") as infile:
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
                # print(counter)
                # print(self_leaf)
                # print(op_name)
                # print(counter_val)
                # print(line)
                if op_name not in cnt_dict:
                    cnt_dict[op_name] = {}
                    cnt_dict[op_name][self_port] = {}
                    cnt_dict[op_name][self_port][counter_type] = counter_val
                    # print(cnt_dict)

                else:
                    if self_port not in cnt_dict[op_name]:
                        cnt_dict[op_name][self_port] = {}
                        cnt_dict[op_name][self_port][counter_type] = counter_val
                    else:
                        cnt_dict[op_name][self_port][counter_type] = counter_val

            if line.startswith('elapsed time: '):
                latency = line.split()[2]
            if line.startswith('accuracy: '):
                accuracy = line.split()[2]
            if line.startswith('TEST PASSED'):
                print(latency)
                print(accuracy)

                # print(cnt_dict)
                for op_name in sorted(cnt_dict):
                    print(op_name, cnt_dict[op_name])
        # print()

        return latency, accuracy, cnt_dict


# def gen_next_param(benchmark, cur_param_dict, bottleneck_op, metric = "latency"):
#     with open('./input_src/' + benchmark + '/params_annotate.json', 'r') as infile:
#         params_annotate_dict = json.load(infile)
#     # e.g. params_annotate_dict = { "PAR_RAST": ["latency", "timing"],
#     #                               "PAR_ZCULLING": ["latency", "timing"]}

#     with open('./input_src/' + benchmark + '/params.json', 'r') as infile:
#         params_dict = json.load(infile)
#     # print(params_dict)

#     param_to_tune, new_param_val = None, None

#     # Prioritize non-"kernel_clk" parameters
#     for param in sorted(cur_param_dict[bottleneck_op].keys()): # sorted for deterministic refinement
#         if (param != "num_leaf_interface") and \
#            (param != "kernel_clk") and \
#            (metric in params_annotate_dict[param]): # if this parameter is helping current metric
#             param_search_space = params_dict[bottleneck_op][param] # e.g. [1,2,4]
#             cur_param_val = cur_param_dict[bottleneck_op][param] # e.g. 2
#             if cur_param_val != param_search_space[-1]:
#                 param_to_tune = param
#                 new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
#                 if checked_visited(bottleneck_op, param_to_tune, new_param_val):
#                     param_to_tune = None # reset, already tested
#                     new_param_val = None # reset, already tested

#     # Explore kernel_clk
#     if param_to_tune != None and new_param_val != None:
#         param_search_space = params_dict[bottleneck_op]["kernel_clk"] # e.g. [200, 250, 300, 350, 400]
#         cur_param_val = cur_param_dict[bottleneck_op]["kernel_clk"] # e.g. 200
#         if cur_param_val != param_search_space[-1] and metric == "latency": # increase kernel clk
#             param_to_tune = "kernel_clk"
#             new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
#             if checked_visited(bottleneck_op, param_to_tune, new_param_val):
#                 param_to_tune = None # reset, already tested
#                 new_param_val = None # reset, already tested
#         elif cur_param_val != param_search_space[0] and metric == "timing": # decrease kernel clk
#             param_to_tune = "kernel_clk"
#             new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
#             if checked_visited(bottleneck_op, param_to_tune, new_param_val):
#                 param_to_tune = None # reset, already tested
#                 new_param_val = None # reset, already tested
#     return param_to_tune, new_param_val

# def is_improved(benchmark, metric, fom):
#     with open('./input_src/' + benchmark + '/params/best.txt', 'r') as infile:
#         best_fom = infile.read()
#     if metric == "latency":
#         if fom < best_fom: # the lower, the better
#             return True
#     elif metric == "accuracy":
#         if fom > best_fom: # the higher, the better
#             return True
#     else:
#         raise Exception("metric: " + metric + ", unsupported")
#     return False


# cur_param_dict didn't improve metric or caused timing violation
# Revert to the most recent prev_param
def revert_cur_param(benchmark, cur_param_dict, cur_pblock_assign_dict, is_timing_violate = False):
    if is_timing_violate:
        idx = timing_prev_param_idx()
        with open('./input_src/' + benchmark + '/params/visited/timing_prev_param_' + str(idx) + '.json', 'w') as outfile:
            json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
        with open('./input_src/' + benchmark + '/params/visited/timing_prev_pblock_assignment_' + str(idx) + '.json', 'w') as outfile:
            json.dump(cur_pblock_assign_dict, outfile, sort_keys=True, indent=4)

        if prev_param_idx() != 0:
            idx_most_recent = prev_param_idx() - 1
            with open('./input_src/' + benchmark + '/params/visited/prev_param_' + str(idx_most_recent) + '.json', 'r') as infile:
                reveretd_cur_param_dict = json.load(infile)
            with open('./input_src/' + benchmark + '/params/visited/prev_pblock_assignment_' + str(idx_most_recent) + '.json', 'r') as infile:
                reverted_pblock_assign_dict = json.load(infile)

            return reveretd_cur_param_dict, reverted_pblock_assign_dict
 
        else: # if the first run violates timing
            with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
                pblock_assign_dict = json.load(infile)
            return cur_param_dict, pblock_assign_dict
    else:
        if prev_param_idx() != 0:
            idx_most_recent = prev_param_idx() - 1
            with open('./input_src/' + benchmark + '/params/visited/prev_param_' + str(idx_most_recent) + '.json', 'r') as infile:
                reveretd_cur_param_dict = json.load(infile)
            with open('./input_src/' + benchmark + '/params/visited/prev_pblock_assignment_' + str(idx_most_recent) + '.json', 'r') as infile:
                reverted_pblock_assign_dict = json.load(infile)

            with open('./input_src/' + benchmark + '/params/visited/prev_param_' + str(idx_most_recent) + '.json', 'w') as outfile:
                json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
            with open('./input_src/' + benchmark + '/params/visited/prev_pblock_assignment_' + str(idx_most_recent) + '.json', 'w') as outfile:
                json.dump(cur_pblock_assign_dict, outfile, sort_keys=True, indent=4)

            return reveretd_cur_param_dict, reverted_pblock_assign_dict
        else:
            raise Exception("The first run should be always better than the default fom value")



def update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, cur_page_assign_dict, cnt_dict):
    #############################################
    ## Check whether NoC is bottleneck or not. ## ==> update cur_param_dict.json
    #############################################
    # For each link in the graph, full_diff = sender's full cnt - receiver's full cnt
    #     => if the link's full_diff is large, NoC could be bottleneck
    # For each link in the graph, empty_diff = receiver's empty_cnt - sedner's empty_cnt
    #     => if the link's empty_diff is large, NoC could be bottleneck
    # Thus, take average of full_diff and empty_diff 

    operator_list = list(cur_page_assign_dict.keys())
    # print(operator_list)

    operator_arg_dict = return_operator_io_argument_dict_local(operator_list, benchmark)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': ['Input_1', 'Output_1' .. }

    operator_var_dict = return_operator_inst_dict_local(operator_list, benchmark)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...
    # print(operator_arg_dict)
    # print(operator_var_dict)

    connection_list = return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    # print(connection_list)

    connection_diff_dict = {}
    # 'data_transfer.Output_1->prj_rast1.Input_1': (full_diff, empty_diff)

    for connection in connection_list:
        if 'DMA.' not in connection:
            sender_op = connection.split('->')[0].split('.')[0]
            sender_output_port = connection.split('->')[0].split('.')[1]
            receiver_op = connection.split('->')[1].split('.')[0]
            receiver_input_port = connection.split('->')[1].split('.')[1]

            sender_output_port_num = get_port_num(sender_output_port)
            sender_full_cnt = cnt_dict[sender_op][sender_output_port_num]['full']
            receiver_input_port_num = get_port_num(receiver_input_port)
            receiver_full_cnt = cnt_dict[receiver_op][receiver_input_port_num]['full']
            full_diff = sender_full_cnt - receiver_full_cnt

            sender_empty_cnt = cnt_dict[sender_op][sender_output_port_num]['empty']
            receiver_empty_cnt = cnt_dict[receiver_op][receiver_input_port_num]['empty']
            empty_diff = receiver_empty_cnt - sender_empty_cnt

            connection_diff_dict[connection] = (full_diff, empty_diff)

    print()
    print("connection_diff_dict: ")
    print(connection_diff_dict)

    # Increase num_leaf_interface if NoC is bottleneck
    for connection in connection_diff_dict:
        full_diff, empty_diff = connection_diff_dict[connection]
        if full_diff > 0 or empty_diff > 0: # NoC bandwidth could be bottleneck
            # print(connection)
            # Increase sender's num_leaf_interface
            sender_op = connection.split('->')[0].split('.')[0]
            num_sender_output = len([port for port in operator_arg_dict[sender_op] if port.startswith('Output_')])
            cur_sender_num_leaf_interface = cur_param_dict[sender_op]
            if cur_sender_num_leaf_interface == 1 and num_sender_output > 1:
                cur_param_dict[sender_op]["num_leaf_interface"] = 2 
            elif cur_sender_num_leaf_interface == 2 and num_sender_output > 2:
                cur_param_dict[sender_op]["num_leaf_interface"] = 4 

            # Increase sender's num_leaf_interface
            receiver_op = connection.split('->')[1].split('.')[0]
            num_receiver_input = len([port for port in operator_arg_dict[receiver_op] if port.startswith('Input_')])
            cur_sender_num_leaf_interface = cur_param_dict[receiver_op]
            if cur_sender_num_leaf_interface == 1 and num_receiver_input > 1:
                cur_param_dict[receiver_op]["num_leaf_interface"] = 2 
            elif cur_sender_num_leaf_interface == 2 and num_receiver_input > 2:
                cur_param_dict[receiver_op]["num_leaf_interface"] = 4 
    return cur_param_dict


def update_cur_param(benchmark, cur_param_dict, cur_page_assign_dict, cnt_dict, accuracy, minimum_accuracy):

    with open('./input_src/' + benchmark + '/params_annotate.json', 'r') as infile:
        params_annotate_dict = json.load(infile)
    # e.g. params_annotate_dict = { "PAR_FACTOR": ["latency"],
    #                               "K_CONST": ["accuracy"]}

    with open('./input_src/' + benchmark + '/params.json', 'r') as infile:
        params_search_space_dict = json.load(infile)
    # print(params_search_space_dict)

    # Find the bottleneck operator
    min_stall = sys.maxsize
    bottleneck_op = None
    print()
    for op_name in cnt_dict:
        stall_cnt = cnt_dict[op_name][0]['stall']
        print(op_name, str(stall_cnt))

        if stall_cnt < min_stall:
            min_stall = stall_cnt
            bottleneck_op = op_name
    print()
    print("bottleneck_op: ")
    print(bottleneck_op, min_stall)

    cur_param_dict = update_cur_param_NoC_bottleneck(benchmark, cur_param_dict, cur_page_assign_dict, cnt_dict)
    print(cur_param_dict)
    # return False

    if minimum_accuracy != -1: # Benchmarks that have accuracy metric like Digit Recognition, Optical Flow, etc
        if accuracy > minimum_accuracy:
            metric = "accuracy"
        else:
            metric = "latency"
    else:
        metric = "latency"

    ######################
    ## Parameter tuning ## ==> update cur_param_dict.json
    ######################
    # - If param space is all explored or not enough area, them move to monolithic
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
                    if (not found) and (param_acc in cur_param_dict[op].keys()):
                        op_accuracy = op # any operator that's holding this param_acc
                        cur_param_val = cur_param_dict[op_accuracy][param_acc]
                        found = True
                param_search_space = params_search_space_dict[param_acc]
                if cur_param_val != param_search_space[-1]:
                    param_to_tune = param_acc
                    new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
                    if checked_visited(op_accuracy, param_to_tune, new_param_val):
                        param_to_tune = None
                        new_param_val = None

        # # Update cur_param for the incremental refinement
        # if param_to_tune != None and new_param_val != None:
        #     # Update for all other ops if they have param_to_tune because
        #     # if param variable names are the same, the values are consistent accross operators
        #     for op in cur_param_dict.keys():
        #         if param_to_tune in cur_param_dict[op]:
        #             cur_param_dict[op][param_to_tune] = new_param_val

        #     idx = prev_param_idx()
        #     os.system('cp ./input_src/' + benchmark + '/params/cur_param.json ./input_src/' + benchmark + '/params/prev_param_' + str(idx) + '.json')
        #     cur_param_dict[bottleneck_op][param] = new_param_val
        #     with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
        #         json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
        #     return False
        # else:
        #     print("We can't improve accuracy anymore")
        #     return True

    else:
        assert(metric == "latency")

        param_to_tune, new_param_val = None, None
        # Prioritize non-"kernel_clk" parameters
        for param in sorted(cur_param_dict[bottleneck_op].keys()): # sorted for deterministic refinement
            if param != "num_leaf_interface" and param != "kernel_clk":
                param_search_space = params_search_space_dict[param] # e.g. [1,2,4]
                cur_param_val = cur_param_dict[bottleneck_op][param] # e.g. 2
                # print(param)
                # print(cur_param_val)
                # print(param_search_space)
                if cur_param_val != param_search_space[-1]:
                    param_to_tune = param
                    new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
                    if checked_visited(bottleneck_op, param_to_tune, new_param_val):
                        param_to_tune = None
                        new_param_val = None

        # Explore kernel_clk
        if param_to_tune == None and new_param_val == None:
            param_search_space = params_search_space_dict["kernel_clk"] # [200, 250, 300, 350, 400]
            cur_param_val = cur_param_dict[bottleneck_op]["kernel_clk"] # e.g. 200
            if cur_param_val != param_search_space[-1]:
                param_to_tune = "kernel_clk"
                new_param_val = param_search_space[param_search_space.index(cur_param_val) + 1]
                if checked_visited(bottleneck_op, param_to_tune, new_param_val):
                    param_to_tune = None
                    new_param_val = None

        print(param_to_tune)
        print(new_param_val)
        # Update cur_param for the incremental refinement
        if param_to_tune != None and new_param_val != None:
            # Update for all other ops if they have param_to_tune because
            # if param variable names are the same, the values are consistent accross operators
            for op in cur_param_dict.keys():
                if param_to_tune != "num_leaf_interface" and \
                   param_to_tune != "kernel_clk" and \
                   param_to_tune in cur_param_dict[op]:
                    cur_param_dict[op][param_to_tune] = new_param_val
            print(cur_param_dict)

            idx = prev_param_idx()
            os.system('cp ./input_src/' + benchmark + '/params/cur_param.json ' + \
                         './input_src/' + benchmark + '/params/visited/prev_param_' + str(idx) + '.json')

            with open('./input_src/' + benchmark + '/params/cur_param.json', 'w') as outfile:
                json.dump(cur_param_dict, outfile, sort_keys=True, indent=4)
            return False
        else:
            return True


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # args = parser.parse_args()
    # bottleneck = args.bottleneck

    is_timing_violate = False
    op_pblock_not_enough_area = None
    # metric = "latency" # latency, accuracy, timing?
    minimum_accuracy = -1

    benchmark = 'rendering'
    filename = "results.txt"

    with open('./input_src/' + benchmark + '/params/cur_param.json', 'r') as infile:
        cur_param_dict = json.load(infile)

    with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
        cur_pblock_assign_dict = json.load(infile)
    cur_page_assign_dict = get_page_assign_dict(cur_pblock_assign_dict)

    # page_assign_dict = {"rasterization2_m": [12,13,14,15], "data_transfer": [4], ...} # multiple leaf interfaces
    # print(page_assign_dict)

    if is_timing_violate:
        cur_param_dict, cur_pblock_assign_dict = revert_cur_param(benchmark, cur_param_dict, cur_pblock_assign_dict, is_timing_violate = True)
        cur_page_assign_dict = get_page_assign_dict(cur_pblock_assign_dict)

        latency, accuracy, cnt_dict = coutner_dict(benchmark, filename, cur_page_assign_dict) # use old result
        move_to_mono = update_cur_param(benchmark, cur_param_dict, cur_page_assign_dict, cnt_dict, accuracy, minimum_accuracy)

    elif op_pblock_not_enough_area is not None:
        print("Move to monolithic!")
        # return False

    else:

        latency, accuracy, cnt_dict = coutner_dict(benchmark, filename, cur_page_assign_dict)
        print(latency, accuracy)
        print(cnt_dict)

        with open('./input_src/' + benchmark + '/params/best.txt', 'r') as infile:
            best_latency = infile.read()

        if latency > best_latency: # not improved
            cur_param_dict, cur_pblock_assign_dict = revert_cur_param(benchmark, cur_param_dict, cur_pblock_assign_dict, is_timing_violate = False)
            cur_page_assign_dict = get_page_assign_dict(cur_pblock_assign_dict)
        else:
            # Update the best latency
            with open('./input_src/' + benchmark + '/params/best.txt', 'w') as outfile:
                outfile.write(latency)

        move_to_mono = update_cur_param(benchmark, cur_param_dict, cur_page_assign_dict, cnt_dict, accuracy, minimum_accuracy)

    print(move_to_mono)
    # if move_to_mono:
    #     print("Move to monolithic!")
    #     return False
    # else:
    #     return True