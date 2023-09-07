# -*- coding: utf-8 -*-   
# Company: IC group, University of Pennsylvania
# Engineer: Yuanlong Xiao
#
# Create Date: 12/18/2021
# Design Name: monolithic
# Project Name: PLD
# Versions: 1.0
# Description: This is a python script to prepare the script for static region 
#              compile for PRflow.
# Dependencies: python3, gen_basic
# Revision:
# Revision 0.01 - File Created
#
# Additional Comments:


import os, json
import subprocess
from pr_flow.gen_basic import gen_basic
import re

class monolithic(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)

  # from the source header file, find the input or output number
  def return_io_num(self, io_pattern, file_list):
    max_num = 0
    for line in file_list:
      num_list = re.findall(r""+io_pattern+"\d*", line)
      if(len(num_list)>0 and int(num_list[0].replace(io_pattern,''))): max_num = int(num_list[0].replace(io_pattern,''))
    return max_num
 
  # find all the operators page num  
  def return_page_num_dict_local(self, operators):
    operator_list = operators.split()
    page_num_dict = {'DMA':1, 'DMA2': 7, 'ARM':0, 'DEBUG':2}
    for operator in operator_list:
      HW_exist, target = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h', 'map_target')
      page_exist, page_num = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h', 'page_num')
      #if HW_exist and target=='HW' and page_exist:
      if page_exist:
        page_num_dict[operator] = page_num
    return page_num_dict 

  # find all the operators arguments order
  # in case the user define the input and output arguments out of order 
  def return_operator_io_argument_dict_local(self, operators):
    operator_list = operators.split()
    operator_arg_dict = {}
    operator_width_dict = {}
    for operator in operator_list:
      file_list = self.shell.file_to_list('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h')
      arguments_list = [] 
      width_list = [] 
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
        input_str_list  = re.findall(r"Input_\d+", arg_str)
        output_str_list = re.findall(r"Output_\d+", arg_str)
        str_width_list = re.findall(r"ap_uint\<\d+\>", arg_str)
        input_str_list.extend(output_str_list)
        io_str = input_str_list
        width_list.append(str_width_list[0]) 
        arguments_list.append(io_str[0])
      operator_arg_dict[operator] = arguments_list
      operator_width_dict[operator] = width_list
    return operator_arg_dict, operator_width_dict 


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
        if operator+'(' in line: inst_cnt = inst_cnt + 1
        if inst_cnt == 1: 
          line_str=re.sub('\s+', '', line)
          line_str=re.sub('\t+', '', line_str)
          line_str=re.sub('//.*', '', line_str)
          inst_str=inst_str+line_str
        if ')' in line and inst_cnt == 1: inst_cnt = 2
      inst_str = inst_str.replace(operator+'(','')
      inst_str = inst_str.replace(');','')
      var_str_list = inst_str.split(',')
      operator_var_dict[operator] = var_str_list
    
    return operator_var_dict 
 

  def return_operator_connect_list_local(self, operator_arg_dict, operator_var_dict, operator_width_dict):
    connection_list = []
    for key_a in operator_var_dict:
      operator = key_a

      for i_a, var_value_a in enumerate(operator_var_dict[key_a]):
        if var_value_a == 'Input_1': 
          tmp_str='DMA.Output_1->'+key_a+'.Input_1' 
          tmp_tup = (tmp_str, 512)
          connection_list.append(tmp_tup)
        if var_value_a == 'Input_2': 
          tmp_str='DMA2.Output_1->'+key_a+'.Input_1' 
          tmp_tup = (tmp_str, 512)
          connection_list.append(tmp_tup)
        if var_value_a == 'Output_1': 
          tmp_str=key_a+'.Output_1->'+'DMA.Input_1'
          tmp_tup = (tmp_str, 512)
          connection_list.append(tmp_tup)

        for key_b in operator_var_dict:
          for i_b, var_value_b in enumerate(operator_var_dict[key_b]):
            if var_value_a==var_value_b and key_a!=key_b:
              if 'Input' in operator_arg_dict[key_a][i_a]:
                key_b_width = int(operator_width_dict[key_b][i_b].replace('ap_uint<','').replace('>',''))
                tmp_str = key_b+'.'+operator_arg_dict[key_b][i_b]+'->'+key_a+'.'+operator_arg_dict[key_a][i_a]
              else:
                key_b_width = int(operator_width_dict[key_b][i_b].replace('ap_uint<','').replace('>',''))
                tmp_str = key_a+'.'+operator_arg_dict[key_a][i_a]+'->'+key_b+'.'+operator_arg_dict[key_b][i_b]
              tmp_tup = (tmp_str, key_b_width) # key_b_width == key_a_width
              connection_list.append(tmp_tup)

    connection_list = sorted(list(set(connection_list))) # sorted to be deterministic, debugging purpose
    return connection_list


  def return_operator_inst_v_list(self, operator_arg_dict, connection_list, operator_var_dict, operator_width_dict, output_size, specs_dict):
    out_list = ['module mono #(',
                '    parameter OUTPUT_SIZE = ' + str(output_size),
                '  )(',
                '  input          clk_200,',
                '  input          clk_250,',
                '  input          clk_300,',
                '  input          clk_350,',
                '  input          clk_400,',
                '  input          ap_rst_n,',
                '',
                '  input [63:0]   Input_1_TDATA,',
                '  input          Input_1_TVALID,',
                '  output         Input_1_TREADY,',
                '  output [63:0]  Output_1_TDATA,',
                '  output         Output_1_TVALID,',
                '  input          Output_1_TREADY,',
                '',
                '  input [511:0]  Input_2_TDATA,',
                '  input          Input_2_TVALID,',
                '  output         Input_2_TREADY,',
                '  output [511:0] Output_2_TDATA,',
                '  output         Output_2_TVALID,',
                '  input          Output_2_TREADY,',
                '',
                '  input         ap_start);']
    out_list.append('')
    out_list.append('  localparam WAIT_CNT = 20;')
    out_list.append('')
    out_list.append('  wire [511:0] DMA_Input_1_TDATA;')
    out_list.append('  wire         DMA_Input_1_TVALID;')
    out_list.append('  wire         DMA_Input_1_TREADY;')
    out_list.append('  wire [511:0] DMA_Output_1_TDATA;')
    out_list.append('  wire         DMA_Output_1_TVALID;')
    out_list.append('  wire         DMA_Output_1_TREADY;')
    out_list.append('')

    for op in operator_arg_dict:
      for idx, port in enumerate(operator_arg_dict[op]):
        width = int(operator_width_dict[op][idx].split('<')[1].split('>')[0])
        out_list.append('  wire ['+str(width-1)+':0] '+op+'_'+port+'_TDATA;')
        out_list.append('  wire        '+op+'_'+port+'_TVALID;')
        out_list.append('  wire        '+op+'_'+port+'_TREADY;')
    out_list.append('')

    out_list.append('  wire [31:0] full_cnt_wr_dummy, empty_cnt_rd_dummy, read_cnt_rd_dummy;')
    for idx, connect_tup in enumerate(connection_list):
      out_list.append('  wire [31:0] full_cnt_wr_' + str(idx) + ', empty_cnt_rd_' + str(idx) + ', read_cnt_rd_' + str(idx) + ';')
    out_list.append('')

    out_list.append('  wire full_dummy, empty_dummy;')
    for idx, connect_tup in enumerate(connection_list):
      out_list.append('  wire full_' + str(idx) + ', empty_' + str(idx) + ';')
    out_list.append('')

    for op in operator_arg_dict.keys():
      out_list.append('  wire [31:0] stall_cnt_' + op + ';')
    out_list.append('')

    out_list.append('  ///////////////')
    out_list.append('  // reset CDC //')
    out_list.append('  ///////////////')
    out_list.append('')
    out_list.append('  wire reset_200, reset_250, reset_300, reset_350, reset_400;')
    out_list.append('  assign reset_300 = ~ap_rst_n;')
    out_list.append('')
    out_list.append('  xpm_cdc_async_rst #(')
    out_list.append('     .DEST_SYNC_FF(4),    // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),    // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .RST_ACTIVE_HIGH(1)  // DECIMAL; 0=active low reset, 1=active high reset')
    out_list.append('  )')
    out_list.append('  xpm_cdc_async_reset_200_inst (')
    out_list.append('     .dest_arst(reset_200), // 1-bit output: src_arst asynchronous reset signal synchronized to destination')
    out_list.append('                            // clock domain. This output is registered. NOTE: Signal asserts asynchronously')
    out_list.append('                            // but deasserts synchronously to dest_clk. Width of the reset signal is at least')
    out_list.append('                            // (DEST_SYNC_FF*dest_clk) period.')
    out_list.append('     .dest_clk(clk_200),   // 1-bit input: Destination clock.')
    out_list.append('     .src_arst(reset_300)    // 1-bit input: Source asynchronous reset signal.')
    out_list.append('  );')
    out_list.append('')
    out_list.append('  xpm_cdc_async_rst #(')
    out_list.append('     .DEST_SYNC_FF(4),    // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),    // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .RST_ACTIVE_HIGH(1)  // DECIMAL; 0=active low reset, 1=active high reset')
    out_list.append('  )')
    out_list.append('  xpm_cdc_async_reset_250_inst (')
    out_list.append('     .dest_arst(reset_250), // 1-bit output: src_arst asynchronous reset signal synchronized to destination')
    out_list.append('                            // clock domain. This output is registered. NOTE: Signal asserts asynchronously')
    out_list.append('                            // but deasserts synchronously to dest_clk. Width of the reset signal is at least')
    out_list.append('                            // (DEST_SYNC_FF*dest_clk) period.')
    out_list.append('     .dest_clk(clk_250),   // 1-bit input: Destination clock.')
    out_list.append('     .src_arst(reset_300)    // 1-bit input: Source asynchronous reset signal.')
    out_list.append('  );')
    out_list.append('')
    out_list.append('  xpm_cdc_async_rst #(')
    out_list.append('     .DEST_SYNC_FF(4),    // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),    // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .RST_ACTIVE_HIGH(1)  // DECIMAL; 0=active low reset, 1=active high reset')
    out_list.append('  )')
    out_list.append('  xpm_cdc_async_reset_350_inst (')
    out_list.append('     .dest_arst(reset_350), // 1-bit output: src_arst asynchronous reset signal synchronized to destination')
    out_list.append('                            // clock domain. This output is registered. NOTE: Signal asserts asynchronously')
    out_list.append('                            // but deasserts synchronously to dest_clk. Width of the reset signal is at least')
    out_list.append('                            // (DEST_SYNC_FF*dest_clk) period.')
    out_list.append('     .dest_clk(clk_350),   // 1-bit input: Destination clock.')
    out_list.append('     .src_arst(reset_300)    // 1-bit input: Source asynchronous reset signal.')
    out_list.append('  );')
    out_list.append('')
    out_list.append('  xpm_cdc_async_rst #(')
    out_list.append('     .DEST_SYNC_FF(4),    // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),    // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .RST_ACTIVE_HIGH(1)  // DECIMAL; 0=active low reset, 1=active high reset')
    out_list.append('  )')
    out_list.append('  xpm_cdc_async_reset_400_inst (')
    out_list.append('     .dest_arst(reset_400), // 1-bit output: src_arst asynchronous reset signal synchronized to destination')
    out_list.append('                            // clock domain. This output is registered. NOTE: Signal asserts asynchronously')
    out_list.append('                            // but deasserts synchronously to dest_clk. Width of the reset signal is at least')
    out_list.append('                            // (DEST_SYNC_FF*dest_clk) period.')
    out_list.append('     .dest_clk(clk_400),   // 1-bit input: Destination clock.')
    out_list.append('     .src_arst(reset_300)    // 1-bit input: Source asynchronous reset signal.')
    out_list.append('  );')
    out_list.append('')
    out_list.append('  ///////////////////////////')
    out_list.append('  // ap_start to reset 300 //')
    out_list.append('  ///////////////////////////')
    out_list.append('')
    out_list.append('  wire ap_start_asserted_300;')
    out_list.append('  wire reset_ap_start_300; ')
    out_list.append('  reg ap_start_1, ap_start_2; // in order to stretch ap_start for two more cycles')
    out_list.append('')
    out_list.append('  rise_detect #(')
    out_list.append('      .data_width(1)')
    out_list.append('  )rise_detect_ap_start_u(')
    out_list.append('      .data_out(ap_start_asserted_300),')
    out_list.append('      .data_in(ap_start),')
    out_list.append('      .clk(clk_300),')
    out_list.append('      .reset(reset_300)')
    out_list.append('  );')
    out_list.append('  assign reset_ap_start_300 = reset_300 || ap_start_asserted_300;')
    out_list.append('')
    out_list.append('  // CDC for ap_start, can also be done with xpm_cdc_pulse')
    out_list.append('  always @ (posedge clk_300) begin')
    out_list.append('      ap_start_1 <= ap_start;')
    out_list.append('      ap_start_2 <= ap_start_1;')
    out_list.append('  end')
    out_list.append('')
    out_list.append('  // I want to reset counters with ap_start')
    out_list.append('  //////////////////////////////////////////')
    out_list.append('  // ap_start to reset 200, 250, 350, 400 //')
    out_list.append('  //////////////////////////////////////////')
    out_list.append('  wire ap_start_200, ap_start_250, ap_start_350, ap_start_400;')
    out_list.append('  wire ap_start_asserted_200, ap_start_asserted_250, ap_start_asserted_350, ap_start_asserted_400;')
    out_list.append('  wire reset_ap_start_200, reset_ap_start_250, reset_ap_start_350, reset_ap_start_400;')
    out_list.append('')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_ap_start_200_inst (')
    out_list.append('     .dest_out(ap_start_200), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                                 // registered.')
    out_list.append('     .dest_clk(clk_200),        // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),              // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(ap_start | ap_start_1 | ap_start_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  rise_detect #(')
    out_list.append('      .data_width(1)')
    out_list.append('  )rise_detect_ap_start_200_u(')
    out_list.append('      .data_out(ap_start_asserted_200),')
    out_list.append('      .data_in(ap_start_200),')
    out_list.append('      .clk(clk_200),')
    out_list.append('      .reset(reset_200)')
    out_list.append('  );')
    out_list.append('  assign reset_ap_start_200 = reset_200 || ap_start_asserted_200;')
    out_list.append('')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_ap_start_250_inst (')
    out_list.append('     .dest_out(ap_start_250), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                                 // registered.')
    out_list.append('     .dest_clk(clk_250),        // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),              // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(ap_start | ap_start_1 | ap_start_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  rise_detect #(')
    out_list.append('      .data_width(1)')
    out_list.append('  )rise_detect_ap_start_250_u(')
    out_list.append('      .data_out(ap_start_asserted_250),')
    out_list.append('      .data_in(ap_start_250),')
    out_list.append('      .clk(clk_250),')
    out_list.append('      .reset(reset_250)')
    out_list.append('  );')
    out_list.append('  assign reset_ap_start_250 = reset_250 || ap_start_asserted_250;')
    out_list.append('')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_ap_start_350_inst (')
    out_list.append('     .dest_out(ap_start_350), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                                 // registered.')
    out_list.append('     .dest_clk(clk_350),        // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),              // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(ap_start | ap_start_1 | ap_start_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  rise_detect #(')
    out_list.append('      .data_width(1)')
    out_list.append('  )rise_detect_ap_start_350_u(')
    out_list.append('      .data_out(ap_start_asserted_350),')
    out_list.append('      .data_in(ap_start_350),')
    out_list.append('      .clk(clk_350),')
    out_list.append('      .reset(reset_350)')
    out_list.append('  );')
    out_list.append('  assign reset_ap_start_350 = reset_350 || ap_start_asserted_350;')
    out_list.append('')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_ap_start_400_inst (')
    out_list.append('     .dest_out(ap_start_400), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                                 // registered.')
    out_list.append('     .dest_clk(clk_400),        // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),              // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(ap_start | ap_start_1 | ap_start_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  rise_detect #(')
    out_list.append('      .data_width(1)')
    out_list.append('  )rise_detect_ap_start_400_u(')
    out_list.append('      .data_out(ap_start_asserted_400),')
    out_list.append('      .data_in(ap_start_400),')
    out_list.append('      .clk(clk_400),')
    out_list.append('      .reset(reset_400)')
    out_list.append('  );')
    out_list.append('  assign reset_ap_start_400 = reset_400 || ap_start_asserted_400;')
    out_list.append('')
    out_list.append('')
    out_list.append('  wire [63:0] cnt_data_in;')
    out_list.append('  wire cnt_data_valid;')
    out_list.append('  wire cnt_data_ready;')
    out_list.append('')
    out_list.append('  // counter logic for output_size here')
    out_list.append('  // feed is_done to all the stream_shells')
    out_list.append('  // async_fifo for counter, separate clk (200,250,350,400)')
    out_list.append('  reg [63:0] Output_1_TDATA_reg;')
    out_list.append('  reg        Output_1_TVALID_reg;')
    out_list.append('  // assign Output_1_TDATA = Output_1_TDATA_reg;')
    out_list.append('  // assign Output_1_TVALID = Output_1_TVALID_reg;')
    out_list.append('  assign Input_1_TREADY = 1; // not used')
    out_list.append('')
    out_list.append('  reg state_300; // 0: processing, 1: is_done state_300')
    out_list.append('  reg [31:0] output_cnt, is_done_wait_cnt;')
    out_list.append('')
    out_list.append('  wire state_200, state_250, state_350, state_400;')
    out_list.append('')
    out_list.append('  assign cnt_data_in = (!state_300) ? Input_1_TDATA : Output_1_TDATA_reg;')
    out_list.append('  assign cnt_data_valid = (!state_300) ? Input_1_TVALID : Output_1_TVALID_reg;')
    out_list.append('')
    out_list.append('  // Stream shell to send cnt to host')
    out_list.append('  stream_shell #(')
    out_list.append('   .PAYLOAD_BITS(64),')
    out_list.append('   .NUM_BRAM_ADDR_BITS(9)')
    out_list.append('   )stream_shell_cnt(')
    out_list.append('   .wr_clk(clk_300),')
    out_list.append('   .wr_rst(reset_300),')
    out_list.append('   .din(cnt_data_in),')
    out_list.append('   .val_in(cnt_data_valid),')
    out_list.append('   .ready_upward(cnt_data_ready),')
    out_list.append('')
    out_list.append('   .rd_clk(clk_300),')
    out_list.append('   .rd_rst(reset_300),')
    out_list.append('   .dout(Output_1_TDATA),')
    out_list.append('   .val_out(Output_1_TVALID),')
    out_list.append('   .ready_downward(Output_1_TREADY),')
    out_list.append('')
    out_list.append('   .reset_ap_start_wr(reset_ap_start_300),')
    out_list.append('   .reset_ap_start_rd(reset_ap_start_300),')
    out_list.append('   .state_wr(state_300),')
    out_list.append('   .state_rd(state_300),')
    out_list.append('   .full_cnt_wr(full_cnt_wr_dummy),')
    out_list.append('   .empty_cnt_rd(empty_cnt_rd_dummy),')
    out_list.append('   .read_cnt_rd(read_cnt_rd_dummy),')
    out_list.append('   .full(full_dummy),')
    out_list.append('   .empty(empty_dummy));')

    out_list.append('')
    out_list.append('')
    out_list.append('  always@(posedge clk_300)begin')
    out_list.append('    if(reset_ap_start_300) begin')
    out_list.append('      output_cnt <= 0;')
    out_list.append('      state_300 <= 0;')
    out_list.append('      is_done_wait_cnt <= 0;')
    out_list.append('      Output_1_TDATA_reg <= 0;')
    out_list.append('      Output_1_TVALID_reg <= 0;')
    out_list.append('    end')
    out_list.append('    else begin')
    out_list.append('      if (Output_2_TVALID && Output_2_TREADY && state_300 == 0) begin')
    out_list.append('        output_cnt <= output_cnt + 1;')
    out_list.append('      end')
    out_list.append('      if (output_cnt == OUTPUT_SIZE && state_300 == 0) begin')
    out_list.append('        state_300 <= 1; // is_done state_300')
    out_list.append('      end')
    out_list.append('')
    out_list.append('      // WAIT_CNT is long enough num of cycles to make counters from different clk frequencies to be static')
    out_list.append('      if (state_300 && is_done_wait_cnt < WAIT_CNT) begin ')
    out_list.append('        is_done_wait_cnt <= is_done_wait_cnt + 1;')
    out_list.append('      end')
    out_list.append('      else begin')


    mono_counter_idx_dict = {} # Will be used to interpret counter  values (counter_analyze.py)
    # mono_counter_idx_dict, e.g. {'zculling_i4_Output_1->coloringFB_i1_Input_1': 7, ...
    #                              'zculling_i4': 31, ...}

    cycle_cnt = 0
    for idx, connect_tup in enumerate(connection_list):
      out_list.append('        // stream shell ' + str(idx))
      if idx == 0:
        out_list.append('        if (is_done_wait_cnt == WAIT_CNT) begin')
      else:
        out_list.append('        else if (is_done_wait_cnt == WAIT_CNT + ' + str(cycle_cnt) + ') begin')        
      out_list.append('          if (cnt_data_ready) begin')
      out_list.append('            Output_1_TDATA_reg <= {32\'b0,full_cnt_wr_' + str(idx) + '};')
      out_list.append('            Output_1_TVALID_reg <= 1;')
      out_list.append('            is_done_wait_cnt <= is_done_wait_cnt + 1;')
      out_list.append('          end')
      out_list.append('          else begin')
      out_list.append('            Output_1_TDATA_reg <= 0; // garbage')
      out_list.append('            Output_1_TVALID_reg <= 0;')
      out_list.append('          end')
      out_list.append('        end')
      cycle_cnt = cycle_cnt + 1
      out_list.append('        else if (is_done_wait_cnt == WAIT_CNT + ' + str(cycle_cnt) + ') begin')
      out_list.append('          if (cnt_data_ready) begin')
      out_list.append('            Output_1_TDATA_reg <= {32\'b0,empty_cnt_rd_' + str(idx) + '};')
      out_list.append('            Output_1_TVALID_reg <= 1;')
      out_list.append('            is_done_wait_cnt <= is_done_wait_cnt + 1;')
      out_list.append('          end')
      out_list.append('          else begin')
      out_list.append('            Output_1_TDATA_reg <= 0;')
      out_list.append('            Output_1_TVALID_reg <= 0;')
      out_list.append('          end')
      out_list.append('        end')
      cycle_cnt = cycle_cnt + 1
      out_list.append('        else if (is_done_wait_cnt == WAIT_CNT + ' + str(cycle_cnt) + ') begin')
      out_list.append('          if (cnt_data_ready) begin')
      out_list.append('            Output_1_TDATA_reg <= {32\'b0,read_cnt_rd_' + str(idx) + '};')
      out_list.append('            Output_1_TVALID_reg <= 1;')
      out_list.append('            is_done_wait_cnt <= is_done_wait_cnt + 1;')
      out_list.append('          end')
      out_list.append('          else begin')
      out_list.append('            Output_1_TDATA_reg <= 0;')
      out_list.append('            Output_1_TVALID_reg <= 0;')
      out_list.append('          end')
      out_list.append('        end')
      out_list.append('')
      cycle_cnt = cycle_cnt + 1

      link_str = connect_tup[0]
      mono_counter_idx_dict[link_str] = idx

    out_list.append('        // stall counters')
    for op in operator_arg_dict.keys():
      out_list.append('        else if (is_done_wait_cnt == WAIT_CNT + ' + str(cycle_cnt) + ') begin')
      out_list.append('          if (cnt_data_ready) begin')
      out_list.append('            Output_1_TDATA_reg <= {32\'b0,stall_cnt_' + op + '};')
      out_list.append('            Output_1_TVALID_reg <= 1;')
      out_list.append('            is_done_wait_cnt <= is_done_wait_cnt + 1;')
      out_list.append('          end')
      out_list.append('          else begin')
      out_list.append('            Output_1_TDATA_reg <= 0;')
      out_list.append('            Output_1_TVALID_reg <= 0;')
      out_list.append('          end')
      out_list.append('        end')
      out_list.append('')
      cycle_cnt = cycle_cnt + 1

      mono_counter_idx_dict[op] = cycle_cnt

    print("mono_counter_idx_dict:")
    print(mono_counter_idx_dict)

    out_list.append('        else begin')
    out_list.append('          Output_1_TDATA_reg <= 0;')
    out_list.append('          Output_1_TVALID_reg <= 0;')
    out_list.append('        end')
    out_list.append('      end')
    out_list.append('    end')
    out_list.append('  end')

    out_list.append('')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_is_done_200_inst (')
    out_list.append('     .dest_out(state_200), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                              // registered.')
    out_list.append('     .dest_clk(clk_200),     // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),           // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(state_300)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_is_done_250_inst (')
    out_list.append('     .dest_out(state_250), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                              // registered.')
    out_list.append('     .dest_clk(clk_250),     // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),           // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(state_300)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_is_done_350_inst (')
    out_list.append('     .dest_out(state_350), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                              // registered.')
    out_list.append('     .dest_clk(clk_350),     // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),           // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(state_300)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('  xpm_cdc_single #(')
    out_list.append('     .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10')
    out_list.append('     .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values')
    out_list.append('     .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages')
    out_list.append('     .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input')
    out_list.append('  )')
    out_list.append('  xpm_cdc_single_is_done_400_inst (')
    out_list.append('     .dest_out(state_400), // 1-bit output: src_in synchronized to the destination clock domain. This output is')
    out_list.append('                              // registered.')
    out_list.append('     .dest_clk(clk_400),     // 1-bit input: Clock signal for the destination clock domain.')
    out_list.append('     .src_clk(clk_300),           // 1-bit input: optional; required when SRC_INPUT_REG = 1')
    out_list.append('     .src_in(state_300)      // 1-bit input: Input signal to be synchronized to dest_clk domain.')
    out_list.append('  );')
    out_list.append('')
    out_list.append('')

    stream_shell_idx_dict = {}
    # stream_shell_idx_dict, e.g. {'coloringFB_bot_m_Output_1': 7, ...}

    for idx, connect_tup in enumerate(connection_list):
      link_str = connect_tup[0]
      # print(link_str)
      # print(connect_tup)
      op_sender = link_str.split('->')[0].split('.')[0]
      op_receiver = link_str.split('->')[1].split('.')[0]
      if op_sender == 'DMA':
        wr_freq = '300'
      else:
        wr_freq = specs_dict[op_sender]['kernel_clk']
      if op_receiver == 'DMA':
        rd_freq = '300'
      else:
        rd_freq = specs_dict[op_receiver]['kernel_clk']

      stream_shell_idx_dict[link_str.split('->')[0].replace('.','_')] = idx
      stream_shell_idx_dict[link_str.split('->')[1].replace('.','_')] = idx

      width = connect_tup[1]
      out_list.append('  stream_shell #(')
      out_list.append('    .PAYLOAD_BITS(' + str(width) + '),')
      out_list.append('    .NUM_BRAM_ADDR_BITS(7)')
      out_list.append('    )stream_shell_' + str(idx) + '(')
      out_list.append('    .wr_clk(clk_' + str(wr_freq) + '),')
      out_list.append('    .wr_rst(reset_' + str(wr_freq) + '),')
      out_list.append('    .din(' + link_str.split('->')[0].replace('.','_') + '_TDATA),')
      out_list.append('    .val_in(' + link_str.split('->')[0].replace('.','_') + '_TVALID),')
      out_list.append('    .ready_upward(' + link_str.split('->')[0].replace('.','_') + '_TREADY),')
      out_list.append('')
      out_list.append('    .rd_clk(clk_' + str(rd_freq) + '),')
      out_list.append('    .rd_rst(reset_' + str(rd_freq) + '),')
      out_list.append('    .dout(' + link_str.split('->')[1].replace('.','_') + '_TDATA),')
      out_list.append('    .val_out(' + link_str.split('->')[1].replace('.','_') + '_TVALID),')
      out_list.append('    .ready_downward(' + link_str.split('->')[1].replace('.','_') + '_TREADY),')
      out_list.append('')
      out_list.append('    .reset_ap_start_wr(reset_ap_start_' + str(wr_freq) + '),')
      out_list.append('    .reset_ap_start_rd(reset_ap_start_' + str(rd_freq) + '),')
      out_list.append('    .state_wr(state_' + str(wr_freq) + '),')
      out_list.append('    .state_rd(state_' + str(rd_freq) + '),')
      out_list.append('    .full_cnt_wr(full_cnt_wr_' + str(idx) + '),')
      out_list.append('    .empty_cnt_rd(empty_cnt_rd_' + str(idx) + '),')
      out_list.append('    .read_cnt_rd(read_cnt_rd_' + str(idx) + '),')
      out_list.append('    .full(full_' + str(idx) + '),')
      out_list.append('    .empty(empty_' + str(idx) + '));')
      out_list.append('')

    print("stream_shell_idx_dict:")
    print(stream_shell_idx_dict)

    for op in operator_arg_dict:
      op_freq = specs_dict[op]['kernel_clk']

      # stall condition
      str_input_stall_condition = ''
      str_output_stall_condition = ''
      for port in operator_arg_dict[op]:
        io_str = op + '_' + port # e.g. zculling_bot_Input_1
        if port.startswith('Input_'):
          out_list.append('  wire ' + io_str + '_stall_condition = (!state_' + str(op_freq) + ') && ' + \
                                      io_str + '_TREADY && empty_' + str(stream_shell_idx_dict[io_str]) + ';')
          str_input_stall_condition += io_str + '_stall_condition || '
        else:
          assert(port.startswith('Output_'))
          out_list.append('  wire ' + io_str + '_stall_condition = (!state_' + str(op_freq) + ') && ' + \
                                      io_str + '_TVALID && full_' + str(stream_shell_idx_dict[io_str]) + ';')
          str_output_stall_condition += io_str + '_stall_condition || '
      out_list.append('')

      # stall cnt
      str_input_stall_condition = str_input_stall_condition.strip()[:-2].strip() # remove '||' in the end
      str_output_stall_condition = str_output_stall_condition.strip()[:-2].strip() # remove '||' in the end
      out_list.append('  stall_cnt stall_cnt_' + op + '_inst(')
      out_list.append('    .clk(clk_' + str(op_freq) + '),')
      out_list.append('    .reset(reset_ap_start_' + str(op_freq) + '),')
      out_list.append('    .state(state_' + str(op_freq) + '),')
      out_list.append('    .input_stall_condition(' +  str_input_stall_condition + '),')
      out_list.append('    .output_stall_condition(' + str_output_stall_condition + '),')
      out_list.append('    .stall_cnt(stall_cnt_' + op + ')')
      out_list.append('  );')
      out_list.append('')


      # operator instantiation
      out_list.append('  '+op+' '+op+'_inst(')
      out_list.append('    .ap_clk(clk_' + str(op_freq) + '),')
      out_list.append('    .ap_start(1\'b1),')
      out_list.append('    .ap_done(),')
      out_list.append('    .ap_idle(),')
      out_list.append('    .ap_ready(),')
      for port in operator_arg_dict[op]:
        out_list.append('    .'+port+'_TDATA(' +op+'_'+port+'_TDATA),')
        out_list.append('    .'+port+'_TVALID('+op+'_'+port+'_TVALID),')
        out_list.append('    .'+port+'_TREADY('+op+'_'+port+'_TREADY),')
      out_list.append('    .ap_rst_n(~reset_' + str(op_freq) + ')')
      out_list.append('  );')
      out_list.append('')

    out_list.append('')
    out_list.append('  assign Output_2_TDATA  = DMA_Input_1_TDATA;')
    out_list.append('  assign Output_2_TVALID = DMA_Input_1_TVALID;')
    out_list.append('  assign DMA_Input_1_TREADY = Output_2_TREADY;')
    out_list.append('')
    out_list.append('  assign DMA_Output_1_TDATA  = Input_2_TDATA;')
    out_list.append('  assign DMA_Output_1_TVALID = Input_2_TVALID;')
    out_list.append('  assign Input_2_TREADY = DMA_Output_1_TREADY;')
    out_list.append('')

    out_list.append('endmodule')
 
    return out_list, mono_counter_idx_dict


  def update_cad_path(self, base_dir, operators, overlay_freq, is_mono):
    if not is_mono:
      sub_dir = overlay_freq + 'MHz'
    else:
      sub_dir = 'mono'

    self.shell.replace_lines(base_dir + '/' + self.prflow_params['board'] + '/build.sh',
                            {'export PLATFORM_REPO_PATHS=': 'export PLATFORM_REPO_PATHS='+self.prflow_params['BASE_PLATFORM_REPO_PATHS']})
    self.shell.replace_lines(base_dir + '/' + self.prflow_params['board'] + '/build.sh',
                            {'export ROOTFS'      : 'export ROOTFS='+self.prflow_params['ROOTFS']})
    self.shell.replace_lines(base_dir + '/' + self.prflow_params['board'] + '/build.sh',
                            {'export PLATFORM='   : 'export PLATFORM='+self.prflow_params['BASE_PLATFORM']})
    self.shell.replace_lines(base_dir + '/' + self.prflow_params['board'] + '/build.sh',
                            {'Xilinx_dir'         : 'source '+self.prflow_params['Xilinx_dir']})
    self.shell.replace_lines(base_dir + '/' + self.prflow_params['board'] + '/build.sh',
                            {'sdk_dir'            : 'source '+self.prflow_params['sdk_dir']})
    os.system('chmod +x ' + base_dir + '/' + self.prflow_params['board'] + '/build.sh')


  # main.sh will be used for local compilation
  def return_main_sh_list_local(self, input_list):
    lines_list = []
    lines_list.append('#!/bin/bash -e')
    lines_list.extend(input_list)
    return lines_list


  def run(self, operators):
    overlay_freq = self.prflow_params['overlay_freq']

    # mk work directory
    if self.prflow_params['gen_monolithic']==True:
      self.shell.re_mkdir(self.mono_dir)


    # prepare the source for vitis monolithic run
    self.shell.cp_dir("./common/mono_app/" + self.prflow_params['board'], self.mono_dir) 
    os.system('cp ./common/script_src/write_result.py ' + self.mono_dir)

    self.shell.write_lines(self.mono_dir + '/run.sh',  
                           self.return_main_sh_list_local([
                                  'cd ' + self.prflow_params['board'],
                                  './build.sh',
                                  ]), True)      

    self.shell.write_lines(self.mono_dir + '/main.sh', self.return_main_sh_list_local(['./run.sh']), True)

    self.update_cad_path(self.mono_dir, operators, overlay_freq, is_mono=True)
    # self.update_build_sh(frequency) 

    # Copy hls results for synthesis
    os.system('cp ' + self.hls_dir + '/*/*/syn/verilog/*.v ' + self.mono_dir + '/' + self.prflow_params['board'] + '/mono_syn/app_src/')
    os.system('cp ' + self.hls_dir + '/*/*/syn/verilog/*.dat ' + self.mono_dir + '/' + self.prflow_params['board'] + '/mono_syn/app_src/')
    # os.system('cp ' + self.hls_dir + '/*/*/syn/verilog/*.tcl ' + self.mono_dir +  '/' + self.prflow_params['board'] + '/mono_syn/app_src/')

    # Place design command
    if self.prflow_params['place_design_mono_directive'] != '':
      place_design_command = '  place_design -directive ' + self.prflow_params['place_design_mono_directive']
    else:
      place_design_command = '  place_design'

    # Route design command
    if self.prflow_params['route_design_mono_directive'] != '':
      route_design_command = '  route_design -directive ' + self.prflow_params['route_design_mono_directive']
    else:
      route_design_command = '  route_design'

    with open(self.mono_dir +  '/' + self.prflow_params['board'] + '/mono_impl/impl_mono.tcl', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'place_design_command_with_directive' in line:
        line = place_design_command + '\n' 
      elif 'route_design_command_with_directive' in line:
        line = route_design_command + '\n' 
      filedata += line

    with open(self.mono_dir +  '/' + self.prflow_params['board'] + '/mono_impl/impl_mono.tcl', 'w') as outfile:
      outfile.write(filedata)


    # Generate mono.v for synthesis
    operator_arg_dict, operator_width_dict = self.return_operator_io_argument_dict_local(operators)
    # print(operator_arg_dict)
    # print(operator_width_dict)
    # e.g. operator_arg_dict: {'zculling_bot': ['Input_1', 'Input_2', 'Output_1']}
    # e.g. operator_width_dict: {'zculling_bot': ['ap_uint<32>', 'ap_uint<32>', 'ap_uint<32>']}

    operator_var_dict = self.return_operator_inst_dict_local(operators)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...
    # print(operator_var_dict)

    connection_list = self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict, operator_width_dict)
    # connection_list, e.g. {('coloringFB_bot_m.Output_1->coloringFB_top_m.Input_2', 128), ...
    # link, link_width
    # print(connection_list)

    # Copy for host code and modify
    os.system('cp -r ' + './input_src/' + self.prflow_params['benchmark_name'] + '/* ' + self.mono_dir + '/' + self.prflow_params['board'] + '/mono_host')
    with open(self.mono_dir +  '/' + self.prflow_params['board'] + '/mono_host/host/host.cpp', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if line.startswith('#define NUM_TOTAL_CNT'):
        # 3 is for full_cnt, empty_cnt, read_cnt, + stall cnt for each operator
        line = '#define NUM_TOTAL_CNT CONFIG_SIZE + ' + str(3 * len(connection_list) + len(operator_arg_dict.keys())) + '\n' 
      filedata += line

      if line.startswith('#define OUTPUT_SIZE'):
        output_size = line.split('OUTPUT_SIZE')[1].strip()

    with open(self.mono_dir +  '/' + self.prflow_params['board'] + '/mono_host/host/host.cpp', 'w') as outfile:
      outfile.write(filedata)


    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/operators' + '/specs.json', 'r') as infile:
      specs_dict = json.load(infile)

    # Generate mono.v
    mono_v_list, mono_counter_idx_dict = self.return_operator_inst_v_list(operator_arg_dict, connection_list, operator_var_dict, operator_width_dict, output_size, specs_dict)
    self.shell.write_lines(self.mono_dir + '/' + self.prflow_params['board'] + '/mono_syn/mono_src/mono.v', mono_v_list)

    # Save mono_counter_idx_dict for counter_analyze.py
    with open(self.mono_dir + '/mono_counter_idx_dict.json', 'w') as outfile:
      json.dump(mono_counter_idx_dict, outfile, sort_keys=True, indent=4)
