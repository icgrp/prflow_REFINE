# -*- coding: utf-8 -*-   

import os  
import subprocess
from pr_flow.gen_basic import gen_basic
import re
import json
from pr_flow.p23_pblock import pblock_page_dict, LUT_MARGIN_single_dict, LUT_MARGIN_double_dict, LUT_MARGIN_quad_dict, \
                               BRAM_MARGIN_single_dict, BRAM_MARGIN_double_dict, BRAM_MARGIN_quad_dict


class page_assign(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)


  # Stole from runtime.py
  # find all the operators arguments order
  # in case the user define the input and output arguments out of order 
  def return_operator_io_argument_dict_local(self, operators):
    operator_list = operators.split()
    operator_arg_dict = {}
    for operator in operator_list:
      file_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
      arguments_list = [] 
      def_valid = False # Ture if function definition begins
      def_str = ''
      for line in file_list:
        if self.shell.have_target_string(line, '('): def_valid = True
        if def_valid: 
          line_str=re.sub('\s+', '', line)
          line_str=re.sub('\t+', '', line_str)
          def_str=def_str+line_str
        if self.shell.have_target_string(line, ')'): def_valid = False

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


  # Stole from runtime.py
  # find all the operators instantiation in the top function
  def return_operator_inst_dict_local(self, operators):
    operator_list = operators.split()
    operator_var_dict = {}
    file_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/host/top.cpp')
    for operator in operator_list:
      arguments_list = [] 
      
      # 1 when detect the start of operation instantiation
      # 2 when detect the end of operation instantiation
      inst_cnt = 0 
      inst_str = ''
      for line in file_list:
        if self.shell.have_target_string(line, operator+'('): inst_cnt = inst_cnt + 1
        if inst_cnt == 1: 
          line_str=re.sub('\s+', '', line)
          line_str=re.sub('\t+', '', line_str)
          line_str=re.sub('//.*', '', line_str)
          inst_str=inst_str+line_str
        if self.shell.have_target_string(line, ')') and inst_cnt == 1: inst_cnt = 2
      inst_str = inst_str.replace(operator+'(','')
      inst_str = inst_str.replace(');','')
      var_str_list = inst_str.split(',')
      operator_var_dict[operator] = var_str_list
    
    return operator_var_dict 


  # Stole from runtime.py
  def return_operator_connect_list_local(self, operator_arg_dict, operator_var_dict):
    connection_list = []
    for key_a in operator_var_dict:
      operator = key_a
      src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
      debug_exist, debug_port = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+key_a+'.h', 'debug_port')
      map_target_exist, map_target = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+key_a+'.h', 'map_target')
      if debug_exist:
        src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
        output_num = self.return_io_num('Output_', src_list)
        tmp_str = key_a+'.Output_'+str(output_num+1)+'->DEBUG.Input_'+str(debug_port) 
        connection_list.append(tmp_str)
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
              if self.shell.have_target_string(operator_arg_dict[key_a][i_a], 'Input'):
                tmp_str = key_b+'.'+operator_arg_dict[key_b][i_b]+'->'+key_a+'.'+operator_arg_dict[key_a][i_a]
              else:
                tmp_str = key_a+'.'+operator_arg_dict[key_a][i_a]+'->'+key_b+'.'+operator_arg_dict[key_b][i_b]
              connection_list.append(tmp_str)

    connection_list = set(connection_list)
    return connection_list


  def get_nparts(self, num_nodes):
    if(num_nodes < 6):
      return 3
    elif(num_nodes < 12):
      return 6
    else:
      return 12


  # Stole from runtime.py, originally "add_bft_config_to_host_cpp"
  def gen_graphfile(self, operators, node_weight_dict):

    operator_arg_dict = self.return_operator_io_argument_dict_local(operators)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': ['Input_1', 'Output_1' .. }

    operator_var_dict = self.return_operator_inst_dict_local(operators)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...

    connection_list=self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    # print(connection_list)
    connection_list_new = []
    for connection in connection_list:
      sender, receiver = connection.split("->")
      sender = sender.split(".")[0]
      receiver = receiver.split(".")[0]
      connection_list_new.append([sender,receiver])
    # print(connection_list_new)
    operators_dma = ["DMA"] + operators.split()
    # print(operators_dma)

    num_nodes = len(operators_dma)
    num_edges = len(connection_list_new)
    # print(num_nodes)
    # print(num_edges)

    with open("./_graph_dir/" + self.prflow_params['benchmark_name'] + "_graphfile", "w") as f_graph:
      f_graph.write(str(num_nodes) + " " + str(num_edges) + " 011\n")
      for op in operators_dma:
        # print("op: " + op)
        # print(operators_dma.index(op) + 1)
        node_weight = node_weight_dict[op]
        f_graph.write(str(node_weight) + " ")
        for connection in connection_list_new:
          if op in connection:
            for op_connected in connection:
              if op != op_connected:
                # print(op_connected)
                # print(operators_dma.index(op_connected) + 1)
                op_connected_idx = operators_dma.index(op_connected) + 1
                f_graph.write(str(op_connected_idx) + " " + "1 ") # edge weight fixed to 1
        f_graph.write("\n")

    nparts = self.get_nparts(num_nodes)
    graphfile = "./_graph_dir/" + self.prflow_params['benchmark_name'] + "_graphfile"
    return nparts, graphfile, operators_dma


  def get_page_size(self, pblock_name):
    return len(pblock_page_dict[pblock_name])


  def get_pblock_list(self, size):
    pblock_list = []
    for pblock in pblock_page_dict.keys():
      if self.get_page_size(pblock) == size:
        pblock_list.append(pblock)
    return pblock_list


  def get_pblock_assign_dict(self, node_weight_dict, page_valid_dict, operators_dma):
    pblock_assign_dict = {}
    for op in operators_dma:
      if op != "DMA":
        node_weight = node_weight_dict[op]
        pages_used = [page for page in page_valid_dict if page_valid_dict[page] == op]
        possible_pblock_list = self.get_pblock_list(int(node_weight))
        # print(op)
        # print(pages_used)
        # print(possible_pblock_list)
        pages_used.sort()
        for pblock in possible_pblock_list:
          pages = pblock_page_dict[pblock]
          pages.sort()
          # print(pages)
          if pages == pages_used: # python list compare
            pblock_assign_dict[op] = pblock
            # print(pblock)
    return pblock_assign_dict

  def get_page_assign_dict(self, pblock_assign_dict):
    page_assign_dict = {}
    for pblock_op in pblock_assign_dict: 
      pblock_name = pblock_assign_dict[pblock_op]
      pages = pblock_page_dict[pblock_name]
      min_page = str(min(int(p) for p in pages))
      page_assign_dict[pblock_op] = min_page
    return page_assign_dict


  # In partition list(parts), change a to b
  def change_part(self, a, b, parts):
    new_parts = []
    for part in parts:
      if a == part:
        new_parts.append(b)
      else:
        new_parts.append(part)
    return new_parts

  # Return list of opeartors that are assigned to the target_part value
  def get_ops_in_part(self, parts, operators_dma, target_part):
    ops_in_part = []
    for idx, part in enumerate(parts):
      if(part == target_part):
        op = operators_dma[idx]
        ops_in_part.append(op)
    return ops_in_part

  # Among all ops in the same target_part, start from the larger op first
  def sort_ops_in_part(self, ops_in_part, node_weight_dict):
    sorted_ops_in_part = []
    # Add quad first
    for op in ops_in_part:
      node_weight = node_weight_dict[op]
      if(node_weight == "4"):
        sorted_ops_in_part.append(op)
    # Add double next
    for op in ops_in_part:
      node_weight = node_weight_dict[op]
      if(node_weight == "2"):
        sorted_ops_in_part.append(op)
    # Add single last
    for op in ops_in_part:
      node_weight = node_weight_dict[op]
      if(node_weight == "1"):
        sorted_ops_in_part.append(op)
    return sorted_ops_in_part

  # Returns valid page numbers for the target_part
  def get_valid_page_nums(self, target_part, nparts):
    if(nparts == 12):
      subtree_size = 2
    elif(nparts == 6):
      subtree_size = 4
    elif(nparts == 3):
      subtree_size = 8

    lower_bound = target_part * subtree_size
    upper_bound = (target_part + 1) * subtree_size # not included
    valid_page_nums = list(range(lower_bound, upper_bound))
    if 0 in valid_page_nums or 1 in valid_page_nums:
      valid_page_nums.remove(0)
      valid_page_nums.remove(1)
    return [str(page) for page in valid_page_nums]


  def gen_page_assign_dict(self, parts, operators_dma, node_weight_dict, nparts):
    page_valid_dict = {'2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 
        '9': None, '10': None, '11': None, '12': None, '13': None, '14': None, '15': None, '16': None, 
        '17': None, '18': None, '19': None, '20': None, '21': None, '22': None, '23': None}

    for target_part in range(nparts): # starting from part_num == 0
      ops_in_part = self.get_ops_in_part(parts, operators_dma, str(target_part))
      # print(ops_in_part)
      sorted_ops_in_part = self.sort_ops_in_part(ops_in_part, node_weight_dict)
      assert(len(sorted_ops_in_part) == len(ops_in_part))
      # print(sorted_ops_in_part)
      valid_page_nums = self.get_valid_page_nums(target_part, nparts)
      # print(valid_page_nums)
      for op in sorted_ops_in_part:
        if op != "DMA":
          node_weight = node_weight_dict[op]
          for i in range(int(node_weight)):
            page_num = valid_page_nums[0]
            valid_page_nums.remove(page_num)
            page_valid_dict[page_num] = op
        else:
          pass
          # print("DMA")

    # print(page_valid_dict)
    pblock_assign_dict = self.get_pblock_assign_dict(node_weight_dict, page_valid_dict, operators_dma)
    # print(pblock_assign_dict)
    page_assign_dict = self.get_page_assign_dict(pblock_assign_dict)
    # print(page_assign_dict)
    return page_assign_dict, pblock_assign_dict


  def reverse_partitioned_list(self, partitioned_file, max_val):
    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]

    new_parts = []
    for part in parts:
      new_part = (max_val - int(part))
      new_parts.append(str(new_part))

    with open(partitioned_file, "w") as infile:
      for part in new_parts:
        infile.write(part + "\n")


  def assign_3(self, partitioned_file, operators_dma, node_weight_dict):
    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]
    print(operators_dma)
    print(parts)

    DMA_idx = operators_dma.index("DMA")
    DMA_part = parts[DMA_idx]
    if(DMA_part == '0'):
      # print(parts)
      page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
      return page_assign_dict, pblock_assign_dict
    elif(DMA_part == '1'):
      parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
      parts = self.change_part('1','0',parts)
      parts = self.change_part('2','1',parts)
      parts = self.change_part('-1','2',parts) # -1->2, change to valid part
      # print(parts)
      page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
      return page_assign_dict, pblock_assign_dict
    else: # DMA_part == '2'
      parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
      parts = self.change_part('2','0',parts)
      parts = self.change_part('-1','2',parts) # -1->2, change to valid part
      # print(parts)
      page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
      return page_assign_dict, pblock_assign_dict


  def assign_6(self, partitioned_file, operators_dma, node_weight_dict):

    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]
    print(operators_dma)
    print(parts)

    DMA_idx = operators_dma.index("DMA")
    DMA_part = parts[DMA_idx]
    if(DMA_part in ['0','1','2']):
      if(DMA_part == '0'):
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
        return page_assign_dict, pblock_assign_dict
      elif(DMA_part == '1'):
        parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
        parts = self.change_part('1','0',parts)
        parts = self.change_part('2','1',parts)
        parts = self.change_part('-1','2',parts) # -1->2, change to valid part
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
        return page_assign_dict, pblock_assign_dict
      else: # DMA_part == '2'
        parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
        parts = self.change_part('2','0',parts)
        parts = self.change_part('-1','2',parts) # -1->2, change to valid part
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 6)
        return page_assign_dict, pblock_assign_dict
    else:
      self.reverse_partitioned_list(partitioned_file, 6-1)
      self.assign_6(partitioned_file, operators_dma, node_weight_dict)

    
  def assign_12(self, partitioned_file, operators_dma, node_weight_dict):
    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]
    print(operators_dma)
    print(parts)

    DMA_idx = operators_dma.index("DMA")
    DMA_part = parts[DMA_idx]
    if(DMA_part in ['0','1','2','3','4','5']):
      if(DMA_part == '0'):
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 12)
        return page_assign_dict, pblock_assign_dict
      elif(DMA_part == '1'):
        parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
        parts = self.change_part('1','0',parts)
        parts = self.change_part('2','1',parts)
        parts = self.change_part('-1','2',parts) # -1->2, change to valid part
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 12)
        return page_assign_dict, pblock_assign_dict
      elif(DMA_part == '2'): # DMA_part == '2'
        parts = self.change_part('0','-1',parts) # 0->-1, invalid, temp
        parts = self.change_part('2','0',parts)
        parts = self.change_part('-1','2',parts) # -1->2, change to valid part
        # print(parts)
        page_assign_dict, pblock_assign_dict = self.gen_page_assign_dict(parts, operators_dma, node_weight_dict, 12)
        return page_assign_dict, pblock_assign_dict
      else: # DMA_part == 3 ~ 5, reverse part number 0~5 only
        with open(partitioned_file, "r") as infile:
          parts = infile.readlines()
          parts = [part.strip() for part in parts]
        new_parts = []
        for part in parts:
          if int(part) < 6:
            new_part = (5 - int(part))
          new_parts.append(str(new_part))
        with open(partitioned_file, "w") as infile:
          for part in new_parts:
            infile.write(part + "\n")
        self.assign_12(partitioned_file, operators_dma)
    else: # DMA_part == 6 ~ 11
      self.reverse_partitioned_list(partitioned_file, 12-1)
      self.assign_12(partitioned_file, operators_dma, node_weight_dict)


  def assign(self, nparts, operators_dma, node_weight_dict, partitioned_file):
    if(nparts == 3):
      page_assign_dict, pblock_assign_dict = self.assign_3(partitioned_file, operators_dma, node_weight_dict)
    elif(nparts == 6):
      page_assign_dict, pblock_assign_dict = self.assign_6(partitioned_file, operators_dma, node_weight_dict)
    elif(nparts == 12):
      page_assign_dict, pblock_assign_dict = self.assign_12(partitioned_file, operators_dma, node_weight_dict)
    else:
      print("Invalid nparts value")
    return page_assign_dict, pblock_assign_dict


  # Returns operator's utilization dict
  def get_util_dict(self, pblock_operators_list):
    util_dict = {}
    for pblock_op in pblock_operators_list:
      pblock_op_list = pblock_op.split()
      if(len(pblock_op_list) == 1):
        with open(self.syn_dir + "/" + pblock_op_list[0] + '/utilization.rpt', 'r') as file:
          for line in file:
            if(line.startswith('| leaf')):
              # print(line.split())
              num_clb = str(line.split()[5])
              num_ram36 = str(line.split()[15])
              num_ram18 = str(int(line.split()[15])*2 + int(line.split()[17]))
              num_dsp = str(line.split()[21])
              # print(num_clb, num_ram18, num_dsp)
              util_dict[pblock_op] = (num_clb, num_ram36, num_ram18, num_dsp)
      else: # multiple ops in a single page
        (num_clb, num_ram36, num_ram18, num_dsp) = (0, 0, 0, 0)
        for sub_op in pblock_op_list:
          # print(sub_op)
          with open(self.syn_dir + "/" + sub_op + '/utilization.rpt', 'r') as file:
            for line in file:
              if(line.startswith('| leaf')):
                # print(line.split())
                num_clb = int(line.split()[5]) + num_clb
                num_ram36 = int(line.split()[15]) + num_ram36
                num_ram18 = int(line.split()[15])*2 + int(line.split()[17]) + num_ram18
                num_dsp = int(line.split()[21]) + num_dsp
        util_dict[pblock_op] = (num_clb, num_ram36, num_ram18, num_dsp)
    return util_dict
 

  def get_pblock_operators_list(self, project_name):
    pblock_ops_dir = './input_src/' + project_name + '/operators'
    with open(pblock_ops_dir + '/pblock_operators_list.json', 'r') as infile:
        pblock_operators_list = json.load(infile)
    # print(pblock_operators_list)
    # temp_list = [tuple(pblock_op.split()) for pblock_op in pblock_operators_list]
    # pblock_operators_list = temp_list
    return pblock_operators_list


  # Add criterial to operator's util_dict based on resource usage
  def add_criteria_util_dict(self, util_dict):
    # get total resource available
    with open(self.syn_dir + "/" + './resource.txt', 'r') as file:
      for line in file:
        if(not line.startswith('Total')):
          resources = line.split()
          total_LUT = int(resources[0])
          # total_dict['FFs'] = int(resources[1])
          total_BRAM = int(resources[2])
          total_DSP = int(resources[3])

    # add criteria in util_dict's value
    for key, value in util_dict.items():
      [num_clb, num_ram36, num_ram18, num_dsp] = value
      num_clb, num_ram18, num_dsp = int(num_clb), int(num_ram18), int(num_dsp) # ignore num_ram36
      LUT_percent = float(num_clb) / total_LUT 
      BRAM_percent = float(num_ram18) / total_BRAM 
      DSP_percent = float(num_dsp) / total_DSP
      criteria = LUT_percent + BRAM_percent + DSP_percent
      # print(criteria)
      util_dict[key] = (value, criteria)
    return util_dict


  def get_overlay_util_dict(self, overlay_util_dict):
    overlay_util_dict_single = {}
    overlay_util_dict_double = {}
    overlay_util_dict_quad = {}
    for pblock in overlay_util_dict:
      if(self.get_page_size(pblock) == 1):
        overlay_util_dict_single[pblock] = overlay_util_dict[pblock]
      elif(self.get_page_size(pblock) == 2):
        overlay_util_dict_double[pblock] = overlay_util_dict[pblock]
      elif(self.get_page_size(pblock) == 4):
        overlay_util_dict_quad[pblock] = overlay_util_dict[pblock]
    return overlay_util_dict_single, overlay_util_dict_double, overlay_util_dict_quad


  # TODO: need smarter way
  # returns whether the operator fits in the page
  def is_fit(self, op_resource_tuple, overlay_resource_tuple, pblock_name, frequency):
    [num_clb, num_ram36, num_ram18, num_dsp] = op_resource_tuple
    [num_clb_overlay, num_ram36_overlay, num_ram18_overlay, num_dsp_overlay] = overlay_resource_tuple
    num_clb, num_ram36, num_ram18, num_dsp = int(num_clb), int(num_ram36), int(num_ram18), int(num_dsp)
    num_clb_overlay, num_ram36_overlay, num_ram18_overlay, num_dsp_overlay = \
                int(num_clb_overlay), int(num_ram36_overlay), int(num_ram18_overlay), int(num_dsp_overlay)

    pblock_pages = pblock_page_dict[pblock_name]
    pblock_size = len(pblock_pages)

    if(pblock_size == 1):
      LUT_MARGIN = LUT_MARGIN_single_dict[frequency][pblock_name]
    elif(pblock_size == 2):
      LUT_MARGIN = LUT_MARGIN_double_dict[frequency][pblock_name]
    elif(pblock_size == 4):
      LUT_MARGIN = LUT_MARGIN_quad_dict[frequency][pblock_name]
    else:
      raise Exception("Invalid pblock size")

    if(pblock_size == 1):
      RAM_DSP_MARGIN = BRAM_MARGIN_single_dict[frequency][pblock_name]
    elif(pblock_size == 2):
      RAM_DSP_MARGIN = BRAM_MARGIN_double_dict[frequency][pblock_name]
    elif(pblock_size == 4):
      RAM_DSP_MARGIN = BRAM_MARGIN_quad_dict[frequency][pblock_name]
    else:
      raise Exception("Invalid pblock size")

    # print(RAM_DSP_MARGIN)
    # print(num_dsp)
    # print(num_dsp_overlay)
    resource_condition = ((num_clb * (1+LUT_MARGIN) < num_clb_overlay) and \
                            num_ram36 * (1+RAM_DSP_MARGIN) <= num_ram36_overlay and \
                            num_ram18 * (1+RAM_DSP_MARGIN) <= num_ram18_overlay and \
                            num_dsp * (1+RAM_DSP_MARGIN) <= num_dsp_overlay)
    return resource_condition


  # Returns False if the page is occupied by different operator
  def is_valid_pblock(self, page_valid_dict, pblock_name):
    pblock_pages = pblock_page_dict[pblock_name]
    for page in pblock_pages:
      if(page_valid_dict[page] is not None):
        return False
    return True


  def get_tightest_pblock(self, op_resource_tuple, overlay_util_dict, possible_pblock_list):
      [num_clb, num_ram36, num_ram18, num_dsp] = op_resource_tuple
      num_clb, num_ram36, num_ram18, num_dsp = int(num_clb), int(num_ram36), int(num_ram18), int(num_dsp)
      pblock_ratio_dict = {} # contains tightness ratio for each pblock
      for pblock_name in possible_pblock_list:
          overlay_resource_tuple = overlay_util_dict[pblock_name]
          [num_clb_overlay, num_ram36_overlay, num_ram18_overlay, num_dsp_overlay] = overlay_resource_tuple
          num_clb_overlay, num_ram36_overlay, num_ram18_overlay, num_dsp_overlay = \
                      int(num_clb_overlay), int(num_ram36_overlay), int(num_ram18_overlay), int(num_dsp_overlay)
          LUT_percent = float(num_clb) / num_clb_overlay 
          BRAM_percent = float(num_ram18) / num_ram18_overlay 
          DSP_percent = float(num_dsp) / num_dsp_overlay
          pblock_ratio_dict[pblock_name] = LUT_percent + BRAM_percent + DSP_percent
      # print(pblock_ratio_dict)

      return max(pblock_ratio_dict, key=pblock_ratio_dict.get) # returns tightest pblock


  # Updates page_valid_dict and pblock_assign_dict
  def update_assignment(self, overlay_util_dict, pblock_op, op_resource_tuple, page_valid_dict, pblock_assign_dict, frequency):
    # iterate through overlay_util_dict's page_num in ascending order
    # We don't need to, but for the debuging purposes..
    possible_pblock_list = []
    for pblock_name in sorted(overlay_util_dict.keys()):
      overlay_resource_tuple = overlay_util_dict[pblock_name]
      # print(pblock_name, overlay_resource_tuple)
      if(self.is_fit(op_resource_tuple, overlay_resource_tuple, pblock_name, frequency) and 
         self.is_valid_pblock(page_valid_dict, pblock_name)):
        possible_pblock_list.append(pblock_name)
    # print(possible_pblock_list)

    if(possible_pblock_list): # if not empty
      pblock_name_final = self.get_tightest_pblock(op_resource_tuple, overlay_util_dict, possible_pblock_list)
      # print(pblock_name_final)
      pblock_assign_dict[pblock_op] = pblock_name_final
      pblock_pages = pblock_page_dict[pblock_name_final]
      for page in pblock_pages:
        page_valid_dict[page] = pblock_op


  def is_assigned_all(self, pblock_assign_dict, pblock_operators_list):
    for pblock_op in pblock_operators_list:
      if(pblock_op not in pblock_assign_dict):
        return False
    return True


  # Make sure that all operators are mappable and output page size
  def gen_node_weight_dict(self, util_dict, overlay_util_dict_single, 
                                            overlay_util_dict_double, 
                                            overlay_util_dict_quad, pblock_operators_list, frequency):
    page_valid_dict = {'2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 
        '9': None, '10': None, '11': None, '12': None, '13': None, '14': None, '15': None, '16': None, 
        '17': None, '18': None, '19': None, '20': None, '21': None, '22': None, '23': None}
    pblock_assign_dict = {}

    # iterate through util_dict's pblock_op in descending order of resource usage
    # iterate through overlay_util_dict's page_num in ascending order
    for pblock_op, value in sorted(util_dict.items(), key=lambda x:x[1][1], reverse=True): # sorted by criteria
      op_resource_tuple = value[0]
      # print(pblock_op, op_resource_tuple)

      pblock_op_list = pblock_op.split()
      num_op = len(pblock_op_list)
      if(num_op == 1):
        self.update_assignment(overlay_util_dict_single, pblock_op, op_resource_tuple, page_valid_dict, pblock_assign_dict, frequency)
      if(num_op <= 2 and not pblock_op in pblock_assign_dict):
        self.update_assignment(overlay_util_dict_double, pblock_op, op_resource_tuple, page_valid_dict, pblock_assign_dict, frequency)
      if(num_op <= 4 and not pblock_op in pblock_assign_dict):
        self.update_assignment(overlay_util_dict_quad, pblock_op, op_resource_tuple, page_valid_dict, pblock_assign_dict, frequency)

    # print(pblock_assign_dict)
    # print(pblock_operators_list)
    if(not self.is_assigned_all(pblock_assign_dict, pblock_operators_list)):
      raise Exception("Operators do not fit in any of the pre-generated NoC overlay")
    
    node_weight_dict = {"DMA": "2"}
    for op, pblock in pblock_assign_dict.items():
      node_weight_dict[op] = str(self.get_page_size(pblock))
    return node_weight_dict


  def run(self, operators, bft_n, frequency="200"):

    pblock_operators_list = self.get_pblock_operators_list(self.prflow_params['benchmark_name'])
    # print(pblock_operators_list)
    # e.g. pblock_operators_list = ["coloringFB_bot_m coloringFB_top_m", "data_redir_m", ... , "zculling_top"]
    # This is because we potentially wanted multiple ops in one page
    # Not sure we keep this...

    util_dict = self.get_util_dict(pblock_operators_list)
    # print(util_dict)
    # e.g.: at this point, util_dict = {"coloringFB_bot_m coloringFB_top_m": ('8839', '31', '0'), 
    #                                   "data_transfer": ('2303', '7', '6'), ... }
    util_dict = self.add_criteria_util_dict(util_dict)
    # print(util_dict)
    # e.g.: at this point, util_dict = {"coloringFB_bot_m, coloringFB_top_m": (('8839', '31', '0'), 0.049), 
    #                                   "data_transfer": (('2303', '7', '6'), 0.014), ... }

    overlay_n = 'overlay_p' + str(bft_n)
    overlay_util_json_file = self.overlay_dir + "/ydma/zcu102/" + frequency + "MHz/" + "zcu102_dfx_manual/" + overlay_n + "/util_all.json"
    with open(overlay_util_json_file, 'r') as infile:
        overlay_util_dict = json.load(infile)
    # print(overlay_util_dict)

    # for elem in util_dict:
    #     print(str(util_dict[elem][0])) # operator's resource tuple

    overlay_util_dict_single, overlay_util_dict_double, overlay_util_dict_quad = \
        self.get_overlay_util_dict(overlay_util_dict)
    # print(overlay_util_dict_single)
    # print(overlay_util_dict_double)
    # print(overlay_util_dict_quad)

    node_weight_dict = self.gen_node_weight_dict(util_dict, overlay_util_dict_single, 
                                                            overlay_util_dict_double, 
                                                            overlay_util_dict_quad, pblock_operators_list, frequency)

    print(node_weight_dict)
    # with open(self.prflow_params['benchmark_name'] + "_node_weight_dict.json", "r") as infile:
    #   node_weight_dict = json.load(infile)

    nparts, graphfile, operators_dma = self.gen_graphfile(operators, node_weight_dict) # generate graphfile
    os.system('gpmetis -ptype=rb ' + graphfile + " " + str(nparts)) # call Metis
    os.system('mv ' + self.prflow_params['benchmark_name'] + "_graphfile" + ".part." + str(nparts) + "./graph_dir/")
    partitioned_file = "./_graph_dir/" + self.prflow_params['benchmark_name'] + "_graphfile" + ".part." + str(nparts)
    page_assign_dict, pblock_assign_dict = self.assign(nparts, operators_dma, node_weight_dict, partitioned_file) # page assign

    if(not self.is_assigned_all(pblock_assign_dict, pblock_operators_list)):
      raise Exception("TODO: what should we do if metis's output doesn't result in valid assignment?")

    print("## page_assign_dict")
    print(page_assign_dict)
    print("")
    print("## pblock_assign_dict")
    print(pblock_assign_dict)
    print("")

    # In pblock_assignment, both "coloringFB_bot_m" and "coloringFB_top_m" belong to the same pblock, p2
    with open(self.syn_dir + '/pblock_assignment.json', 'w') as outfile:
      json.dump((overlay_n, pblock_assign_dict), outfile)

    # For incremental compile, let each operator to have separate .json file
    for op_impl in pblock_assign_dict:
        ops = op_impl.split()
        for op in ops:
            pblock_name = pblock_assign_dict[op_impl]
            page_num = page_assign_dict[op]
            # IMPORTANT!, changes pblock.json only when the contents have been changed
            if(os.path.exists(self.syn_dir + '/' + op + '/pblock.json')):
                with open(self.syn_dir + '/' + op + '/pblock.json', 'r') as infile:
                    (overlay_n_old, pblock_name_old, page_num_old) = json.load(infile)
                if(overlay_n != overlay_n_old or pblock_name != pblock_name_old or page_num != page_num_old):
                    with open('./' + op + '/pblock.json', 'w') as outfile:
                        json.dump((overlay_n, pblock_name, page_num), outfile)
            else: # first time
                with open(self.syn_dir + '/' + op + '/pblock.json', 'w') as outfile:
                    json.dump((overlay_n, pblock_name, page_num), outfile)
