#!/usr/bin/env python
import sys
import os
import xml.etree.ElementTree
import argparse
import re
import math
import subprocess
import json
from pr_flow.gen_basic import gen_basic


# DJP: report_syn is to report some resource estimates or design complexity at the post-synthesis phase.
#      The output of report_syn is quite different from report.py
class report_syn(gen_basic):


  # Post-synthesis resource estimates report
  def gen_resource_report(self, benchmark_name, operators_list):
    resource_report_dict = {}

    for fun_name in operators_list:

      try:
        file_name = './workspace/F003_syn_'+benchmark_name+'/' + fun_name + '/utilization.rpt'
        file_list = self.shell.file_to_list(file_name)
        for idx, line in enumerate(file_list):
          if 'Instance' in line:
            resource_list =  file_list[idx+2].replace(' ', '').split('|') # 2 lines later...
            num_luts = resource_list[3]
            num_ffs = resource_list[7]
            num_brams = int(resource_list[8])*2+int(resource_list[9])
            num_dsps = resource_list[11]
            resource_report_dict[fun_name] = " {: <8}{: <8}{: <9}{: <8}"\
                                            .format(num_luts, num_ffs, num_brams, num_dsps)
      except:
        print ('Something is wrong with '+file_name) 


    resource_report_file = open('./workspace/report/resource_report_syn_'+benchmark_name+'.csv', 'w')
    top_row_str = 'LUTs,FFs,BRAM18s,DSPs\n'
    # resource_report_file.write('operator                  \ttarget\tpblock\t\tpage\tLUTs\tFFs\tBRAM18s\tDSPs\n')
    resource_report_file.write(top_row_str)
    for key, value in sorted(resource_report_dict.items()):
      value_list = value.split()
      value_csv = ','.join(value_list)
      resource_report_file.write(value_csv+'\n')  
    print(' ' * 32, 'LUTs',' ' * 2, 'FFs',' ' * 3, 'BRAM18s  DSPs')
    # print '\n                               operator                  \ttarget\tpblock\t\tpage\tLUTs\tFFs\tBRAM18s\tDSPs'
    print('----------------------------------------------------------------------------------------------------------------------------')
    self.print_dict(resource_report_dict)


  # Post-synthesis design analysis estimates report
  def gen_da_report(self, benchmark_name, operators_list):
    da_report_dict = {}

    for fun_name in operators_list:
      try:
        file_name = './workspace/F003_syn_'+benchmark_name+'/' + fun_name + '/design_analysis.rpt'
        file_list = self.shell.file_to_list(file_name)
        for idx, line in enumerate(file_list):
          if 'Instance' in line:
            resource_list =  file_list[idx+2].replace(' ', '').split('|') # 2 lines later...
            rent = resource_list[3]
            avg_fanout = resource_list[4]
            total_inst = resource_list[5]
            da_report_dict[fun_name] = " {: <8}{: <14}{: <8}"\
                                            .format(rent, avg_fanout, total_inst)
      except:
        print ('Something is wrong with '+file_name) 


    da_report_syn_file = open('./workspace/report/da_report_syn_'+benchmark_name+'.csv', 'w')
    top_row_str = 'rent,avg_fanout,total_inst\n'
    da_report_syn_file.write(top_row_str)
    for key, value in sorted(da_report_dict.items()):
      value_list = value.split()
      value_csv = ','.join(value_list)
      da_report_syn_file.write(value_csv+'\n')  
    print(' ' * 32, 'rent',' ' * 2, 'avg_fanout',' ' * 2, 'total_inst')
    print('----------------------------------------------------------------------------------------------------------------------------')
    self.print_dict(da_report_dict)

  def run(self, operators_str):

    self.shell.mkdir(self.rpt_dir)
    benchmark_name = self.prflow_params['benchmark_name']
    operators_list = operators_str.split() 
    self.gen_resource_report(benchmark_name, operators_list)
    print()
    self.gen_da_report(benchmark_name, operators_list)
    print('You can find the post-synthesis resource estimates and design analysis estimates: ./workspace/report')

