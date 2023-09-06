# -*- coding: utf-8 -*-   

import os  
import subprocess
from pr_flow.gen_basic import gen_basic
import re
import json
from pr_flow.p23_pblock import pblock_page_dict, LUT_MARGIN_single_dict, LUT_MARGIN_double_dict, LUT_MARGIN_quad_dict, \
                               BRAM_MARGIN_single_dict, BRAM_MARGIN_double_dict, BRAM_MARGIN_quad_dict

import pandas as pd
import numpy as np
import pickle
RECALL_THRESHOLD = 0.97
resource_ratio_dict = {"single": [(0.6,1),(0.5,1),(0.5,1)],
                        "double": [(0.6,1),(0.6,1),(0.6,1)],
                        "quad": [(0.6,1),(0.6,1),(0.6,1)]}

class page_assign(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)


  # Stole from runtime.py
  # find all the operators arguments order
  # in case the user define the input and output arguments out of order 
  def return_operator_io_argument_dict_local(self, operators_list):
    operator_arg_dict = {}
    for operator in operators_list:
      if operator != 'DMA':
        file_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
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


  # Stole from runtime.py
  # find all the operators instantiation in the top function
  def return_operator_inst_dict_local(self, operators_list):
    operator_var_dict = {}
    file_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/host/top.cpp')
    for operator in operators_list:
      if (operator != 'DMA'):
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


  # Stole from runtime.py
  def return_operator_connect_list_local(self, operator_arg_dict, operator_var_dict, operators_list):
    connection_list = []
    for key_a in operator_var_dict:
      operator = key_a
      src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
      debug_exist, debug_port = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+\
                                                          '/operators/'+key_a+'.h', 'debug_port')
      map_target_exist, map_target = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+\
                                                               '/operators/'+key_a+'.h', 'map_target')
      if debug_exist:
        src_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
        output_num = self.return_io_num('Output_', src_list)
        tmp_str = key_a+'.Output_'+str(output_num+1)+'->DEBUG.Input_'+str(debug_port) 
        connection_list.append(tmp_str)
      for i_a, var_value_a in enumerate(operator_var_dict[key_a]):
        if 'DMA' in operators_list and var_value_a == 'Input_1': 
          tmp_str='DMA.Output_1->'+key_a+'.Input_1' 
          connection_list.append(tmp_str)
        if 'DMA' in operators_list and var_value_a == 'Input_2': 
          tmp_str='DMA2.Output_1->'+key_a+'.Input_1' 
          connection_list.append(tmp_str)
        if 'DMA' in operators_list:
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


  ## New stuff begins

  def get_page_size(self, pblock_name):
    return len(pblock_page_dict[pblock_name])


  # In partition list(parts), change a to b
  def change_part(self, a, b, parts):
    new_parts = []
    for part in parts:
      if a == part:
        new_parts.append(b)
      else:
        new_parts.append(part)
    return new_parts


  def is_pblock_in_range(self, pblock, low, high):
    is_in_range = True
    page_nums = pblock_page_dict[pblock]
    for page_num in page_nums:
      if int(page_num) < low or high < int(page_num):
        is_in_range = False
    return is_in_range



  # is_fit based on pre-trained ML model
  # returns True if the operator can be mapped to the pblock
  # returns False if the operator cannot be mapped to the pblock
  def is_fit(self, op_resource_dict, pblock_resource_dict, pblock_name, frequency):
    pblock_size = self.get_page_size(pblock_name)
    if pblock_size == 1: resource_ratio_list = resource_ratio_dict["single"]
    elif pblock_size == 2: resource_ratio_list = resource_ratio_dict["double"]
    else: resource_ratio_list = resource_ratio_dict["quad"]
    LUT_low, LUT_high = resource_ratio_list[0][0], resource_ratio_list[0][1]
    BRAM_low, BRAM_high = resource_ratio_list[1][0], resource_ratio_list[1][1]
    DSP_low, DSP_high = resource_ratio_list[2][0], resource_ratio_list[2][1]
    FF_low, FF_high = 0.6, 1.0
    LUT_mem_low, LUT_mem_high = 0.6, 1.0

    cur_delay = 1000/int(frequency)

    LUT_ratio = op_resource_dict['LUT'] / pblock_resource_dict['LUT']
    LUT_mem_ratio = op_resource_dict['LUT_mem'] / pblock_resource_dict['LUT_mem']
    FF_ratio = op_resource_dict['FF'] / pblock_resource_dict['FF']
    BRAM_ratio = op_resource_dict['RAMB18'] / pblock_resource_dict['RAMB18']
    DSP_ratio = op_resource_dict['DSP48E2'] / pblock_resource_dict['DSP48E2']
    path_delay_ratio = op_resource_dict['path_delay'] / cur_delay
    rent = op_resource_dict['rent']
    avg_fanout = op_resource_dict['avg_fanout']
    total_inst = op_resource_dict['total_inst']

    if LUT_ratio >= LUT_high or LUT_mem_ratio >= LUT_mem_high or FF_ratio >= FF_high or BRAM_ratio >= BRAM_high or DSP_ratio >= DSP_high:
      return False # may overutilize pblock
    elif LUT_ratio < LUT_low and LUT_mem_ratio < LUT_mem_low and FF_ratio < FF_low and BRAM_ratio < BRAM_low and DSP_ratio < DSP_low and path_delay_ratio < 1:
      return True # small enough

    test_feature = pd.DataFrame(np.array([[LUT_ratio, LUT_mem_ratio, FF_ratio, BRAM_ratio, DSP_ratio, path_delay_ratio, rent, avg_fanout, total_inst]]), \
      columns=['LUT ratio', 'LUT_mem ratio', 'FF ratio', 'BRAM ratio', 'DSP ratio', 'path delay', 'Rent', 'average fanout', 'total instances'])

    dir_name = str(RECALL_THRESHOLD).split('.')[1]
    best_model = pickle.load(open('./classifier/' + str(frequency) + 'MHz/' + dir_name + '/' + pblock_name + '.pickle', "rb"))
    if best_model.__class__.__name__ != 'RandomForestClassifier':
        standard_scaler = pickle.load(open('./classifier/' + str(frequency) + 'MHz/' + dir_name + '/' + pblock_name + '_sc.pickle', "rb"))
        test_feature = pd.DataFrame(standard_scaler.transform(test_feature), index=test_feature.index, columns=test_feature.columns)

    y_test_pred = best_model.predict(test_feature)
    return not y_test_pred


  # is_fit based on hard constraint for one operator
  # returns whether the operator fits in the page
  def is_fit_hard(self, op_resource_dict, pblock_resource_dict, pblock_name, frequency):

    pblock_pages = pblock_page_dict[pblock_name]
    pblock_size = len(pblock_pages)
    FF_MARGIN = 0
    LUT_MEM_MARGIN = 0

    if(pblock_size == 1): LUT_MARGIN = LUT_MARGIN_single_dict[frequency][pblock_name]
    elif(pblock_size == 2): LUT_MARGIN = LUT_MARGIN_double_dict[frequency][pblock_name]
    elif(pblock_size == 4): LUT_MARGIN = LUT_MARGIN_quad_dict[frequency][pblock_name]
    else: raise Exception("Invalid pblock size")

    if(pblock_size == 1): RAM_DSP_MARGIN = BRAM_MARGIN_single_dict[frequency][pblock_name]
    elif(pblock_size == 2): RAM_DSP_MARGIN = BRAM_MARGIN_double_dict[frequency][pblock_name]
    elif(pblock_size == 4): RAM_DSP_MARGIN = BRAM_MARGIN_quad_dict[frequency][pblock_name]
    else: raise Exception("Invalid pblock size")

    resource_condition = ((op_resource_dict['LUT'] * (1+LUT_MARGIN) < pblock_resource_dict['LUT']) and \
                           op_resource_dict['LUT_mem'] * (1+LUT_MEM_MARGIN) < pblock_resource_dict['LUT_mem'] and \
                           op_resource_dict['FF'] * (1+FF_MARGIN) < pblock_resource_dict['FF'] and \
                           op_resource_dict['RAMB36'] * (1+RAM_DSP_MARGIN) <= pblock_resource_dict['RAMB36'] and \
                           op_resource_dict['RAMB18'] * (1+RAM_DSP_MARGIN) <= pblock_resource_dict['RAMB18'] and \
                           op_resource_dict['DSP48E2'] * (1+RAM_DSP_MARGIN) <= pblock_resource_dict['DSP48E2'])
    return resource_condition


  # Returns False if the page is occupied by different operator
  def is_valid_pblock(self, page_valid_dict, pblock_name):
    pblock_pages = pblock_page_dict[pblock_name]
    for page in pblock_pages:
      if(page_valid_dict[page] is not None):
        return False
    return True


  # Returns one pblock from possible_pblock_list, based on is_tightest setting
  def get_final_pblock(self, op_resource_dict, pblock_in_range_resource_dict, possible_pblock_list, is_tightest = True):

    pblock_ratio_dict = {} # contains tightness ratio for each pblock
    for pblock_name in possible_pblock_list:
      pblock_resource_dict = pblock_in_range_resource_dict[pblock_name]

      LUT_logic_percent = float(op_resource_dict['LUT']) / pblock_resource_dict['LUT'] 
      LUT_mem_percent = float(op_resource_dict['LUT_mem']) / pblock_resource_dict['LUT_mem'] 
      FF_percent = float(op_resource_dict['FF']) / pblock_resource_dict['FF']
      BRAM_percent = float(op_resource_dict['RAMB18']) / pblock_resource_dict['RAMB18']
      DSP_percent = float(op_resource_dict['DSP48E2']) / pblock_resource_dict['DSP48E2']
      pblock_ratio_dict[pblock_name] = LUT_logic_percent + LUT_mem_percent + FF_percent + BRAM_percent + DSP_percent
    # print(pblock_ratio_dict)

    if is_tightest:
      return max(pblock_ratio_dict, key=pblock_ratio_dict.get) # returns tightest pblock
    else:
      return min(pblock_ratio_dict, key=pblock_ratio_dict.get) # returns relaxed pblock        


  def is_assigned_all(self, pblock_assign_dict, operators_list):
    # Check all assigned
    for pblock_op in operators_list:
      if(pblock_op != 'DMA' and pblock_op not in pblock_assign_dict):
        return False
    # Check duplicate
    for op, pblock in pblock_assign_dict.items():
      for test_op, test_pblock in pblock_assign_dict.items():
        if (op != test_op and pblock == test_pblock):
          return False
    return True


  # Updates page_valid_dict and pblock_assign_dict
  # pblock_in_range_resource_dict: part of util_all.json
  # op_resource_dict: util dict for ONE operator
  def update_assignment(self, pblock_in_range_resource_dict, pblock_op, op_resource_dict, 
                              page_valid_dict, pblock_assign_dict, specs_dict, requirements, is_tightest = True):
    frequency = specs_dict[pblock_op]['kernel_clk']
    num_leaf_interface = specs_dict[pblock_op]['num_leaf_interface']

    # e.g. requirements = {"data_transfer": 2, ... } indicates the minimum size the operator needs to be mapped
    if pblock_op in requirements:
      min_size = requirements[pblock_op]
    else:
      min_size = 1

    # iterate through pblock_in_range_resource_dict's page_num in ascending order
    # We don't need to, but for the debuging purposes..
    possible_pblock_list = []
    for pblock_name in sorted(pblock_in_range_resource_dict.keys()):
      pblock_resource_dict = pblock_in_range_resource_dict[pblock_name]
      # is_fit_result = self.is_fit(op_resource_dict, pblock_resource_dict, pblock_name, frequency)
      is_fit_hard_result = self.is_fit_hard(op_resource_dict, pblock_resource_dict, pblock_name, frequency)
      # print(is_fit_result)
      # if(not is_fit_result and is_fit_hard_result):
      #   print("examples---")
      #   print(op_resource_dict)
      #   print(pblock_resource_dict)
      #   print(pblock_name)
      #   print(is_fit_result)
      #   print()
      # TODO: Fix line below
      if(is_fit_hard_result and 
        self.is_valid_pblock(page_valid_dict, pblock_name) and 
        self.get_page_size(pblock_name) >= num_leaf_interface and 
        self.get_page_size(pblock_name) >= min_size):
        possible_pblock_list.append(pblock_name)

    # print("operator: " + pblock_op)
    # print("possible pblock list: " + str(possible_pblock_list))
    # print("pblock_assign_dict:")
    # print(pblock_assign_dict)

    if(possible_pblock_list): # if not empty
      if is_tightest:
        pblock_name_final = self.get_final_pblock(op_resource_dict, pblock_in_range_resource_dict, possible_pblock_list, True)
      else:
        pblock_name_final = self.get_final_pblock(op_resource_dict, pblock_in_range_resource_dict, possible_pblock_list, False)
      # print(pblock_name_final)
      pblock_assign_dict[pblock_op] = pblock_name_final
      pblock_pages = pblock_page_dict[pblock_name_final]
      for page in pblock_pages:
        page_valid_dict[page] = pblock_op


  def get_util_dict_sub(self, operators_subtree, util_dict):
    util_dict_subtree = {}
    for op in util_dict.keys():
      if op in operators_subtree:
        util_dict_subtree[op] = util_dict[op]
    return util_dict_subtree


  def get_pblock_operators_list(self, project_name):
    pblock_ops_dir = './input_src/' + project_name + '/operators'
    with open(pblock_ops_dir + '/specs.json', 'r') as infile:
      # specs_dict = json.load(infile)
      specs_dict = json.load(infile)
    # return pblock_operators_list
    return list(specs_dict.keys())


  # Returns operator's utilization and design analysis dict
  def get_util_dict(self, operators_list):
    util_dict = {}
    for op in operators_list:
      with open(self.syn_dir + "/" + op + '/utilization.rpt', 'r') as file:
        for line in file:
          # if(line.startswith('| user_kernel')):
          if(line.startswith('| leaf')):
            # print(line.split())
            num_LUT = int(line.split()[5]) # LUT_logic + LUT_mem
            num_LUT_mem = int(line.split()[9])
            num_FF = int(line.split()[13])
            num_ram36 = int(line.split()[15])
            num_ram18 = int(int(line.split()[15])*2 + int(line.split()[17]))
            num_dsp = int(line.split()[21])
      with open(self.syn_dir + "/" + op + '/design_analysis.rpt', 'r') as file:
        for line in file:
          if line.startswith('| Path Delay '):
            path_delay = float(line.split()[4])
          elif line.startswith('| (top) '):
            try:
              rent = float(line.split()[5])
            except ValueError:
              rent = -1
            avg_fanout = float(line.split()[7])
            total_inst = int(line.split()[9])

      util_dict[op] = {'LUT': num_LUT,
                       'LUT_mem': num_LUT_mem,
                       'FF': num_FF,
                       'RAMB36': num_ram36,
                       'RAMB18': num_ram18,
                       'DSP48E2': num_dsp,
                       'path_delay': path_delay,
                       'rent': rent,
                       'avg_fanout': avg_fanout,
                       'total_inst': total_inst}

    return util_dict


  # For double and quad pages, returns the average criteria value
  # Take the average for the all pages and assume 50% filled in for each resource (LUT, LUT_mem, FF, BRAM, DSP)
  def get_avg_criteria(self, min_size, pblock_all_resource_dict):
    # get total resource available
    with open(self.syn_dir + "/" + './resource.json', 'r') as infile:
      resource_dict = json.load(infile)

    cnt = 0
    LUT_total, LUT_mem_total, FF_total, BRAM_total, DSP_total = 0, 0, 0, 0, 0
    for pblock in pblock_all_resource_dict:
      if self.get_page_size(pblock) == min_size:
        LUT_total     += pblock_all_resource_dict[pblock]['LUT']
        LUT_mem_total += pblock_all_resource_dict[pblock]['LUT_mem']
        FF_total      += pblock_all_resource_dict[pblock]['FF']
        BRAM_total    += pblock_all_resource_dict[pblock]['RAMB18']
        DSP_total     += pblock_all_resource_dict[pblock]['DSP48E2']
        cnt += 1

    avg_LUT     = LUT_total     / cnt
    avg_LUT_mem = LUT_mem_total / cnt
    avg_FF      = FF_total      / cnt
    avg_BRAM    = BRAM_total    / cnt
    avg_DSP     = DSP_total     / cnt

    LUT_logic_percent = float(avg_LUT)     / resource_dict['LUT'] 
    LUT_mem_percent   = float(avg_LUT_mem) / resource_dict['LUT_mem']
    FF_percent        = float(avg_FF)      / resource_dict['FF']
    BRAM_percent      = float(avg_BRAM)    / resource_dict['RAMB18']
    DSP_percent       = float(avg_DSP)     / resource_dict['DSP48E2']
    criteria = LUT_logic_percent + LUT_mem_percent + FF_percent + BRAM_percent + DSP_percent
    return criteria


  # Add criterial to operator's util_dict based on resource usage
  def add_criteria_util_dict(self, util_dict, pblock_all_resource_dict, requirements):
    # get total resource available
    with open(self.syn_dir + "/" + './resource.json', 'r') as infile:
      resource_dict = json.load(infile)

    # add criteria to each op's resource dict
    for op in util_dict.keys():
      if op not in requirements:
        LUT_logic_percent = float(util_dict[op]['LUT'])     / resource_dict['LUT'] 
        LUT_mem_percent   = float(util_dict[op]['LUT_mem']) / resource_dict['LUT_mem']
        FF_percent        = float(util_dict[op]['FF'])      / resource_dict['FF']
        BRAM_percent      = float(util_dict[op]['RAMB18'])  / resource_dict['RAMB18']
        DSP_percent       = float(util_dict[op]['DSP48E2']) / resource_dict['DSP48E2']
        criteria = LUT_logic_percent + LUT_mem_percent + FF_percent + BRAM_percent + DSP_percent
        # print(criteria)
        util_dict[op]['criteria'] = criteria
      else:
        min_size = requirements[op]
        criteria = self.get_avg_criteria(min_size, pblock_all_resource_dict)
        util_dict[op]['criteria'] = criteria        

    return util_dict


  def get_pblock_in_range_resource_dict(self, pblock_all_resource_dict, low, high):
    pblock_in_range_resource_dict = {}
    for pblock in pblock_all_resource_dict:
      if(self.is_pblock_in_range(pblock, low, high)):
        pblock_in_range_resource_dict[pblock] = pblock_all_resource_dict[pblock]
    return pblock_in_range_resource_dict


  # Makes sure that all operators are mappable and outputs node weights
  # This page assignment is capacity-based(NoC congestion is not considered), greedy
  def gen_greedy_node_weight_dict(self, util_dict_selected, 
                                 pblock_in_range_resource_dict, specs_dict, requirements):
    page_valid_dict = {'2': None, '3': None, '4': None, '5': None, '6': None, '7': None, '8': None, 
        '9': None, '10': None, '11': None, '12': None, '13': None, '14': None, '15': None, '16': None, 
        '17': None, '18': None, '19': None, '20': None, '21': None, '22': None, '23': None}
    pblock_assign_dict = {}

    # iterate through util_dict_selected's op in descending order of resource usage
    # iterate through overlay_util_dict's page_num in ascending order, x[1] is op's resource dict
    for op, op_resource_dict in sorted(util_dict_selected.items(), key=lambda x:x[1]['criteria'], reverse=True): # sorted by criteria

      # op_resource_tuple = value[0]
      # print(op, op_resource_tuple)

      self.update_assignment(pblock_in_range_resource_dict, op, op_resource_dict, 
                               page_valid_dict, pblock_assign_dict, specs_dict, requirements)

    operators_list = list(util_dict_selected.keys())
    # print(operators_list)
    if(not self.is_assigned_all(pblock_assign_dict, operators_list)):
      raise Exception("Operators do not fit in any of the pre-generated NoC overlay")
    # print("## pblock_assign_dict with greedy algorithm")
    # print(pblock_assign_dict)
    # print("")    
    node_weight_dict = {"DMA": "2"}
    for op, pblock in pblock_assign_dict.items():
      node_weight_dict[op] = str(self.get_page_size(pblock))
      num_leaf_interface = specs_dict[op]['num_leaf_interface']
      assert(int(node_weight_dict[op]) >= num_leaf_interface)
    return node_weight_dict, pblock_assign_dict


  # Returns is_fit results and node weights that result in valid assignment 
  def check_is_fit_subtree(self, operators_subtree, 
                                 pblock_all_resource_dict, util_dict, 
                                 low, high, 
                                 specs_dict, requirements):
    if(low == 0 or low == 1):
      low = 2
    page_valid_dict = {}
    for i in range(low, high + 1):
      page_valid_dict[str(i)] = None
    pblock_assign_dict = {}

    pblock_in_range_resource_dict = self.get_pblock_in_range_resource_dict(pblock_all_resource_dict, low, high)

    # iterate through util_dict's op in descending order of resource usage
    # iterate through pblock_all_resource_dict's page_num in ascending order, x[1] is op's resource dict
    for op, op_resource_dict in sorted(util_dict.items(), key=lambda x:x[1]['criteria'], reverse=True): # sorted by criteria
      frequency = specs_dict[op]['kernel_clk']
      # op_resource_tuple = value[0]
      # print(op, op_resource_tuple)

      if len(util_dict) == 1: # when there's only one op to map in the subtree, try the largest first
        self.update_assignment(pblock_in_range_resource_dict, op, op_resource_dict, 
                                 page_valid_dict, pblock_assign_dict, specs_dict, requirements, False)
      else:
        self.update_assignment(pblock_in_range_resource_dict, op, op_resource_dict, 
                                 page_valid_dict, pblock_assign_dict, specs_dict, requirements)

    node_weight_dict = {}
    # print("node_weight_dict")
    # print(node_weight_dict)
    for op, pblock in pblock_assign_dict.items():
      node_weight_dict[op] = str(self.get_page_size(pblock))
    result = self.is_assigned_all(pblock_assign_dict, operators_subtree)
    return node_weight_dict, result


  # As the current BFT has 24 leaves, initially need to divide into 3 parts
  def assign_3(self, ops_dma, util_dict, pblock_all_resource_dict, partitioned_file, specs_dict, requirements):

    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]
    print(ops_dma)
    DMA_idx = ops_dma.index("DMA")
    DMA_part = parts[DMA_idx]
    if(DMA_part == '0'):
      pass
    elif(DMA_part == '1'):
      parts = self.change_part('0','-1',parts) # 0 -> -1, invalid, temp
      parts = self.change_part('1','0',parts)
      parts = self.change_part('-1','1',parts) # -1 -> 1, change to valid part
    else: # DMA_part == '2'
      parts = self.change_part('0','-1',parts) # 0 -> -1, invalid, temp
      parts = self.change_part('2','0',parts)
      parts = self.change_part('-1','2',parts) # -1 -> 2, change to valid part

    # print(parts)
    ops_0 = [ops_dma[idx] for idx in range(len(parts)) if parts[idx] == '0']
    # print(ops_0)
    util_dict_0 = self.get_util_dict_sub(ops_0, util_dict)
    # print(util_dict_0) # DMA not included
    node_w_dict_0, is_fit_subtree_0 = self.check_is_fit_subtree(ops_0, 
                                                                pblock_all_resource_dict, util_dict_0, 
                                                                0, 7, 
                                                                specs_dict, requirements)
    node_w_dict_0['DMA'] = '2'
    # print(node_w_dict_0)
    # print(is_fit_subtree_0)

    ops_1 = [ops_dma[idx] for idx in range(len(parts)) if parts[idx] == '1']
    util_dict_1 = self.get_util_dict_sub(ops_1, util_dict)
    node_w_dict_1, is_fit_subtree_1 = self.check_is_fit_subtree(ops_1, 
                                                                pblock_all_resource_dict, util_dict_1, 
                                                                8, 15, 
                                                                specs_dict, requirements)
    # print(node_w_dict_1)
    # print(is_fit_subtree_1)

    ops_2 = [ops_dma[idx] for idx in range(len(parts)) if parts[idx] == '2']
    util_dict_2 = self.get_util_dict_sub(ops_2, util_dict)
    node_w_dict_2, is_fit_subtree_2 = self.check_is_fit_subtree(ops_2, 
                                                                pblock_all_resource_dict, util_dict_2, 
                                                                16, 23, 
                                                                specs_dict, requirements)
    # print(node_w_dict_2)
    # print(is_fit_subtree_2)

    if(not is_fit_subtree_1 or not is_fit_subtree_2):
      parts = self.change_part('1','-1',parts) # 1->-1, invalid, temp
      parts = self.change_part('2','1',parts)
      parts = self.change_part('-1','2',parts) # -1->2, change to valid part

      ops_1 = [ops_dma[idx] for idx in range(len(parts)) if parts[idx] == '1']
      util_dict_1 = self.get_util_dict_sub(ops_1, util_dict)
      node_w_dict_1, is_fit_subtree_1 = self.check_is_fit_subtree(ops_1, 
                                                                  pblock_all_resource_dict, util_dict_1, 
                                                                  8, 15, specs_dict, requirements)
      # print(is_fit_subtree_1)

      ops_2 = [ops_dma[idx] for idx in range(len(parts)) if parts[idx] == '2']
      util_dict_2 = self.get_util_dict_sub(ops_2, util_dict)
      node_w_dict_2, is_fit_subtree_2 = self.check_is_fit_subtree(ops_2, 
                                                                  pblock_all_resource_dict, util_dict_2, 
                                                                  16, 23, specs_dict, requirements)
      # print(is_fit_subtree_2)


    if(not is_fit_subtree_0 or not is_fit_subtree_1 or not is_fit_subtree_2):
      node_w_dict, pblock_assign_dict_greedy = self.gen_greedy_node_weight_dict(util_dict, pblock_all_resource_dict, specs_dict, requirements)
      ops_0, ops_1, ops_2, node_w_dict_0, node_w_dict_1, node_w_dict_2 = self.assign_3_greedy(pblock_assign_dict_greedy)

    return ops_0, ops_1, ops_2, node_w_dict_0, node_w_dict_1, node_w_dict_2, parts


  # Stole from runtime.py, originally "add_bft_config_to_host_cpp"
  # For input operators, this function generates graphfile from top.cpp
  # Also Generates _operators.txt and _nodes_w.txt(node weight dictionary)
  def gen_graphfile(self, operators_list, node_w_dict, is_first_graph, graph_name):

    operator_arg_dict = self.return_operator_io_argument_dict_local(operators_list)
    print(operator_arg_dict)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': .. }

    operator_var_dict = self.return_operator_inst_dict_local(operators_list)
    print(operator_var_dict)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...

    if(is_first_graph):
      operators_dma = ["DMA"] + operators_list
    else:
      operators_dma = operators_list
    print(operators_dma)

    connection_list=self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict, operators_dma)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    connection_list = list(connection_list)
    connection_list.sort() # deterministic
    print(connection_list)
    connection_list_new = []
    for connection in connection_list:
      sender, receiver = connection.split("->")
      sender = sender.split(".")[0]
      receiver = receiver.split(".")[0]
      small_list = [sender, receiver]
      small_list.sort() # to remove duplicates
      small_tup = (small_list[0], small_list[1])
      connection_list_new.append(small_tup)
    # print(connection_list_new)
    connection_list_new = list(set(connection_list_new))
    connection_list_new.sort() # deterministic
    # print(connection_list_new)

    num_nodes = len(operators_dma)
    num_edges = len(connection_list_new)
    # print(num_nodes)
    # print(num_edges)

    # Debugging_purpose
    with open("./_graph_dir/" + self.prflow_params['benchmark_name'] + "/" + graph_name + "_nodes_w.txt", "w") as f_op:
      for op in operators_dma:
        f_op.write(str(op) + ' ' + node_w_dict[op] + '\n')

    # Used in update_parts function
    with open("./_graph_dir/" + self.prflow_params['benchmark_name'] + "/" + graph_name + "_operators.txt", "w") as f_op:
      for op in operators_dma:
        f_op.write(str(op) + '\n')

    with open("./_graph_dir/" + self.prflow_params['benchmark_name'] + "/" + graph_name + "_graphfile", "w") as f_graph:
      f_graph.write(str(num_nodes) + " " + str(num_edges) + " 011\n")
      for op in operators_dma: # graphfile is in same order as operators_dma
        # print("op: " + op)
        # print(operators_dma.index(op) + 1)
        node_weight = node_w_dict[op]
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

    # nparts = self.get_nparts(num_nodes)
    graphfile = "./_graph_dir/" + self.prflow_params['benchmark_name'] + "/" + graph_name + "_graphfile"
    return graphfile, operators_dma, num_edges


  # Update parts_old based on the assign_2 result
  def update_parts(self, parts_old, operators_0, operators_1, subtree_size, tag):
    with open("./_graph_dir/" + self.prflow_params['benchmark_name'] + "/top_p" + tag + "_operators.txt", "r") as infile:
      ops_0 = infile.readlines()   
      ops_0 = [op.strip() for op in ops_0] # contains all ops in p0 or p1 or p2

    new_parts = []
    for elem in parts_old:
      new_parts.append(int(elem))
    # print(ops_0)
    for op in operators_1:
      idx = ops_0.index(op)
      new_parts[idx] = new_parts[idx] + subtree_size

    for i, elem in enumerate(parts_old):
        parts_old[i] = new_parts[i]


  # Update node_w_dict_old based on the assign_2 result
  def update_node_w(self, node_w_dict_old, node_w_dict_0, node_w_dict_1):
    for op, weight in node_w_dict_0.items():
      node_w_dict_old[op] = node_w_dict_0[op]
    for op, weight in node_w_dict_1.items():
      node_w_dict_old[op] = node_w_dict_1[op]

  def assign_3_greedy(self, pblock_assign_dict_greedy):
    ops_0 = []
    node_w_dict_0 = {}
    ops_1 = []
    node_w_dict_1 = {}
    ops_2 = []
    node_w_dict_2 = {}
    for op, pblock_name in pblock_assign_dict_greedy.items():
      page_num_list = pblock_page_dict[pblock_name]
      page_num = min([int(page_num) for page_num in page_num_list])
      if page_num < 8:
        ops_0.append(op)
        node_w_dict_0[op] = str(self.get_page_size(pblock_name))
      elif page_num < 16:
        ops_1.append(op)
        node_w_dict_1[op] = str(self.get_page_size(pblock_name))
      else:
        ops_2.append(op)
        node_w_dict_2[op] = str(self.get_page_size(pblock_name))        
    return ops_0, ops_1, ops_2, node_w_dict_0, node_w_dict_1, node_w_dict_2

  def assign_2_greedy(self, pblock_assign_dict_greedy, low, high):
    ops_0 = []
    node_w_dict_0 = {}
    ops_1 = []
    node_w_dict_1 = {}
    half = low + (high - low + 1)//2
    for op, pblock_name in pblock_assign_dict_greedy.items():
      page_num_list = pblock_page_dict[pblock_name]
      page_num = min([int(page_num) for page_num in page_num_list])
      if page_num < half:
        ops_0.append(op)
        node_w_dict_0[op] = str(self.get_page_size(pblock_name))
      else:
        ops_1.append(op)
        node_w_dict_1[op] = str(self.get_page_size(pblock_name))
    return ops_0, ops_1, node_w_dict_0, node_w_dict_1


  # Reorder partitions if necessary and returns bi-partitioned ops
  # TODO: even is_fit_subtree_0 and is_fit_subtree_1 are True, 
  #       there's a chance that it just uses larger pages.
  #       Should I handle this to reduce fragmentation?
  #       But isn't larger page good for compile time?
  def assign_2(self, ops, 
                     util_dict, pblock_all_resource_dict, 
                     partitioned_file,
                     subtree_size, start,
                     specs_dict, requirements):

    with open(partitioned_file, "r") as infile:
      parts = infile.readlines()
      parts = [part.strip() for part in parts]
    print(ops)
    print("parts:")
    print(parts)

    # If the number of ops == 2, then parts should be [0,1] no matter what
    # metis somehow doesn't return 0,1 sometimes ;-(
    if len(ops) == 2:
      parts = ['0','1']

    if('DMA' in ops): # If this partition contains DMA, reorder
      DMA_idx = ops.index("DMA")
      DMA_part = parts[DMA_idx]
      if(DMA_part == '0'):
        pass
      else: # DMA_part == '1'
        parts = self.change_part('0','-1',parts) # 0 -> -1, invalid, temp
        parts = self.change_part('1','0',parts)
        parts = self.change_part('-1','1',parts) # -1 -> 1, change to valid part

    ops_0 = [ops[idx] for idx in range(len(parts)) if parts[idx] == '0']
    # print(ops_0)
    util_dict_0 = self.get_util_dict_sub(ops_0, util_dict)
    # print(util_dict_0) # DMA not included
    node_w_dict_0, is_fit_subtree_0 = self.check_is_fit_subtree(ops_0, 
                                                                pblock_all_resource_dict, util_dict_0, 
                                                                start, start+subtree_size//2-1, 
                                                                specs_dict, requirements)
    print("node_w_dict_0")
    print(node_w_dict_0)
    if('DMA' in ops):
      node_w_dict_0['DMA'] = '2'
    print(is_fit_subtree_0)

    ops_1 = [ops[idx] for idx in range(len(parts)) if parts[idx] == '1']
    util_dict_1 = self.get_util_dict_sub(ops_1, util_dict)
    node_w_dict_1, is_fit_subtree_1 = self.check_is_fit_subtree(ops_1, 
                                                                pblock_all_resource_dict, util_dict_1, 
                                                                start+subtree_size//2, start+subtree_size-1, 
                                                                specs_dict, requirements)
    print("node_w_dict_1")
    print(node_w_dict_1)
    print(is_fit_subtree_1)

    if((not ('DMA' in ops)) and (not is_fit_subtree_0 or not is_fit_subtree_1)):
      parts = self.change_part('1','-1',parts) # 1 -> -1, invalid, temp
      parts = self.change_part('0','1',parts)
      parts = self.change_part('-1','0',parts) # -1 -> 0, change to valid part

      ops_0 = [ops[idx] for idx in range(len(parts)) if parts[idx] == '0']
      util_dict_0 = self.get_util_dict_sub(ops_0, util_dict)
      node_w_dict_0, is_fit_subtree_0 = self.check_is_fit_subtree(ops_0, 
                                                                  pblock_all_resource_dict, util_dict_1, 
                                                                  start, start+subtree_size//2-1, 
                                                                  specs_dict, requirements)
      # print(is_fit_subtree_0)

      ops_1 = [ops[idx] for idx in range(len(parts)) if parts[idx] == '1']
      util_dict_1 = self.get_util_dict_sub(ops_1, util_dict)
      node_w_dict_1, is_fit_subtree_1 = self.check_is_fit_subtree(ops_1, 
                                                                  pblock_all_resource_dict, util_dict_1, 
                                                                  start+subtree_size//2, start+subtree_size-1, 
                                                                  specs_dict, requirements)
      # print(is_fit_subtree_1)

    # Through Error for now
    if(not is_fit_subtree_0 or not is_fit_subtree_1):
      low = start
      high = start + subtree_size - 1
      pblock_in_range_resource_dict = self.get_pblock_in_range_resource_dict(pblock_all_resource_dict, low, high)
      util_dict_01 = self.get_util_dict_sub(ops, util_dict)

      print(util_dict_01)
      print(pblock_in_range_resource_dict)
      print(ops)
      node_w_dict, pblock_assign_dict_greedy = self.gen_greedy_node_weight_dict(util_dict_01, pblock_in_range_resource_dict, specs_dict, requirements)
      print(node_w_dict)
      print(pblock_assign_dict_greedy)
      ops_0, ops_1, node_w_dict_0, node_w_dict_1 = self.assign_2_greedy(pblock_assign_dict_greedy, low, high)
      # raise Exception("TODO: what should we do if metis's output doesn't result in valid assignment?")

    # print(parts_sub)
    # self.update_parts(parts_sub, ops_0, ops_1, subtree_size//2, tag)
    # self.update_node_w(node_w_dict, node_w_dict_0, node_w_dict_1)
    # print("ops_0:")
    # print(ops_0)
    # print("node_w_dict_0:")
    # print(node_w_dict_0)
    # print("ops_1:")
    # print(ops_1)
    # print("node_w_dict_1:")
    # print(node_w_dict_1)
    # print("node_w_dict:")
    # print(node_w_dict)

    return ops_0, ops_1, node_w_dict_0, node_w_dict_1 # new node weights will be used in generating graphfile


  # As the num of edges in the graph is zero, randomly bipartition
  def gen_partition_rand(self, ops, partitioned_file):
    with open(partitioned_file, "w") as infile:
      num_ops = len(ops)
      for op in range(num_ops//2):
        infile.write('0\n')
      for op in range(num_ops//2, num_ops):
        infile.write('1\n')


  # Updates parts_sub and node_w_dict based on the results of Metis's bi-partition results
  # tag: "0", "1", "2", initial part number after dividing into three
  def recursive_bisect(self, ops, 
                             node_w_dict, util_dict, pblock_all_resource_dict,
                             subtree_size, start, filename, append, parts_sub,
                             specs_dict, tag, requirements):
    if len(node_w_dict) > 1:
      filename = filename + append
      is_first_graph = False
      graphfile, ops, num_edges = self.gen_graphfile(ops, node_w_dict, is_first_graph, filename)
      partitioned_file = "./_graph_dir/" + self.prflow_params['benchmark_name'] + "/" +\
                          str(filename) + "_graphfile" + ".part.2"
      if(num_edges > 0):
        os.system('gpmetis -ptype=rb ' + graphfile + " " + str(2) + " >/dev/null") # call Metis
      else:
        self.gen_partition_rand(ops, partitioned_file)

      ops_l, ops_r, node_w_dict_l, node_w_dict_r = \
          self.assign_2(ops, util_dict, pblock_all_resource_dict, partitioned_file, subtree_size, start, specs_dict, requirements)
      self.update_parts(parts_sub, ops_l, ops_r, subtree_size//2, tag)
      # self.update_node_w(node_w_dict, node_w_dict_l, node_w_dict_r)
      # # node_w_dict is updated at this point

      print("##################### parts_sub: ")
      print(parts_sub)
      print("")

      self.recursive_bisect(ops_l, 
                            node_w_dict_l, util_dict, pblock_all_resource_dict, 
                            subtree_size//2, start, filename, '_l', parts_sub, 
                            specs_dict, tag, requirements)
      # node_w_dict_l is updated at this point

      self.recursive_bisect(ops_r, 
                            node_w_dict_r, util_dict, pblock_all_resource_dict,
                            subtree_size//2, start+subtree_size//2, filename, '_r', parts_sub, 
                            specs_dict, tag, requirements)
      # node_w_dict_r is updated at this point

      self.update_node_w(node_w_dict, node_w_dict_l, node_w_dict_r)
      # node_w_dict is updated at this point

  # Returns pblock_assign_dict and page_assign_dict based on recursive bi-partitions
  def get_assign_dict(self, ops_0, ops_1, ops_2,
                            parts_0, parts_1, parts_2,
                            node_w_dict_0, node_w_dict_1, node_w_dict_2):
    page_assign_dict = {}
    pblock_assign_dict = {}

    for idx, op in enumerate(ops_0):
      if(op != 'DMA'):
        part_val = parts_0[idx]
        page_assign_dict[op] = part_val
        weight = node_w_dict_0[op]
        for pblock, page_list in pblock_page_dict.items():
          if(len(page_list) == int(weight) and str(part_val) in page_list):
            pblock_assign_dict[op] = pblock

    for idx, op in enumerate(ops_1):
      assert(op != 'DMA')
      part_val = parts_1[idx]
      page_assign_dict[op] = part_val
      weight = node_w_dict_1[op]
      for pblock, page_list in pblock_page_dict.items():
        if(len(page_list) == int(weight) and str(part_val) in page_list):
          pblock_assign_dict[op] = pblock

    for idx, op in enumerate(ops_2):
      assert(op != 'DMA')
      part_val = parts_2[idx]
      page_assign_dict[op] = part_val
      weight = node_w_dict_2[op]
      for pblock, page_list in pblock_page_dict.items():
        if(len(page_list) == int(weight) and str(part_val) in page_list):
          pblock_assign_dict[op] = pblock
    return pblock_assign_dict, page_assign_dict


  # Incremental, if previous assignment fits to the new netlist, use the previous assignment
  # If any of operator does not fit or new operator is introduced, perform new page assignment
  def is_prev_map_works(self, operators_list, specs_dict, pblock_all_resource_dict, util_dict):
    if(os.path.exists(self.syn_dir + '/pblock_assignment.json')):
      with open(self.syn_dir + '/pblock_assignment.json', 'r') as infile:
        pblock_assign_dict = json.load(infile)

      is_ops_all_fit = True
      for op in operators_list:
        frequency = specs_dict[op]['kernel_clk']

        if op not in pblock_assign_dict: # new operator
          is_ops_all_fit = False
        else:
          pblock_name = pblock_assign_dict[op]['pblock']
          pblock_resource_dict = pblock_all_resource_dict[pblock_name]
          op_resource_dict = util_dict[op]
          if_fit_result = self.is_fit_hard(op_resource_dict, pblock_resource_dict, pblock_name, frequency)
          # if_fit_result = self.is_fit(op_resource_dict, pblock_resource_dict, pblock_name, frequency)
          if not if_fit_result:
            is_ops_all_fit = False
      if is_ops_all_fit:
        print("##################################")
        print("## Previous page mapping works! ##")
        print("##################################")
        # In this case, there's no such op that runs implementation only ==> ops_to_compile.json and ops_to_pnr.json are the same
        os.system('cp ./input_src/' + self.prflow_params['benchmark_name'] + '/params/ops_to_compile.json ' + self.syn_dir + '/ops_to_pnr.json')
        # IMPORTANT!, write pblock.json only if the file doesn't exist (because it's newly generated and the syn directory was reset)
        for op in operators_list:
          pblock_name = pblock_assign_dict[op]["pblock"]
          page_num = pblock_assign_dict[op]["page_num"]
          if(not os.path.exists(self.syn_dir + '/' + op + '/pblock.json')):
            pblock_dict = {}
            pblock_dict['pblock'] = pblock_name
            pblock_dict['page_num'] = page_num
            with open(self.syn_dir + '/' + op + '/pblock.json', 'w') as outfile:
              json.dump(pblock_dict, outfile, sort_keys=True, indent=4)
        return True
      else:
        return False
    else:
      return False


  # For ops in operators_list, increment the pblock size based on the previous mapping (pblock.json)
  def increment_pblock_size(self, operators_list):
    requirements = {}
    for op in operators_list:
      with open(self.syn_dir + '/' + op + '/pblock.json', 'r') as infile:
        old_pblock_dict = json.load(infile)
        pblock_name_old = old_pblock_dict['pblock']
        page_num_old = old_pblock_dict['page_num']

      if self.get_page_size(pblock_name_old) == 1:
        requirements[op] = 2
      elif self.get_page_size(pblock_name_old) == 2:
        requirements[op] = 4
      elif self.get_page_size(pblock_name_old) == 4:
        raise Exception(op + " was already mapped to the quad page")

    return requirements


  def run(self, operators):
    operators_tmp_list = operators.split()
    print(operators_tmp_list)
    # e.g. operators_tmp_list could be either the full list of operators or the list of previously failed operators in implementation

    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/operators' + '/specs.json', 'r') as infile:
      specs_dict = json.load(infile)

    operators_list = list(specs_dict.keys()) # operators_list is the full list of operators

    util_dict = self.get_util_dict(operators_list)
    # print(util_dict)
    # e.g.: at this point, util_dict = {"coloringFB_bot_m": {'LUT': 1221', 'LUT_mem': 28', 'FF': 1836, ...}, 
    #                                   "data_redir_m": {'LUT': 2579', 'LUT_mem': 36', 'FF': 2560, ...}, ... }

    overlay_util_json_file = self.overlay_dir + "/ydma/zcu102/" + self.prflow_params['overlay_freq'] + "MHz/" + \
                                                "zcu102_dfx_manual/" + self.prflow_params['overlay_n'] + "/util_all.json"
    with open(overlay_util_json_file, 'r') as infile:
      pblock_all_resource_dict = json.load(infile)


    # Previous page assignment failed in implementation
    if operators_tmp_list != operators_list:
      if operators_tmp_list == []:
        raise Exception("Which operators failed in previous implementation?")

      if(os.path.exists(self.syn_dir + '/pblock_assignment.json')):
        os.system('rm ' + self.syn_dir + '/pblock_assignment.json')

      # Set requirements and revert operators_list to normal
      requirements = self.increment_pblock_size(operators_tmp_list)
      util_dict = self.add_criteria_util_dict(util_dict, pblock_all_resource_dict, requirements)
      # print(util_dict)
      # e.g.: at this point, util_dict = {"coloringFB_bot_m,": {'LUT': 1221', 'LUT_mem': 28', 'FF': 1836, ..., 'criteria': 0.049}, 
      #                                   "data_redir_m": {'LUT': 2579', 'LUT_mem': 36', 'FF': 2560, ..., 'criteria': 0.014}, ... }
      with open(self.syn_dir + '/op_recompile_list.json', 'w') as outfile:
        json.dump(operators_tmp_list, outfile, sort_keys=True, indent=4)

    else:
      requirements = {}
      util_dict = self.add_criteria_util_dict(util_dict, pblock_all_resource_dict, requirements)
      # print(util_dict)
      # e.g.: at this point, util_dict = {"coloringFB_bot_m,": {'LUT': 1221', 'LUT_mem': 28', 'FF': 1836, ..., 'criteria': 0.049}, 
      #                                   "data_redir_m": {'LUT': 2579', 'LUT_mem': 36', 'FF': 2560, ..., 'criteria': 0.014}, ... }
      if self.is_prev_map_works(operators_list, specs_dict, pblock_all_resource_dict, util_dict):
        return # Finished
      if(os.path.exists(self.syn_dir + '/pblock_assignment.json')):
        os.system('rm ' + self.syn_dir + '/pblock_assignment.json')

    print(requirements)


    # New page assginment starts
    node_w_dict, pblock_assign_dict_greedy = self.gen_greedy_node_weight_dict(util_dict, pblock_all_resource_dict, specs_dict, requirements)
    print(node_w_dict)

    os.system('mkdir -p _graph_dir/' + self.prflow_params['benchmark_name'])
    os.system('rm _graph_dir/' + self.prflow_params['benchmark_name'] + '/*')
    # print("operators")
    # print(operators)
    graph_name = "top"
    is_first_graph = True
    graphfile, operators_dma, _ = self.gen_graphfile(operators_list, node_w_dict, is_first_graph, graph_name)
    # print(graphfile)
    os.system('gpmetis -ptype=rb ' + graphfile + " " + "3" + " >/dev/null") # call Metis
    partitioned_file = "./_graph_dir/" + self.prflow_params['benchmark_name'] + "/top_graphfile" + ".part.3"


    # Initially, split into 3 parts
    ops_0, ops_1, ops_2, node_w_dict_0, node_w_dict_1, node_w_dict_2, parts = \
          self.assign_3(operators_dma, util_dict, pblock_all_resource_dict, partitioned_file, specs_dict, requirements)

    print()
    print("ops_0")
    print(ops_0) # e.g. ['DMA', 'update_knn1', 'update_knn2', 'update_knn20']
    print(node_w_dict_0)
    print("ops_1")
    print(ops_1)
    print(node_w_dict_1)
    print("ops_2")
    print(ops_2)
    print(node_w_dict_2)
    print("parts")
    print(parts)
    print()

    subtree_size, append = 8, ""

    start_0, filename_0 = 0, "top_p0"
    parts_0 = [0 for i in range(len(ops_0))]
    tag_0 = "0"
    self.recursive_bisect(ops_0, 
                          node_w_dict_0, util_dict, pblock_all_resource_dict, 
                          subtree_size, start_0, filename_0, "", parts_0,  
                          specs_dict, tag_0, requirements)

    start_1, filename_1 = 8, "top_p1"
    parts_1 = [8 for i in range(len(ops_1))]
    tag_1 = "1"
    self.recursive_bisect(ops_1, 
                          node_w_dict_1, util_dict, pblock_all_resource_dict, 
                          subtree_size, start_1, filename_1, "", parts_1,  
                          specs_dict, tag_1, requirements)

    start_2, filename_2 = 16, "top_p2"
    parts_2 = [16 for i in range(len(ops_2)) ]
    tag_2 = "2"
    self.recursive_bisect(ops_2, 
                          node_w_dict_2, util_dict, pblock_all_resource_dict, 
                          subtree_size, start_2, filename_2, "", parts_2,  
                          specs_dict, tag_2, requirements)

    pblock_assign_dict, page_assign_dict = self.get_assign_dict(ops_0, ops_1, ops_2, 
                                                                parts_0, parts_1, parts_2,
                                                                node_w_dict_0, node_w_dict_1, node_w_dict_2)

    # print(ops_0) # e.g. ['DMA', 'update_knn1', 'update_knn2', 'update_knn20']
    # print(ops_1)
    # print(ops_2)

    # print(parts_0)
    # print(parts_1)
    # print(parts_2)
    print("")
    print("## node weight dict")
    print(node_w_dict_0)
    print(node_w_dict_1)
    print(node_w_dict_2)

    print("")
    print("## page_assign_dict")
    print(page_assign_dict)
    print("")
    print("## pblock_assign_dict")
    print(pblock_assign_dict)
    print("")
    # assert(len(operators.split()) == len(pblock_assign_dict))
    # assert(len(operators.split()) == len(page_assign_dict))
    if(not self.is_assigned_all(pblock_assign_dict, operators_list)):
      raise Exception("SHOULD NOT REACH HERE, SHOULD HAVE CAUGHT EARLIER")    

    # Add leaf interface mapping to pblock_assign_dict
    new_pblock_assign_dict = {} 
    for op in pblock_assign_dict.keys():
      new_pblock_assign_dict[op] = {}
      new_pblock_assign_dict[op]["pblock"] = pblock_assign_dict[op]
      new_pblock_assign_dict[op]["page_num"] = page_assign_dict[op]

      with open(self.syn_dir + '/' + op + '/leaf_interface_mapping.json', 'r') as infile:
        print(op)
        leaf_interface_mapping_dict = json.load(infile)
      new_pblock_assign_dict[op]["leaf_interface"] = leaf_interface_mapping_dict

    with open(self.syn_dir + '/pblock_assignment.json', 'w') as outfile:
      json.dump(new_pblock_assign_dict, outfile, sort_keys=True, indent=4)

    # ops_to_compile should be subset of ops_to_pnr
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/ops_to_compile.json', 'r') as infile:
      ops_to_pnr = json.load(infile)

    # For incremental compile, let each operator to have separate .json file
    for op_impl in pblock_assign_dict:
      ops = op_impl.split()
      for op in ops:
        pblock_name = new_pblock_assign_dict[op_impl]["pblock"]
        page_num = new_pblock_assign_dict[op_impl]["page_num"]
        # IMPORTANT!, update pblock.json only when the contents have been changed
        if(os.path.exists(self.syn_dir + '/' + op + '/pblock.json')):
          with open(self.syn_dir + '/' + op + '/pblock.json', 'r') as infile:
            old_pblock_dict = json.load(infile)
            pblock_name_old = old_pblock_dict['pblock']
            page_num_old = old_pblock_dict['page_num']
            # if leaf interface has changed, netlist has changed. And definitely runs a new impl => don't need to check here
          if(pblock_name != pblock_name_old or page_num != page_num_old):
            pblock_dict = {}
            pblock_dict['pblock'] = pblock_name
            pblock_dict['page_num'] = page_num

            if op not in ops_to_pnr:
              ops_to_pnr.append(op)
            with open(self.syn_dir + '/' + op + '/pblock.json', 'w') as outfile:
              json.dump(pblock_dict, outfile, sort_keys=True, indent=4)

        else: # first time
          pblock_dict = {}
          pblock_dict['pblock'] = pblock_name
          pblock_dict['page_num'] = page_num
          with open(self.syn_dir + '/' + op + '/leaf_interface_mapping.json', 'r') as infile:
            leaf_interface_mapping_dict = json.load(infile)
          pblock_dict['leaf_interface'] = leaf_interface_mapping_dict

          if op not in ops_to_pnr:
            ops_to_pnr.append(op)
          with open(self.syn_dir + '/' + op + '/pblock.json', 'w') as outfile:
            json.dump(pblock_dict, outfile, sort_keys=True, indent=4)
    
    with open(self.syn_dir + '/ops_to_pnr.json', 'w') as outfile:
      json.dump(ops_to_pnr, outfile, sort_keys=True, indent=4)
