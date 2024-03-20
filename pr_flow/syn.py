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
  # operator_input_width_dict, e.g. {'Input_1':96, 'Input_2':128, 'Input_3':32}
  # operator_output_width_dict, e.g. {'Output_1':32}
  # returns {0: ['Input_1', 'Input_3', 'Output_1'],   # sum of input ports' channel width: 128
  #          1: ['Input_2']}                          # sum of input ports' channel width: 128
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
 

  def calculate_small_fifo_depth(self, leaf_interface_mapping_dict):
    num_i_ports_include_dummy = 0 # includes dummy ports for this operator
    num_o_ports_include_dummy = 0 # includes dummy ports for this operator
    for idx_leaf_interface in range(len(leaf_interface_mapping_dict)):
      mapped_IO_ports = leaf_interface_mapping_dict[idx_leaf_interface] # io ports for this leaf interface
      mapped_I_ports = [io_port for io_port in mapped_IO_ports if io_port.startswith('Input_')] # input port for this leaf interface
      mapped_O_ports = [io_port for io_port in mapped_IO_ports if io_port.startswith('Output_')] # output port for this leaf interface
      i_port_cnt = len(mapped_I_ports)
      o_port_cnt = len(mapped_O_ports)
      if i_port_cnt == 0:
        num_i_ports_include_dummy += 1
      else:
        num_i_ports_include_dummy += i_port_cnt
      if o_port_cnt == 0:
        num_o_ports_include_dummy += 1
      else:
        num_o_ports_include_dummy += o_port_cnt
    num_total_counter = 3*num_i_ports_include_dummy + 2*num_o_ports_include_dummy + 1
    if(num_total_counter>32): return 64
    elif(num_total_counter>16): return 32
    else: return 16


  # Placeholder
  # def gen_leaf_interface_mapping(self, operator_input_width_dict, operator_output_width_dict, num_leaf_interface):
  #   leaf_interface_mapping_dict = {}
  #   for i in range(num_leaf_interface):
  #     leaf_interface_mapping_dict[str(i)] = []

  #   leaf_interface_mapping_dict['0'] += list(operator_input_width_dict.keys())
  #   leaf_interface_mapping_dict['0'] += list(operator_output_width_dict.keys())
  #   return leaf_interface_mapping_dict

  # leaf_interface_mapping_dict, e.g. {"0": ["Input_1","Output_1"],"1": ["Input_2"],"2": ["Input_3"],"3": []}
  # operator_input_width_dict, e.g. {'Input_1':32, 'Input_2': 64}
  def write_input_port_cluster(self, operator_input_width_dict, leaf_interface_mapping_dict, input_num, operator):
    # Input_Port_Cluster per leaf interface
    for idx_leaf_interface in range(len(leaf_interface_mapping_dict)):
      filedata_str_list = []
      filedata_str_list.append('`timescale 1ns / 1ps')
      filedata_str_list.append('module Input_Port_Cluster_' + str(idx_leaf_interface) + ' # (')
      filedata_str_list.append('    parameter PACKET_BITS = 97,')
      filedata_str_list.append('    parameter NUM_LEAF_BITS = 6,')
      filedata_str_list.append('    parameter NUM_PORT_BITS = 4,')
      filedata_str_list.append('    parameter NUM_ADDR_BITS = 7,')
      filedata_str_list.append('    parameter PAYLOAD_BITS = 64, ')
      filedata_str_list.append('    parameter NUM_IN_PORTS = 7, ')
      filedata_str_list.append('    parameter NUM_OUT_PORTS = 7,')
      filedata_str_list.append('    parameter NUM_BRAM_ADDR_BITS = 7,')
      filedata_str_list.append('    parameter FREESPACE_UPDATE_SIZE = 64,')
      filedata_str_list.append('    parameter DATA_USER_IN_TOTAL = 32')
      filedata_str_list.append('    )(')
      filedata_str_list.append('    input clk,')
      filedata_str_list.append('    input clk_user,')
      filedata_str_list.append('    input reset,')
      filedata_str_list.append('    input reset_user,')
      filedata_str_list.append('')
      filedata_str_list.append('    // internal interface')
      filedata_str_list.append('    output [NUM_IN_PORTS-1:0] freespace_update,')
      filedata_str_list.append('    output [PACKET_BITS*NUM_IN_PORTS-1:0] packet_from_input_ports,')
      filedata_str_list.append('    input [PACKET_BITS-1:0] stream_in,')
      filedata_str_list.append('    input [(NUM_LEAF_BITS+NUM_PORT_BITS)*NUM_IN_PORTS-1:0] in_control_reg,')
      filedata_str_list.append('')
      filedata_str_list.append('    // user interface')
      filedata_str_list.append('    output [DATA_USER_IN_TOTAL-1:0] dout2user,')
      filedata_str_list.append('    output [NUM_IN_PORTS-1:0] vld2user,')
      filedata_str_list.append('    input [NUM_IN_PORTS-1:0] ack_user2b_in,')
      filedata_str_list.append('')
      filedata_str_list.append('    input is_done_mode, // clk(_bft) domain')
      filedata_str_list.append('    input is_done_mode_user, // clk_user domain')
      filedata_str_list.append('    output [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_full_cnt,')
      filedata_str_list.append('    output [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_empty_cnt,')
      filedata_str_list.append('    output [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_read_cnt,')
      filedata_str_list.append('    output input_port_cluster_stall_condition')
      filedata_str_list.append('    );')
      filedata_str_list.append('')
      filedata_str_list.append('    wire [NUM_IN_PORTS-1:0] input_port_stall_condition;')
      filedata_str_list.append('    assign input_port_cluster_stall_condition = |input_port_stall_condition;')
      filedata_str_list.append('')
      filedata_str_list.append('')
      mapped_IO_ports = leaf_interface_mapping_dict[idx_leaf_interface] # io ports for this leaf interface
      mapped_I_ports = [io_port for io_port in mapped_IO_ports if io_port.startswith('Input_')] # input port for this leaf interface
      DATA_USER_IN_TOTAL = 0
      for i_port in mapped_I_ports:
        DATA_USER_IN_TOTAL += operator_input_width_dict[i_port] # input port width total for this leaf interface

      count = 0
      DATA_USER_IN_TOTAL_min32 = 0
      for i in range(int(input_num),0,-1): # descending.. e.g. 3, 2, 1, 0
        if 'Input_' + str(i) in mapped_I_ports:
          idx_port = len(mapped_I_ports)-1-count
          DATA_USER_IN = operator_input_width_dict['Input_' + str(i)]
          if DATA_USER_IN < 32:
            DATA_USER_IN_min32 = 32
          else:
            DATA_USER_IN_min32 = DATA_USER_IN
          DATA_USER_IN_TOTAL_min32 += DATA_USER_IN_min32
          count += 1

      if len(mapped_I_ports) == 0: # dummy input port
        filedata_str_list.append('    wire [31:0] dout2user_tmp;')
        filedata_str_list.append('')

        filedata_str_list.append('    Input_Port #(')
        filedata_str_list.append('        .PACKET_BITS(PACKET_BITS),')
        filedata_str_list.append('        .NUM_LEAF_BITS(NUM_LEAF_BITS),')
        filedata_str_list.append('        .NUM_PORT_BITS(NUM_PORT_BITS),')
        filedata_str_list.append('        .NUM_ADDR_BITS(NUM_ADDR_BITS),')
        filedata_str_list.append('        .PAYLOAD_BITS(PAYLOAD_BITS),')
        filedata_str_list.append('        .NUM_IN_PORTS(NUM_IN_PORTS),')
        filedata_str_list.append('        .NUM_OUT_PORTS(NUM_OUT_PORTS),')
        filedata_str_list.append('        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),')
        filedata_str_list.append('        .PORT_No(0+2),')
        filedata_str_list.append('        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),')
        filedata_str_list.append('        .DATA_USER_IN(32) // OPERATOR SPECIFIC!')
        filedata_str_list.append('    )IPort_0(')
        filedata_str_list.append('        .clk(clk),')
        filedata_str_list.append('        .clk_user(clk_user),')
        filedata_str_list.append('        .reset(reset),')
        filedata_str_list.append('        .reset_user(reset_user),')
        filedata_str_list.append('        .freespace_update(freespace_update[0]),')
        filedata_str_list.append('        .packet_from_input_port(packet_from_input_ports[PACKET_BITS*(0+1)-1:PACKET_BITS*0]),')
        filedata_str_list.append('        .din_leaf_bft2interface(stream_in),')
        filedata_str_list.append('        .src_leaf(in_control_reg[(NUM_LEAF_BITS+NUM_PORT_BITS)*(0+1)-1:(NUM_LEAF_BITS+NUM_PORT_BITS)*0+NUM_PORT_BITS]),')
        filedata_str_list.append('        .src_port(in_control_reg[(NUM_LEAF_BITS+NUM_PORT_BITS)*0+NUM_PORT_BITS-1:(NUM_LEAF_BITS+NUM_PORT_BITS)*0]),')
        filedata_str_list.append('')
        filedata_str_list.append('        .dout2user(dout2user_tmp[31:0]), // OPERATOR SPECIFIC!')
        filedata_str_list.append('        .vld2user(vld2user[0]),')
        filedata_str_list.append('        .ack_user2b_in(ack_user2b_in[0]),')
        filedata_str_list.append('')
        filedata_str_list.append('        .is_done_mode(is_done_mode),')
        filedata_str_list.append('        .is_done_mode_user(is_done_mode_user),')
        filedata_str_list.append('        .input_port_full_cnt(input_port_full_cnt[PAYLOAD_BITS*(0+1)-1:PAYLOAD_BITS*0]),')
        filedata_str_list.append('        .input_port_empty_cnt(input_port_empty_cnt[PAYLOAD_BITS*(0+1)-1:PAYLOAD_BITS*0]),')
        filedata_str_list.append('        .input_port_read_cnt(input_port_read_cnt[PAYLOAD_BITS*(0+1)-1:PAYLOAD_BITS*0]),')
        filedata_str_list.append('        .input_port_stall_condition(input_port_stall_condition[0])')
        filedata_str_list.append('    );')
        filedata_str_list.append('    assign dout2user = dout2user_tmp; // only low bits')
        filedata_str_list.append('')
      else:
        filedata_str_list.append('    wire [' + str(DATA_USER_IN_TOTAL_min32-1) + ':0] dout2user_tmp;')
        filedata_str_list.append('')
        count = 0
        for i in range(int(input_num),0,-1): # descending.. e.g. 3, 2, 1, 0
          if 'Input_' + str(i) in mapped_I_ports:
            idx_port = len(mapped_I_ports)-1-count
            DATA_USER_IN = operator_input_width_dict['Input_' + str(i)]
            if DATA_USER_IN < 32:
              DATA_USER_IN_min32 = 32
            else:
              DATA_USER_IN_min32 = DATA_USER_IN

            filedata_str_list.append('    Input_Port #(')
            filedata_str_list.append('        .PACKET_BITS(PACKET_BITS),')
            filedata_str_list.append('        .NUM_LEAF_BITS(NUM_LEAF_BITS),')
            filedata_str_list.append('        .NUM_PORT_BITS(NUM_PORT_BITS),')
            filedata_str_list.append('        .NUM_ADDR_BITS(NUM_ADDR_BITS),')
            filedata_str_list.append('        .PAYLOAD_BITS(PAYLOAD_BITS),')
            filedata_str_list.append('        .NUM_IN_PORTS(NUM_IN_PORTS),')
            filedata_str_list.append('        .NUM_OUT_PORTS(NUM_OUT_PORTS),')
            filedata_str_list.append('        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),')
            filedata_str_list.append('        .PORT_No(' + str(idx_port) + '+2),')
            filedata_str_list.append('        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),')
            filedata_str_list.append('        .DATA_USER_IN(' + str(DATA_USER_IN_min32) + ') // OPERATOR SPECIFIC!')
            filedata_str_list.append('    )IPort_' + str(idx_port) +  '(')
            filedata_str_list.append('        .clk(clk),')
            filedata_str_list.append('        .clk_user(clk_user),')
            filedata_str_list.append('        .reset(reset),')
            filedata_str_list.append('        .reset_user(reset_user),')
            filedata_str_list.append('        .freespace_update(freespace_update[' + str(idx_port) + ']),')
            filedata_str_list.append('        .packet_from_input_port(packet_from_input_ports[PACKET_BITS*(' + str(idx_port) + '+1)-1:PACKET_BITS*' + str(idx_port) + ']),')
            filedata_str_list.append('        .din_leaf_bft2interface(stream_in),')
            filedata_str_list.append('        .src_leaf(in_control_reg[(NUM_LEAF_BITS+NUM_PORT_BITS)*(' + str(idx_port) + '+1)-1:(NUM_LEAF_BITS+NUM_PORT_BITS)*' + str(idx_port) + '+NUM_PORT_BITS]),')
            filedata_str_list.append('        .src_port(in_control_reg[(NUM_LEAF_BITS+NUM_PORT_BITS)*' + str(idx_port) + '+NUM_PORT_BITS-1:(NUM_LEAF_BITS+NUM_PORT_BITS)*' + str(idx_port) + ']),')
            filedata_str_list.append('')
            high_addr_tmp = DATA_USER_IN_TOTAL_min32 - 1
            low_addr_tmp = DATA_USER_IN_TOTAL_min32 - DATA_USER_IN_min32
            filedata_str_list.append('        .dout2user(dout2user_tmp[' + str(high_addr_tmp) + ':' + str(low_addr_tmp) + ']), // OPERATOR SPECIFIC!')
            DATA_USER_IN_TOTAL_min32 = DATA_USER_IN_TOTAL_min32 - DATA_USER_IN_min32
            filedata_str_list.append('        .vld2user(vld2user[' + str(idx_port) + ']),')
            filedata_str_list.append('        .ack_user2b_in(ack_user2b_in[' + str(idx_port) + ']),')
            filedata_str_list.append('')
            filedata_str_list.append('        .is_done_mode(is_done_mode),')
            filedata_str_list.append('        .is_done_mode_user(is_done_mode_user),')
            filedata_str_list.append('        .input_port_full_cnt(input_port_full_cnt[PAYLOAD_BITS*(' + str(idx_port) + '+1)-1:PAYLOAD_BITS*' + str(idx_port) + ']),')
            filedata_str_list.append('        .input_port_empty_cnt(input_port_empty_cnt[PAYLOAD_BITS*(' + str(idx_port) + '+1)-1:PAYLOAD_BITS*' + str(idx_port) + ']),')
            filedata_str_list.append('        .input_port_read_cnt(input_port_read_cnt[PAYLOAD_BITS*(' + str(idx_port) + '+1)-1:PAYLOAD_BITS*' + str(idx_port) + ']),')
            filedata_str_list.append('        .input_port_stall_condition(input_port_stall_condition[' + str(idx_port) + '])')
            filedata_str_list.append('    );')

            high_addr = DATA_USER_IN_TOTAL - 1
            low_addr = DATA_USER_IN_TOTAL - DATA_USER_IN
            DATA_USER_IN_TOTAL = DATA_USER_IN_TOTAL - DATA_USER_IN
            filedata_str_list.append('    assign dout2user[' + str(high_addr) + ':' + str(low_addr) + '] = dout2user_tmp[' + str(low_addr_tmp + DATA_USER_IN - 1) + ':' + str(low_addr_tmp) + ']; // only low bits')
            filedata_str_list.append('')
            count += 1

      filedata_str_list.append('endmodule')

      filedata_str = "\n".join(filedata_str_list)
      with open(self.syn_dir+'/'+operator+'/src/Input_Port_Cluster_' + str(idx_leaf_interface) + '.v', 'w') as outfile:
        outfile.write(filedata_str)


  # leaf_interface_mapping_dict, e.g. {"0": ["Input_1","Output_1"],"1": ["Input_2"],"2": ["Input_3"],"3": []}
  # operator_output_width_dict, e.g. {'Output_1':32, 'Output_2': 64}
  def write_output_port_cluster(self, operator_output_width_dict, leaf_interface_mapping_dict, output_num, operator, fifo_depth_counter):
    # Output_Port_Cluster per leaf interface
    for idx_leaf_interface in range(len(leaf_interface_mapping_dict)):
      filedata_str_list = []
      filedata_str_list.append('`timescale 1ns / 1ps')
      filedata_str_list.append('module Output_Port_Cluster_' + str(idx_leaf_interface) + ' #(')
      filedata_str_list.append('    parameter PACKET_BITS = 97,')
      filedata_str_list.append('    parameter NUM_LEAF_BITS = 6,')
      filedata_str_list.append('    parameter NUM_PORT_BITS = 4,')
      filedata_str_list.append('    parameter NUM_ADDR_BITS = 7,')
      filedata_str_list.append('    parameter PAYLOAD_BITS = 64,')
      filedata_str_list.append('    parameter NUM_IN_PORTS = 1,')
      filedata_str_list.append('    parameter NUM_OUT_PORTS = 7,')
      filedata_str_list.append('    parameter NUM_BRAM_ADDR_BITS = 7,')
      filedata_str_list.append('    parameter FREESPACE_UPDATE_SIZE = 64,')
      filedata_str_list.append('    parameter DATA_USER_OUT_TOTAL = 32,')
      filedata_str_list.append('    localparam OUT_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS+NUM_ADDR_BITS+NUM_ADDR_BITS+3')
      filedata_str_list.append('    )(')
      filedata_str_list.append('    input clk,')
      filedata_str_list.append('    input clk_user,')
      filedata_str_list.append('    input reset,')
      filedata_str_list.append('    input reset_user,')
      filedata_str_list.append('')
      filedata_str_list.append('    // internal')
      filedata_str_list.append('    input [OUT_PORTS_REG_BITS*NUM_OUT_PORTS-1:0] out_control_reg,')
      filedata_str_list.append('    output [PACKET_BITS*NUM_OUT_PORTS-1:0] internal_out,')
      filedata_str_list.append('    output [NUM_OUT_PORTS-1:0] empty,')
      filedata_str_list.append('    input [NUM_OUT_PORTS-1:0] rd_en_sel,')
      filedata_str_list.append('')
      filedata_str_list.append('    // user interface')
      filedata_str_list.append('    output [NUM_OUT_PORTS-1:0] ack_b_out2user,')
      filedata_str_list.append('    input [DATA_USER_OUT_TOTAL-1:0] din_leaf_user2interface,')
      filedata_str_list.append('    input [NUM_OUT_PORTS-1:0] vld_user2b_out,')
      filedata_str_list.append('')
      filedata_str_list.append('    input is_done_mode, // clk(_bft) domain')
      filedata_str_list.append('    input is_done_mode_user, // clk_user domain')
      filedata_str_list.append('    output [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_full_cnt,')
      filedata_str_list.append('    output [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_empty_cnt,')
      filedata_str_list.append('')
      filedata_str_list.append('    input is_sending_full_cnt_reg,')
      filedata_str_list.append('    input [NUM_LEAF_BITS-1:0] self_leaf_reg,')
      filedata_str_list.append('    input [NUM_PORT_BITS-1:0] self_port_reg,')
      filedata_str_list.append('    input [1:0] cnt_type_reg,')
      filedata_str_list.append('')
      filedata_str_list.append('    input vld_cnt,')
      filedata_str_list.append('    input [PAYLOAD_BITS-1:0] cnt_val,')
      filedata_str_list.append('')
      filedata_str_list.append('    output output_port_cluster_stall_condition')
      filedata_str_list.append('    );')
      filedata_str_list.append('')
      filedata_str_list.append('    wire [NUM_OUT_PORTS-1:0] output_port_stall_condition;')
      filedata_str_list.append('    assign output_port_cluster_stall_condition = |output_port_stall_condition;')
      filedata_str_list.append('')
      filedata_str_list.append('')
      mapped_IO_ports = leaf_interface_mapping_dict[idx_leaf_interface] # io ports for this leaf interface
      mapped_O_ports = [io_port for io_port in mapped_IO_ports if io_port.startswith('Output_')] # output port for this leaf interface
      DATA_USER_OUT_TOTAL = 0
      for o_port in mapped_O_ports:
        DATA_USER_OUT_TOTAL += operator_output_width_dict[o_port] # output port width total for this leaf interface

      if len(mapped_O_ports) == 0: # dummy output_port, still needs to output counters
          filedata_str_list.append('    Output_Port#(')
          filedata_str_list.append('        .PACKET_BITS(PACKET_BITS),')
          filedata_str_list.append('        .NUM_LEAF_BITS(NUM_LEAF_BITS),')
          filedata_str_list.append('        .NUM_PORT_BITS(NUM_PORT_BITS),')
          filedata_str_list.append('        .NUM_ADDR_BITS(NUM_ADDR_BITS),')
          filedata_str_list.append('        .PAYLOAD_BITS(PAYLOAD_BITS),')
          filedata_str_list.append('        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),')
          filedata_str_list.append('        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),')
          filedata_str_list.append('        .DATA_USER_OUT(32), // OPERATOR SPECIFIC!')
          filedata_str_list.append('        .OUTPUT_0(' + str(fifo_depth_counter) + ') // only one output port')
          filedata_str_list.append('    )OPort_0(')
          filedata_str_list.append('        .clk(clk),')
          filedata_str_list.append('        .clk_user(clk_user),')
          filedata_str_list.append('        .reset(reset),')
          filedata_str_list.append('        .reset_user(reset_user),')
          filedata_str_list.append('        .update_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+2]),')
          filedata_str_list.append('        .update_fifo_addr_en(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+1]),')
          filedata_str_list.append('        .add_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS]),')
          filedata_str_list.append('        .dst_leaf(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS-1:OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS]),')
          filedata_str_list.append('        .dst_port(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS-1:OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS]),')
          filedata_str_list.append('        .fifo_addr(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS]),')
          filedata_str_list.append('        .freespace(out_control_reg[OUT_PORTS_REG_BITS*0+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*0]),')
          filedata_str_list.append('        .vld_user2b_out(vld_user2b_out[0]),')
          filedata_str_list.append('        .rd_en_sel(rd_en_sel[0]),')
          filedata_str_list.append('        .din_leaf_user2interface(din_leaf_user2interface[31:0]), // OPERATOR SPECIFIC!, if <32, zero-padded')
          filedata_str_list.append('        .internal_out(internal_out[PACKET_BITS*(0+1)-1:PACKET_BITS*0]),')
          filedata_str_list.append('        .empty(empty[0]),')
          filedata_str_list.append('        .ack_b_out2user(ack_b_out2user[0]),')
          filedata_str_list.append('')
          filedata_str_list.append('        .is_done_mode(is_done_mode),')
          filedata_str_list.append('        .is_done_mode_user(is_done_mode_user),')
          filedata_str_list.append('        .output_port_full_cnt(output_port_full_cnt[PAYLOAD_BITS*(0+1)-1:PAYLOAD_BITS*0]),')
          filedata_str_list.append('        .output_port_empty_cnt(output_port_empty_cnt[PAYLOAD_BITS*(0+1)-1:PAYLOAD_BITS*0]),')
          if idx_port == 0: 
            filedata_str_list.append('        .is_sending_full_cnt_reg(is_sending_full_cnt_reg), // only output_port_0')
            filedata_str_list.append('        .self_leaf_reg(self_leaf_reg), // only output_port_0')
            filedata_str_list.append('        .self_port_reg(self_port_reg), // only output_port_0')
            filedata_str_list.append('        .cnt_type_reg(cnt_type_reg), // only output_port_0')
            filedata_str_list.append('')
            filedata_str_list.append('        .vld_cnt(vld_cnt), // only output_port_0')
            filedata_str_list.append('        .cnt_val(cnt_val), // only output_port_0')
          else: 
            filedata_str_list.append('        .is_sending_full_cnt_reg(), // non-output_port_0')
            filedata_str_list.append('        .self_leaf_reg(), // non-output_port_0')
            filedata_str_list.append('        .self_port_reg(), // non-output_port_0')
            filedata_str_list.append('        .cnt_type_reg(), // non-output_port_0')
            filedata_str_list.append('')
            filedata_str_list.append('        .vld_cnt(), // non-output_port_0')
            filedata_str_list.append('        .cnt_val(), // non-output_port_0')
          filedata_str_list.append('')
          filedata_str_list.append('        .output_port_stall_condition(output_port_stall_condition[0])')
          filedata_str_list.append('    );')
          filedata_str_list.append('')
      else:
        count = 0
        for i in range(int(output_num),0,-1): # descending.. e.g. 3, 2, 1, 0
          if 'Output_' + str(i) in mapped_O_ports:
            idx_port = len(mapped_O_ports)-1-count
            DATA_USER_OUT = operator_output_width_dict['Output_' + str(i)]
            if DATA_USER_OUT < 32:
              DATA_USER_OUT_min32 = 32
            else:
              DATA_USER_OUT_min32 = DATA_USER_OUT

            filedata_str_list.append('    Output_Port#(')
            filedata_str_list.append('        .PACKET_BITS(PACKET_BITS),')
            filedata_str_list.append('        .NUM_LEAF_BITS(NUM_LEAF_BITS),')
            filedata_str_list.append('        .NUM_PORT_BITS(NUM_PORT_BITS),')
            filedata_str_list.append('        .NUM_ADDR_BITS(NUM_ADDR_BITS),')
            filedata_str_list.append('        .PAYLOAD_BITS(PAYLOAD_BITS),')
            filedata_str_list.append('        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),')
            filedata_str_list.append('        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),')
            filedata_str_list.append('        .DATA_USER_OUT(' + str(DATA_USER_OUT_min32) + '), // OPERATOR SPECIFIC!')

            if idx_port == 0: filedata_str_list.append('        .OUTPUT_0(' + str(fifo_depth_counter) + ') // only one output port')
            else: filedata_str_list.append('        .OUTPUT_0(0) // only one output port')

            filedata_str_list.append('    )OPort_' + str(idx_port)  + '(')
            filedata_str_list.append('        .clk(clk),')
            filedata_str_list.append('        .clk_user(clk_user),')
            filedata_str_list.append('        .reset(reset),')
            filedata_str_list.append('        .reset_user(reset_user),')
            filedata_str_list.append('        .update_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+2]),')
            filedata_str_list.append('        .update_fifo_addr_en(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+1]),')
            filedata_str_list.append('        .add_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS]),')
            filedata_str_list.append('        .dst_leaf(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS-1:OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS]),')
            filedata_str_list.append('        .dst_port(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS-1:OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS]),')
            filedata_str_list.append('        .fifo_addr(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS]),')
            filedata_str_list.append('        .freespace(out_control_reg[OUT_PORTS_REG_BITS*' + str(idx_port)+ '+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*' + str(idx_port)+ ']),')
            filedata_str_list.append('        .vld_user2b_out(vld_user2b_out[' + str(idx_port)+ ']),')
            filedata_str_list.append('        .rd_en_sel(rd_en_sel[' + str(idx_port)+ ']),')

            high_addr = DATA_USER_OUT_TOTAL - 1
            low_addr = DATA_USER_OUT_TOTAL - DATA_USER_OUT
            filedata_str_list.append('        .din_leaf_user2interface(din_leaf_user2interface[' + str(high_addr) + ':' + str(low_addr) + ']), // OPERATOR SPECIFIC!, if <32, zero-padded')
            DATA_USER_OUT_TOTAL = DATA_USER_OUT_TOTAL - DATA_USER_OUT

            filedata_str_list.append('        .internal_out(internal_out[PACKET_BITS*(' + str(idx_port)+ '+1)-1:PACKET_BITS*' + str(idx_port)+ ']),')
            filedata_str_list.append('        .empty(empty[' + str(idx_port)+ ']),')
            filedata_str_list.append('        .ack_b_out2user(ack_b_out2user[' + str(idx_port)+ ']),')
            filedata_str_list.append('')
            filedata_str_list.append('        .is_done_mode(is_done_mode),')
            filedata_str_list.append('        .is_done_mode_user(is_done_mode_user),')
            filedata_str_list.append('        .output_port_full_cnt(output_port_full_cnt[PAYLOAD_BITS*(' + str(idx_port)+ '+1)-1:PAYLOAD_BITS*' + str(idx_port)+ ']),')
            filedata_str_list.append('        .output_port_empty_cnt(output_port_empty_cnt[PAYLOAD_BITS*(' + str(idx_port)+ '+1)-1:PAYLOAD_BITS*' + str(idx_port)+ ']),')
            if idx_port == 0: 
              filedata_str_list.append('        .is_sending_full_cnt_reg(is_sending_full_cnt_reg), // only output_port_0')
              filedata_str_list.append('        .self_leaf_reg(self_leaf_reg), // only output_port_0')
              filedata_str_list.append('        .self_port_reg(self_port_reg), // only output_port_0')
              filedata_str_list.append('        .cnt_type_reg(cnt_type_reg), // only output_port_0')
              filedata_str_list.append('')
              filedata_str_list.append('        .vld_cnt(vld_cnt), // only output_port_0')
              filedata_str_list.append('        .cnt_val(cnt_val), // only output_port_0')
            else: 
              filedata_str_list.append('        .is_sending_full_cnt_reg(), // non-output_port_0')
              filedata_str_list.append('        .self_leaf_reg(), // non-output_port_0')
              filedata_str_list.append('        .self_port_reg(), // non-output_port_0')
              filedata_str_list.append('        .cnt_type_reg(), // non-output_port_0')
              filedata_str_list.append('')
              filedata_str_list.append('        .vld_cnt(), // non-output_port_0')
              filedata_str_list.append('        .cnt_val(), // non-output_port_0')
            filedata_str_list.append('')
            filedata_str_list.append('        .output_port_stall_condition(output_port_stall_condition[' + str(idx_port) + '])')
            filedata_str_list.append('    );')
            filedata_str_list.append('')
            count += 1

      filedata_str_list.append('endmodule')

      filedata_str = "\n".join(filedata_str_list)
      with open(self.syn_dir+'/'+operator+'/src/Output_Port_Cluster_' + str(idx_leaf_interface) + '.v', 'w') as outfile:
        outfile.write(filedata_str)


  def prepare_HW(self, operator, page_num, specs_dict):
    frequency = specs_dict[operator]['kernel_clk']
    num_leaf_interface = specs_dict[operator]['num_leaf_interface']

    # Update syn.xdc for multiple leaf interface case
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

    # If the map target is Hardware, we need to prepare the HDL files and scripts to compile it.
    self.shell.mkdir(self.syn_dir+'/'+operator+'/src')
    file_list = [ 'Config_Controls.v', 'rise_detect.v',         'converge_ctrl.v',
                  'ExtractCtrl.v',                                                                           #'Input_Port_Cluster.v',  
                  'Input_Port.v',      'leaf_interface.v',                                                   #'Output_Port_Cluster.v',
                  'Output_Port.v',     'read_b_in.v',           'ram0.v',                'single_ram.v',       'SynFIFO.v',
                  'xram_triple.v',     'Stream_Flow_Control.v', 'write_b_in.v',          'write_b_out.v',      'send_IO_queue_cnt.v']
                  # 'expand_queue.v',    'shrink_queue.v',        'send_IO_queue_cnt.v',   'expand_queue_fifo.v','shrink_queue_fifo.v',
                  # 'nth_fifo.v']

    # copy the necessary leaf interface verilog files for out-of-context compilation
    for name in file_list: self.shell.cp_file(self.overlay_dir+'/src/'+name, self.syn_dir+'/'+operator+'/src/'+name)

    # prepare the tcl files for out-of-context compilation
    self.shell.write_lines(self.syn_dir+'/'+operator+'/syn_page.tcl', self.tcl.return_syn_page_tcl_list(operator, 
                                                                                                          ['./leaf.v'], 
                                                                                                          rpt_name='utilization.rpt', 
                                                                                                          frequency=frequency))

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
    leaf_interface_mapping_dict = self.gen_leaf_interface_mapping(operator_input_width_dict, operator_output_width_dict, num_leaf_interface)
    # print(leaf_interface_mapping_dict) #{"0": ["Input_1", "Output_1"]}
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

    # Update Input_Port_Cluster.v and Output_Port_Cluster.v
    fifo_depth_counter = self.calculate_small_fifo_depth(leaf_interface_mapping_dict)
    self.write_output_port_cluster(operator_output_width_dict, leaf_interface_mapping_dict, output_num, operator, fifo_depth_counter)
    self.write_input_port_cluster(operator_input_width_dict, leaf_interface_mapping_dict, input_num, operator)

    # Update/write leaf_interface.v and Stream_Flow_Control.v
    for idx_leaf_interface in range(num_leaf_interface):
      with open(self.syn_dir + '/' + operator + '/src/leaf_interface.v', 'r') as infile:
        filedata = infile.read()
      filedata = filedata.replace('_IDX_LEAF_INTERFACE', '_' + str(idx_leaf_interface))
      with open(self.syn_dir + '/' + operator + '/src/leaf_interface_' + str(idx_leaf_interface) + '.v', 'w') as outfile:
        outfile.write(filedata)

      with open(self.syn_dir + '/' + operator + '/src/Stream_Flow_Control.v', 'r') as infile:
        filedata = infile.read()
      filedata = filedata.replace('_IDX_LEAF_INTERFACE', '_' + str(idx_leaf_interface))
      with open(self.syn_dir + '/' + operator + '/src/Stream_Flow_Control_' + str(idx_leaf_interface) + '.v', 'w') as outfile:
        outfile.write(filedata)

    # rm old leaf_interface.v and Stream_Flow_Control.v
    os.system('rm ' + self.syn_dir + '/' + operator + '/src/leaf_interface.v')
    os.system('rm ' + self.syn_dir + '/' + operator + '/src/Stream_Flow_Control.v')

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

     
