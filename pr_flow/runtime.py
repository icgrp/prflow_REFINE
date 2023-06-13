# -*- coding: utf-8 -*-   

import os  
import subprocess
from pr_flow.gen_basic import gen_basic
import re
import json
from pr_flow.p23_pblock import pblock_page_dict, pblock_xclbin_dict

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
              if self.shell.have_target_string(operator_arg_dict[key_a][i_a], 'Input'):
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


  def return_config_packet_list_local(self, page_assign_dict, connection_list, operator_list):
    packet_list = []
    packet_num = 2
    for str_value in connection_list:
      packet_list.append('//'+str_value)
      str_list = str_value.split('->')
      [src_operator, src_output] = str_list[0].split('.')
      [dest_operator, dest_input] = str_list[1].split('.')
      src_page = int(page_assign_dict[src_operator])
      src_port = int(src_output.replace('Output_',''))+int(self.prflow_params['output_port_base'])-1
      dest_page = int(page_assign_dict[dest_operator])
      dest_port = int(dest_input.replace('Input_',''))+int(self.prflow_params['input_port_base'])-1
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

    bft_addr_shift = int(self.prflow_params['pks']) - int(self.prflow_params['payload_bits']) - 1 - int(self.prflow_params['addr_bits'])
    include_str = '#include \"typedefs.h\"\n'
    for op in operator_list: 
      HW_exist, target = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+op+'.h', 'map_target')
      instr_size_exist, instr_size = self.pragma.return_pragma('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+op+'.h', 'inst_mem_size')
      if target == 'RISCVV': 
        value_high = (int(page_assign_dict[op]) << bft_addr_shift) + 1 
        packet_list.append('      for( int i=0; i<'+str(int(instr_size)/4)+'; i++){')
        packet_list.append("        in1["+str(packet_num)+"+i*4+0].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
        packet_list.append("        in1["+str(packet_num)+"+i*4+0].range(31,  0) = ((i*4+0) << 8) + ((instr_data"+str(page_assign_dict[op])+"[i]>>0 )  & 0x000000ff);")
        packet_list.append("        in1["+str(packet_num)+"+i*4+1].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
        packet_list.append("        in1["+str(packet_num)+"+i*4+1].range(31,  0) = ((i*4+1) << 8) + ((instr_data"+str(page_assign_dict[op])+"[i]>>8 )  & 0x000000ff);")
        packet_list.append("        in1["+str(packet_num)+"+i*4+2].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
        packet_list.append("        in1["+str(packet_num)+"+i*4+2].range(31,  0) = ((i*4+2) << 8) + ((instr_data"+str(page_assign_dict[op])+"[i]>>16)  & 0x000000ff);")
        packet_list.append("        in1["+str(packet_num)+"+i*4+3].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
        packet_list.append("        in1["+str(packet_num)+"+i*4+3].range(31,  0) = ((i*4+3) << 8) + ((instr_data"+str(page_assign_dict[op])+"[i]>>24)  & 0x000000ff);")
        packet_list.append("      }")
        packet_num += int(instr_size)
        include_str += '#include \"instr_data'+str(page_assign_dict[op])+'.h\"\n'
        self.shell.cp_dir(self.syn_dir+'/'+op+'/instr_data'+str(page_assign_dict[op])+'.h', self.bit_dir) 
    # self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host.cpp', {'typedefss.h': include_str}) 

    for op in operator_list: 
      value_high = (int(page_assign_dict[op]) << bft_addr_shift) + 2 
      value_low  = 0
      packet_list.append('    // start page'+str(page_assign_dict[op])+'; ')
      packet_list.append("    in1["+str(packet_num)+"].range(63, 32) = 0x" + str(hex(value_high)).replace('L', '').replace('0x','').zfill(8) + '; ')
      packet_list.append("    in1["+str(packet_num)+"].range(31,  0) = 0x" + str(hex(value_low )).replace('L', '').replace('0x','').zfill(8) + ";")
      packet_num += 1
    return packet_list, packet_num

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

  def get_recombined_pblock_xclbin_list(self, syn_directory, pblock_operators_list):
    with open(syn_directory+'/pblock_assignment.json', 'r') as infile:
      (overlay_n, pblock_assign_dict) = json.load(infile)

    recombined_pblock_xclbin_list = []
    for pblock_op in pblock_operators_list:
      pblock_name = pblock_assign_dict[pblock_op]
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
    with open(pblock_ops_dir + '/pblock_operators_dict.json', 'r') as infile:
      pblock_operators_dict = json.load(infile)
    pblock_operators_list = list(pblock_operators_dict.keys())

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
  def gen_sd_run_app_sh(self, operator_list, overlay_n, syn_directory, frequency, operator):
    if operator != None:
      exec_filename = 'app_bi-'+operator+'.exe'
      filename = 'run_app_bi-'+operator+'.sh'
    else:
      exec_filename = 'app.exe'
      filename = 'run_app.sh'

    tmp_list = ['#!/bin/bash -e', \
                'date', \
                'if [ ! -f __static_loaded__ ]; then', \
                '    touch __static_loaded__', \
                '    ./' + exec_filename + ' dynamic_region.xclbin', \
                'else', \
                '    ./' + exec_filename, \
                'fi']

    # pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
    # with open(pblock_ops_dir + '/pblock_operators_dict.json', 'r') as infile:
    #   pblock_operators_dict = json.load(infile)
    # pblock_operators_list = list(pblock_operators_dict.keys())

    recombined_pblock_xclbin_list = self.get_recombined_pblock_xclbin_list(syn_directory, operator_list)
    # need to load from higher level DFX xclbins first
    for re_xclbin in recombined_pblock_xclbin_list:
      if(self.get_dfx_lvl(re_xclbin) == 2):
        tmp_list[4] = tmp_list[4] + " " + re_xclbin
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
    # operators_impl_list = self.get_operators_impl_list()
    operators_impl_list = operator_list
    for idx, operator_impl in enumerate(operators_impl_list):
      tmp_list[4] = tmp_list[4] + " " + str(operator_impl) + ".xclbin" # ./app.exe dynamic_region.xclbin A.xclbin B.xclbin ...

    for idx, operator_impl in enumerate(operators_impl_list):
      tmp_list[6] = tmp_list[6] + " " + str(operator_impl) + ".xclbin" # ./app.exe A.xclbin B.xclbin ...

    self.shell.cp_file(self.overlay_dir+'/ydma/'+self.prflow_params['board']+"/"+frequency+"MHz"+'/xrt.ini', self.bit_dir)
    # self.shell.cp_file(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/load.exe', self.bit_dir+'/sd_card')

    # self.shell.cp_file(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/dynamic_region.xclbin', self.bit_dir+'/sd_card')
    # self.shell.cp_file(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/*.xclbin', self.bit_dir+'/sd_card')
    self.shell.write_lines(self.bit_dir+ '/sd_card/'+filename, tmp_list, True)

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


  def gen_runtime_sh(self, host_cpp_str, operator, host_opt_lvl):
    if operator != None:
      exec_filename = 'app_bi-'+operator+'.exe'
      filename = 'gen_runtime_bi-'+operator+'.sh'
    else:
      exec_filename = 'app.exe'
      filename = 'gen_runtime.sh'

    self.shell.cp_file('common/script_src/gen_runtime_'+self.prflow_params['board']+'.sh', self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/'+filename)
    if('optical_flow' in self.prflow_params['benchmark_name']):
      host_compile_str = host_cpp_str + ' ./imageLib/*.o'
    else:
      host_compile_str = host_cpp_str
    tmp_dict = {'Vitis'               : 'source '+self.prflow_params['Xilinx_dir'],
                'Xilinx_dir'          : 'source '+self.prflow_params['Xilinx_dir'],
                'make'                : 'make ' + exec_filename + '\ncp ./' +\
                                             exec_filename + ' ../../\ncp ./' +\
                                             exec_filename + ' ../../sd_card\n cp ../../sd_card/dynamic_region.xclbin ../../',
                'cp_cmd'              : 'cp ./' + exec_filename + ' ../../sd_card',
                '${CXX} -Wall -g'     : '${CXX} -Wall -' + host_opt_lvl + ' -g -std=c++11 ' + host_compile_str +' -o ./' + exec_filename + ' \\',
                'XCL_EMULATION_MODE'  : '',
                'PLATFORM_REPO_PATHS' : 'export PLATFORM_REPO_PATHS='+self.prflow_params['PLATFORM_REPO_PATHS'],
                'ROOTFS'              : 'export ROOTFS='+self.prflow_params['ROOTFS'],
                'sdk_dir'             : 'source '+self.prflow_params['sdk_dir']}

    self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/'+filename, tmp_dict)
    os.system('chmod +x '+ self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/'+filename)

  # e.g.: output_w_str = 'Output_1_WIDTH'
  # returns the width of Output_1
  def get_output_width(self, output_w_str, operator):
    with open('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.h', 'r') as infile:
      lines = infile.readlines()
    output_str = output_w_str.replace('_WIDTH','')
    for line in lines:
      if output_str in line:
        tmp = re.findall(r"ap_uint<\d*>", line)[0]
        width = tmp.replace("ap_uint<","").replace(">","")
        return int(width)

  # e.g.: output_size_formula = "640*numReps_mva_1*MH1_mva_1/PE1_mva_1*32/512*min(1,32/Output_1_WIDTH)"
  def get_output_size(self, operator, output_size_formula):
    variable_val_dict = {}
    special_exp_dict = {}

    # Handle special expressions first
    special_exp_list = ['min', 'max'] # for now, supports only min or max
    for exp in special_exp_list:
        count = output_size_formula.count(exp)
        for i in range(count):
            if exp in output_size_formula:
                complete_string = exp + '('
                remain = output_size_formula.split(exp+'(')[1]
                buf = ''
                for c in remain:
                    if c != ')':
                        buf = buf + c
                    else:
                        buf = buf + c
                        break
                complete_string += buf
                special_exp_dict[exp + '_' + str(i)] = str(complete_string)
                output_size_formula = output_size_formula.replace(complete_string, exp + '_' + str(i))
    # print(output_size_formula)
    # print(special_exp_dict)

    # Get all variables necessary to compute output_size_formula
    # in variable_val_dict and special_exp_dict
    math_exps = ['+','-','*','/'] # for now, supports only four operations
    variables = output_size_formula
    for math_exp in math_exps:
        variables = variables.replace(math_exp,',')
    variables = variables.split(',')

    for var in variables:
        is_valid = True
        for exp in special_exp_list:
            if var.startswith(exp):
                is_valid = False
        if var.isdigit():
            is_valid = False
        if is_valid:
            variable_val_dict[var] = -1
    # print(variable_val_dict)

    # Extract var for variable_val_dict
    with open('./input_src/'+self.prflow_params['benchmark_name']+'/operators/'+operator+'.cpp', 'r') as infile:
        lines = infile.readlines()
    for var in variable_val_dict.keys():
        if var.startswith('Output_'):
            val = self.get_output_width(var, operator)
            variable_val_dict[var] = val
        for line in lines:
            if '#define ' + var in line:
                val = int(line.split('#define ' + var + ' ')[1].strip())
                variable_val_dict[var] = val
    # print(variable_val_dict)

    # Extract var for special_exp_dict
    for special_var, special_exp in special_exp_dict.items():
        for var in variable_val_dict.keys():
            if var in special_exp:
                special_exp = special_exp.replace(var,str(variable_val_dict[var]))
        if 'Output_' in special_exp:
            output_w_str = re.findall(r"Output_\d*_WIDTH", special_exp)[0]
            val = self.get_output_width(output_w_str, operator)
            special_exp = special_exp.replace(output_w_str,str(val))
            print(special_exp)
        special_exp_dict[special_var] = eval(special_exp)
    # print(special_exp_dict)

    # Evaluate output_size_formula
    for var,val in variable_val_dict.items():
        if var in output_size_formula:
            output_size_formula = output_size_formula.replace(var,str(val))
    for special_var,val in special_exp_dict.items():
        if special_var in output_size_formula:
            output_size_formula = output_size_formula.replace(special_var,str(val))

    print(output_size_formula)
    print(eval(output_size_formula))
    return int(eval(output_size_formula))

  def add_bft_config_to_host_cpp(self, operators, page_assign_dict, feed_forward_order):

    # page_assign_dict, overlay_n = self.return_page_assign_dict_local(self.syn_dir, operators)
    # page_assign_dict, e.g. {'DMA': 1, 'rasterization2_m_1': 7, 'coloringFB_bot_m': 2, 'zculling_bot': 12, ... }

    operator_arg_dict = self.return_operator_io_argument_dict_local(operators)
    # operator_arg_dict, e.g. {'zculling_bot': ['Input_1', 'Input_2', 'Output_1'], 'rasterization2_m': ['Input_1', 'Output_1' .. }

    operator_var_dict = self.return_operator_inst_dict_local(operators)
    # operator_var_dict, e.g. {'rasterization2_m': ['Output_redir_odd', 'Output_r2_odd_top', 'Output_r2_odd_bot' ...
    print(operator_arg_dict)
    print(operator_var_dict)

    connection_list=self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...
    print(connection_list)

    print(feed_forward_order[:-1])
    # host.cpp for Bottleneck Identification
    for idx, operator in enumerate(feed_forward_order[:-1]):
      ops_to_be_removed = feed_forward_order[idx+1:]
      connection_list_short = []
      for connection in connection_list:
        send,recv = connection.split('->')
        send = send.split('.')[0]
        recv = recv.split('.')[0]
        is_valid_connection = True
        for op_rm in ops_to_be_removed:
          if op_rm == send or op_rm == recv:
            is_valid_connection = False
        if is_valid_connection:
          connection_list_short.append(connection)
      connection_list_short.append(operator + '.Output_1->DMA.Input_1')
      print(connection_list_short)
      ops_short = feed_forward_order[:idx+1]

      pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
      with open(pblock_ops_dir + '/pblock_operators_dict.json', 'r') as infile:
        pblock_operators_dict = json.load(infile)
      output_size_formula = pblock_operators_dict[operator]
      output_size = self.get_output_size(operator, output_size_formula)

      packet_list, packet_num = self.return_config_packet_list_local(page_assign_dict, connection_list_short, ops_short)
      tmp_dict = {'in1[0].range(31': '    in1[0].range(31,  0) = 0x'+str(hex(packet_num-2)).replace('L', '').replace('0x','').zfill(8)+';',
                  '#define CONFIG_SIZE': '#define CONFIG_SIZE '+str(packet_num),
                  '#define OUTPUT_SIZE': '#define OUTPUT_SIZE '+str(output_size),
                  '    outfile << "CUR_OPERATOR, avg elapsed time: "': \
                  '    outfile << "' + operator + ', avg elapsed time: " << elapsed_sum/elapsed_vector.size() << "us\\n";'}
      self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host_bi-' + operator + '.cpp', tmp_dict) 
      self.shell.add_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host_bi-' + operator + '.cpp', '// configure packets', packet_list)

    # normal host.cpp
    operator_list = operators.split()
    packet_list, packet_num = self.return_config_packet_list_local(page_assign_dict, connection_list, operator_list)
    tmp_dict = {'in1[0].range(31': '    in1[0].range(31,  0) = 0x'+str(hex(packet_num-2)).replace('L', '').replace('0x','').zfill(8)+';',
                '#define CONFIG_SIZE': '#define CONFIG_SIZE '+str(packet_num)} 
    self.shell.replace_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host.cpp', tmp_dict) 
    self.shell.add_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/host.cpp', '// configure packets', packet_list)


  def gen_host_cpp(self, operators):
    operator_arg_dict = self.return_operator_io_argument_dict_local(operators)
    operator_var_dict = self.return_operator_inst_dict_local(operators)
    connection_list = self.return_operator_connect_list_local(operator_arg_dict, operator_var_dict)
    # connection_list, e.g. set(['DMA.Output_1->data_transfer.Input_1', 'coloringFB_top_m->DMA.Input_2' ...

    # Assume feed-forward
    feed_forward_order = ['DMA']
    send_recv_list = []
    for connection in connection_list:
      send,recv = connection.split('->')
      send = send.split('.')[0]
      recv = recv.split('.')[0]
      send_recv_list.append((send,recv))

    operator_list = operators.split()
    for i in range(len(operator_list)):
      cur_op = feed_forward_order[-1]
      for send,recv in send_recv_list:
        if cur_op == send:
          feed_forward_order.append(recv)
          break
    
    feed_forward_order = feed_forward_order[1:] # drop 'DMA'
    pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
    with open(pblock_ops_dir + '/pblock_operators_dict.json', 'r') as infile:
      pblock_operators_dict = json.load(infile)
    for operator in feed_forward_order[:-1]:
      os.system("cp " + self.bit_dir + '/' + self.prflow_params['benchmark_name'] + '/host/host_bi.cpp ' +\
        self.bit_dir + '/' + self.prflow_params['benchmark_name'] + '/host/host_bi-' + operator + '.cpp')

    return feed_forward_order

  def run(self, operators, frequency="200"):
    host_opt_lvl = 'O3'

    # mk work directory
    if self.prflow_params['gen_runtime']==True:
      self.shell.mkdir(self.bit_dir)
    
    # prepare the host driver source for vitis runtime
    self.shell.cp_file('input_src/'+self.prflow_params['benchmark_name'], self.bit_dir)

    # generate multiple host.cpp for Bottleneck Identification
    feed_forward_order = self.gen_host_cpp(operators)


    with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
      (overlay_n, pblock_assign_dict) = json.load(infile)
    page_assign_dict = self.get_page_assign_dict(pblock_assign_dict)
    page_assign_dict['DMA'] = '1'
    page_assign_dict['ARM'] = '0'
    print("############################ page_assign_dict: ")
    print(page_assign_dict)
 
    # add configuration packets to host.cpp
    # and reads overlay_n from syn_dir/page_assignment.pickle
    self.add_bft_config_to_host_cpp(operators, page_assign_dict, feed_forward_order)

    gen_runtime_files_str = ''
    run_app_bi_files_str = ''
    operator_list = operators.split()
    self.shell.re_mkdir(self.bit_dir+'/sd_card')
    # Prepare gen_runtime.sh for bottleneck identification
    for idx,operator in enumerate(feed_forward_order[:-1]):
      gen_runtime_files_str += './gen_runtime_bi-' + operator + '.sh\n'
      run_app_bi_files_str += './run_app_bi-' + operator + '.sh\n'
      host_cpp_str = 'host_bi-' + operator + '.cpp'
      self.gen_runtime_sh(host_cpp_str,operator,host_opt_lvl)
      # Generate the run_app.sh for embedded platform, the main host.cpp
      self.gen_sd_run_app_sh(feed_forward_order[:idx+1], overlay_n, self.syn_dir, frequency, operator)


    # Prepare gen_runtime.sh for the main host.cpp
    host_cpp_str = 'host.cpp'
    self.gen_runtime_sh(host_cpp_str,None,host_opt_lvl)
    # Generate the run_app.sh for embedded platform, the main host.cpp
    self.gen_sd_run_app_sh(operator_list, overlay_n, self.syn_dir, frequency, None)
    gen_runtime_files_str += './gen_runtime.sh\n'

    # Will call all gen_runtime*.sh to generate host executables
    self.shell.write_lines(self.bit_dir+'/'+self.prflow_params['benchmark_name']+'/host/main.sh', ['#!/bin/bash -e',
                                                                                                  gen_runtime_files_str],
                                                                                                  True)
    # On FPGA device, will run all run_app_bi-* to identify bottleneck
    self.shell.write_lines(self.bit_dir+'/'+'/sd_card/run_app_bi_all.sh', ['#!/bin/bash -e',
                                                                                                  run_app_bi_files_str],
                                                                                                  True)