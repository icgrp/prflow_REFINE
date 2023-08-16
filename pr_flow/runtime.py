# -*- coding: utf-8 -*-   

import os  
import subprocess
from pr_flow.gen_basic import gen_basic
import re
import json
from pr_flow.p23_pblock import pblock_page_dict, pblock_xclbin_dict

is_done_config_dict = {2: ('0x00001004','0x90900fe0'), 3: ('0x00001804','0x90900fe0'), 4: ('0x00002004','0x90900fe0'), 5: ('0x00002804','0x90900fe0'),
                       6: ('0x00003004','0x90900fe0'), 7: ('0x00003804','0x90900fe0'), 8: ('0x00004004','0x90900fe0'), 9: ('0x00004804','0x90900fe0'),
                       10: ('0x00005004','0x90900fe0'), 11: ('0x00005804','0x90900fe0'), 12: ('0x00006004','0x90900fe0'), 13: ('0x00006804','0x90900fe0'),
                       14: ('0x00007004','0x90900fe0'), 15: ('0x00007804','0x90900fe0'), 16: ('0x00008004','0x90900fe0'), 17: ('0x00008804','0x90900fe0'),
                       18: ('0x00009004','0x90900fe0'), 19: ('0x00009804','0x90900fe0'), 20: ('0x0000A004','0x90900fe0'), 21: ('0x0000A804','0x90900fe0'),
                       22: ('0x0000B004','0x90900fe0'), 23: ('0x0000B804','0x90900fe0')}

class runtime(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)
    self.packet_bits        = int(self.prflow_params['packet_bits'])
    self.addr_bits          = int(self.prflow_params['addr_bits']) 
    self.port_bits          = int(self.prflow_params['port_bits'])
    self.payload_bits       = int(self.prflow_params['payload_bits'])
    self.bram_addr_bits     = int(self.prflow_params['bram_addr_bits'])
    self.freespace          = int(self.prflow_params['freespace'])
    self.page_addr_offset   = self.packet_bits - 1 - self.addr_bits
    self.port_offset        = self.packet_bits - 1 - self.addr_bits - self.port_bits
    self.config_port_offset = self.payload_bits - self.port_bits 
    self.dest_page_offset   = self.payload_bits - self.port_bits - self.addr_bits
    self.dest_port_offset   = self.payload_bits - self.port_bits - self.addr_bits - self.port_bits
    self.src_page_offset    = self.payload_bits - self.port_bits - self.addr_bits
    self.src_port_offset    = self.payload_bits - self.port_bits - self.addr_bits - self.port_bits
    self.freespace_offset   = self.payload_bits - self.port_bits - self.addr_bits - self.port_bits - self.bram_addr_bits - self.bram_addr_bits

  # # find all the operators page num  
  # def return_page_num_dict_local(self, syn_directory, operators):
  #   with open(self.syn_dir+'/page_assignment.json', 'r') as infile:
  #     (overlay_n, page_num_dict) = json.load(infile)
  #   page_num_dict['DMA'] = '1'
  #   page_num_dict['ARM'] = '0'
  #   print("############################ page_num_dict: ")
  #   print(page_num_dict)

  #   return page_num_dict, overlay_n 


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
              if 'Input' in operator_arg_dict[key_a][i_a]:
                tmp_str = key_b+'.'+operator_arg_dict[key_b][i_b]+'->'+key_a+'.'+operator_arg_dict[key_a][i_a]
              else:
                tmp_str = key_a+'.'+operator_arg_dict[key_a][i_a]+'->'+key_b+'.'+operator_arg_dict[key_b][i_b]
              connection_list.append(tmp_str)

    #connection_list = []
    #connection_list.append('DEBUG.Output_1->add1.Input_1')
    #connection_list.append('add1.Output_1->DEBUG.Input_1')
    #connection_list.append('add1.Output_2->DEBUG.Input_3')
    #connection_list.append('add1.Output_3->DEBUG.Input_3')
    #connection_list.append('add1.Output_5->DEBUG.Input_5')
    connection_list = set(connection_list)
    return connection_list


  # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
  # port_page_assign_dict, (page num, port number in the leaf interface)
  # , e.g. {'DMA.Input_1': (1, 2), 
  #         'DMA.Output_1': (1, 9), 
  #         'data_redir_m.Input_1': (4, 2), 
  #         'data_redir_m.Input_2': (5, 2), ...}
  def return_config_packet_list_local(self, port_page_assign_dict, connection_list, operators):
    packet_list = []
    # packet_num = 2
    packet_num = 5 # changed for bottleneck identification

    for str_value in connection_list:
      packet_list.append('//'+str_value)
      str_list = str_value.split('->')
      src_op_port_name = str_list[0]
      dest_op_port_name = str_list[1]

      [src_operator, src_output] = str_list[0].split('.')
      [dest_operator, dest_input] = str_list[1].split('.')

      # src_page = int(page_assign_dict[src_operator])
      # src_port = int(src_output.replace('Output_',''))+int(self.prflow_params['output_port_base'])-1
      # dest_page = int(page_assign_dict[dest_operator])
      # dest_port = int(dest_input.replace('Input_',''))+int(self.prflow_params['input_port_base'])-1

      src_page = port_page_assign_dict[src_op_port_name][0]
      src_port = port_page_assign_dict[src_op_port_name][1]
      dest_page = port_page_assign_dict[dest_op_port_name][0]
      dest_port = port_page_assign_dict[dest_op_port_name][1]
      print(src_page,src_port,'->',dest_page,dest_port) 

      src_page_packet =                   (src_page  << self.page_addr_offset)
      src_page_packet = src_page_packet + (       0  << self.port_offset)
      src_page_packet = src_page_packet + (src_port  << self.config_port_offset)
      src_page_packet = src_page_packet + (dest_page << self.dest_page_offset)
      src_page_packet = src_page_packet + (dest_port << self.dest_port_offset)
      src_page_packet = src_page_packet + ((2**self.bram_addr_bits-1) << self.freespace_offset)
      value_low  =  (src_page_packet      ) & 0xffffffff
      value_high =  (src_page_packet >> 32) & 0xffffffff
      # print 'src_page_packet: ', str(hex(value_high)).replace('L', ''), str(hex(value_low)).replace('L', '') 
      # packet_list.append("  write_to_fifo(" + str(hex(value_high)).replace('L', '') + ', ' + str(hex(value_low)).replace('L', '') + ");")

      packet_list.append("    in1["+str(packet_num)+"].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
      packet_list.append("    in1["+str(packet_num)+"].range(31,  0) = " + str(hex(value_low)).replace('L', '') + ";")
      packet_num += 1

      dest_page_packet =                    (dest_page  << self.page_addr_offset)
      dest_page_packet = dest_page_packet + (        1  << self.port_offset)
      dest_page_packet = dest_page_packet + (dest_port  << self.config_port_offset)
      dest_page_packet = dest_page_packet + (src_page   << self.src_page_offset)
      dest_page_packet = dest_page_packet + (src_port   << self.src_port_offset)
      value_low  =  (dest_page_packet      ) & 0xffffffff
      value_high =  (dest_page_packet >> 32) & 0xffffffff
      # print 'src_page_packet: ', str(hex(value_high)).replace('L', ''), str(hex(value_low)).replace('L', '') 
      # packet_list.append("  write_to_fifo(" + str(hex(value_high)).replace('L', '') + ', ' + str(hex(value_low)).replace('L', '') + ");")
      packet_list.append("    in1["+str(packet_num)+"].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
      packet_list.append("    in1["+str(packet_num)+"].range(31,  0) = " + str(hex(value_low)).replace('L', '') + ";")
      packet_num += 1

    operator_list = operators.split()
    bft_addr_shift = int(self.prflow_params['pks']) - int(self.prflow_params['payload_bits']) - 1 - int(self.prflow_params['addr_bits'])
    include_str = '#include \"typedefs.h\"\n'

    op_page_dict = {}
    # op_page_dict[op] = list of page num that op's leaf interface is connected to
    # e.g. op_page_dict = {'data_redir_m': [4, 5], 'data_transfer': [6], ...}
    for op_port_name in port_page_assign_dict.keys():
      op = op_port_name.split('.')[0]
      page_num = port_page_assign_dict[op_port_name][0]
      if op not in op_page_dict.keys():
        op_page_dict[op] = []
      else:
        if page_num not in op_page_dict[op]:
          op_page_dict[op].append(page_num)
    print("op_page_dict:")
    print(op_page_dict)
    print()

    # start page, DJP: probably not necessary if we are not using risc-v processor ver.
    for op in op_page_dict.keys(): 
      if op != 'DMA' and op != 'ARM':
        for page_num in op_page_dict[op]:
          value_high = (page_num << bft_addr_shift) + 2 # 2 is magic number in ExtractCtrl.v
          value_low  = 0
          packet_list.append('    // start page'+str(page_num)+'; ')
          packet_list.append("    in1["+str(packet_num)+"].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
          packet_list.append("    in1["+str(packet_num)+"].range(31,  0) = 0x" + str(hex(value_low )).replace('L', '').replace('0x','').zfill(8) + ";")
          packet_num += 1

    # is_done configuration
    num_is_done_config = 0
    for op in op_page_dict.keys(): 
      if op != 'DMA' and op != 'ARM':
        for page_num in op_page_dict[op]:
          value_high_hex = is_done_config_dict[page_num][0]
          value_low_hex = is_done_config_dict[page_num][1]
          packet_list.append('    // is_done config for ' + op + ', page_num:' + str(page_num))
          packet_list.append("    in1["+str(packet_num)+"].range(63, 32) = " + value_high_hex + '; ')
          packet_list.append("    in1["+str(packet_num)+"].range(31,  0) = " + value_low_hex + ";")
          packet_num += 1
          num_is_done_config += 1

    return packet_list, packet_num, num_is_done_config

  def return_run_sdk_sh_list_local(self, vivado_dir, tcl_file):
    return ([
      '#!/bin/bash -e',
      'source ' + vivado_dir,
      'xsdk -batch -source ' + tcl_file,
      ''])

  def return_sh_list_local(self, command):
    return ([
      '#!/bin/bash -e',
      command,
      ''])

  def get_recombined_pblock_xclbin_list(self, pblock_operators_list):
    with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
      pblock_assign_dict = json.load(infile)

    recombined_pblock_xclbin_list = []
    for op in pblock_operators_list:
      pblock_name = pblock_assign_dict[op]["pblock"]
      recombined_pblock_xclbin_list = recombined_pblock_xclbin_list + pblock_xclbin_dict[pblock_name]
    recombined_pblock_xclbin_list = list(set(recombined_pblock_xclbin_list))
    print(recombined_pblock_xclbin_list)
    return recombined_pblock_xclbin_list

  def get_dfx_lvl(self, re_xclbin):
    return re_xclbin.count('_') + 1

  def get_num_op(self, operator):
      return len(operator.split())


  # operators_impl_list has representative op only
  def get_operators_impl_list(self):
    pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
    with open(pblock_ops_dir + '/specs.json', 'r') as infile:
      # pblock_operators_list = json.load(infile)
      specs_dict = json.load(infile)
    pblock_operators_list = specs_dict.keys()

    operators_impl_list = []
    for pblock_op in pblock_operators_list:
        if(self.get_num_op(pblock_op)==1):
            operators_impl_list.append(pblock_op)
        else:
            pblock_op = pblock_op.split()[0] # only the first operator as representative op
            operators_impl_list.append(pblock_op)            
    # print(operators_impl_list)
    return operators_impl_list

  # prepare the run_app.sh for embedded system
  def gen_sd_run_app_sh(self, operators, overlay_freq):
    tmp_list = ['#!/bin/bash -e', \
                'date', \
                'if [ ! -f __static_loaded__ ]; then', \
                '    touch __static_loaded__', \
                '    ./app.exe dynamic_region.xclbin', \
                'else', \
                '    ./app.exe', \
                'fi']

    pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
    with open(pblock_ops_dir + '/specs.json', 'r') as infile:
      # pblock_operators_list = json.load(infile)
      specs_dict = json.load(infile)
    pblock_operators_list = specs_dict.keys()

    recombined_pblock_xclbin_list = self.get_recombined_pblock_xclbin_list(pblock_operators_list)
    # need to load from higher level DFX xclbins first
    for re_xclbin in recombined_pblock_xclbin_list:
      if(self.get_dfx_lvl(re_xclbin) == 2):
        tmp_list[4] = tmp_list[4] + " " + re_xclbin # 4,6 are just line numbers in run_app.sh
        tmp_list[6] = tmp_list[6] + " " + re_xclbin

    for re_xclbin in recombined_pblock_xclbin_list:
      if(self.get_dfx_lvl(re_xclbin) == 3):
        tmp_list[4] = tmp_list[4] + " " + re_xclbin
        tmp_list[6] = tmp_list[6] + " " + re_xclbin

    for re_xclbin in recombined_pblock_xclbin_list:
      if(self.get_dfx_lvl(re_xclbin) == 4):
        tmp_list[4] = tmp_list[4] + " " + re_xclbin
        tmp_list[6] = tmp_list[6] + " " + re_xclbin

    ##############
    # run_app.sh #
    ##############
    operators_impl_list = self.get_operators_impl_list()
    for idx, operator_impl in enumerate(operators_impl_list):
      tmp_list[4] = tmp_list[4] + " " + str(operator_impl) + ".xclbin" # ./app.exe dynamic_region.xclbin A.xclbin B.xclbin ...

    for idx, operator_impl in enumerate(operators_impl_list):
      tmp_list[6] = tmp_list[6] + " " + str(operator_impl) + ".xclbin" # ./app.exe A.xclbin B.xclbin ...

    self.shell.re_mkdir(self.bit_dir+'/sd_card')
    self.shell.cp_file(self.overlay_dir+'/ydma/'+self.prflow_params['board']+"/"+overlay_freq+"MHz"+'/xrt.ini', self.bit_dir)
    self.shell.write_lines(self.bit_dir+ '/sd_card/run_app.sh', tmp_list, True)

    self.shell.cp_file('common/script_src/compile_next.sh', self.bit_dir+'/sd_card')
    self.shell.cp_file('common/script_src/run_on_fpga.sh', self.bit_dir)


  # prepare the run_app.sh for Data Center Card 
  def gen_run_app_sh(self, operators):
    self.shell.cp_file('common/script_src/gen_runtime_'+self.prflow_params['board']+'.sh', self.bit_dir+'/run_app.sh')
    tmp_dict = {'Vitis'               : 'source '+self.prflow_params['Xilinx_dir'],
                'Xilinx_dir'          : 'source '+self.prflow_params['Xilinx_dir'],
                'make'                : 'make app.exe\ncp ./app.exe ../../\ncp ./app.exe ../../sd_card\n cp ../../sd_card/dynamic_region.xclbin ../../',
                'XCL_EMULATION_MODE'  : '',
                'PLATFORM_REPO_PATHS' : 'export PLATFORM_REPO_PATHS='+self.prflow_params['PLATFORM_REPO_PATHS'],
                'ROOTFS'              : 'export ROOTFS='+self.prflow_params['ROOTFS'],
                'sdk_dir'             : 'source '+self.prflow_params['sdk_dir']}
    xclbin_list_str = 'dynamic_region.xclbin' 
    for operator in operators.split(): xclbin_list_str += ' '+operator+'.xclbin'

    self.shell.replace_lines(self.bit_dir+'/run_app.sh', tmp_dict)
    self.shell.replace_lines(self.bit_dir+'/run_app.sh', {'g++': './app.exe '+xclbin_list_str})
    os.system('chmod +x '+ self.bit_dir+'/run_app.sh')


  def gen_runtime_sh(self):
    self.shell.cp_file('common/script_src/gen_runtime_'+self.prflow_params['board']+'.sh', self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/gen_runtime.sh')
    if('optical_flow' in self.prflow_params['benchmark_name']):
      host_compile_str = 'host.cpp ./imageLib/*.o'
    else:
      host_compile_str = 'host.cpp'
    tmp_dict = {'Vitis'               : 'source '+self.prflow_params['Xilinx_dir'],
                'Xilinx_dir'          : 'source '+self.prflow_params['Xilinx_dir'],
                'make'                : 'make app.exe\ncp ./app.exe ../../\ncp ./app.exe ../../sd_card\n cp ../../sd_card/dynamic_region.xclbin ../../',
                'cp_cmd'              : 'cp ./app.exe ../../sd_card',
                '${CXX} -Wall -g'     : '${CXX} -Wall -g -std=c++11 ' + host_compile_str +' -o ./app.exe \\',
                'XCL_EMULATION_MODE'  : '',
                'PLATFORM_REPO_PATHS' : 'export PLATFORM_REPO_PATHS='+self.prflow_params['PLATFORM_REPO_PATHS'],
                'ROOTFS'              : 'export ROOTFS='+self.prflow_params['ROOTFS'],
                'sdk_dir'             : 'source '+self.prflow_params['sdk_dir']}

    self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/gen_runtime.sh', tmp_dict)
    os.system('chmod +x '+ self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/gen_runtime.sh')



  def add_bft_config_to_host_cpp(self, operators, port_page_assign_dict, num_total_counter):

    # page_assign_dict, overlay_n = self.return_page_assign_dict_local(self.syn_dir, operators)
    # page_assign_dict, e.g. {'DMA': 1, 'rasterization2_m_1': 7, 'coloringFB_bot_m': 2, 'zculling_bot': 12, ... }

    operator_arg_dict = self.return_operator_io_argument_dict_local(operators)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': ['Input_1', 'Output_1' .. }

    operator_var_dict = self.return_operator_inst_dict_local(operators)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...
    # print(operator_arg_dict)
    # print(operator_var_dict)

    connection_list=self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    # print(connection_list)

    packet_list, packet_num, num_is_done_config = self.return_config_packet_list_local(port_page_assign_dict, connection_list, operators)
    # num_total_counter = 0
    # num_total_ports = 0
    # for op in operator_var_dict:
    #   num_total_ports += len(operator_var_dict[op])
    # num_total_counter = int(2.5*num_total_ports + num_is_done_config)
    num_total_counter += num_is_done_config

    # -5 for five constants
    tmp_dict = {'in1[0].range(31': '    in1[0].range(31,  0) = 0x'+str(hex(packet_num - 5 - num_is_done_config)).replace('L', '').replace('0x','').zfill(8)+';',
                '#define CONFIG_SIZE': '#define CONFIG_SIZE '+str(packet_num),
                '#define NUM_IS_DONE': '#define NUM_IS_DONE '+str(num_is_done_config),
                '#define NUM_TOTAL_CNT': '#define NUM_TOTAL_CNT '+str(num_total_counter)} 

    self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host.cpp', tmp_dict) 
    self.shell.add_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host.cpp', '// configure packets', packet_list)


 
  def run(self, operators):
    # mk work directory
    if self.prflow_params['gen_runtime']==True:
      self.shell.mkdir(self.bit_dir)
    
    overlay_freq = self.prflow_params['overlay_freq']
    # prepare the host driver source for vitis runtime
    self.shell.cp_file('input_src/'+self.prflow_params['benchmark_name'], self.bit_dir)

    with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
      pblock_assign_dict = json.load(infile)
    # page_assign_dict = self.get_page_assign_dict(pblock_assign_dict)

    port_page_assign_dict = {}
    # port_page_assign_dict, (page num, port number in the leaf interface)
    # , e.g. {'DMA.Input_1': (1, 2), 
    #         'DMA.Output_1': (1, 9), 
    #         'data_redir_m.Input_1': (4, 2), 
    #         'data_redir_m.Input_2': (5, 2), ...}
    port_page_assign_dict['DMA.Input_1'] = (1, int(self.prflow_params['input_port_base']))
    port_page_assign_dict['DMA.Output_1'] = (1, int(self.prflow_params['output_port_base']))

    num_i_ports_include_dummy = 0 # includes dummy ports
    num_o_ports_include_dummy = 0 # includes dummy ports
    for op in pblock_assign_dict.keys():
      page_num = pblock_assign_dict[op]['page_num']
      leaf_interface_dict = pblock_assign_dict[op]['leaf_interface']
      num_leaf_interface = len(leaf_interface_dict.keys())
      for i in range(num_leaf_interface):
        i_port_cnt = 0
        o_port_cnt = 0
        io_ports = leaf_interface_dict[str(i)]
        for io_port in io_ports:
          op_io_port = op + '.' + io_port

          if io_port.startswith('Input_'):
            port_num = int(self.prflow_params['input_port_base']) + i_port_cnt
            i_port_cnt += 1
          else:
            assert(io_port.startswith('Output_'))
            port_num = int(self.prflow_params['output_port_base']) + o_port_cnt
            o_port_cnt += 1
          port_page_assign_dict[op_io_port] = (page_num + i, port_num)

        if i_port_cnt == 0:
          num_i_ports_include_dummy += 1
        else:
          num_i_ports_include_dummy += i_port_cnt
        if o_port_cnt == 0:
          num_o_ports_include_dummy += 1
        else:
          num_o_ports_include_dummy += o_port_cnt

    # read, empty, full cnt for input port
    # empty, full cnt for output port
    # stall cnt not included in num_total_counter yet
    num_total_counter = 3*num_i_ports_include_dummy + 2*num_o_ports_include_dummy


    # page_assign_dict['DMA'] = '1'
    # page_assign_dict['ARM'] = '0'
    print("############################ port_page_assign_dict: ")
    print(port_page_assign_dict)

    # add configuration packets to host.cpp
    # and reads overlay_n from syn_dir/page_assignment.pickle
    self.add_bft_config_to_host_cpp(operators, port_page_assign_dict, num_total_counter)

    # prepare the gen_runtime.sh to generate the app.exe 
    self.gen_runtime_sh()

    # generate the run_app.sh for embedded platform
    self.gen_sd_run_app_sh(operators, overlay_freq)
