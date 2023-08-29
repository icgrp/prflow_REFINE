import json
from pr_flow.p23_pblock import pblock_page_dict
import argparse
import sys
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

def tuner():
    return None

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # args = parser.parse_args()
    # bottleneck = args.bottleneck


    benchmark = 'rendering'
    filename = "results.txt"


    with open("./workspace/F003_syn_" + benchmark + "/pblock_assignment.json", "r") as infile:
        pblock_assign_dict = json.load(infile)
    page_assign_dict = get_page_assign_dict(pblock_assign_dict)
    # page_assign_dict = {"rasterization2_m": [12,13,14,15], "data_transfer": [4], ...} # multiple leaf interfaces
    print(page_assign_dict)


    cnt_dict = {}
    # e.g.
    # coloringFB_1 : {2: {'read': 10542, 'empty': 117184, 'full': 0}, 
    #                 0: {'stall': 117130}, 
    #                 9: {'full': 16735, 'empty': 210347}}
    # ...
    with open("./_bi_results/" + filename, "r") as infile:
        lines = infile.readlines()

        # Parse results

        # result_cnt = 0

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
                dst_leaf = int(cnt[0:5],2)
                dst_port = int(cnt[5:9],2)
                self_leaf = int(cnt[9:14],2)
                self_port = int(cnt[14:18],2)
                counter = int(cnt[18:20],2)
                counter_val = int(cnt[20:],2)
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

                # op_list += [(op_name + '-' + str(self_leaf), self_port, counter_type, counter_val)]
                # print(op_name + " " + str(self_port) + " " + str(counter) + " " + str(counter_val))
                # result_cnt += 1
                # if(result_cnt%(num_cnt_read) == 0):
                #     for elem in sorted(op_list):
                #         print(*elem)
                #     op_list = []
                #     print()
                #     break

            if line.startswith('elapsed time: '):
                elapsed_time = line.split()[2]
            if line.startswith('TEST'):
                print(elapsed_time)
                # print(cnt_dict)
                for op_name in sorted(cnt_dict):
                    print(op_name, cnt_dict[op_name])
                #     print(cnt)
                #     print(*elem)
                # op_list = []
                # print()


        print()
        # Find the bottleneck operator
        min_stall = sys.maxsize
        bottleneck_op = None
        for op_name in cnt_dict:
            stall_cnt = cnt_dict[op_name][0]['stall']
            print(op_name, str(stall_cnt))

            if stall_cnt < min_stall:
                min_stall = stall_cnt
                bottleneck_op = op_name

        print(min_stall)
        print(bottleneck_op)


    # Check whether NoC is bottleneck or not.
    # sender has large full cnt && receiver has small funn cnt
    # OR sender has small empty cnt && receiver has larger empty cnt

    # For each link in the graph, full_diff = sender's full cnt - receiver's full cnt
    #     => if the link's full_diff is large, NoC could be bottleneck
    # For each link in the graph, empty_diff = receiver's empty_cnt - sedner's empty_cnt
    #     => if the link's empty_diff is large, NoC could be bottleneck
    # Thus, take average of full_diff and empty_diff 

    operator_list = list(page_assign_dict.keys())
    print(operator_list)

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
    print(connection_diff_dict)
    for connection in connection_diff_dict:
        full_diff, empty_diff = connection_diff_dict[connection]
        if full_diff > 0 or empty_diff > 0:
            print(connection)


    # TODO-1: Call tuner
    with open('./input_src/' + benchmark + '/params.json', 'r') as infile:
        params_dict = json.load(infile)
    print(params_dict)
    # - Maybe optimize NoC bottleneck (changing num_leaf_interface, merge?) along with operator bottleneck
    # - If param space is all explored or not enough area, them move to monolithic
    # - Incrementally explore param like par factor first, and then increase kernel clk

    # Don't touch params.json; initially param space is set by the user
    # TODO-2: Update cur_param.json and mv cur_param.json prev_pram.json


    # Call gen_next_param.py
