#!/usr/bin/env python
import sys
import os
import argparse
import re
import math
import json
from pr_flow.gen_basic import gen_basic

class record_time(gen_basic):


  def gen_resource_report(self, benchmark_name, operators_list, is_mono):
    resource_report_dict = {}

    ##############
    ## NoC ver. ##
    ##############
    if not is_mono:

      for fun_name in operators_list:
        if os.path.isfile(self.syn_dir+'/pblock_assignment.json'): 
          with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
            pblock_assign_dict = json.load(infile)

          pblock_name = pblock_assign_dict[fun_name]['pblock']
          page_num = pblock_assign_dict[fun_name]["page_num"]

          # Post-synthesis resource utilization
          # if os.path.isfile(self.syn_dir + '/' + fun_name + '/utilization.rpt'):
          #   file_name = self.syn_dir + '/' + fun_name + '/utilization.rpt'
          #   file_list = self.shell.file_to_list(file_name)
          #   for idx, line in enumerate(file_list):
          #     if 'Instance' in line:
          #       resource_list =  file_list[idx+2].replace(' ', '').split('|')
          #       num_LUT = int(resource_list[3])
          #       num_LUT_mem = int(resource_list[5])
          #       num_FF = int(resource_list[7])
          #       num_ram18 = int(resource_list[8])*2+int(resource_list[9])
          #       num_dsp = int(resource_list[11])
          #       resource_report_dict[fun_name] = {}
          #       resource_report_dict[fun_name]['pblock'] = pblock_name
          #       resource_report_dict[fun_name]['LUT'] = num_LUT
          #       resource_report_dict[fun_name]['LUT_mem'] = num_LUT_mem
          #       resource_report_dict[fun_name]['FF'] = num_FF
          #       resource_report_dict[fun_name]['RAMB18'] = num_ram18
          #       resource_report_dict[fun_name]['DSP48E2'] = num_dsp
          # else:
          #       resource_report_dict[fun_name] = {}
          #       resource_report_dict[fun_name]['pblock'] = None
          #       resource_report_dict[fun_name]['LUT'] = -1
          #       resource_report_dict[fun_name]['LUT_mem'] = -1
          #       resource_report_dict[fun_name]['FF'] = -1
          #       resource_report_dict[fun_name]['RAMB18'] = -1
          #       resource_report_dict[fun_name]['DSP48E2'] = -1
          # print(fun_name)
          # print(pblock_name)
          # print(page_num)

          # Post-implementation resource utilization
          num_LUT, num_LUT_mem, num_FF, num_ram18, num_dsp = -1, -1, -1, -1, -1

          if os.path.isfile(self.pr_dir + '/' + fun_name + '/' + fun_name + '_' + pblock_name + '.rpt'):
            file_name = self.pr_dir + '/' + fun_name + '/' + fun_name + '_' + pblock_name + '.rpt'
            file_list = self.shell.file_to_list(file_name)
            for idx, line in enumerate(file_list):
              if 'PR_pages_top_0' in line:
                resource_list =  file_list[idx].replace(' ', '').split('|')
                num_LUT = int(resource_list[5])
                num_LUT_mem = int(resource_list[7])
                num_FF = int(resource_list[9])
                num_ram18 = int(resource_list[10])*2+int(resource_list[11])
                num_dsp = int(resource_list[13])

        # If failed in page assignment,
        else:
          pblock_name = None
          num_LUT, num_LUT_mem, num_FF, num_ram18, num_dsp = -1, -1, -1, -1, -1

        resource_report_dict[fun_name] = {}
        resource_report_dict[fun_name]['pblock'] = pblock_name
        resource_report_dict[fun_name]['LUT'] = num_LUT
        resource_report_dict[fun_name]['LUT_mem'] = num_LUT_mem
        resource_report_dict[fun_name]['FF'] = num_FF
        resource_report_dict[fun_name]['RAMB18'] = num_ram18
        resource_report_dict[fun_name]['DSP48E2'] = num_dsp

    #####################
    ## Monolithic ver. ##
    #####################
    else:
      # Post-implementation resource utilization
      num_LUT, num_LUT_mem, num_FF, num_ram18, num_dsp = -1, -1, -1, -1, -1

      if os.path.isfile(self.mono_dir + '/' + self.prflow_params['board'] + '/mono_impl/mono_util.rpt'):
        file_name = self.mono_dir + '/' + self.prflow_params['board'] + '/mono_impl/mono_util.rpt'
        file_list = self.shell.file_to_list(file_name)
        for idx, line in enumerate(file_list):
          if 'vitis_design_wrapper' in line and '(top)' in line:
            resource_list =  file_list[idx].replace(' ', '').split('|')
            num_LUT = int(resource_list[3])
            num_LUT_mem = int(resource_list[5])
            num_FF = int(resource_list[7])
            num_ram18 = int(resource_list[8])*2+int(resource_list[9])
            num_dsp = int(resource_list[11])

      resource_report_dict['mono'] = {}
      resource_report_dict['mono']['pblock'] = None
      resource_report_dict['mono']['LUT'] = num_LUT
      resource_report_dict['mono']['LUT_mem'] = num_LUT_mem
      resource_report_dict['mono']['FF'] = num_FF
      resource_report_dict['mono']['RAMB18'] = num_ram18
      resource_report_dict['mono']['DSP48E2'] = num_dsp

    return resource_report_dict


  # NoC ver. if op in ops_only_pnr, include only impl time
  # Monolithic ver. if op in ops_only_pnr, include only synth, impl time
  def gen_compile_time_report(self, benchmark_name, operators_list, ops_only_pnr, is_mono):
    time_report_dict = {}

    ##############
    ## NoC ver. ##
    ##############
    if not is_mono:
      # Max compile time for HLS + syn
      t_hls_syn_max = 0
      for fun_name in operators_list:

        t_hls = 0
        if os.path.isfile(self.hls_dir + '/run_log_' + fun_name + '.log'):
          file_name = self.hls_dir + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            t_hls = int(re.findall(r"\d+", line)[0])
          file_in.close()

        t_syn = 0
        if os.path.isfile(self.syn_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'):
          file_name = self.syn_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            t_syn = int(re.findall(r"\d+", line)[0])
          file_in.close()

        if(t_hls + t_syn  > t_hls_syn_max):
          t_hls_syn_max = t_hls + t_syn

      # Compile time
      for fun_name in operators_list:

        # HLS compile time
        t_hls = 0
        if os.path.isfile(self.hls_dir  + '/run_log_' + fun_name + '.log'):
          file_name = self.hls_dir  + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            t_hls = int(re.findall(r"\d+", line)[0])
          file_in.close()

        # Synthesis compile time
        t_syn = 0
        if os.path.isfile(self.syn_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'):
          file_name = self.syn_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            t_syn = int(re.findall(r"\d+", line)[0])
          file_in.close()

        # Implementation compile time
        t_rdchk, t_opt, t_place, t_popt, t_route, t_bitgen = 0, 0, 0, 0, 0, 0
        t_total_max_syn, t_total = 0, 0

        if os.path.isfile(self.pr_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'):
          file_name = self.pr_dir + '/' + fun_name + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            if(line.startswith('read_checkpoint:')):
              t_rdchk = int(re.findall(r"\d+", line)[0])
            elif(line.startswith('opt:')):
              t_opt = int(re.findall(r"\d+", line)[0])
            elif(line.startswith('place:')):
              t_place = int(re.findall(r"\d+", line)[0])
            elif(line.startswith('opt_physical:')):
              t_popt = int(re.findall(r"\d+", line)[0])
            elif(line.startswith('route:')):
              t_route = int(re.findall(r"\d+", line)[0])
            elif(line.startswith('bitgen:')):
              t_bitgen = int(re.findall(r"\d+", line)[0])
          file_in.close()

        if fun_name in ops_only_pnr:
          t_hls, t_syn = 0, 0

        # If failed in page assignment,
        if not os.path.isfile(self.syn_dir+'/pblock_assignment.json'): 
          t_rdchk, t_opt, t_place, t_popt, t_route, t_bitgen = 0, 0, 0, 0, 0, 0

        t_total_max_syn = t_hls_syn_max + t_rdchk + t_opt + t_place + t_popt + t_route + t_bitgen
        t_total = t_hls + t_syn + t_rdchk + t_opt + t_place + t_popt + t_route + t_bitgen

        time_report_dict[fun_name] = {}
        time_report_dict[fun_name]['hls'] = t_hls
        time_report_dict[fun_name]['syn'] = t_syn
        time_report_dict[fun_name]['rdchk'] = t_rdchk
        time_report_dict[fun_name]['opt'] = t_opt
        time_report_dict[fun_name]['place'] = t_place
        time_report_dict[fun_name]['popt'] = t_popt
        time_report_dict[fun_name]['route'] = t_route
        time_report_dict[fun_name]['bitgen'] = t_bitgen
        time_report_dict[fun_name]['total_max_syn'] = t_total_max_syn
        time_report_dict[fun_name]['total'] = t_total

    #####################
    ## Monolithic ver. ##
    #####################
    else:

      # HLS compile time, still parallel
      t_hls_max = 0
      t_hls = 0
      for fun_name in operators_list:
        if os.path.isfile(self.hls_dir + '/run_log_' + fun_name + '.log'):
          file_name = self.hls_dir + '/run_log_' + fun_name + '.log'
          file_in = open(file_name, 'r')
          for line in file_in:
            t_hls = int(re.findall(r"\d+", line)[0])
          file_in.close()

        if (t_hls > t_hls_max) and (fun_name not in ops_only_pnr):
          t_hls_max = t_hls


      # Monolithic synthesis compile time
      t_syn = 0
      if os.path.isfile(self.mono_dir + '/' + self.prflow_params['board'] + '/mono_syn/run_mono_syn.log'):
        file_name = self.mono_dir + '/' + self.prflow_params['board'] + '/mono_syn/run_mono_syn.log'
        file_in = open(file_name, 'r')
        for line in file_in:
          t_syn = int(re.findall(r"\d+", line)[0])
        file_in.close()


      # Monolithic implementation compile time
      t_rdchk, t_opt, t_place, t_popt, t_route, t_bitgen = 0, 0, 0, 0, 0, 0
      t_total = 0
      if os.path.isfile(self.mono_dir + '/' + self.prflow_params['board'] + '/mono_impl/run_mono_impl.log'):
        file_name = self.mono_dir + '/' + self.prflow_params['board'] + '/mono_impl/run_mono_impl.log'
        file_in = open(file_name, 'r')
        for line in file_in:
          if(line.startswith('read_checkpoint:')):
            t_rdchk = int(re.findall(r"\d+", line)[0])
          elif(line.startswith('opt:')):
            t_opt = int(re.findall(r"\d+", line)[0])
          elif(line.startswith('place:')):
            t_place = int(re.findall(r"\d+", line)[0])
          elif(line.startswith('opt_physical:')):
            t_popt = int(re.findall(r"\d+", line)[0])
          elif(line.startswith('route:')):
            t_route = int(re.findall(r"\d+", line)[0])
          elif(line.startswith('bitgen:')):
            t_bitgen = int(re.findall(r"\d+", line)[0])
        file_in.close()
        t_total = t_hls_max + t_syn + t_rdchk + t_opt + t_place + t_popt + t_route + t_bitgen


      # Packaging time for non-DFX platform
      t_package_s = 0
      if os.path.isfile(self.mono_dir + '/' + self.prflow_params['board'] + '/v++_package.log'):
        file_name = self.mono_dir + '/' + self.prflow_params['board'] + '/v++_package.log'
        file_in = open(file_name, 'r')
        for line in file_in:
          if '[v++ 60-791] Total elapsed time' in line:
            t_package_h = int(re.findall(r"\d+h", line)[0].replace('h',''))
            t_package_m = int(re.findall(r"\d+m", line)[0].replace('m',''))
            t_package_s = int(re.findall(r"\d+s", line)[0].replace('s',''))
            # Usually t_package_s is less than 1 min
            t_package_s = 3600*t_package_h + 60*t_package_m + t_package_s
        file_in.close()



      time_report_dict['mono'] = {}
      time_report_dict['mono']['hls'] = t_hls_max
      time_report_dict['mono']['syn'] = t_syn
      time_report_dict['mono']['rdchk'] = t_rdchk
      time_report_dict['mono']['opt'] = t_opt
      time_report_dict['mono']['place'] = t_place
      time_report_dict['mono']['popt'] = t_popt
      time_report_dict['mono']['route'] = t_route
      time_report_dict['mono']['bitgen'] = t_bitgen
      time_report_dict['mono']['total'] = t_total
      time_report_dict['mono']['package'] = t_package_s

    return time_report_dict


  def gen_timing_report(self, benchmark_name, operators_list, is_mono):
    timing_report_dict = {}

    ##############
    ## NoC ver. ##
    ##############
    if not is_mono:

      for fun_name in operators_list:
        if os.path.isfile(self.syn_dir+'/pblock_assignment.json'): 
          with open(self.syn_dir+'/pblock_assignment.json', 'r') as infile:
            pblock_assign_dict = json.load(infile)

          pblock_name = pblock_assign_dict[fun_name]['pblock']
          page_num = pblock_assign_dict[fun_name]["page_num"]

          # Timing report
          WNS = None
          if os.path.isfile(self.pr_dir + '/' + fun_name + '/timing_' + pblock_name + '.rpt'):
            file_name = self.pr_dir + '/' + fun_name + '/timing_' + pblock_name + '.rpt'
            file_in = open(file_name, 'r')
            find_summary_flag = False
            line_offset = 0
            for line in file_in:
              if 'Design Timing Summary' in line:
                find_summary_flag = True
              if find_summary_flag:
                line_offset += 1
              if line_offset == 7:
                timing_list =  line.split()
                WNS = timing_list[0]

            file_in.close()

        # If failed in page assignment,
        else:
          WNS = None

        timing_report_dict[fun_name] = WNS

    #####################
    ## Monolithic ver. ##
    #####################
    else:
      WNS = None
      if os.path.isfile(self.mono_dir + '/' + self.prflow_params['board'] + '/mono_timing.rpt'):
        file_name = self.mono_dir + '/' + self.prflow_params['board'] + '/mono_timing.rpt'
        file_in = open(file_name, 'r')
        find_summary_flag = False
        line_offset = 0
        for line in file_in:
          if 'Design Timing Summary' in line:
            find_summary_flag = True
          if find_summary_flag:
            line_offset += 1
          if line_offset == 7:
            timing_list =  line.split()
            WNS = timing_list[0]

        file_in.close()

      timing_report_dict['mono'] = WNS

    return timing_report_dict


  def result_idx(self):
    prev_file_list = [x for x in os.listdir("./input_src/" + self.prflow_params['benchmark_name'] + "/params/results/")\
                        if (x.startswith('comp_time_') and x.endswith('.json'))]
    return len(prev_file_list)

  # Similar to counter_dict function in counter_analyze.py
  def extract_results(self):
    accuracy = -1
    with open('./_bi_results/' + self.prflow_params['benchmark_name'] + '/results.txt', 'r') as infile:
      lines = infile.readlines()
      for line in lines:
        if line.startswith('accuracy: '):
          accuracy = float(line.split()[1])

    with open("./_bi_results/" + self.prflow_params['benchmark_name'] + "/summary.csv", "r") as infile:
        lines = infile.readlines()
        next_line = False
        # Parse results
        for line in lines:
            if line.startswith('Kernel,Number Of Enqueues'):
                next_line = True
            elif next_line == True:
                kernel_name, num_enqueue, latency, _, _, _, _ = line.split(',') 
                break
    latency = float(latency)
    print(">> accuracy: " + str(accuracy))
    print(">> latency: " + str(latency))
    return latency, accuracy


  def record_results(self, resource_report_dict, compile_time_report_dict, timing_report_dict, is_impl_success):
    idx = self.result_idx()
    # resource_*.json, comp_time_*.json, timing_*.json
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/results/resource_' + str(idx) + '.json', 'w') as outfile:
      json.dump(resource_report_dict, outfile, sort_keys=True, indent=4)
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/results/comp_time_' + str(idx) + '.json', 'w') as outfile:
      json.dump(compile_time_report_dict, outfile, indent=4)
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/results/timing_' + str(idx) + '.json', 'w') as outfile:
      json.dump(timing_report_dict, outfile, sort_keys=True, indent=4)

    if is_impl_success:
      latency, accuracy = self.extract_results()
    else:
      latency, accuracy = -1, -1
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/results/metric.txt', 'a') as outfile:
      outfile.write(str(latency) + ' ' + str(accuracy) + '\n')


  def run(self, is_record_time_mono, is_impl_success):

    # 1) ./input_src/rendering/params/ops_to_compile.json is created by gen_next_param.py
    # 2) Only measure compile time in ops_to_compile.json
    with open('./input_src/' + self.prflow_params['benchmark_name'] + '/params/ops_to_compile.json', 'r') as infile:
      ops_to_compile_list = json.load(infile)

    # ops_to_compile: Ops that run hls, synthesis, impl
    # ops_only_pnr: In incremental compile, there are ops that are already synthesized but their pages are changed.
    #               Ops that didn't run hls, synthesis
    # ops_to_compile is subset of ops_to_pnr
    if(os.path.exists(self.syn_dir + '/ops_to_pnr.json')):
      with open(self.syn_dir + '/ops_to_pnr.json', 'r') as infile:
        ops_to_pnr = json.load(infile)
    else: # If page assignment failed,
      ops_to_pnr = ops_to_compile_list
    os.system('rm -rf ' + self.syn_dir + '/ops_to_pnr.json')

    ops_only_pnr = []
    for op in ops_to_pnr:
      if op not in ops_to_compile_list:
        ops_only_pnr.append(op)


    # Monolithic ver.
    if is_record_time_mono:
      is_mono = True
      ops_to_pnr = ops_to_compile_list

      # op_recompile_list: Ops that go thropugh incremental compile because the previous page mapping failed
      if(os.path.exists(self.syn_dir + '/op_recompile_list.json')):
        with open(self.syn_dir + '/op_recompile_list.json', 'r') as infile:
          ops_recompile = json.load(infile)
        os.system('rm ' + self.syn_dir + '/op_recompile_list.json')
        for op in ops_recompile:
          if op not in ops_only_pnr:
            ops_only_pnr.append(op)

      # 1)the previous run was NoC version or 
      # 2)the previous run was monolithic version
      # 3)this was the first compile
      resource_report_dict = self.gen_resource_report(self.prflow_params['benchmark_name'], ops_to_pnr, is_mono)
      compile_time_report_dict = self.gen_compile_time_report(self.prflow_params['benchmark_name'], ops_to_pnr, ops_only_pnr, is_mono)
      timing_report_dict = self.gen_timing_report(self.prflow_params['benchmark_name'], ops_to_pnr, is_mono)
      print(resource_report_dict)
      print(compile_time_report_dict)
      print(timing_report_dict)

      self.record_results(resource_report_dict, compile_time_report_dict, timing_report_dict, is_impl_success)

    # NoC ver.
    else:
      is_mono = False

      # op_recompile_list: Ops that go thropugh incremental compile because the previous page mapping failed
      if(os.path.exists(self.syn_dir + '/op_recompile_list.json')):
        with open(self.syn_dir + '/op_recompile_list.json', 'r') as infile:
          ops_recompile = json.load(infile)
        os.system('rm ' + self.syn_dir + '/op_recompile_list.json')
        for op in ops_recompile:
          if op not in ops_only_pnr:
            ops_only_pnr.append(op)

      print("ops_to_pnr:")
      print(ops_to_pnr)
      print("ops_only_pnr:")
      print(ops_only_pnr)

      resource_report_dict = self.gen_resource_report(self.prflow_params['benchmark_name'], ops_to_pnr, is_mono)
      compile_time_report_dict = self.gen_compile_time_report(self.prflow_params['benchmark_name'], ops_to_pnr, ops_only_pnr, is_mono)
      timing_report_dict = self.gen_timing_report(self.prflow_params['benchmark_name'], ops_to_pnr, is_mono)
      print("resource_report_dict:")
      print(resource_report_dict)
      print("compile_time_report_dict:")
      print(compile_time_report_dict)
      print("timing_report_dict:")
      print(timing_report_dict)

      self.record_results(resource_report_dict, compile_time_report_dict, timing_report_dict, is_impl_success)

