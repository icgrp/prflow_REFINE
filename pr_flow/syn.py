# -*- coding: utf-8 -*-   
# Company: IC group, University of Pennsylvania
# Contributor: Yuanlong Xiao
#
# Create Date: 02/11/2021
# Design Name: syn.py
# Project Name: PLD
# Versions: 1.0
# Description: This is a python script to prepare the script for Out-Context-Synthesis 
#              from verilog to DCP for PRFlow
# Dependencies: python2, gen_basic.py hls.py config.py
# Revision:
# Revision 0.01 - File Created
# Revision 0.02 - Update cotents for HiPR
#
# Additional Comments:

import os, json
import subprocess
from pr_flow.gen_basic import gen_basic
import math
import numpy as np

class syn(gen_basic):

  # helper function for gen_leaf_interface_mapping
  # from https://more-itertools.readthedocs.io/en/stable/
  def set_partition(self, iterable, k=None):
      """
      Yield the set partitions of *iterable* into *k* parts. Set partitions are
      not order-preserving.

      >>> iterable = 'abc'
      >>> for part in set_partitions(iterable, 2):
      ...     print([''.join(p) for p in part])
      ['a', 'bc']
      ['ab', 'c']
      ['b', 'ac']


      If *k* is not given, every set partition is generated.

      >>> iterable = 'abc'
      >>> for part in set_partitions(iterable):
      ...     print([''.join(p) for p in part])
      ['abc']
      ['a', 'bc']
      ['ab', 'c']
      ['b', 'ac']
      ['a', 'b', 'c']

      """
      L = list(iterable)
      n = len(L)
      if k is not None:
          if k < 1:
              raise ValueError(
                  "Can't partition in a negative or zero number of groups"
              )
          elif k > n:
              return

      def set_partitions_helper(L, k):
          n = len(L)
          if k == 1:
              yield [L]
          elif n == k:
              yield [[s] for s in L]
          else:
              e, *M = L
              for p in set_partitions_helper(M, k - 1):
                  yield [[e], *p]
              for p in set_partitions_helper(M, k):
                  for i in range(len(p)):
                      yield p[:i] + [[e] + p[i]] + p[i + 1 :]

      if k is None:
          for k in range(1, n + 1):
              yield from set_partitions_helper(L, k)
      else:
          yield from set_partitions_helper(L, k)

  # helper function for gen_leaf_interface_mapping
  def minimize_partition_difference(self, arr, number_subs):
      total_sum = sum(arr)
      min_diff = float('inf')
      best_partitions = []
      
      avg = total_sum / len(arr)

      for partition in self.set_partition(arr, number_subs):
          partition_sums = [sum(group) for group in partition]
          partition_sums = [sum_element-avg for sum_element in partition_sums]
          diff = math.sqrt(sum(np.square(partition_sums))/number_subs)
          if diff < min_diff:
              min_diff = diff
              best_partitions = partition
      return best_partitions

  # helper function for gen_leaf_interface_mapping
  def map_value_to_keys_dict(self, input_dict):
      output_dict = {}
      
      for key, value in input_dict.items():
          if value not in output_dict:
              output_dict[value] = [key]
          else:
              output_dict[value].append(key)
      
      return output_dict

  # generates leaf interface mapping for user operator's IO to minimize the standard deviation of sums of channel widths
  # e.g.: num_leaf_interface = 2
  # operator_input_width_dict, e.g. {'Input_1':96, 'Input_2':32, 'Input_3':128}
  # operator_output_width_dict, e.g. {'Output_1':32}
  # returns {0: ['Input_1', 'Input_2', 'Output_1'],   # sum of input ports' channel width: 128
  #          1: ['Input_3']}                          # sum of input ports' channel width: 128
  def gen_leaf_interface_mapping(self, operator_input_width_dict, operator_output_width_dict, num_leaf_interface):
      
      ## dict input loading
      input_load = list(operator_input_width_dict.values())
      input_load_keys = list(operator_input_width_dict.keys())
      output_load = list(operator_output_width_dict.values())
      output_load_keys = list(operator_output_width_dict.keys())
      
      ## Initialization of output dict
      leaf_interface_mapping_dict = {}

      ## input width dict
      input_leaf_interface_mapping_dict = {}
      for index in range(num_leaf_interface) :
          input_leaf_interface_mapping_dict[index] = []
      # if not enough elements in the input dict, simply append keys
      if len(input_load) < num_leaf_interface :
          for index in range(len(input_load)) :
              input_leaf_interface_mapping_dict[index].append(input_load_keys[index])
      else :
          idx = 0
          input_distinct_list = []
          for item in input_load:
              if item not in input_distinct_list:
                  input_distinct_list.append(item)

          input_map_dict = self.map_value_to_keys_dict(operator_input_width_dict)
          input_minimized_pattern_dict = self.minimize_partition_difference(input_load, num_leaf_interface)
          for item in input_minimized_pattern_dict :
              for elem in item :
                  input_leaf_interface_mapping_dict[idx].append(input_map_dict[elem][0])
                  input_map_dict[elem].pop(0)
              idx += 1

      ## output width dict
      output_leaf_interface_mapping_dict = {}
      for index in range(num_leaf_interface) :
          output_leaf_interface_mapping_dict[index] = []
      # if not enough elements in the output dict, simply append keys
      if len(output_load) < num_leaf_interface :
          for index in range(len(output_load)) :
              output_leaf_interface_mapping_dict[index].append(output_load_keys[index])
      else :
          idx = 0
          output_distinct_list = []
          for item in output_load:
              if item not in output_distinct_list:
                  output_distinct_list.append(item)

          output_map_dict = self.map_value_to_keys_dict(operator_output_width_dict)
          output_minimized_pattern_dict = self.minimize_partition_difference(output_load, num_leaf_interface)
          for item in output_minimized_pattern_dict :
              for elem in item :
                  output_leaf_interface_mapping_dict[idx].append(output_map_dict[elem][0])
                  output_map_dict[elem].pop(0)
              idx += 1

      ## filling the output dict
      for index in range(num_leaf_interface) :
          leaf_interface_mapping_dict[index] = input_leaf_interface_mapping_dict[index] + output_leaf_interface_mapping_dict[index]
      
      return leaf_interface_mapping_dict




  def return_bit_size(self, num):
    bit_size = 1
    num_local = int(num)
    while (True):
      if (num_local >> 1) != 0:
        num_local = num_local >> 1 
        bit_size = bit_size + 1
      else:
        return bit_size


  def ceiling_mem_size(self, size_in):
    size_out = 1
    # use 3/4 of the power-of-2 size to improve BRAM effeciency
    is_triple = 0
    while(size_out < int(size_in)):
      size_out = size_out * 2

    if size_out/4*3 < int(size_in):
      is_triple = 0
      return is_triple, size_out
    else:
      is_triple = 1
      return is_triple, size_out/4*3

  def return_bram18_number(self, size_in, input_num, output_num):
    out= int(size_in)/2048 + int(self.prflow_params['input_port_bram_cost'])*input_num+int(self.prflow_params['output_port_bram_cost'])*output_num + 1
    return out
 

  # Placeholder
  # def gen_leaf_interface_mapping(self, operator_input_width_dict, operator_output_width_dict, num_leaf_interface):
  #   leaf_interface_mapping_dict = {}
  #   for i in range(num_leaf_interface):
  #     leaf_interface_mapping_dict[str(i)] = []

  #   leaf_interface_mapping_dict['0'] += list(operator_input_width_dict.keys())
  #   leaf_interface_mapping_dict['0'] += list(operator_output_width_dict.keys())
  #   return leaf_interface_mapping_dict


  def prepare_HW(self, operator, page_num, specs_dict):
    frequency = specs_dict[operator]['kernel_clk']
    num_leaf_interface = specs_dict[operator]['num_leaf_interface']

    # Update syn.xdc
    filedata = ''
    if num_leaf_interface > 1:
      for i in range(num_leaf_interface):
        filedata += "create_clock -period 5.0 -name clk_200_" + str(i) + " [get_ports clk_200_" + str(i) + "]\n"
        filedata += "create_clock -period 4.0 -name clk_250_" + str(i) + " [get_ports clk_250_" + str(i) + "]\n"
        filedata += "create_clock -period 3.33 -name clk_300_" + str(i) + " [get_ports clk_300_" + str(i) + "]\n"
        filedata += "create_clock -period 2.85 -name clk_350_" + str(i) + " [get_ports clk_350_" + str(i) + "]\n"
        filedata += "create_clock -period 2.5 -name clk_400_" + str(i) + " [get_ports clk_400_" + str(i) + "]\n"
    with open (self.syn_dir+'/'+operator+'/syn.xdc', 'w') as outfile:
      outfile.write(filedata)

    # # Update target clock, edit: now each kernel different kernel clk
    # clk_period = '{:.1f}'.format(1000 / int(frequency))
    # # with open (self.syn_dir+'/'+operator+'/syn.xdc', 'r') as infile:
    # #   filedata = infile.readlines()
    # # assert(len(filedata) == 1)
    # # filedata = filedata[0]
    # # filedata = filedata.replace('TARGET_CLK', clk_period)
    # filedata = "create_clock -period " + str(clk_period) + " -name clk_user [get_ports clk_user]"
    # with open (self.syn_dir+'/'+operator+'/syn.xdc', 'w') as outfile:
    #   outfile.write(filedata)

    # If the map target is Hardware, we need to prepare the HDL files and scripts to compile it.
    self.shell.mkdir(self.syn_dir+'/'+operator+'/src')
    file_list = [ 'Config_Controls.v', 'rise_detect.v',         'converge_ctrl.v',
                  'ExtractCtrl.v',     'Input_Port_Cluster.v',  'Input_Port.v',          'leaf_interface.v',   'Output_Port_Cluster.v',
                  'Output_Port.v',     'read_b_in.v',           'ram0.v',                'single_ram.v',       'SynFIFO.v',
                  'xram_triple.v',     'Stream_Flow_Control.v', 'write_b_in.v',          'write_b_out.v',
                  'expand_queue.v',        'shrink_queue.v',        'send_IO_queue_cnt.v']
    # file_list = ['expand_queue.v',        'shrink_queue.v']

    # copy the necessary leaf interface verilog files for out-of-context compilation
    for name in file_list: self.shell.cp_file(self.overlay_dir+'/src/'+name, self.syn_dir+'/'+operator+'/src/'+name)

    # prepare the tcl files for out-of-context compilation

    self.shell.write_lines(self.syn_dir+'/'+operator+'/syn_page.tcl', self.tcl.return_syn_page_tcl_list(operator, 
                                                                                                          ['./leaf.v'], 
                                                                                                          rpt_name='utilization.rpt', 
                                                                                                          frequency=frequency))

    # prepare the leaf verilog files.
    # Id depends on the IO numbers and operator name

    # extract the stream arguments and types (in/out and width) for all the operators
    operator_arg_dict, operator_width_dict = self.dataflow.return_operator_io_argument_dict(operator)
    # e.g. operator_arg_dict: {'zculling_bot': ['Input_1', 'Input_2', 'Output_1']}
    # e.g. operator_width_dict: {'zculling_bot': ['ap_uint<32>', 'ap_uint<32>', 'ap_uint<32>']}
    # in_width_list, out_width_list = self.dataflow.return_io_width(operator_width_dict[operator], operator_arg_dict[operator])
    input_num  = len([io_port for io_port in operator_arg_dict[operator] if io_port.startswith('Input_')]) 
    output_num = len([io_port for io_port in operator_arg_dict[operator] if io_port.startswith('Output_')]) 
    # print(operator_arg_dict)
    # print(operator_width_dict)

    operator_input_width_dict = {}
    operator_output_width_dict = {}
    for idx, io_port in enumerate(operator_arg_dict[operator]):
      if io_port.startswith('Input_'):
        operator_input_width_dict[io_port] = int(operator_width_dict[operator][idx].split('<')[1].split('>')[0]) # extract 32 from ap_uint<32>
      else:
        assert(io_port.startswith('Output_'))
        operator_output_width_dict[io_port] = int(operator_width_dict[operator][idx].split('<')[1].split('>')[0])

    # print(operator_arg_dict)
    # print(operator_width_dict)
    # print(operator_input_width_dict)
    # print(operator_output_width_dict)
    # TODO: fix this
    leaf_interface_mapping_dict = self.gen_leaf_interface_mapping(operator_input_width_dict, operator_output_width_dict, num_leaf_interface)
    # print(leaf_interface_mapping_dict)
    with open(self.syn_dir + '/' + operator + '/leaf_interface_mapping.json', 'w') as outfile:
      json.dump(leaf_interface_mapping_dict, outfile, sort_keys=True, indent=4)

    # prepare the leaf Verilog file for the DFX page
    if num_leaf_interface == 1:
      self.shell.write_lines(self.syn_dir+'/'+operator+'/leaf.v',
                           self.verilog.return_single_page_v_list(page_num,
                                                           operator,
                                                           input_num,
                                                           output_num,
                                                           operator_arg_dict[operator],
                                                           operator_width_dict[operator],
                                                           frequency,
                                                           for_syn=True,
                                                           is_riscv=False),
                           False)
    else:
      self.shell.write_lines(self.syn_dir+'/'+operator+'/leaf.v',
                           self.verilog.return_non_single_page_v_list(page_num,
                                                           operator,
                                                           input_num,
                                                           output_num,
                                                           operator_arg_dict[operator],
                                                           operator_width_dict[operator],
                                                           frequency,
                                                           num_leaf_interface,
                                                           leaf_interface_mapping_dict,
                                                           for_syn=True,
                                                           is_riscv=False),
                           False)


    # Prepare the shell script to run vivado
    self.shell.write_lines(self.syn_dir+'/'+operator+'/run.sh', self.shell.return_run_sh_list(self.prflow_params['Xilinx_dir'], 
                                                                                              'syn_page.tcl', 
                                                                                              self.prflow_params['back_end'] 
                                                                                              ), True)

  # update OVERLAY_DIR in pg_assign.py
  def update_pg_assign(self, directory, dest_dir):
    pyfile = directory + '/nested_pg_assign.py'
    filedata = ''
    with open(pyfile, 'r') as file:
      filedata = file.read()
    filedata = filedata.replace('/PATH_TO_OVERLAY', dest_dir)

    with open(pyfile, 'w') as file:
      file.write(filedata)


  # create one directory for each page 
  def create_page(self, operator, specs_dict):
    self.shell.re_mkdir(self.syn_dir+'/'+operator)

    # map_target_exist, map_target = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h', 'map_target')
    # page_num_exist,   page_num   =  self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h', 'map_target')
    self.shell.write_lines(self.syn_dir+'/'+operator+'/main.sh', self.shell.return_main_sh_list(
                                                                                                  './run.sh', 
                                                                                                  self.prflow_params['back_end'], 
                                                                                                  'hls_'+operator, 
                                                                                                  'syn_'+operator, 
                                                                                                  self.prflow_params['grid'], 
                                                                                                  'qsub@qsub.com',
                                                                                                  self.prflow_params['mem'], 
                                                                                                  self.prflow_params['node']
                                                                                                   ), True)

    # copy the script to monitor mem usage and the number of running cores
    # self.shell.cp_dir('./common/script_src/parse_htop.py', self.syn_dir)
    # copy the script to assign operator to an appropriate page based on resource util after synthesis
    # self.shell.cp_dir('./common/script_src/nested_pg_assign.py', self.syn_dir)
    dest_dir = self.overlay_dir +'/ydma/'+self.prflow_params['board']+'/'+self.prflow_params['board']+'_dfx_manual'+'/'
    dest_dir = os.path.abspath(dest_dir)
    # self.update_pg_assign(self.syn_dir, dest_dir) # don't need anymore
    # copy resource data for the board
    self.shell.cp_dir('./common/script_src/resource_' + self.prflow_params['board'] + '.json', self.syn_dir + '/resource.json')
    self.shell.cp_dir('./common/script_src/syn.xdc', self.syn_dir + '/' + operator + '/syn.xdc')

    # Not using RISC-V
    page_num = 42 # 42 is random value, page_num can be used when generating simulation sources
    self.prepare_HW(operator, page_num, specs_dict)
    # if map_target == 'HW': 
    #   self.prepare_HW(operator, page_num, monitor_on)
    # else:
    #   # prepare script files for riscv implementation.
    #   # As we don't need to compile any verilog files, we only need to perform 
    #   # RISC-V compile flow
    #   self.prepare_RISCV(operator, page_num, input_num, output_num)


  def run(self, operator):
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/operators' + '/specs.json', 'r') as infile:
      # pblock_operators_list = json.load(infile)
      specs_dict = json.load(infile)

    # mk work directory
    self.shell.mkdir(self.syn_dir)
    # create ip directories for the operator
    self.create_page(operator, specs_dict)

     
