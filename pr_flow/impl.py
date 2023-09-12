# -*- coding: utf-8 -*-   

import os  
import subprocess
from pr_flow.gen_basic import gen_basic
import re
import pr_flow.syn 
import json
from pr_flow.p23_pblock import pblock_page_dict

class impl(gen_basic):

  def get_num_op(self, operator):
    return len(operator.split())

  def get_page_size(self, pblock_name):
    return len(pblock_page_dict[pblock_name])

  def get_page_inst(self, pblock_name):
    split_str = pblock_name.split('_')
    base_page = split_str[0] # split_str[0] is 'p12' 
    base_page_num = base_page.split('p')[1] # '12'

    if(len(split_str) >= 2):
        # print(split_str[1:])
        page_inst = 'page' + base_page_num + '_inst'
        for elem in split_str[1:]:
            page_inst = page_inst + '/' + elem
    else: # p2, p4, p8, p12, p16, p20
        page_inst = 'page' + base_page_num + '_inst'
    return page_inst

  # create one directory for each page
  def create_page(self, pblock_op_impl, pblock_name, syn_dcp, specs_dict, operator):
    overlay_freq = self.prflow_params['overlay_freq']
    overlay_n = self.prflow_params['overlay_n']
    frequency = specs_dict[operator]['kernel_clk']
    num_leaf_interface = specs_dict[operator]['num_leaf_interface']

    # DJP: num_op is artifact of when we plan to include multiple ops in single pblock
    #      Probably won't use it.
    num_op = self.get_num_op(pblock_op_impl)
    if(num_op > 1): # if pblock_op_impl="coloringFB_bot_m coloringFB_top_m", operator_impl=coloringFB_bot_m
      operator_impl = pblock_op_impl.split()[0]
    else:
      operator_impl = pblock_op_impl

    page_inst = self.get_page_inst(pblock_name)
    self.shell.re_mkdir(self.pr_dir+'/'+operator_impl)
    self.shell.cp_file('./common/script_src/impl_page_'+self.prflow_params['board']+'.tcl', \
                        self.pr_dir+'/'+operator_impl+'/impl_'+operator_impl+'.tcl')

    #if(num_op > 1):
    op_list =  pblock_op_impl.split() # e.g.: ["coloringFB_bot_m", "coloringFB_top_m"]
    set_operator_replace = ''
    set_user_logic_replace = ''
    set_bit_name_replace = 'set bit_name "../../F005_bits_${benchmark}/${operator_0}.bit"'
    set_logFileId_replace = 'set logFileId [open ./run_log_${operator_0}.log "w"]'
    add_files_user_logic_dcp_replace = ''
    for i in range(num_op):
      set_operator_replace = set_operator_replace + 'set operator_' + str(i) + ' ' + op_list[i] + '\n'
      if(syn_dcp is not None):
        set_user_logic_replace = set_user_logic_replace \
                               + 'set user_logic_dcp_'+ str(i) +' "../../F003_syn_${benchmark}/'+syn_dcp+'/page_netlist.dcp"\n'
      else:
        set_user_logic_replace = set_user_logic_replace \
                               + 'set user_logic_dcp_'+ str(i) +' "../../F003_syn_${benchmark}/${operator_'+str(i)+'}/page_netlist.dcp"\n'
      add_files_user_logic_dcp_replace = add_files_user_logic_dcp_replace \
                                       + 'add_files $user_logic_dcp_' + str(i) + '\n'

    # else:
    #   set_operator_replace = 'set operator '+operator
    #   set_user_logic_replace = 'set user_logic_dcp "../../F003_syn_${benchmark}/${operator}/page_netlist.dcp"'
    #   set_bit_name_replace = 'set bit_name "../../F005_bits_${benchmark}/${operator}.bit"'
    #   set_logFileId_replace = 'set logFileId [open ./runLogImpl_${operator}.log "w"]'
    #   add_files_user_logic_dcp_replace = 'add_files $user_logic_dcp'

    ###########################
    ## Modifying impl script ##
    ###########################



    clk_src_list = {"clk_200": "clk_out5_pfm_top_clkwiz_sysclks_0", "clk_250": "clk_250_pfm_dynamic_clk_wiz_0_0_1",
                    "clk_300": "clk_out2_pfm_top_clkwiz_sysclks_0", "clk_350": "clk_350_pfm_dynamic_clk_wiz_0_0_1", \
                    "clk_400": "clk_out6_pfm_top_clkwiz_sysclks_0"}

    tmp_dict = {'set operator'                : set_operator_replace,
                'set benchmark'               : 'set benchmark '+self.prflow_params['benchmark_name'],
                'set pblock_name'             : 'set pblock_name '+pblock_name,
                'set part'                    : 'set part '+self.prflow_params['part'],
                'set user_logic_dcp'          : set_user_logic_replace,
                'set bit_name'                : set_bit_name_replace,
                'set logFileId'               : set_logFileId_replace,
                'add_files $user_logic_dcp'   : add_files_user_logic_dcp_replace,
                'set_property SCOPED_TO_CELLS': '',
                'link_design'                 : 'link_design -mode default -reconfig_partitions {'\
                                                 + self.prflow_params['inst_name']\
                                                +'/'+page_inst + '} -part $part -top '\
                                                + self.prflow_params['top_name'],
                'report_timing_summary >'     : 'report_timing_summary > timing_${pblock_name}.rpt\n'
                                                +'report_utilization -hierarchical -file ' \
                                                + operator_impl + '_' + str(pblock_name) + '.rpt'
                }

    # Place design command
    if self.prflow_params['place_design_NoC_directive'] != '':
      place_design_command = '  place_design -directive ' + self.prflow_params['place_design_NoC_directive']
    else:
      place_design_command = '  place_design'
    tmp_dict["place_design_command_with_directive"] = place_design_command

    # Route design command
    if self.prflow_params['route_design_NoC_directive'] != '':
      route_design_command = '  route_design -directive ' + self.prflow_params['route_design_NoC_directive']
    else:
      route_design_command = '  route_design'
    tmp_dict["route_design_command_with_directive"] = route_design_command


    if frequency == 400:
      tmp_dict["set_max_delay "] = "" # remove this constraint
    else:
      clk_src = clk_src_list["clk_" + str(frequency)]
      tmp_dict["set_max_delay "] = "set_max_delay -datapath_only 2.5 -from [get_clocks clk_out6_pfm_top_clkwiz_sysclks_0] -to [get_clocks " +\
                                    clk_src + "]"


    if(self.get_page_size(pblock_name) == 1):
      tmp_dict['set leaf_dcp']     = ''
    elif(self.get_page_size(pblock_name) == 2):
      if(num_leaf_interface == 1):
        tmp_dict['set leaf_dcp']     = 'set leaf_dcp "../../F001_overlay/ydma/'+self.prflow_params['board']\
                                     +'/'+overlay_freq+'MHz/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/leaf_double_1.dcp"'
      elif(num_leaf_interface == 2):
        tmp_dict['set leaf_dcp']     = ''
      else:
        raise Exception("Invalid num_leaf_interface")
    elif(self.get_page_size(pblock_name) == 4):
      if(num_leaf_interface == 1):
        tmp_dict['set leaf_dcp']     = 'set leaf_dcp "../../F001_overlay/ydma/'+self.prflow_params['board']\
                                     +'/'+overlay_freq+'MHz/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/leaf_quad_1.dcp"'
      elif(num_leaf_interface == 2):
        tmp_dict['set leaf_dcp']     = 'set leaf_dcp "../../F001_overlay/ydma/'+self.prflow_params['board']\
                                     +'/'+overlay_freq+'MHz/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/leaf_quad_2.dcp"'
      elif(num_leaf_interface == 3):
        tmp_dict['set leaf_dcp']     = 'set leaf_dcp "../../F001_overlay/ydma/'+self.prflow_params['board']\
                                     +'/'+overlay_freq+'MHz/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/leaf_quad_3.dcp"'
      elif(num_leaf_interface == 4):
        tmp_dict['set leaf_dcp']     = ''
      else:
        raise Exception("Invalid num_leaf_interface")


    if(self.get_page_size(pblock_name) == 1): 
      tmp_dict['add_files $leaf_dcp'] = '' # don't need leaf_dcp
      tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/' +\
                                    page_inst + '} [get_files $user_logic_dcp_0]'
    elif(self.get_page_size(pblock_name) == 2):
      if(num_leaf_interface == 1):
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst + '} [get_files $leaf_dcp]\n'
        tmp_dict['CELL_ANCHOR']     = tmp_dict['CELL_ANCHOR']\
                                    + 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst+ '/leaf_single_inst_0} [get_files $user_logic_dcp_'+str(i)+']'
      elif(num_leaf_interface == 2):
        tmp_dict['add_files $leaf_dcp'] = '' # don't need leaf_dcp
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/' +\
                                      page_inst + '} [get_files $user_logic_dcp_0]'
      else:
        raise Exception("Invalid num_leaf_interface")  
    elif(self.get_page_size(pblock_name) == 4):
      if(num_leaf_interface == 1):
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst + '} [get_files $leaf_dcp]\n'
        tmp_dict['CELL_ANCHOR']     = tmp_dict['CELL_ANCHOR']\
                                    + 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst+ '/leaf_single_inst_0} [get_files $user_logic_dcp_'+str(i)+']'
      elif(num_leaf_interface == 2):
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst + '} [get_files $leaf_dcp]\n'
        tmp_dict['CELL_ANCHOR']     = tmp_dict['CELL_ANCHOR']\
                                    + 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst+ '/leaf_double_inst_0} [get_files $user_logic_dcp_'+str(i)+']'
      elif(num_leaf_interface == 3):
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst + '} [get_files $leaf_dcp]\n'
        tmp_dict['CELL_ANCHOR']     = tmp_dict['CELL_ANCHOR']\
                                    + 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/'+\
                                      page_inst+ '/leaf_tri_inst_0} [get_files $user_logic_dcp_'+str(i)+']'
      elif(num_leaf_interface == 4):
        tmp_dict['add_files $leaf_dcp'] = '' # don't need leaf_dcp
        tmp_dict['CELL_ANCHOR']     = 'set_property SCOPED_TO_CELLS { '+self.prflow_params['inst_name']+'/' +\
                                      page_inst + '} [get_files $user_logic_dcp_0]'
      else:
        raise Exception("Invalid num_leaf_interface")  
    else:
      raise Exception("Invalid pblock size")  


    tmp_dict['set inst_name']   = 'set inst_name "'+self.prflow_params['inst_name']+'/' + page_inst + '"'
    tmp_dict['set context_dcp'] = 'set context_dcp "../../F001_overlay/ydma/'+self.prflow_params['board']\
                                +'/'+overlay_freq+'MHz/'+self.prflow_params['board']+'_dfx_manual/'+overlay_n+'/' + pblock_name + '.dcp"'


    # self.shell.cp_dir('./common/script_src/monitor_impl.sh', self.pr_dir+'/monitor.sh') # syn and impl are type 2
    # self.shell.cp_dir('./common/script_src/parse_htop.py', self.pr_dir)

    self.shell.cp_dir('./common/constraints/'+self.prflow_params['board']+'/*', self.pr_dir+'/'+operator_impl)
    self.shell.mkdir(self.pr_dir+'/'+operator_impl+'/output')
    os.system('touch '+self.pr_dir+'/'+operator_impl+'/output/_user_impl_clk.xdc') 
    self.shell.replace_lines(self.pr_dir+'/'+operator_impl+'/impl_'+operator_impl+'.tcl', tmp_dict)    

    self.shell.cp_dir('./common/script_src/write_result.py', self.pr_dir+'/'+operator_impl)
    tmp_dict = {}
    tmp_dict['PARAM_FILE'] = '            cur_param_dict_file = "../../../input_src/' + self.prflow_params['benchmark_name'] + '/params/cur_param.json"'
    self.shell.replace_lines(self.pr_dir+'/'+operator_impl+'/write_result.py', tmp_dict)    


    self.shell.write_lines(self.pr_dir+'/'+operator_impl+'/run.sh', self.shell.return_run_sh_list(self.prflow_params['Xilinx_dir'], 
                                                                                 'impl_'+operator_impl+'.tcl', 
                                                                                 self.prflow_params['back_end'],
                                                                                 ), True)
    self.shell.write_lines(self.pr_dir+'/'+operator_impl+'/main.sh', self.shell.return_main_sh_list('./run.sh', 
                                                                                 self.prflow_params['back_end'], 
                                                                                 'syn_'+operator_impl, 
                                                                                 'impl_'+operator_impl, 
                                                                                 self.prflow_params['grid'], 
                                                                                 'qsub@qsub.com',
                                                                                 self.prflow_params['mem'],
                                                                                 self.prflow_params['node']
                                                                                  ), True)
  

  def create_shell_file(self):
  # local run:
  #   main.sh <- |_ execute each impl_page.tcl
  #
  # qsub run:
  #   qsub_main.sh <-|_ Qsubmit each qsub_run.sh <- impl_page.tcl
    pass   

  def run(self, operator_impl, syn_dcp):
    # mk work directory
    if self.prflow_params['gen_impl']==True:
      print("gen_impl")
      self.shell.mkdir(self.pr_dir)
      self.shell.mkdir(self.bit_dir)
    
    pblock_ops_dir = './input_src/' + self.prflow_params['benchmark_name'] + '/operators'
    with open(pblock_ops_dir + '/specs.json', 'r') as infile:
      # pblock_operators_list = json.load(infile)
        specs_dict = json.load(infile)
    pblock_operators_list = specs_dict.keys()

    for pblock_op in pblock_operators_list:
      if(operator_impl in pblock_op.split()):
        # replace representiative op to multiple pblock_op, e.g.:"coloringFB_bot_m" to "coloringFB_bot_m coloringFB_top_m"
        pblock_op_impl = pblock_op 

    if('test_single_' in self.prflow_params['benchmark_name'] or\
        'test_double_' in self.prflow_params['benchmark_name'] or\
        'test_quad_' in self.prflow_params['benchmark_name']):
      # For routing test...
      with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
        pblock_assign_dict = json.load(infile)
      pblock_name = pblock_assign_dict[pblock_op_impl]["pblock"]
    else:
      # For incremental compile, each op has its own pblock.json
      with open(self.syn_dir+'/'+operator_impl+'/pblock.json', 'r') as infile:
        pblock_dict = json.load(infile)
        pblock_name = pblock_dict["pblock"]

    print("############################ PBLOCK NAME: " + pblock_name)
    # print("############################ OVERLAY_N: " + overlay_n)

    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/operators' + '/specs.json', 'r') as infile:
      # pblock_operators_list = json.load(infile)
      specs_dict = json.load(infile)

    self.create_page(pblock_op_impl, pblock_name, syn_dcp, specs_dict, operator_impl)