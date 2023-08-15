# -*- coding: utf-8 -*-   
# Company: IC group, University of Pennsylvania
# Contributor: Yuanlong Xiao
#
# Create Date: 02/23/2021
# Design Name: overlay
# Project Name: PLD
# Versions: 1.0
# Description: This is a python script to prepare the script for static region 
#              compile for PLD (https://github.com/icgrp/pld2022).
# Dependencies: python2, gen_basic.py hls.py
# Revision:
# Revision 0.01 - File Created
# Revision 0.02 - Update cotents for HiPR
#
# Additional Comments:


import os  
import subprocess
from pr_flow.gen_basic import gen_basic
from pr_flow.hls import hls

class overlay(gen_basic):
  def __init__(self, prflow_params):
    gen_basic.__init__(self, prflow_params)


  # create dummy directory for each empty block
  def create_place_holder(self, base_dir, operators):
    # extract the stream arguments and types (in/out and width) for all the operators
    operator_arg_dict, operator_width_dict = self.dataflow.return_operator_io_argument_dict(operators)

    # extract the variables used in top.cpp 
    operator_var_dict = self.dataflow.return_operator_inst_dict(operators)
   
    # extract the how different operators are connected from top.cpp 
    connection_list=self.dataflow.return_operator_connect_list(operator_arg_dict, operator_var_dict, operator_width_dict)

    # generate Verilog netlist for the dataflow graph
    mono_v_list = self.verilog.return_operator_inst_v_list(operator_arg_dict, connection_list, operator_var_dict, operator_width_dict)

    # Utilize hls class to prepare the high-level-synthesis work directory
    hls_inst = hls(self.prflow_params)
    for operator in operators.split():
      hls_inst.run(operator, base_dir+'/place_holder', '../../..', ['syn_'+operator+'.tcl'])
      self.shell.write_lines(base_dir+'/place_holder/syn_'+operator+'.tcl', \
                            self.tcl.return_syn_page_tcl_list(operator,  
                                                              [], 
                                                              top_name=operator, 
                                                              hls_src='./'+operator+'_prj/'+operator+'/syn/verilog', 
                                                              dcp_name=operator+'_netlist.dcp', 
                                                              rpt_name='utilization_'+operator+'.rpt'))


  # run.sh will be used for generating the overlay.dcp 
  def return_run_sh_list_local(self, operators, bft_n, overlay_freq):
    lines_list = []
    lines_list.append('#!/bin/bash -e')
    lines_list.append('#place_holder anchor')
    str_line = 'cd place_holder\n'

    # launch hls for each operator
    operators_list = operators.split()
    for idx, operator in enumerate(operators_list):
      if idx % 8 == 7 or idx+1 == len(operators_list): str_line += './run_'+operator+'.sh\n'
      else: str_line += './run_'+operator+'.sh&\n'
    str_line += 'cd -\n' 

    # launch the vitis compilation for ydma kernel
    lines_list.append(str_line) 
    # if not the 1st overlay gen, remove previously generated utilization*.rpt
    # lines_list.append('rm -rf utilization*.rpt') 

    lines_list.append('cd ydma/'+self.prflow_params['board']+'/'+overlay_freq+'MHz')
    lines_list.append('./build.sh')

    # generate the 2nd-level DFX regions 
    if self.prflow_params['overlay_type'] == 'hipr': # generate abstract shell dcps for hipr overlay 
      lines_list.append('cd '+self.prflow_params['board']+'_dfx_hipr')
    else: # generate abstract shell dcps for psnoc overlay
      lines_list.append('cd '+self.prflow_params['board']+'_dfx_manual')
    lines_list.append('source '+self.prflow_params['Xilinx_dir'])
    lines_list.append('make -j8') # to be safe
    # lines_list.append('make -j$(nproc)')
    lines_list.append('./shell/run_xclbin.sh')

    # copy the dcps and xclbins from overlay workspace
    # lines_list.append('cp ./ydma/'+self.prflow_params['board']+'/_x/link/int/ydma.xml ./dynamic_region.xml')
    # lines_list.append('cp ./ydma/'+self.prflow_params['board']+'/_x/link/vivado/vpl/prj/prj.runs/impl_1/dynamic_region.bit ./')
    # lines_list.append('./gen_xclbin_'+self.prflow_params['board']+'.sh dynamic_region.bit dynamic_region.xml dynamic_region.xclbin')
    lines_list.append('cp -r ../package ./overlay_p'+str(bft_n)+'/')
    lines_list.append('cp ./overlay_p'+str(bft_n)+'/*.xclbin ./overlay_p'+str(bft_n)+'/package/sd_card')
    # lines_list.append('mv *.rpt ./ydma/'+self.prflow_params['board']+'/'+self.prflow_params['board']+'_dfx_manual/'+'overlay_p'+str(bft_n)+'/')
    # lines_list.append('cd ./ydma/'+self.prflow_params['board']+'/'+self.prflow_params['board']+'_dfx_manual/'+'overlay_p'+str(bft_n))
    lines_list.append('cd overlay_p'+str(bft_n))
    lines_list.append('cp ../util_scripts/get_blocked_resources_abs_shell.py .')
    lines_list.append('cp ../util_scripts/parse_ovly_util.py .')
    lines_list.append('cp ../util_scripts/blocked_analysis.py .')
    lines_list.append('python get_blocked_resources_abs_shell.py')
    lines_list.append('python parse_ovly_util.py')
    lines_list.append('python blocked_analysis.py')

    return lines_list

 
  def create_shell_file(self, operators, bft_n, overlay_freq):
    # copy the shell script to generate xclbin
    self.shell.cp_file('./common/script_src/gen_xclbin_'+self.prflow_params['board']+'.sh ', self.overlay_dir)

    # generate the shell script to generate the overlay
    self.shell.write_lines(self.overlay_dir+'/run.sh', self.return_run_sh_list_local(operators, bft_n, overlay_freq), True)
    
    # generate the shell script to call run.sh depends on the scheduler.
    # scheduler: slurm, qsub, local 
    self.shell.write_lines(self.overlay_dir+'/main.sh', self.shell.return_main_sh_list(\
                                                       './run.sh', \
                                                       self.prflow_params['back_end'], \
                                                       'NONE',\
                                                       'overlay', \
                                                       self.prflow_params['grid'],  \
                                                       self.prflow_params['email'], \
                                                       self.prflow_params['mem'],  \
                                                       self.prflow_params['maxThreads']), True)
 

  def update_cad_path(self, base_dir, operators, overlay_freq, is_mono):
    kl_name = 'ydma'
    if not is_mono:
      overlay_sub_dir = overlay_freq + 'MHz'
      cfg_file = self.prflow_params['board']+'_dfx.cfg'
    else:
      overlay_sub_dir = 'mono'
      cfg_file = self.prflow_params['board'] # use non-dfx platform

    # update the cad path for build.sh
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'export ROOTFS'      : 'export ROOTFS='+self.prflow_params['ROOTFS']})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'export kl_name'      : 'export kl_name=' + kl_name})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh',
                            {'export PLATFORM_REPO_PATHS=': 'export PLATFORM_REPO_PATHS='+self.prflow_params['PLATFORM_REPO_PATHS']})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'export PLATFORM='   : 'export PLATFORM='+self.prflow_params['PLATFORM']})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'xrt_dir'            : 'source '+self.prflow_params['xrt_dir']})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'sdk_dir'            : 'source '+self.prflow_params['sdk_dir']})
    self.shell.replace_lines(base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh', 
                            {'Xilinx_dir'         : 'source '+self.prflow_params['Xilinx_dir']})
    os.system('chmod +x '+base_dir + '/ydma/'+self.prflow_params['board']+'/'+ overlay_sub_dir +'/build.sh')

    # replace device definistion in cfg file
    self.shell.replace_lines(base_dir + '/ydma/src/' + cfg_file, \
                            {'platform'         : 'platform='+self.prflow_params['PLATFORM']})


  def update_makefile_overlay(self, directory, bft_n):
    makefile = directory+'Makefile'
    with open(makefile, "r") as file:
      filedata = file.read()
    filedata = filedata.replace("checkpoint", "overlay_p"+str(bft_n))
    filedata = filedata.replace("_p31", "_p"+str(bft_n))
    filedata = filedata.replace('sub.xdc', 'sub_p'+str(bft_n)+'.xdc')

    with open(makefile, "w") as file:
      file.write(filedata)


  def update_py_overlay(self, directory, bft_n):
    pyfile = directory + 'mk_overlay_tcl.py'
    with open(pyfile, "r") as file:
      filedata = file.read()
    filedata = filedata.replace("/checkpoint", "/overlay_p"+str(bft_n))
    filedata = filedata.replace('sub.xdc', 'sub_p'+str(bft_n)+'.xdc')

    with open(pyfile, "w") as file:
      file.write(filedata)


  def update_sh_overlay(self, directory, bft_n):
    shellfiles = ['run_gen_pfm_dynamic.sh']
    for shellfile in shellfiles:
      with open(directory + shellfile, "r") as file:
        filedata = file.read()
      filedata = filedata.replace("/checkpoint", "/overlay_p"+str(bft_n))
      with open(directory + shellfile, "w") as file:
        file.write(filedata)

    shellfiles_nested = [f for f in os.listdir(directory+'nested/') if f.endswith('.sh')]
    for shellfile in shellfiles_nested:
      with open(directory + 'nested/' + shellfile, "r") as file:
        filedata = file.read()
      filedata = filedata.replace("/checkpoint", "/overlay_p"+str(bft_n))
      filedata = filedata.replace("Xilinx_dir",'source '+self.prflow_params['Xilinx_dir'])
      with open(directory + 'nested/' + shellfile, "w") as file:
        file.write(filedata)


  def update_tcl_overlay(self, directory, bft_n):
    sub_dir_list = ['','leaf_syn/','nested/','page_syn/','subdivide_syn/' ,'abs_analysis/']
    for sub_dir in sub_dir_list:
      tclfiles = [f for f in os.listdir(directory + sub_dir) if f.endswith('.tcl')]

      for tclfile in tclfiles:
        with open(directory + sub_dir + tclfile, "r") as file:
          filedata = file.read()
        filedata = filedata.replace("/checkpoint", "/overlay_p"+str(bft_n))
        with open(directory + sub_dir + tclfile, "w") as file:
          file.write(filedata)


  def update_main_overlay(self, directory, bft_n, overlay_freq):
    mainfile = directory+"main.sh"
    with open(mainfile, "r") as file:
      filedata = file.read()

    check_file = './ydma/'+self.prflow_params['board']+'/'+overlay_freq+'MHz'+\
                  '/'+self.prflow_params['board']+'_dfx_manual'+'/overlay_p'+str(bft_n) + '/overlay.dcp'
    new_str = 'if [ ! -f "' + check_file + '" ]; then ./run.sh "$@"; fi'
    filedata = filedata.replace('./run.sh "$@"', new_str)
 
    with open(mainfile, "w") as file:
      file.write(filedata)


  # main.sh will be used for local compilation
  def return_main_sh_list_local(self, input_list):
    lines_list = []
    lines_list.append('#!/bin/bash -e')
    lines_list.extend(input_list)
    return lines_list



  def run(self, operators, is_mono = False):
    overlay_freq = self.prflow_params['overlay_freq']
    bft_n = str(self.prflow_params['overlay_n'].split('_p')[1])

    if(not is_mono):
      # self.shell.mkdir(self.prflow_params['workspace'])
      self.shell.re_mkdir(self.overlay_dir)
      
      # copy the hld/xdc files from input source directory
      self.shell.del_dir(self.overlay_dir+'/src')
      self.shell.cp_dir('./common/verilog_src', self.overlay_dir+'/src')

      # copy the initial source files for vitis compile
      self.shell.cp_dir('./common/ydma', self.overlay_dir)

      # copy the parsing script to generate overlay's resource map
      # self.shell.cp_dir('./common/script_src/get_blocked_resources.py', self.overlay_dir)
      # self.shell.cp_dir('./common/script_src/parse_ovly_util.py', self.overlay_dir)

      # modifications for single-overlay-version to multiple-overlays-version
      self.update_py_overlay(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/'+overlay_freq+'MHz'\
                                    +'/'+self.prflow_params['board']+'_dfx_manual'+'/python/',bft_n)
      self.update_sh_overlay(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/'+overlay_freq+'MHz'\
                                    +'/'+self.prflow_params['board']+'_dfx_manual'+'/shell/',bft_n)
      self.update_tcl_overlay(self.overlay_dir+'/ydma/'+self.prflow_params['board']+'/'+overlay_freq+'MHz'\
                                    +'/'+self.prflow_params['board']+'_dfx_manual'+'/tcl/',bft_n)

      # update the cad tool path
      self.update_cad_path(self.overlay_dir, operators, overlay_freq, is_mono)

      # update the pragma for hipr ovelay generation
      # self.update_resource_pragma(operators)

      # generate shell files for local run
      self.create_shell_file(operators, bft_n, overlay_freq)
      self.update_main_overlay(self.overlay_dir+'/',bft_n,overlay_freq)

      # create dummy logic place and route the overlay.dcp
      self.create_place_holder(self.overlay_dir, operators)

      # create a folder to store the partial bitstreams for different versions of riscv
      # implementations for different pages
      self.shell.re_mkdir(self.overlay_dir+'/riscv_bit_lib')
    else:
      self.shell.re_mkdir(self.overlay_mono_dir)
      # prepare the source for vitis monolithic run
      self.shell.cp_dir("./common/ydma", self.overlay_mono_dir) 
      self.shell.del_dir(self.overlay_mono_dir + '/ydma/' + self.prflow_params['board'] + '/' + overlay_freq + 'MHz') 
      self.shell.del_dir(self.overlay_mono_dir + '/ydma/' + self.prflow_params['board'] + '/pre_gen_overlay') 

      self.shell.write_lines(self.overlay_mono_dir+'/run.sh',  self.return_main_sh_list_local([
                            'cd ./ydma/'+self.prflow_params['board']+'/mono',
                            './build.sh',
                            'cd ./overlay_mono',
                            'make overlay_mono_syn',
                            'cd ..',
                            'rm -rf ./package' # not used
                            ]), True) 

      self.shell.write_lines(self.overlay_mono_dir+'/main_overlay_mono.sh', self.return_main_sh_list_local(['./run.sh']), True)

      # update the cad tool path
      self.update_cad_path(self.overlay_mono_dir, operators, overlay_freq, is_mono)

      # create dummy logic place and route the overlay.dcp
      self.create_place_holder(self.overlay_mono_dir, operators)