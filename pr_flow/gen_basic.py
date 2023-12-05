# -*- coding: utf-8 -*-


import os
import subprocess
import xml.etree.ElementTree
import re
# import commands
from pr_flow.p23_pblock import pblock_page_dict




class _shell:
  def __init__(self, prflow_params):
    self.prflow_params = prflow_params

      
  def file_to_list(self, file_name):
    file_list = []
    file_in = open(file_name, 'r')
    for line in file_in:
      file_list.append(line.replace('\n',''))
    return file_list

  # return the qsub command according to the input parameters
  def return_qsub_command_str(self, shell_file='./qsub_run', hold_jid='NONE', name='NONE', q='70s', email='qsub@qsub.com', MEM='2G', node_num='1'):
    return ('qsub -N '+name + ' -q ' + q + ' -hold_jid ' + hold_jid + ' -m abe -M ' + email + ' -l mem='+MEM + ' -pe onenode '+node_num + '  -cwd '+ shell_file)

  # return the slurm command according to the input parameters
  def return_slurm_command_str(self, shell_file='./qsub_run', hold_jid='NONE', name='NONE', q='70s', email='qsub@qsub.com', MEM='2G', node_num='1'):
    return ('sbatch --ntasks=1 --cpus-per-task='+node_num+' --mem-per-cpu='+MEM+' --job-name='+name+' --dependency=$(squeue --noheader --format %i --user=$USER --name '+hold_jid+'| sed -n -e \'H;${x;s/\\n/,/g;s/^,//;p;}\') '+shell_file)


  def get_file_name(self, file_dir):
  # return a file list under a file_dir
    for root, dirs, files in os.walk(file_dir):
      return files

  def replace_lines(self, filename, modification_dict):
  # change the string(key of modification_dict) to
  # target string (value of modification_dict)
    try:
      file_in =  open(filename, 'r')
      file_out = open(filename+'tmp', 'w')
      for line in file_in:
        find_target = False
        for key, value in modification_dict.items():
          if line.replace(key, '') != line:
            file_out.write(value+'\n')
            find_target = True
            break
        if find_target == False:
          file_out.write(line)
      file_out.close()
      file_in.close()
      os.system('mv '+filename+'tmp '+filename)
    except:
      print("Modification for "+filename+" failed!")

  def my_sed(self, filename, modification_dict):
  # change the string(key of modification_dict) to
  # target string (value of modification_dict)
    try:
      print(modification_dict)
      file_in =  open(filename, 'r')
      file_out = open(filename+'tmp', 'w')
      for line in file_in:
        print(line)
        for key, value in modification_dict.items():
          print(key, value)
          line = line.replace(key, value)
        file_out.write(line)
      file_out.close()
      file_in.close()
      os.system('mv '+filename+'tmp '+filename)
    except:
      print("Modification for "+filename+" failed!")


  def add_lines(self, filename, anchor, lines_list):
  # add more lines in a file according to
  # some anchor string
    try:
      file_in =  open(filename, 'r')
      file_out = open(filename+'tmp', 'w')
      for line in file_in:
        if line.replace(anchor, '') != line:
          file_out.write('\n'.join(lines_list)+'\n')
        file_out.write(line)
      file_out.close()
      file_in.close()
      os.system('mv '+filename+'tmp '+filename)
    except:
      print("Adding more line in "+filename+" failed!")

  def write_lines(self, filename, lines_list, executable=False, write_or_add='w'):
    try:
      os.system('mkdir -p '+filename.replace(filename.split('/')[-1], ''))
      file_out = open(filename, write_or_add)
      file_out.write('\n'.join(lines_list)+'\n')
      file_out.close()
      if executable == True:
         os.system('chmod +x ' + filename)
    except:
      print("Writing "+filename+" failed!")

  def re_mkdir(self, dir_name):
     os.system('rm -rf ' + dir_name)
     os.system('mkdir -p ' + dir_name)

  def mkdir(self, dir_name):
     os.system('mkdir -p ' + dir_name)

  def del_dir(self, dir_name):
     os.system('rm -rf ' + dir_name)

  def cp_dir(self, src_dir, dst_dir):
     os.system('cp -rf '+src_dir+' '+dst_dir)

  def cp_file(self, src_file, dst_file):
     os.system('cp -rf '+src_file+' '+dst_file)

  def return_run_sh_list(self, vivado_dir, tcl_file, back_end='qsub'):
    out_file = []
    out_file.append('#!/bin/bash -e')
    if (back_end == 'slurm'):
      # out_file.append('module load ' + vivado_dir)
      out_file.append('source ' + vivado_dir)
      out_file.append('srun vivado -mode batch -source  ' + tcl_file)
    else:
      out_file.append('source ' + vivado_dir)
      # if(monitor_on == True):
      #   out_file.append('if [ ! -f ../__monitoring_running__ ]; then')
      #   out_file.append('    ../monitor.sh "$@" &')
      #   out_file.append('    touch ../__monitoring_running__')
      #   out_file.append('fi')
      out_file.append('vivado -mode batch -source  ' + tcl_file)
      # if(monitor_on == True):
      #   out_file.append('touch __done__')
    return out_file 


  def return_run_hls_sh_list(self, vivado_dir, hls_tcl_file=None, syn_tcl_file_list=[], back_end='qsub', operator_dir='test_prj'):
    out_file = []
    out_file.append('#!/bin/bash -e')
    if (back_end == 'slurm'):
      # out_file.append('module load ' + vivado_dir)
      out_file.append('source ' + vivado_dir)
      if(hls_tcl_file != None): out_file.append('srun vitis_hls -f ' + hls_tcl_file)
      for syn_tcl_file in syn_tcl_file_list: out_file.append('srun vivado -mode batch -source ' + syn_tcl_file)
    else:
      out_file.append('source ' + vivado_dir)

      out_file.append('')
      # if(monitor_on == True):
      #   out_file.append('# The earliest impl run launches ../monitor.sh and marks ../__monitoring_running__')
      #   out_file.append('# Following impl runs are blocked')
      #   out_file.append('if [ ! -f __monitoring_running__ ]; then')
      #   out_file.append('    ./monitor.sh "$@" &')
      #   out_file.append('    touch __monitoring_running__')
      #   out_file.append('fi')
      out_file.append('vitis_hls -f ' + hls_tcl_file)
      # if(monitor_on == True):
      #   out_file.append('touch '+'./'+operator_dir+'/'+'__done__')
      # if(hls_tcl_file != None): out_file.append('vitis_hls -f ' + hls_tcl_file)
      # for syn_tcl_file in syn_tcl_file_list: out_file.append('vivado -mode batch -source ' + syn_tcl_file)
    return out_file 

  def return_main_sh_list(self, run_file='run.sh', back_end='qsub', hold_jid='NONE', name='NONE', q='70s', email='qsub@qsub.com', MEM='2G', node_num='1'):
    out_list = []
    out_list.append('#!/bin/bash -e')

    # out_list.append('# The earliest impl run launches ../monitor.sh and marks ../__monitoring_running__')
    # out_list.append('# Following impl runs are blocked')

    # if(monitor_dir=='./'): #F002, F005 case
    #   out_list.append('if [ ! -f __monitoring_running__ ]; then')
    #   out_list.append('    ./monitor.sh "$@" &')
    #   out_list.append('    touch __monitoring_running__')
    #   out_list.append('fi')
    # elif(monitor_dir=='../'): #F003, F004 case
    #   out_list.append('if [ ! -f ../__monitoring_running__ ]; then')
    #   out_list.append('    ../monitor.sh "$@" &')
    #   out_list.append('    touch ../__monitoring_running__')
    #   out_list.append('fi')

    if back_end == 'qsub':
      out_list.append(self.return_qsub_command_str(run_file, hold_jid, name, q, email, MEM, node_num))
    elif back_end == 'slurm':
      out_list.append(self.return_slurm_command_str(run_file, hold_jid, name, q, email, MEM, node_num))
    else:
      out_list.append(run_file + ' "$@"')

    # if(monitor_dir=='./'): #F002, F005 case
    #    out_list.append('touch '+'./'+operator_dir+'/'+'__done__')
    # elif(monitor_dir=='../'): #F003, F004 case
    #   out_list.append('touch __done__')

    return (out_list)

  def return_empty_sh_list(self):
    return ([
      '#!/bin/bash -e',
      ''])


  def return_qsub_scan_sh_list(self, scan_dir, run_shell='qsub_run.sh', hold_prefix='hls_', name_prefix='mono_bft_'):
    return ([
      '#!/bin/bash -e',
      'source ' + self.prflow_params['Xilinx_dir'],
      'emailAddr="' + self.prflow_params['email'] + '"',
      'file_list=\'dummy\'',
      'for file in $(ls '+scan_dir+')',
      'do',
      '  if [ "$file" != "synth_1" ]; then',
      '    file_list=$file_list\','+name_prefix+'\'$file',
      '    cd \''+scan_dir+'/\'$file',
      '    qsub  -hold_jid '+hold_prefix+'$file -N '+name_prefix+'$file -q ' + self.prflow_params['grid'] + ' -m abe -M $emailAddr -l mem=8G  -cwd ./'+run_shell,
      '    cd -',
      '  fi',
      'done',
      ''])


class _pragma(_shell):
  def return_pragma(self, file_name, pragma_name, pragma_object=''):
    src_list = self.file_to_list(file_name)
    if_exist = False
    value = 0
    for line in src_list:
      if(line.replace("#pragma", "") != line):
        line_list = line.replace('=', ' ').split()
        if(line_list[0].startswith('//')):
          continue
        for idx, ele in enumerate(line_list):
          if(ele == pragma_name):
            if_exist = True
            value = line_list[idx+1]
    return if_exist, value 
 
class _verilog:
  def __init__(self, prflow_params):
    self.prflow_params = prflow_params
    pass

  def return_idx_in_list_local(self, in_list, ele):
    print(ele, in_list)
    for idx, val in enumerate(in_list):
      if val == ele:
        return idx
    return 'NONE'


  def my_max(self, a, b):
    if(a>b): return a
    else: return b



  # def return_place_holder_v_list(self, operator, input_width_list, output_width_list, is_dummy = False):
  #   input_num = len(input_width_list)
  #   output_num = len(output_width_list) 
  #   lines_list = []
  #   lines_list.append('`timescale 1ns / 1ps')
  #   lines_list.append('module '+operator+'(')
  #   lines_list.append('    input wire ap_clk,')
  #   lines_list.append('    input wire ap_start,')
  #   lines_list.append('    output reg ap_done,')
  #   lines_list.append('    output reg ap_idle,')
  #   lines_list.append('    output reg ap_ready,')
  #   for i in range(int(input_num)):
  #     lines_list.append('    input wire ['+str(input_width_list[i]-1)+':0] Input_'+str(i+1)+'_V_TDATA,')
  #     lines_list.append('    input wire Input_'+str(i+1)+'_V_TVALID,')
  #     lines_list.append('    output reg Input_'+str(i+1)+'_V_TREADY,')
  #   for i in range(int(output_num)):
  #     lines_list.append('    output reg ['+str(output_width_list[i]-1)+':0] Output_'+str(i+1)+'_V_TDATA,')
  #     lines_list.append('    output reg Output_'+str(i+1)+'_V_TVALID,')
  #     lines_list.append('    input wire Output_'+str(i+1)+'_V_TREADY,')
  #   lines_list.append('    input wire ap_rst_n')
  #   lines_list.append('    );')
  #   lines_list.append('')
  #   lines_list.append('')
  #   lines_list.append('')
  #   if is_dummy == False:
  #     lines_list.append('  always@(posedge ap_clk) begin')
  #     lines_list.append('    if(ap_rst_n) begin')
  #     lines_list.append('      ap_done  <= 1\'b0;')
  #     lines_list.append('      ap_idle  <= 1\'b0;')
  #     lines_list.append('      ap_ready <= 1\'b0;')
  #     for i in range(int(input_num)):
  #       lines_list.append('      Input_'+str(i+1)+'_V_TREADY  <= 0;')
  #     for i in range(int(output_num)):
  #       lines_list.append('      Output_'+str(i+1)+'_V_TVALID <= 0;')
  #       lines_list.append('      Output_'+str(i+1)+'_V_TDATA  <= 0;')
  #     lines_list.append('    end else begin')
  #     lines_list.append('      ap_done  <= ap_start;')
  #     lines_list.append('      ap_idle  <= ap_start;')
  #     lines_list.append('      ap_ready <= ap_start;')
  #     for i in range(int(input_num)):
  #       lines_list.append('      Input_'+str(i+1)+'_V_TREADY  <= Input_'+str(i+1)+'_V_TVALID & (|Input_'+str(i+1)+'_V_TDATA['+str(input_width_list[i]-1)+':0]);')
  #     for i in range(int(output_num)):
  #       lines_list.append('      Output_'+str(i+1)+'_V_TVALID <= Output_'+str(i+1)+'_V_TREADY;')
  #       lines_list.append('      Output_'+str(i+1)+'_V_TDATA  <= {('+str(output_width_list[i])+'){Output_'+str(i+1)+'_V_TREADY}} ;')
  #     lines_list.append('    end')
  #     lines_list.append('  end')
  #     lines_list.append('')
  #     lines_list.append('')
  #   lines_list.append('endmodule')
  #   lines_list.append('')

  #   return lines_list


  # def return_operator_inst_v_list(self, operator_arg_dict, connection_list, operator_var_dict, operator_width_dict):
  #   out_list = ['module mono(',
  #               '  input         ap_clk,',
  #               '  input         ap_rst_n,',
  #               '  input [511:0]  Input_1_TDATA,',
  #               '  input         Input_1_TVALID,',
  #               '  output        Input_1_TREADY,',
  #               '  output [511:0] Output_1_TDATA,',
  #               '  output        Output_1_TVALID,',
  #               '  input         Output_1_TREADY,',
  #               '  input         ap_start);']
  #   out_list.append('wire [511:0] DMA_Input_1_TDATA;')
  #   out_list.append('wire        DMA_Input_1_TVALID;')
  #   out_list.append('wire        DMA_Input_1_TREADY;')
  #   out_list.append('wire [511:0] DMA_Output_1_TDATA;')
  #   out_list.append('wire        DMA_Output_1_TVALID;')
  #   out_list.append('wire        DMA_Output_1_TREADY;')
 
  #   for op in operator_arg_dict:
  #     for idx, port in enumerate(operator_arg_dict[op]):
  #       width = int(operator_width_dict[op][idx].split('<')[1].split('>')[0])
  #       out_list.append('wire ['+str(width-1)+':0] '+op+'_'+port+'_TDATA;')
  #       out_list.append('wire        '+op+'_'+port+'_TVALID;')
  #       out_list.append('wire        '+op+'_'+port+'_TREADY;')
  #   for idx, connect_str in enumerate(connection_list):
  #     connect_str_list = connect_str.split('->')      
  #     if connect_str_list[1] == 'DMA.Input_1': out_list.append('\nstream_shell #(')
  #     else:                                    out_list.append('\nRelayStation #(')
  #     out_list.append('  .PAYLOAD_BITS('+str(int(connect_str_list[2]))+'),')
  #     out_list.append('  .NUM_BRAM_ADDR_BITS(7)')
  #     out_list.append('  )stream_link_'+str(idx)+'(')
  #     out_list.append('  .clk(ap_clk),')
  #     out_list.append('  .din('+connect_str_list[0].replace('.','_')+'_TDATA),')
  #     out_list.append('  .val_in('+connect_str_list[0].replace('.','_')+'_TVALID),')
  #     out_list.append('  .ready_upward('+connect_str_list[0].replace('.','_')+'_TREADY),')
  #     out_list.append('  .dout('+connect_str_list[1].replace('.','_')+'_TDATA),')
  #     out_list.append('  .val_out('+connect_str_list[1].replace('.','_')+'_TVALID),')
  #     out_list.append('  .ready_downward('+connect_str_list[1].replace('.','_')+'_TREADY),')
  #     out_list.append('  .reset(~ap_rst_n));')
  #   for op in operator_arg_dict:
  #     out_list.append('\n  '+op+' '+op+'_inst(')
  #     out_list.append('    .ap_clk(ap_clk),')
  #     out_list.append('    .ap_start(1\'b1),')
  #     out_list.append('    .ap_done(),')
  #     out_list.append('    .ap_idle(),')
  #     out_list.append('    .ap_ready(),')
  #     for port in operator_arg_dict[op]:
  #       out_list.append('    .'+port+'_TDATA(' +op+'_'+port+'_TDATA),')
  #       out_list.append('    .'+port+'_TVALID('+op+'_'+port+'_TVALID),')
  #       out_list.append('    .'+port+'_TREADY('+op+'_'+port+'_TREADY),')
  #     out_list.append('    .ap_rst_n(ap_rst_n)')
  #     out_list.append('  );')
  #   out_list.append('assign Output_1_TDATA  = DMA_Input_1_TDATA;')
  #   out_list.append('assign Output_1_TVALID = DMA_Input_1_TVALID;')
  #   out_list.append('assign DMA_Input_1_TREADY = Output_1_TREADY;')
  #   out_list.append('assign DMA_Output_1_TDATA  = Input_1_TDATA;')
  #   out_list.append('assign DMA_Output_1_TVALID = Input_1_TVALID;')
  #   out_list.append('assign Input_1_TREADY = DMA_Output_1_TREADY;')
  #   out_list.append('endmodule')
 
  #   return out_list

  def return_hipr_page_v_list(self, 
                              fun_name,
                              operator_arg_list,
                              operator_width_list,
                              addr_width_dict):

    lines_list = []
    lines_list.append('`timescale 1ns / 1ps')
    lines_list.append('module '+fun_name+'_top(')
    lines_list.append('        input  ap_clk,')
    lines_list.append('        input  ap_start,')
    lines_list.append('        output ap_done,')
    lines_list.append('        output ap_idle,')
    lines_list.append('        output ap_ready,')
    for idx, port in enumerate(operator_arg_list): 
      if port.replace('Input','') != port:
        WIDTH = operator_width_list[idx].replace('ap_uint<', '').replace('>', '').replace(' ', '')
        lines_list.append('        input ['+WIDTH+'-1:0] '+port+'_V_TDATA,')
        lines_list.append('        input  '+port+'_V_TVALID,')
        lines_list.append('        output '+port+'_V_TREADY,')
      elif port.replace('Output','') != port:
        WIDTH = operator_width_list[idx].replace('ap_uint<', '').replace('>', '').replace(' ', '')
        lines_list.append('        output ['+WIDTH+'-1:0] '+port+'_V_TDATA,')
        lines_list.append('        output  '+port+'_V_TVALID,')
        lines_list.append('        input  '+port+'_V_TREADY,')
    lines_list.append('        input   ap_rst_n);\n\n')

    for idx, port in enumerate(operator_arg_list): 
      if port.replace('Output','') != port:
        WIDTH = operator_width_list[idx].replace('ap_uint<', '').replace('>', '').replace(' ', '')
        lines_list.append('  wire ['+WIDTH+'-1:0] '+port+'_V_TDATA_tmp;')
        lines_list.append('  wire '+port+'_V_TVALID_tmp;')
        lines_list.append('  wire '+port+'_V_TREADY_tmp;')
 
    lines_list.append('\n\n')

    lines_list.append('  '+fun_name+' '+fun_name+'_inst(')
    lines_list.append('        .ap_clk(ap_clk),')
    lines_list.append('        .ap_start(ap_start),')
    lines_list.append('        .ap_done(ap_done),')
    lines_list.append('        .ap_idle(ap_idle),')
    lines_list.append('        .ap_ready(ap_ready),')
    for idx, port in enumerate(operator_arg_list): 
      if port.replace('Input','') != port:
        lines_list.append('        .'+port+'_V_TDATA('+port+'_V_TDATA),')
        lines_list.append('        .'+port+'_V_TVALID('+port+'_V_TVALID),')
        lines_list.append('        .'+port+'_V_TREADY('+port+'_V_TREADY),')
      elif port.replace('Output','') != port:
        lines_list.append('        .'+port+'_V_TDATA('+port+'_V_TDATA_tmp),')
        lines_list.append('        .'+port+'_V_TVALID('+port+'_V_TVALID_tmp),')
        lines_list.append('        .'+port+'_V_TREADY('+port+'_V_TREADY_tmp),')
    lines_list.append('        .ap_rst_n(ap_rst_n));')
    lines_list.append('\n\n')


    for idx, port in enumerate(operator_arg_list): 
      if port.replace('Output','') != port:
        WIDTH = operator_width_list[idx].replace('ap_uint<', '').replace('>', '').replace(' ', '')
        lines_list.append('  stream_shell #(')
        lines_list.append('         .PAYLOAD_BITS('+WIDTH+'),')
        lines_list.append('         .NUM_BRAM_ADDR_BITS('+addr_width_dict[port]+')')
        lines_list.append('  )stream_link_'+port+'(')
        lines_list.append('         .clk(ap_clk),')
        lines_list.append('         .din('+port+'_V_TDATA_tmp),')
        lines_list.append('         .val_in('+port+'_V_TVALID_tmp),')
        lines_list.append('         .ready_upward('+port+'_V_TREADY_tmp),')
        lines_list.append('         .dout('+port+'_V_TDATA),')
        lines_list.append('         .val_out('+port+'_V_TVALID),')
        lines_list.append('         .ready_downward('+port+'_V_TREADY),')
        lines_list.append('         .reset(~ap_rst_n));\n\n')

    lines_list.append('endmodule')
 
    print (operator_arg_list)
    print (operator_width_list)
    return lines_list


  # Creates verilog file that includes expand/shrink queue + user operator
  # No leaf interface!
  def return_user_kernel_v_list(self, 
                         page_num, 
                         fun_name,
                         input_num,
                         output_num,
                         operator_arg_list,
                         operator_width_list,
                         frequency,
                         for_syn=False,
                         is_riscv=False,
                         PAYLOAD_BITS=None,
                         PACKET_BITS=None,
                         NUM_LEAF_BITS=None,
                         NUM_PORT_BITS=None,
                         NUM_ADDR_BITS=None,
                         NUM_BRAM_ADDR_BITS=None,
                         FREESPACE_UPDATE_SIZE=None
                         ):
    PAYLOAD_BITS=self.prflow_params['payload_bits'] if PAYLOAD_BITS == None else PAYLOAD_BITS
    PACKET_BITS=self.prflow_params['packet_bits'] if PACKET_BITS == None else PACKET_BITS
    NUM_LEAF_BITS=self.prflow_params['addr_bits'] if NUM_LEAF_BITS == None  else NUM_LEAF_BITS
    NUM_PORT_BITS=self.prflow_params['port_bits'] if NUM_PORT_BITS == None  else NUM_PORT_BITS
    NUM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_ADDR_BITS == None else NUM_ADDR_BITS
    NUM_BRAM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_BRAM_ADDR_BITS == None else NUM_BRAM_ADDR_BITS
    FREESPACE_UPDATE_SIZE=self.prflow_params['freespace'] if FREESPACE_UPDATE_SIZE == None  else FREESPACE_UPDATE_SIZE
 
    lines_list = []
    lines_list.append('`timescale 1ns / 1ps')
    if for_syn:
      lines_list.append('module user_kernel(')
    else:
      lines_list.append('module user_kernel_'+str(page_num)+'(')

    lines_list.append('    input wire clk_user,')
    lines_list.append('    input wire reset,')
    for i in range(input_num,0,-1):
      lines_list.append('    input wire [32-1:0] dout_leaf_interface2user_' + str(i) + ',')
    for i in range(input_num,0,-1):
      lines_list.append("    input wire vld_interface2user_" + str(i) +  ",")
    for i in range(input_num,0,-1):
      lines_list.append("    output wire ack_user2interface_" + str(i) +  ",")
    lines_list.append('')

    for i in range(output_num,0,-1):
      lines_list.append("    output wire [32-1:0] din_leaf_user2interface_" + str(i) + ",")
    for i in range(output_num,0,-1):
      lines_list.append("    output wire vld_user2interface_" + str(i) +  ",")
    for i in range(output_num,0,-1):
      if i == 1:
        lines_list.append("    input wire ack_interface2user_" + str(i) +  "")
      else:
        lines_list.append("    input wire ack_interface2user_" + str(i) +  ",")
    lines_list.append('    );')
     
    # interface -> user, wire declaration
    for i in range(self.my_max(1, int(input_num)),0,-1): 
      if int(input_num) != 0:
        WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Input_'+str(i))].split('<')[1].split('>')[0]
      else:
        WIDTH = 32
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] dout_leaf_interface2user_'+str(i)+'_user;')
      lines_list.append('    wire vld_interface2user_'+str(i)+'_user;')
      lines_list.append('    wire ack_user2interface_'+str(i)+'_user;')
 
    # user -> interface, wire declaration
    din_list = []
    val_in_list = [] 
    ack_in_list = []
    for i in range(int(output_num),0,-1): 
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Output_'+str(i))].split('<')[1].split('>')[0]
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] din_leaf_user2interface_'+str(i)+'_user;')
      lines_list.append('    wire vld_user2interface_'+str(i)+'_user;')
      lines_list.append('    wire ack_interface2user_'+str(i)+'_user;')
    lines_list.append('')

    if int(input_num) == 0: lines_list.append('    assign ack_user2interface_1_user = 0;')

    # interface -> user, width matching
    for i in range(self.my_max(1, int(input_num)),0,-1): 
      if int(input_num) != 0:
        WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Input_'+str(i))].split('<')[1].split('>')[0]
      else:
        WIDTH = 32
 
      if int(WIDTH) > 32 and (int(WIDTH) % 32 == 0) and is_riscv == False: # multiple of 32
         lines_list.append('    expand_queue_fifo#(')
         lines_list.append('      .IN_WIDTH(32),')
         lines_list.append('      .OUT_WIDTH('+str(WIDTH)+')')
         lines_list.append('    )Input_'+str(i)+'_converter(')
         lines_list.append('      .clk(clk_user),')
         lines_list.append('      .reset(reset),')
         lines_list.append('      .d_a(dout_leaf_interface2user_'+str(i)+'),')
         lines_list.append('      .vld_a(vld_interface2user_'+str(i)+'),')
         lines_list.append('      .rdy_a(ack_user2interface_'+str(i)+'),')

         lines_list.append('      .d_b(dout_leaf_interface2user_'+str(i)+'_user),')
         lines_list.append('      .vld_b(vld_interface2user_'+str(i)+'_user),')
         lines_list.append('      .rdy_b(ack_user2interface_'+str(i)+'_user)')
         lines_list.append('    );')
      elif int(WIDTH) < 32 and (32 % int(WIDTH) == 0) and is_riscv == False: # divisor of 32
         lines_list.append('    shrink_queue_fifo#(')
         lines_list.append('      .IN_WIDTH(32),')
         lines_list.append('      .OUT_WIDTH('+str(WIDTH)+')')
         lines_list.append('    )Input_'+str(i)+'_converter(')
         lines_list.append('      .clk(clk_user),')
         lines_list.append('      .reset(reset),')
         lines_list.append('      .d_a(dout_leaf_interface2user_'+str(i)+'),')
         lines_list.append('      .vld_a(vld_interface2user_'+str(i)+'),')
         lines_list.append('      .rdy_a(ack_user2interface_'+str(i)+'),')

         lines_list.append('      .d_b(dout_leaf_interface2user_'+str(i)+'_user),')
         lines_list.append('      .vld_b(vld_interface2user_'+str(i)+'_user),')
         lines_list.append('      .rdy_b(ack_user2interface_'+str(i)+'_user)')
         lines_list.append('    );')
      else:
         lines_list.append('    assign dout_leaf_interface2user_'+str(i)+'_user = dout_leaf_interface2user_'+str(i)+';')
         lines_list.append('    assign vld_interface2user_'+str(i)+'_user = vld_interface2user_'+str(i)+';')
         lines_list.append('    assign ack_user2interface_'+str(i)+' = ack_user2interface_'+str(i)+'_user;')
      lines_list.append('')

    # user -> interface, width matching
    for i in range(int(output_num),0,-1): 
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Output_'+str(i))].split('<')[1].split('>')[0]

      if int(WIDTH) > 32 and (int(WIDTH) % 32 == 0) and is_riscv == False: # multiple of 32
         lines_list.append('    shrink_queue_fifo#(')
         lines_list.append('      .IN_WIDTH('+str(WIDTH)+'),')
         lines_list.append('      .OUT_WIDTH(32)')
         lines_list.append('    )Output_'+str(i)+'_converter(')
         lines_list.append('      .clk(clk_user),')
         lines_list.append('      .reset(reset),')
         lines_list.append('      .d_a(din_leaf_user2interface_'+str(i)+'_user),')
         lines_list.append('      .vld_a(vld_user2interface_'+str(i)+'_user),')
         lines_list.append('      .rdy_a(ack_interface2user_'+str(i)+'_user),') 
         lines_list.append('      .d_b(din_leaf_user2interface_'+str(i)+'),')
         lines_list.append('      .vld_b(vld_user2interface_'+str(i)+'),')
         lines_list.append('      .rdy_b(ack_interface2user_'+str(i)+')')
         lines_list.append('    );')
      elif int(WIDTH) < 32 and (32 % int(WIDTH) == 0) and is_riscv == False: # divisor of 32
         lines_list.append('    expand_queue_fifo#(')
         lines_list.append('      .IN_WIDTH('+str(WIDTH)+'),')
         lines_list.append('      .OUT_WIDTH(32)')
         lines_list.append('    )Output_'+str(i)+'_converter(')
         lines_list.append('      .clk(clk_user),')
         lines_list.append('      .reset(reset),')
         lines_list.append('      .d_a(din_leaf_user2interface_'+str(i)+'_user),')
         lines_list.append('      .vld_a(vld_user2interface_'+str(i)+'_user),')
         lines_list.append('      .rdy_a(ack_interface2user_'+str(i)+'_user),') 
         lines_list.append('      .d_b(din_leaf_user2interface_'+str(i)+'),')
         lines_list.append('      .vld_b(vld_user2interface_'+str(i)+'),')
         lines_list.append('      .rdy_b(ack_interface2user_'+str(i)+')')
         lines_list.append('    );')
      else:
         lines_list.append('    assign din_leaf_user2interface_'+str(i)+' = din_leaf_user2interface_'+str(i)+'_user;')
         lines_list.append('    assign vld_user2interface_'+str(i)+' = vld_user2interface_'+str(i)+'_user;')
         lines_list.append('    assign ack_interface2user_'+str(i)+'_user = ack_interface2user_'+str(i)+';')
      lines_list.append('')

    # user operator declaration
    lines_list.append('    '+fun_name+' '+fun_name+'_inst(')
    lines_list.append('        .ap_clk(clk_user),')
    lines_list.append('        .ap_start(1\'b1), // this should be fine')
    lines_list.append('        .ap_done(),')
    lines_list.append('        .ap_idle(),')
    lines_list.append('        .ap_ready(),')
    for i in range(int(input_num),0,-1): 
      lines_list.append('        .Input_'+str(i)+'_TDATA(dout_leaf_interface2user_'+str(i)+'_user),')
      lines_list.append('        .Input_'+str(i)+'_TVALID(vld_interface2user_'+str(i)+'_user),')
      lines_list.append('        .Input_'+str(i)+'_TREADY(ack_user2interface_'+str(i)+'_user),')
    for i in range(int(output_num),0,-1): 
      lines_list.append('        .Output_'+str(i)+'_TDATA(din_leaf_user2interface_'+str(i)+'_user),')
      lines_list.append('        .Output_'+str(i)+'_TVALID(vld_user2interface_'+str(i)+'_user),')
      lines_list.append('        .Output_'+str(i)+'_TREADY(ack_interface2user_'+str(i)+'_user),')
    lines_list.append('        .ap_rst_n(~reset)')
    lines_list.append('        );  ')
    lines_list.append('    ')
    lines_list.append('endmodule')

    return lines_list


  # creates verilog file that includes leaf interface + expand/shrink queue + user operator
  # Highly redundant with return_single_page_v_list
  def return_non_single_page_v_list(self, 
                         page_num, 
                         fun_name,
                         input_num,
                         output_num,
                         operator_arg_list,
                         operator_width_list,
                         frequency,
                         num_leaf_interface,
                         leaf_interface_mapping_dict,
                         for_syn=False,
                         is_riscv=False,
                         PAYLOAD_BITS=None,
                         PACKET_BITS=None,
                         NUM_LEAF_BITS=None,
                         NUM_PORT_BITS=None,
                         NUM_ADDR_BITS=None,
                         NUM_BRAM_ADDR_BITS=None,
                         FREESPACE_UPDATE_SIZE=None
                         ):
    PAYLOAD_BITS=self.prflow_params['payload_bits'] if PAYLOAD_BITS == None else PAYLOAD_BITS
    PACKET_BITS=self.prflow_params['packet_bits'] if PACKET_BITS == None else PACKET_BITS
    NUM_LEAF_BITS=self.prflow_params['addr_bits'] if NUM_LEAF_BITS == None  else NUM_LEAF_BITS
    NUM_PORT_BITS=self.prflow_params['port_bits'] if NUM_PORT_BITS == None  else NUM_PORT_BITS
    NUM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_ADDR_BITS == None else NUM_ADDR_BITS
    NUM_BRAM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_BRAM_ADDR_BITS == None else NUM_BRAM_ADDR_BITS
    FREESPACE_UPDATE_SIZE=self.prflow_params['freespace'] if FREESPACE_UPDATE_SIZE == None  else FREESPACE_UPDATE_SIZE

    lines_list = []
    lines_list.append('`timescale 1ns / 1ps')
    if for_syn:
      lines_list.append('module leaf(')
    else:
      lines_list.append('module leaf_'+str(page_num)+'(')

    for j in range(num_leaf_interface):
      lines_list.append('    input wire clk_200_' + str(j) + ',')
      lines_list.append('    input wire clk_250_' + str(j) + ',')
      lines_list.append('    input wire clk_300_' + str(j) + ',')
      lines_list.append('    input wire clk_350_' + str(j) + ',')
      lines_list.append('    input wire clk_400_' + str(j) + ',')
      lines_list.append('    input wire ['+str(PACKET_BITS)+'-1 : 0] din_leaf_bft2interface_' + str(j) + ',')
      lines_list.append('    output wire ['+str(PACKET_BITS)+'-1 : 0] dout_leaf_interface2bft_' + str(j) + ',')
      lines_list.append('    input wire resend_' + str(j) + ',')
      lines_list.append('    input wire reset_400_' + str(j) + ',')
      if j == num_leaf_interface-1:
        lines_list.append('    input wire ap_start_' + str(j))
      else:
        lines_list.append('    input wire ap_start_' + str(j) + ',')
    lines_list.append('    );')
    lines_list.append('')
     
    DATA_USER_IN_TOTAL_dict, DATA_USER_OUT_TOTAL_dict = {}, {} # per leaf interface

    # interface -> user, wire declaration
    dout_str_dict, val_out_str_dict, ack_out_str_dict = {}, {}, {}
    dout_list_dict, val_out_list_dict, ack_out_list_dict = {}, {}, {}
    for j in range(num_leaf_interface):
      dout_list_dict[j], val_out_list_dict[j], ack_out_list_dict[j] = [], [], []
      DATA_USER_IN_TOTAL_dict[j] = 0

    for i in range(self.my_max(1, int(input_num)),0,-1): # descending.. e.g. 3, 2, 1, 0
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Input_'+str(i))].split('<')[1].split('>')[0]
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] dout_leaf_interface2user_'+str(i)+';')
      lines_list.append('    wire vld_interface2user_'+str(i)+';')
      lines_list.append('    wire ack_user2interface_'+str(i)+';')

      for j in range(num_leaf_interface):
        mapped_IO_ports = leaf_interface_mapping_dict[j]
        if 'Input_' + str(i) in mapped_IO_ports:
          dout_list_dict[j].append('dout_leaf_interface2user_'+str(i))
          val_out_list_dict[j].append('vld_interface2user_'+str(i))
          ack_out_list_dict[j].append('ack_user2interface_'+str(i))
          DATA_USER_IN_TOTAL_dict[j] += int(WIDTH)


    for j in range(num_leaf_interface):
      if len(dout_list_dict[j]) == 0: dout_str_dict[j] = ''
      else: dout_str_dict[j] = '{'+','.join(dout_list_dict[j])+'}'
      
      if len(val_out_list_dict[j]) == 0: val_out_str_dict[j] = ''
      else: val_out_str_dict[j] = '{'+','.join(val_out_list_dict[j])+'}'

      if len(ack_out_list_dict[j]) == 0: ack_out_str_dict[j] = ''
      else: ack_out_str_dict[j] = '{'+','.join(ack_out_list_dict[j])+'}'


    # user -> interface, wire declaration
    din_str_dict, val_in_str_dict, ack_in_str_dict = {}, {}, {}
    din_list_dict, val_in_list_dict, ack_in_list_dict = {}, {}, {}
    for j in range(num_leaf_interface):
      din_list_dict[j], val_in_list_dict[j], ack_in_list_dict[j] = [], [], []
      DATA_USER_OUT_TOTAL_dict[j] = 0

    for i in range(int(output_num),0,-1): # descending.. e.g. 3, 2, 1, 0
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Output_'+str(i))].split('<')[1].split('>')[0]
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] din_leaf_user2interface_'+str(i)+';')
      lines_list.append('    wire vld_user2interface_'+str(i)+';')
      lines_list.append('    wire ack_interface2user_'+str(i)+';')

      for j in range(num_leaf_interface):
        mapped_IO_ports = leaf_interface_mapping_dict[j]
        if 'Output_' + str(i) in mapped_IO_ports:        
          din_list_dict[j].append('din_leaf_user2interface_'+str(i))
          val_in_list_dict[j].append('vld_user2interface_'+str(i))
          ack_in_list_dict[j].append('ack_interface2user_'+str(i))
          DATA_USER_OUT_TOTAL_dict[j] += int(WIDTH)

    for j in range(num_leaf_interface):
      if len(din_list_dict[j]) == 0: din_str_dict[j] = ''
      else: din_str_dict[j] = '{'+','.join(din_list_dict[j])+'}'

      if len(val_in_list_dict[j]) == 0: val_in_str_dict[j] = ''
      else: val_in_str_dict[j] = '{'+','.join(val_in_list_dict[j])+'}'

      if len(ack_in_list_dict[j]) == 0: ack_in_str_dict[j] = ''
      else: ack_in_str_dict[j] = '{'+','.join(ack_in_list_dict[j])+'}'


    lines_list.append('    wire clk_user;')
    lines_list.append('    assign clk_user = clk_' + str(frequency) + '_0;')

    for j in range(num_leaf_interface):
      lines_list.append('    wire reset_ap_start_user_' + str(j) + ';')
      lines_list.append('    wire input_port_cluster_stall_condition_others_' + str(j) + ';')
      lines_list.append('    wire output_port_cluster_stall_condition_others_' + str(j) + ';')
      lines_list.append('    wire input_port_cluster_stall_condition_self_' + str(j) + ';')
      lines_list.append('    wire output_port_cluster_stall_condition_self_' + str(j) + ';')

    for j in range(num_leaf_interface):
      mapped_IO_ports = leaf_interface_mapping_dict[j]
      # In leaf interface implementation, NUM_IN_PORTS and NUM_OUT_PORTS are > 0
      num_mapped_I_ports = max(1,len([port for port in mapped_IO_ports if port.startswith('Input_')]))
      num_mapped_O_ports = max(1,len([port for port in mapped_IO_ports if port.startswith('Output_')]))

      lines_list.append('')
      lines_list.append('    wire [48:0] dout_leaf_interface2bft_tmp_' + str(j) + ';')
      lines_list.append('    assign dout_leaf_interface2bft_' + str(j) + ' = resend_' + str(j) + ' ? 0 : dout_leaf_interface2bft_tmp_' + str(j) + ';')
      lines_list.append('    ')
      lines_list.append('    leaf_interface_' + str(j) + ' #(')
      lines_list.append('        .PACKET_BITS('+str(PACKET_BITS)+'),')
      lines_list.append('        .PAYLOAD_BITS('+str(PAYLOAD_BITS)+'),')
      lines_list.append('        .NUM_LEAF_BITS('+str(NUM_LEAF_BITS)+'),')
      lines_list.append('        .NUM_PORT_BITS('+str(NUM_PORT_BITS)+'),')
      lines_list.append('        .NUM_ADDR_BITS('+str(NUM_ADDR_BITS)+'),')
      lines_list.append('        .NUM_IN_PORTS('+str(num_mapped_I_ports)+'),')
      lines_list.append('        .NUM_OUT_PORTS('+str(num_mapped_O_ports)+'),')
      lines_list.append('        .NUM_BRAM_ADDR_BITS('+str(NUM_BRAM_ADDR_BITS)+'),')
      lines_list.append('        .FREESPACE_UPDATE_SIZE('+str(FREESPACE_UPDATE_SIZE)+'),')
      if j == 0:
        lines_list.append('        .STALL_CNT(1),')
      else:
        lines_list.append('        .STALL_CNT(0), // no stall counter')

      if DATA_USER_IN_TOTAL_dict[j] == 0:
        lines_list.append('        .DATA_USER_IN_TOTAL(32),')
      else:
        lines_list.append('        .DATA_USER_IN_TOTAL(' + str(DATA_USER_IN_TOTAL_dict[j]) + '),')
      if DATA_USER_OUT_TOTAL_dict[j] == 0:
        lines_list.append('        .DATA_USER_OUT_TOTAL(32)')
      else:
        lines_list.append('        .DATA_USER_OUT_TOTAL(' + str(DATA_USER_OUT_TOTAL_dict[j]) + ')')
      lines_list.append('    )leaf_interface_' + str(j) + '_inst(')
      lines_list.append('        .clk(clk_400_0), // use first port') # clk_bft is fixed to max freq, which is 400MHz
      lines_list.append('        .clk_user(clk_user), // common')
      lines_list.append('        .reset(reset_400_0), // use first port') # clk_bft is fixed to max freq, which is 400MHz
      lines_list.append('        .din_leaf_bft2interface(din_leaf_bft2interface_' + str(j) + '),')
      lines_list.append('        .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp_' + str(j) + '),')
      lines_list.append('        .ap_start_user(), // not used') 
      lines_list.append('        .resend(resend_' + str(j) + '),')
      lines_list.append('        .dout_leaf_interface2user('+dout_str_dict[j]+'),')
      lines_list.append('        .vld_interface2user('+val_out_str_dict[j]+'),')
      if ack_out_str_dict[j] == '': lines_list.append('        .ack_user2interface(0), // prevents stall cnt condition from being x')
      else: lines_list.append('        .ack_user2interface('+ack_out_str_dict[j]+'),')
      lines_list.append('        .ack_interface2user('+ack_in_str_dict[j]+'),')
      if val_in_str_dict[j] == '': lines_list.append('        .vld_user2interface(0), // prevents stall cnt condition from being x')
      else: lines_list.append('        .vld_user2interface('+val_in_str_dict[j]+'),')
      lines_list.append('        .din_leaf_user2interface('+din_str_dict[j]+'),')
      lines_list.append('        .ap_start(ap_start_' + str(j) + '),')
      lines_list.append('        .reset_ap_start_user(reset_ap_start_user_' + str(j) + '),')
      if j == 0:
        lines_list.append('        .input_port_cluster_stall_condition_others(input_port_cluster_stall_condition_others_0),')
        lines_list.append('        .output_port_cluster_stall_condition_others(output_port_cluster_stall_condition_others_0),')
        lines_list.append('        .input_port_cluster_stall_condition_self(),')
        lines_list.append('        .output_port_cluster_stall_condition_self()')
      else:
        lines_list.append('        .input_port_cluster_stall_condition_others(),')
        lines_list.append('        .output_port_cluster_stall_condition_others(),')
        lines_list.append('        .input_port_cluster_stall_condition_self(input_port_cluster_stall_condition_self_' + str(j) + '),')
        lines_list.append('        .output_port_cluster_stall_condition_self(output_port_cluster_stall_condition_self_' + str(j) + ')')
      lines_list.append('    );')
      lines_list.append('')

    str_input_stall_condition = '    assign input_port_cluster_stall_condition_others_0 = '
    str_output_stall_condition = '    assign output_port_cluster_stall_condition_others_0 = '
    for j in range(num_leaf_interface):
      if j!=0 and j != num_leaf_interface-1:
        str_input_stall_condition += 'input_port_cluster_stall_condition_self_' + str(j) + ' || '
        str_output_stall_condition += 'output_port_cluster_stall_condition_self_' + str(j) + ' || '
      elif j:
        str_input_stall_condition += 'input_port_cluster_stall_condition_self_' + str(j) + ';'
        str_output_stall_condition += 'output_port_cluster_stall_condition_self_' + str(j) + ';'
    lines_list.append(str_input_stall_condition)
    lines_list.append(str_output_stall_condition)
    lines_list.append('')

    lines_list.append('    '+fun_name+' '+fun_name+'_inst(')
    lines_list.append('        .ap_clk(clk_user),')
    # lines_list.append('        .ap_start(ap_start_user),')
    lines_list.append('        .ap_start(1\'b1), // this should be fine')
    lines_list.append('        .ap_done(),')
    lines_list.append('        .ap_idle(),')
    lines_list.append('        .ap_ready(),')
    for i in range(int(input_num),0,-1): 
      lines_list.append('        .Input_'+str(i)+'_TDATA(dout_leaf_interface2user_'+str(i)+'),')
      lines_list.append('        .Input_'+str(i)+'_TVALID(vld_interface2user_'+str(i)+'),')
      lines_list.append('        .Input_'+str(i)+'_TREADY(ack_user2interface_'+str(i)+'),')
    for i in range(int(output_num),0,-1): 
      lines_list.append('        .Output_'+str(i)+'_TDATA(din_leaf_user2interface_'+str(i)+'),')
      lines_list.append('        .Output_'+str(i)+'_TVALID(vld_user2interface_'+str(i)+'),')
      lines_list.append('        .Output_'+str(i)+'_TREADY(ack_interface2user_'+str(i)+'),')
    # lines_list.append('        .ap_rst_n(~new_reset)')
    lines_list.append('        .ap_rst_n(~reset_ap_start_user_0)')
    lines_list.append('        );  ')
    lines_list.append('')
    lines_list.append('endmodule')

    return lines_list


  # creates verilog file that includes leaf interface + user operator
  def return_single_page_v_list(self, 
                         page_num, 
                         fun_name,
                         input_num,
                         output_num,
                         operator_arg_list,
                         operator_width_list,
                         frequency,
                         for_syn=False,
                         is_riscv=False,
                         PAYLOAD_BITS=None,
                         PACKET_BITS=None,
                         NUM_LEAF_BITS=None,
                         NUM_PORT_BITS=None,
                         NUM_ADDR_BITS=None,
                         NUM_BRAM_ADDR_BITS=None,
                         FREESPACE_UPDATE_SIZE=None
                         ):
    PAYLOAD_BITS=self.prflow_params['payload_bits'] if PAYLOAD_BITS == None else PAYLOAD_BITS
    PACKET_BITS=self.prflow_params['packet_bits'] if PACKET_BITS == None else PACKET_BITS
    NUM_LEAF_BITS=self.prflow_params['addr_bits'] if NUM_LEAF_BITS == None  else NUM_LEAF_BITS
    NUM_PORT_BITS=self.prflow_params['port_bits'] if NUM_PORT_BITS == None  else NUM_PORT_BITS
    NUM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_ADDR_BITS == None else NUM_ADDR_BITS
    NUM_BRAM_ADDR_BITS=self.prflow_params['bram_addr_bits'] if NUM_BRAM_ADDR_BITS == None else NUM_BRAM_ADDR_BITS
    FREESPACE_UPDATE_SIZE=self.prflow_params['freespace'] if FREESPACE_UPDATE_SIZE == None  else FREESPACE_UPDATE_SIZE

    lines_list = []
    lines_list.append('`timescale 1ns / 1ps')
    if for_syn:
      lines_list.append('module leaf(')
    else:
      lines_list.append('module leaf_'+str(page_num)+'(')

    lines_list.append('    input wire clk_200,')
    lines_list.append('    input wire clk_250,')
    lines_list.append('    input wire clk_300,')
    lines_list.append('    input wire clk_350,')
    lines_list.append('    input wire clk_400,')
    lines_list.append('    input wire ['+str(PACKET_BITS)+'-1 : 0] din_leaf_bft2interface,')
    lines_list.append('    output wire ['+str(PACKET_BITS)+'-1 : 0] dout_leaf_interface2bft,')
    lines_list.append('    input wire resend,')
    lines_list.append('    input wire reset_400,')
    lines_list.append('    input wire ap_start')
    lines_list.append('    );')
    lines_list.append('')
    # lines_list.append('    wire ap_start_user;')

    # interface -> user, wire declaration
    dout_list, val_out_list, ack_out_list = [], [], []
    DATA_USER_IN_TOTAL = 0
    for i in range(self.my_max(1, int(input_num)),0,-1): # descending.. e.g. 3, 2, 1, 0
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Input_'+str(i))].split('<')[1].split('>')[0]
      DATA_USER_IN_TOTAL += int(WIDTH)
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] dout_leaf_interface2user_'+str(i)+';')
      lines_list.append('    wire vld_interface2user_'+str(i)+';')
      lines_list.append('    wire ack_user2interface_'+str(i)+';')
      dout_list.append('dout_leaf_interface2user_'+str(i))
      val_out_list.append('vld_interface2user_'+str(i))
      ack_out_list.append('ack_user2interface_'+str(i))
    dout_str='{'+','.join(dout_list)+'}'
    val_out_str='{'+','.join(val_out_list)+'}'
    ack_out_str='{'+','.join(ack_out_list)+'}'

    # user -> interface, wire declaration
    din_list, val_in_list, ack_in_list = [], [], []
    DATA_USER_OUT_TOTAL = 0
    for i in range(int(output_num),0,-1): # descending.. e.g. 3, 2, 1, 0
      WIDTH = operator_width_list[self.return_idx_in_list_local(operator_arg_list, 'Output_'+str(i))].split('<')[1].split('>')[0]
      DATA_USER_OUT_TOTAL += int(WIDTH)
      lines_list.append('    wire ['+str(WIDTH)+'-1 :0] din_leaf_user2interface_'+str(i)+';')
      lines_list.append('    wire vld_user2interface_'+str(i)+';')
      lines_list.append('    wire ack_interface2user_'+str(i)+';')
      din_list.append('din_leaf_user2interface_'+str(i))
      val_in_list.append('vld_user2interface_'+str(i))
      ack_in_list.append('ack_interface2user_'+str(i))
    din_str='{'+','.join(din_list)+'}'
    val_in_str='{'+','.join(val_in_list)+'}'
    ack_in_str='{'+','.join(ack_in_list)+'}'

    lines_list.append('    wire clk_user;')
    lines_list.append('    assign clk_user = clk_' + str(frequency) +';')
    lines_list.append('    wire reset_ap_start_user;')
    lines_list.append('    ')
    lines_list.append('    wire [48:0] dout_leaf_interface2bft_tmp;')
    lines_list.append('    assign dout_leaf_interface2bft = resend ? 0 : dout_leaf_interface2bft_tmp;')
    lines_list.append('    ')
    lines_list.append('    leaf_interface_0 #(')
    lines_list.append('        .PACKET_BITS('+str(PACKET_BITS)+'),')
    lines_list.append('        .PAYLOAD_BITS('+str(PAYLOAD_BITS)+'),')
    lines_list.append('        .NUM_LEAF_BITS('+str(NUM_LEAF_BITS)+'),')
    lines_list.append('        .NUM_PORT_BITS('+str(NUM_PORT_BITS)+'),')
    lines_list.append('        .NUM_ADDR_BITS('+str(NUM_ADDR_BITS)+'),')
    lines_list.append('        .NUM_IN_PORTS('+str(self.my_max(1, input_num))+'),')
    lines_list.append('        .NUM_OUT_PORTS('+str(output_num)+'),')
    lines_list.append('        .NUM_BRAM_ADDR_BITS('+str(NUM_BRAM_ADDR_BITS)+'),')
    lines_list.append('        .FREESPACE_UPDATE_SIZE('+str(FREESPACE_UPDATE_SIZE)+'),')
    lines_list.append('        .STALL_CNT(1),')
    lines_list.append('        .DATA_USER_IN_TOTAL(' + str(DATA_USER_IN_TOTAL) + '),')
    lines_list.append('        .DATA_USER_OUT_TOTAL(' + str(DATA_USER_OUT_TOTAL) + ')')
    lines_list.append('    )leaf_interface_0_inst(')
    lines_list.append('        .clk(clk_400),') # clk_bft is fixed to max freq, which is 400MHz
    lines_list.append('        .clk_user(clk_user),')
    lines_list.append('        .reset(reset_400),') # clk_bft is fixed to max freq, which is 400MHz
    # lines_list.append('        .reset_user(reset_user),') # use reset_ap_start_user instead
    lines_list.append('        .din_leaf_bft2interface(din_leaf_bft2interface),')
    lines_list.append('        .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp),')
    # lines_list.append('        .riscv_addr(riscv_addr),')
    # lines_list.append('        .riscv_dout(riscv_dout),')
    # lines_list.append('        .instr_wr_en_out(instr_wr_en_out),') 
    lines_list.append('        .ap_start_user(), // not used') 
    # lines_list.append('        .ap_start_user(1),') 
    lines_list.append('        .resend(resend),')
    lines_list.append('        .dout_leaf_interface2user('+dout_str+'),')
    lines_list.append('        .vld_interface2user('+val_out_str+'),')
    lines_list.append('        .ack_user2interface('+ack_out_str+'),')
    lines_list.append('        .ack_interface2user('+ack_in_str+'),')
    lines_list.append('        .vld_user2interface('+val_in_str+'),')
    lines_list.append('        .din_leaf_user2interface('+din_str+'),')
    lines_list.append('        .ap_start(ap_start),')
    lines_list.append('        .reset_ap_start_user(reset_ap_start_user),')
    lines_list.append('        .input_port_cluster_stall_condition_others(0),')
    lines_list.append('        .output_port_cluster_stall_condition_others(0),')
    lines_list.append('        .input_port_cluster_stall_condition_self(),')
    lines_list.append('        .output_port_cluster_stall_condition_self()')
    lines_list.append('    );')
    lines_list.append('    ')

    if is_riscv == False:
      lines_list.append('    '+fun_name+' '+fun_name+'_inst(')
      lines_list.append('        .ap_clk(clk_user),')
      # lines_list.append('        .ap_start(ap_start_user),')
      lines_list.append('        .ap_start(1\'b1), // this should be fine')
      lines_list.append('        .ap_done(),')
      lines_list.append('        .ap_idle(),')
      lines_list.append('        .ap_ready(),')
      for i in range(int(input_num),0,-1): 
        lines_list.append('        .Input_'+str(i)+'_TDATA(dout_leaf_interface2user_'+str(i)+'),')
        lines_list.append('        .Input_'+str(i)+'_TVALID(vld_interface2user_'+str(i)+'),')
        lines_list.append('        .Input_'+str(i)+'_TREADY(ack_user2interface_'+str(i)+'),')
      for i in range(int(output_num),0,-1): 
        lines_list.append('        .Output_'+str(i)+'_TDATA(din_leaf_user2interface_'+str(i)+'),')
        lines_list.append('        .Output_'+str(i)+'_TVALID(vld_user2interface_'+str(i)+'),')
        lines_list.append('        .Output_'+str(i)+'_TREADY(ack_interface2user_'+str(i)+'),')
      # lines_list.append('        .ap_rst_n(~new_reset)')
      lines_list.append('        .ap_rst_n(~reset_ap_start_user)')
      lines_list.append('        );  ')
    lines_list.append('    ')
    lines_list.append('endmodule')

    return lines_list




class _dataflow:
  def __init__(self, prflow_params):
    self.prflow_params = prflow_params
    self.shell         = _shell(prflow_params)
    self.pragma        = _pragma(prflow_params)

  def return_io_width(self, operator_width_list, operator_arg_list):
    input_width_list = []
    output_width_list = []
    for idx, key in enumerate(operator_arg_list):
      if ('Input' in key): input_width_list.append (int(operator_width_list[idx].split('<')[1].split('>')[0]))
      if ('Output' in key): output_width_list.append(int(operator_width_list[idx].split('<')[1].split('>')[0]))
    return input_width_list, output_width_list 

  # find all the operators arguments order
  # in case the user define the input and output arguments out of order 
  def return_operator_io_argument_dict(self, operators):
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
        if ('(' in line): def_valid = True
        if def_valid: 
          line_str=re.sub('\s+', '', line)
          line_str=re.sub('\t+', '', line_str)
          def_str=def_str+line_str
        if (')' in line): def_valid = False

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
  def return_operator_inst_dict(self, operators):
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
        if (operator+'(' in line): inst_cnt = inst_cnt + 1
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

  def return_operator_connect_list(self, operator_arg_dict, operator_var_dict, operator_width_dict):
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
          tmp_str='DMA.Output_1->'+key_a+'.Input_1->512' 
          connection_list.append(tmp_str)
        if var_value_a == 'Input_2': 
          tmp_str='DMA2.Output_1->'+key_a+'.Input_1->512' 
          connection_list.append(tmp_str)
        if var_value_a == 'Output_1': 
          tmp_str=key_a+'.Output_1->'+'DMA.Input_1->512'
          connection_list.append(tmp_str)
        for key_b in operator_var_dict:
          for i_b, var_value_b in enumerate(operator_var_dict[key_b]):
            if var_value_a==var_value_b and key_a!=key_b:
              if ('Input' in operator_arg_dict[key_a][i_a]):
                tmp_str = operator_width_dict[key_b][i_b].replace('>','')
                tmp_str = tmp_str.replace('ap_uint<','->')
                tmp_str = key_b+'.'+operator_arg_dict[key_b][i_b]+'->'+key_a+'.'+operator_arg_dict[key_a][i_a]+tmp_str
              else:
                tmp_str = operator_width_dict[key_b][i_b].replace('>','')
                tmp_str = tmp_str.replace('ap_uint<','->')
                tmp_str = key_a+'.'+operator_arg_dict[key_a][i_a]+'->'+key_b+'.'+operator_arg_dict[key_b][i_b]+tmp_str
              connection_list.append(tmp_str)

    #connection_list = []
    #connection_list.append('DEBUG.Output_1->add1.Input_1')
    #connection_list.append('add1.Output_1->DEBUG.Input_1')
    #connection_list.append('add1.Output_2->DEBUG.Input_3')
    #connection_list.append('add1.Output_3->DEBUG.Input_3')
    #connection_list.append('add1.Output_5->DEBUG.Input_5')
    connection_list = set(connection_list)
    return connection_list



  


class _tcl:
  def __init__(self, prflow_params):
    self.prflow_params = prflow_params

  def return_delete_bd_objs_tcl_str(self, obj_name):
    return('delete_bd_objs  [get_bd_cells '+obj_name+']')

  def return_change_parameter_tcl_str(self, cell_name, par_name, par_value):
    return('set_property -dict [list CONFIG.'+par_name+' {'+str(par_value)+'}] [get_bd_cells '+cell_name+']')

  def return_connect_bd_net_tcl_str(self, src_pin, dest_pin):
    return('connect_bd_net [get_bd_pins '+src_pin + '] [get_bd_pins '+dest_pin+']')

  def return_create_bd_cell_tcl_str(self, obj_name, inst_name, obj_type='ip'):
    return('create_bd_cell -type '+obj_type+' -vlnv '+obj_name+' ' + inst_name)

  def return_connect_bd_stream_tcl_list(self, src_name, dest_name, src_port_name='', dest_port_name=''):
    return([
      'connect_bd_net [get_bd_pins /'+src_name+'/'+src_port_name+'dout] [get_bd_pins /'+dest_name+'/'+dest_port_name+'din]',
      'connect_bd_net [get_bd_pins /'+src_name+'/'+src_port_name+'val_out] [get_bd_pins /'+dest_name+'/'+dest_port_name+'val_in]',
      'connect_bd_net [get_bd_pins /'+src_name+'/'+src_port_name+'ready_upward] [get_bd_pins /'+dest_name+'/'+dest_port_name+'ready_downward]',
      ''])

  def return_syn2bits_tcl_list(self, jobs=8, prj_dir='./prj/', prj_name = 'floorplan_static'):
    threads_num = subprocess.getoutput("nproc")
    return ([
      'open_project '+prj_dir+prj_name+'.xpr',
      'reset_run synth_1',
      'launch_runs synth_1 -jobs '+str(threads_num),
      'wait_on_run synth_1',
      'launch_runs impl_1 -to_step write_bitstream -jobs '+str(threads_num),
      'wait_on_run impl_1',
      'file mkdir '+prj_dir+prj_name+'.sdk',
      'write_hw_platform -fixed -include_bit -force -file ' + prj_dir + prj_name + '.sdk/floorplan_static_wrapper.xsa',
      ''])

  def return_syn2dcp_tcl_list(self, back_end = 'slurm', prj_dir='./prj/', prj_name = 'floorplan_static.xpr'):
    if back_end == 'slurm':
      threads_num = 8
    else:
      threads_num = commands.getoutput("nproc")
    return ([
      'open_project '+prj_dir+prj_name,
      'reset_run synth_1',
      'launch_runs synth_1 -jobs '+str(threads_num),
      'wait_on_run synth_1',
      'open_run synth_1 -name synth_1',
      'write_checkpoint -force floorplan_static.dcp',
      ''])

  def return_gen_abs_tcl_list(self, dcp_in, cell_name, dcp_out):
    lines_list = []
    lines_list.append('open_checkpoint '+dcp_in)
    lines_list.append('update_design -cell '+cell_name+' -black_box')
    lines_list.append('lock_design -level routing')
    lines_list.append('write_abstract_shell -force -cell '+cell_name+' '+dcp_out)
    return lines_list


  def return_ip_page_tcl_list(self, fun_name, fun_num, file_list):
    lines_list = ['create_project floorplan_static ./prj -part '+self.prflow_params['part']]
    for file_name in file_list:
      lines_list.append('add_files -norecurse '+file_name)
     
    lines_list.extend([
     'set dir "../../../F002_hls_'+self.prflow_params['benchmark_name']  + '/' + fun_name + '_prj/' + fun_name + '/syn/verilog"',
      'set contents [glob -nocomplain -directory $dir *]',
      'foreach item $contents {',
      '  if { [regexp {.*\.tcl} $item] } {',
      '    source $item',
      '  } else {',
      '    add_files -norecurse $item',
      '  }',
      '}',
      'set_param general.maxThreads  8',
      'set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]',
      'add_files  -norecurse ./leaf_'+str(fun_num)+'.v',
      'ipx::package_project -root_dir ./prj/floorplan_static.srcs/sources_1 -vendor user.org -library user -taxonomy /UserIP',
      'set_property core_revision 2 [ipx::current_core]',
      'ipx::create_xgui_files [ipx::current_core]',
      'ipx::update_checksums [ipx::current_core]',
      'ipx::save_core [ipx::current_core]',
      'set_property  ip_repo_paths  ./prj/floorplan_static.srcs/sources_1 [current_project]',
      'update_ip_catalog',
      ''])
      
    return lines_list

  def return_syn_page_tcl_list(self, fun_name,  file_list, top_name='leaf', hls_src=None, dcp_name='page_netlist.dcp', rpt_name='',frequency=200):
    #lines_list = ['create_project floorplan_static ./prj -part '+self.prflow_params['part']]
    lines_list = []

    # clk_period = '{:.1f}'.format(1000 / int(frequency))

    for file_name in file_list:
      lines_list.append('add_files -norecurse '+file_name)
 
    lines_list.extend([
      #'set dir "../../F002_hls_'+self.prflow_params['benchmark_name']  + '/' + fun_name + '_prj/' + fun_name + '/syn/verilog"',
      'set dir "./src/"',
      'set contents [glob -nocomplain -directory $dir *]',
      'foreach item $contents {',
      '  if { [regexp {.*\.tcl} $item] } {',
      '    source $item',
      '  } else {',
      '    add_files -norecurse $item',
      '  }',
      '}'])
    if hls_src == None:
      lines_list.append('set dir "../../F002_hls_'+self.prflow_params['benchmark_name']  + '/' + fun_name + '_prj/' + fun_name + '/syn/verilog"')
    else:
      lines_list.append('set dir "'+hls_src+'"')
    lines_list.extend([
      'set contents [glob -nocomplain -directory $dir *]',
      'foreach item $contents {',
      '  if { [regexp {.*\.tcl} $item] } {',
      '    source $item',
      '  } else {',
      '    add_files -norecurse $item',
      '  }',
      '}',
      # 'create_clock -period ' + str(clk_period) +' -name clk [get_ports clk]', # add target clock
      'set_param general.maxThreads  8',
      'set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]',
      'set logFileId [open ./run_log_'+fun_name+'.log "w"]',
      'set start_time [clock seconds]',
      'set_param general.maxThreads  8 ',
      'add_files -fileset constrs_1 -norecurse syn.xdc',
      # 'set_property USED_IN_SYNTHESIS true [get_files syn.xdc]',
      # 'set_property USED_IN_IMPLEMENTATION false [get_files syn.xdc]',
      'set_property USED_IN {synthesis out_of_context} [get_files syn.xdc]',
      'synth_design -top '+top_name+' -part '+self.prflow_params['part']+' -mode out_of_context'])
    lines_list.append('write_checkpoint -force '+dcp_name)
    lines_list.extend([
      'set end_time [clock seconds]',
      'set total_seconds [expr $end_time - $start_time]',
      'puts $logFileId "syn: $total_seconds seconds"',
      'report_utilization -hierarchical > '+rpt_name,
      # 'report_timing_summary > timing.rpt',
      'report_design_analysis -complexity -timing > design_analysis.rpt',
      ''])
     
    return lines_list

  def get_file_name(self, file_dir):                                            
    for root, dirs, files in os.walk(file_dir):                                 
      return files  

  def return_hls_tcl_list(self, fun_name, path='../..', clk_user="5.0"):
    lines_list = []
    lines_list.append('set logFileId [open ./run_log_' + fun_name + '.log "w"]')
    lines_list.append('set_param general.maxThreads ' + self.prflow_params['maxThreads'] + ' ')
    lines_list.append('set start_time [clock seconds]')                     
    lines_list.append('open_project ' + fun_name + '_prj')                  
    lines_list.append('set_top ' + fun_name + '')                           
    lines_list.append('add_files '+path+'/input_src/' + self.prflow_params['benchmark_name'] + '/operators/' + fun_name + '.cpp')
    lines_list.append('add_files '+path+'/input_src/' + self.prflow_params['benchmark_name'] + '/host/typedefs.h')
    lines_list.append('open_solution "' +fun_name +'"')                     
    lines_list.append('set_part {'+self.prflow_params['part']+'}')          
    # lines_list.append('create_clock -period '+self.prflow_params['clk_user']+' -name default')
    lines_list.append('create_clock -period '+ clk_user +' -name default')
    lines_list.append('#source "./Rendering_hls/colorFB/directives.tcl"')   
    lines_list.append('#csim_design')                                       
    lines_list.append('csynth_design')                                      
    lines_list.append('#cosim_design -trace_level all -tool xsim')          
    #if(fun_name == self.prflow_params['mono_function']):                      
    #  lines_list.append('export_design -rtl verilog -format ip_catalog')    
    #else:                                                                     
    lines_list.append('#export_design -rtl verilog -format ip_catalog')   
                                                                              
    lines_list.append('set end_time [clock seconds]')                       
    lines_list.append('set total_seconds [expr $end_time - $start_time]')   
    lines_list.append('puts $logFileId "hls: $total_seconds seconds"')      
    lines_list.append('')                                                     
    lines_list.append('exit')                                               

    return lines_list

  def return_hls_prj_list(self, fun_name):
    lines_list = []
    #generate project files for each function                                 
    #the reason is that one vivado project can only have on active hardware function
    #to be implemented                                                        
    lines_list.append('<project xmlns="com.autoesl.autopilot.project" name="' + fun_name + '_prj" top="'+ fun_name + '">')
    lines_list.append('    <includePaths/>')
    lines_list.append('    <libraryPaths/>')
    lines_list.append('    <Simulation>')
    lines_list.append('        <SimFlow askAgain="false" name="csim" csimMode="0" lastCsimMode="0"/>')
    lines_list.append('    </Simulation>')
    lines_list.append('    <files>')

    #capture all the files under operator dirctory
    lines_list.append('        <file name="../../input_src/' + self.prflow_params['benchmark_name'] + '/operators/' + fun_name + '.cpp " sc="0" tb="false" cflags=""/>')
    lines_list.append('        <file name="../../input_src/' + self.prflow_params['benchmark_name'] + '/host/typedefs.h" sc="0" tb="false" cflags=""/>')
    lines_list.append('    </files> ')
    lines_list.append('    <solutions>')
    lines_list.append('        <solution name="' + fun_name + '" status="active"/>')
    lines_list.append('    </solutions>')
    lines_list.append('</project>')

    return lines_list

  def return_impl_tcl_list(self, fun_name, num, overlay='overlay.dcp', IsNet=False):
    lines_list = []
    lines_list.append('set logFileId [open ./run_log_'+fun_name+'.log "w"]')
    #lines_list.append('set_param general.maxThreads ' + self.prflow_params['maxThreads'] + ' ')
    lines_list.append('set_param general.maxThreads 2 ')
    lines_list.append('')
    lines_list.append('#####################')
    lines_list.append('## read_checkpoint ##')
    lines_list.append('#####################')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('open_checkpoint ../../F001_overlay/'+overlay)
    if IsNet:
      lines_list.append("update_design -cell floorplan_static_i/net" + str(num) + "/inst -black_box")
      lines_list.append("read_checkpoint -cell floorplan_static_i/net" + str(num) + "/inst ../../F003_syn_" + self.prflow_params['benchmark_name'] + '/net' + str(num) + "/net" + str(num) + "_netlist.dcp")
    else:
      lines_list.append("update_design -cell floorplan_static_i/leaf_empty_" + str(num) + "/inst -black_box -quiet")
      lines_list.append("read_checkpoint -cell floorplan_static_i/leaf_empty_" + str(num) + "/inst ../../F003_syn_" + self.prflow_params['benchmark_name'] + '/' + fun_name + "/page_netlist.dcp")
 
    lines_list.append("set end_time [clock seconds]")
    lines_list.append("set total_seconds [expr $end_time - $start_time]")
    lines_list.append('puts $logFileId "read_checkpoint: $total_seconds seconds"')
    lines_list.append("")
    lines_list.append("")

    lines_list.append("####################")
    lines_list.append("## implementation ##")
    lines_list.append("####################")
    lines_list.append("set start_time [clock seconds]")
    lines_list.append("#reset_timing ")
    lines_list.append("opt_design ")
    lines_list.append("set end_time [clock seconds]")
    lines_list.append("set total_seconds [expr $end_time - $start_time]")
    lines_list.append('puts $logFileId "opt: $total_seconds seconds"')
    lines_list.append("write_checkpoint  -force  "+ fun_name + "_opt.dcp")
    lines_list.append("")

    lines_list.append("set start_time [clock seconds]")
    if self.prflow_params['PR_mode'] == 'quick':
      lines_list.append("if { [catch {place_design -directive Quick } errmsg] } {")
    else:
      lines_list.append("if { [catch {place_design} errmsg] } {")
    lines_list.append("  puts $logFileId \"place: 99999 failed!\"")
    lines_list.append("}")

    lines_list.append("set end_time [clock seconds]")
    lines_list.append("set total_seconds [expr $end_time - $start_time]")
    lines_list.append('puts $logFileId "place: $total_seconds seconds"')
    lines_list.append("write_checkpoint  -force  page_placed.dcp")
    lines_list.append("")

    lines_list.append("set start_time [clock seconds]")
    if self.prflow_params['PR_mode'] == 'quick':
      lines_list.append("if { [catch {route_design -directive Quick } errmsg] } {")
    else:
      lines_list.append("if { [catch {route_design  } errmsg] } {")
    lines_list.append("  puts $logFileId \"routing: 99999 failed!\"")
    lines_list.append("}")
          
    lines_list.append("set end_time [clock seconds]")
    lines_list.append("set total_seconds [expr $end_time - $start_time]")
    lines_list.append('puts $logFileId "route: $total_seconds seconds"')
    lines_list.append("write_checkpoint -force   page_routed.dcp")
    lines_list.append("")
    lines_list.append("")

    lines_list.append("###############")
    lines_list.append("## bitstream ##")
    lines_list.append("###############")
    lines_list.append("set_param bitstream.enablePR 2341")
    lines_list.append("set start_time [clock seconds]")
    if IsNet:
      lines_list.append("write_bitstream  -force  -cell floorplan_static_i/net" + str(num) + "/inst ../../F005_bits_"+self.prflow_params['benchmark_name']+"/net_" + str(num) + "")
    else:
      lines_list.append("write_bitstream  -force  -cell floorplan_static_i/leaf_empty_" + str(num) + "/inst ../../F005_bits_"+self.prflow_params['benchmark_name']+'/'+fun_name)
    lines_list.append("set end_time [clock seconds]")
    lines_list.append("set total_seconds [expr $end_time - $start_time]")
    lines_list.append('puts $logFileId "bit_gen: $total_seconds seconds"')
    if IsNet:
      lines_list.append('report_utilization -pblocks ' + fun_name + ' > utilization.rpt')
    else:
      lines_list.append('report_utilization -pblocks p_' + str(num) + ' > utilization.rpt')
    lines_list.append('report_timing_summary > timing.rpt')
    return lines_list






  def return_mk_overlay_tcl_list(self):
    lines_list = []
    lines_list.append('set logFileId [open ./runLog_impl_big_static_' + str(self.prflow_params['nl']) + '.log "w"]')
    lines_list.append('')
    lines_list.append('#####################')
    lines_list.append('## read_checkpoint ##')
    lines_list.append('#####################')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('open_checkpoint ./floorplan_static.dcp')
    for i in range(int(self.prflow_params['nl'])):
      if self.prflow_params['page'+str(i)].replace('RISCV', '') != self.prflow_params['page'+str(i)]:
        lines_list.append('read_checkpoint -cell floorplan_static_i/leaf_empty_' + str(i) + '/inst ./dummy_repo/'+self.prflow_params['page'+str(i)]+'/page_netlist.dcp')
      if self.prflow_params['page'+str(i)].replace('user_kernel', '') != self.prflow_params['page'+str(i)]:
        lines_list.append('read_checkpoint -cell floorplan_static_i/leaf_empty_' + str(i) + '/inst ./dummy_repo/'+self.prflow_params['page'+str(i)]+'/page_netlist.dcp')
    lines_list.append('set end_time [clock seconds]')
    lines_list.append('set total_seconds [expr $end_time - $start_time]')
    lines_list.append('puts $logFileId "read_checkpoint: $total_seconds seconds"')
    lines_list.append('')
    lines_list.append('####################')
    lines_list.append('## implementation ##')
    lines_list.append('####################')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('opt_design')
    lines_list.append('set end_time [clock seconds]')
    lines_list.append('set total_seconds [expr $end_time - $start_time]')
    lines_list.append('puts $logFileId "opt: $total_seconds seconds"')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('place_design')
    lines_list.append('set end_time [clock seconds]')
    lines_list.append('set total_seconds [expr $end_time - $start_time]')
    lines_list.append('puts $logFileId "place: $total_seconds seconds"')
    lines_list.append('# write_hwdef -force pr_test_wrapper.hwdef')
    lines_list.append('write_checkpoint -force init_placed_' + str(self.prflow_params['nl']) + '.dcp')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('route_design')
    lines_list.append('set end_time [clock seconds]')
    lines_list.append('set total_seconds [expr $end_time - $start_time]')
    lines_list.append('puts $logFileId "route: $total_seconds seconds"')
    lines_list.append('write_checkpoint -force init_routed_' + str(self.prflow_params['nl']) + '.dcp')
    lines_list.append('set_param bitstream.enablePR 2341')
    lines_list.append('write_bitstream -force -no_partial_bitfile  ./main.bit')
    for i in range(int(self.prflow_params['nl'])):
      if self.prflow_params['page'+str(i)].replace('RISCV', '') != self.prflow_params['page'+str(i)]:
        lines_list.append('write_bitstream -force -cell floorplan_static_i/leaf_empty_'+str(i)+\
                          '/inst ./riscv_bit_lib/page'+str(i)+'_'+self.prflow_params['page'+str(i)]+'.bit')
    lines_list.append('report_timing_summary > timing.rpt')
    lines_list.append('#############################################')
    lines_list.append('## create static design with no bft pblock ##')
    lines_list.append('#############################################')
    lines_list.append('')
    lines_list.append('set start_time [clock seconds]')
    lines_list.append('update_design -cell floorplan_static_i/bft0 -black_box')
    lines_list.append('update_design -cell floorplan_static_i/bft1 -black_box')
    lines_list.append('update_design -cell floorplan_static_i/bft2 -black_box')
    lines_list.append('update_design -cell floorplan_static_i/bft3 -black_box')
    lines_list.append('update_design -cell floorplan_static_i/bft_center -black_box')
    for i in range(int(self.prflow_params['nl'])):
      if self.prflow_params['page'+str(i)].replace('RISCV', '') != self.prflow_params['page'+str(i)] or \
         self.prflow_params['page'+str(i)].replace('user_kernel', '') != self.prflow_params['page'+str(i)]:
        lines_list.append('update_design -cell floorplan_static_i/leaf_empty_' + str(i) + '/inst -black_box')

    lines_list.append('#############################################')
    lines_list.append('## Only after empty all modules out, can   ##')
    lines_list.append('## you add -buffer_ports                   ##')
    lines_list.append('#############################################')
 
    lines_list.append('update_design -cell floorplan_static_i/bft0 -buffer_ports')
    lines_list.append('update_design -cell floorplan_static_i/bft1 -buffer_ports')
    lines_list.append('update_design -cell floorplan_static_i/bft2 -buffer_ports')
    lines_list.append('update_design -cell floorplan_static_i/bft3 -buffer_ports')
    lines_list.append('update_design -cell floorplan_static_i/bft_center -buffer_ports')
    for i in range(int(self.prflow_params['nl'])):
      if self.prflow_params['page'+str(i)].replace('RISCV', '') != self.prflow_params['page'+str(i)] or \
         self.prflow_params['page'+str(i)].replace('user_kernel', '') != self.prflow_params['page'+str(i)]:
        lines_list.append('update_design -cell floorplan_static_i/leaf_empty_' + str(i) + '/inst -buffer_ports')
        lines_list.append('report_utilization -pblocks p_'+str(i)+' > utilization'+str(i)+'.rpt')
   

    lines_list.append('lock_design -level routing')
    lines_list.append('write_checkpoint -force overlay.dcp')
    lines_list.append('close_design')
    lines_list.append('set end_time [clock seconds]')
    lines_list.append('set total_seconds [expr $end_time - $start_time]')
    lines_list.append('puts $logFileId "update, black_box: $total_seconds seconds"')
    lines_list.append('# set start_time [clock seconds]')
    lines_list.append('# set end_time [clock seconds]')
    lines_list.append('# set total_seconds [expr $end_time - $start_time]')
    lines_list.append('# puts $logFileId "write bitstream: $total_seconds seconds"')

    return lines_list

  def return_download_bit_tcl_list(self, operators):
    lines_list = []
    lines_list.append('open_hw')
    lines_list.append('connect_hw_server')
    lines_list.append('open_hw_target')
    lines_list.append('current_hw_device [get_hw_devices '+self.prflow_params['device']+']')
    lines_list.append('set_property PROBES.FILE {} [get_hw_devices '+self.prflow_params['device']+']')
    lines_list.append('set_property FULL_PROBES.FILE {} [get_hw_devices '+self.prflow_params['device']+']')
    lines_list.append('set_property PROGRAM.FILE {./main.bit} [get_hw_devices '+self.prflow_params['device']+']')
    lines_list.append('program_hw_devices [get_hw_devices '+self.prflow_params['device']+']')
    lines_list.append('refresh_hw_device [lindex [get_hw_devices '+self.prflow_params['device']+'] 0]\n')
    for operator in operators:
      lines_list.append('set_property PROBES.FILE {} [get_hw_devices '+self.prflow_params['device']+']')
      lines_list.append('set_property FULL_PROBES.FILE {} [get_hw_devices '+self.prflow_params['device']+']')
      lines_list.append('set_property PROGRAM.FILE {./'+ operator + '.bit} [get_hw_devices '+self.prflow_params['device']+']')
      lines_list.append('program_hw_devices [get_hw_devices '+self.prflow_params['device']+']')
      lines_list.append('refresh_hw_device [lindex [get_hw_devices '+self.prflow_params['device']+'] 0]\n')
    
    return lines_list 
 




  # tcl command function end
  ######################################################################################################################################################



class gen_basic:
  def __init__(self, prflow_params):
    self.shell         = _shell(   prflow_params)
    self.pragma        = _pragma(  prflow_params)
    self.verilog       = _verilog( prflow_params)
    self.tcl           = _tcl(     prflow_params)
    self.dataflow      = _dataflow(prflow_params)
    self.prflow_params = prflow_params
    self.bft_dir       = self.prflow_params['workspace']+'/F000_bft_gen'
    #self.overlay_dir  = self.prflow_params['workspace']+'/F001_overlay_' + self.prflow_params['nl'] + '_leaves'
    # if self.prflow_params['overlay_type'] == 'hipr':
    #   self.overlay_dir = self.prflow_params['workspace']+'/F001_overlay_'+self.prflow_params['benchmark_name']
    # else:
    #   self.overlay_dir = self.prflow_params['workspace']+'/F001_overlay'
    self.overlay_dir = self.prflow_params['workspace']+'/F001_overlay'
    # print ('inside:', self.overlay_dir)
    self.hls_dir          = self.prflow_params['workspace']+'/F002_hls_'+self.prflow_params['benchmark_name']
    self.syn_dir          = self.prflow_params['workspace']+'/F003_syn_'+self.prflow_params['benchmark_name']
    self.pr_dir           = self.prflow_params['workspace']+'/F004_impl_'+self.prflow_params['benchmark_name']
    self.bit_dir          = self.prflow_params['workspace']+'/F005_bits_'+self.prflow_params['benchmark_name']
    self.mono_dir         = self.prflow_params['workspace']+'/F007_mono_'+self.prflow_params['benchmark_name']
    self.overlay_mono_dir = self.prflow_params['workspace']+'/F007_overlay_mono'
    self.mono_bft_dir     = self.prflow_params['workspace']+'/F007_mono_bft_'+self.prflow_params['benchmark_name']
    self.sdk_dir          = self.prflow_params['workspace']+'/F008_sdk_'+self.prflow_params['benchmark_name']
    self.rpt_dir          = self.prflow_params['workspace']+'/report'
    self.net_list         = ['1', '1', '1', '1', '1', '2', '2', '2',
                         '2', '2', '2', '0', '3', '3', '3', '3',
                         '3', '3', '4', '4', '4', '4', '4', '4',
                         '5', '5', '5', '5', '5', '5', '5', '5']





  ######################################################################################################################################################
  # help functions start
  def print_params(self):
    print(self.prflow_params)

  def print_list(self, in_list):
    for num, value in enumerate(in_list):
      print(str(num)+'\t'+str(value))

  def print_dict(self, in_dict):
    for key, value in sorted(in_dict.items()):
      print(str(key).ljust(30)+'->'+str(value))

  def has_pattern(self, in_str, pattern_str):
    if in_str.replace(pattern_str, '') == in_str:
      return False
    else:
      return True

  # Returns page_assign_dict from pblock_assign_dict
  # def get_page_assign_dict(self, pblock_assign_dict):
  #   page_assign_dict = {}
  #   for op, pblock in pblock_assign_dict.items():
  #     page_num_list = pblock_page_dict[pblock]
  #     min_page = str(min(int(p) for p in page_num_list))
  #     page_assign_dict[op] = min_page
  #   return page_assign_dict


  # help functions end
  ######################################################################################################################################################

if __name__ == '__main__':
  modification_dict = {'parameter PAYLOAD_BITS0': 'parameter PAYLOAD_BITS0 = a,',
                       'parameter PORT_NUM_IN0': 'parameter PORT_NUM_IN0 = b,',
                       'parameter PORT_NUM_OUT0': 'parameter PORT_NUM_OUT0 = c,'}
  filename='net0.v'
  inst = gen_basic()
  inst.replace_lines(filename, modification_dict)
  lines_list = ['hell',
   'you',
   'are',
   'every',
   'thing']

  inst.add_lines(filename, 'input clk', lines_list)
  inst.write_lines('net1.txt',  lines_list)



