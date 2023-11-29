import json


# Helper functions stolen from runtime.py
def return_operator_io_argument_dict_local(operator_list, benchmark, is_no_merge=False):
    # operator_list = operators.split()
    operator_arg_dict = {}
    for operator in operator_list:
        # with open('./operators/no_merge/'+operator+'.h', 'r') as infile:
        #     file_list = infile.readlines()

        if is_no_merge:
            with open('./operators/no_merge/'+operator+'.h', 'r') as infile:
                file_list = infile.readlines()
        else:
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


# def is_valid_num_leaf_interface(represent_op, num_leaf_interface):
#     num_input_streams = 0
#     num_output_streams = 0
#     operator_arg_dict = return_operator_io_argument_dict_local([represent_op], None, is_no_merge=False)
#     for io_stream in operator_arg_dict:
#         if io_stream.startswith('Input_'):
#             num_input_streams += 1
#         elif io_stream.startswith('Output_'):
#             num_output_streams += 1


#     return False

# def get_merged_ops(cur_param_dict, represent_op):
#     merged_op_list = []
#     for op in cur_param_dict.keys():
#         if op != 'metric':
#             if 'merged_to' in cur_param_dict[op].keys() and \
#                 cur_param_dict[op]['merged_to'] == represent_op:
#                 merged_op_list.append(op)
#     return merged_op_list


# with open('./cur_param.json', 'r') as infile:
#     cur_param_dict = json.load(infile)


# represent_op_list = []
# for op in cur_param_dict.keys():
#     if op != 'metric':
#         if 'merged_to' in cur_param_dict[op].keys() and \
#             cur_param_dict[op]['merged_to'] not in represent_op_list:
#             represent_op_list.append(cur_param_dict[op]['merged_to'])

# print(represent_op_list)


# for represent_op in represent_op_list:
#     merged_op_list = get_merged_ops(represent_op)

#     num_leaf_interface_list = []
#     kernel_clk_list = []
#     for sub_op in merged_op_list:
#         if cur_param_dict[sub_op]['num_leaf_interface'] not in num_leaf_interface_list:
#             num_leaf_interface_list.append(cur_param_dict[sub_op]['num_leaf_interface'])
#         if cur_param_dict[sub_op]['kernel_clk'] not in kernel_clk_list:
#             kernel_clk_list.append(cur_param_dict[sub_op]['kernel_clk'])

#     # If sub_op's 'num_leaf_interface' works, use for the merged op
#     for i in sorted(test, reverse=True):
#         if i > cur_param_dict[represent_op]['num_leaf_interface'] and \
#             is_valid_num_leaf_interface(represent_op, i):
#             cur_param_dict[represent_op]['num_leaf_interface'] = i

#     # Use the max kernel_clk for the merged op
#     cur_param_dict[represent_op]['kernel_clk'] = max(kernel_clk_list)

#     # Update for sub_ops
#     for sub_op in merged_op_list:
#         cur_param_dict[sub_op]['kernel_clk'] = max(kernel_clk_list)

operator_arg_dict = return_operator_io_argument_dict_local(['flow_calc'], None, is_no_merge=False)


# test = [1,2,4]
# print(sorted(test, reverse=True))