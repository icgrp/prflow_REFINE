#!/usr/bin/env python
# -*- coding: utf-8 -*-   
#starting
import os  
import subprocess
import pr_flow.utils              as utils
import pr_flow.gen_bft            as bft
import pr_flow.overlay            as overlay
import pr_flow.hls                as hls
import pr_flow.syn                as syn
import pr_flow.impl               as impl
import pr_flow.xclbin             as xclbin
import pr_flow.runtime            as runtime
import pr_flow.monolithic         as monolithic
import pr_flow.ip_repo            as ip_repo
import pr_flow.report             as report
import pr_flow.report_monolithic  as report_mono
import pr_flow.incr               as incr
import pr_flow.page_assign        as page_assign
import pr_flow.check_impl_result  as check_impl_result

import argparse
import xml.etree.ElementTree

if __name__ == '__main__':


  # Use argparse to parse the input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('benchmark_name')
  parser.add_argument('-q',         '--run_qsub',          help="default: don't submit the qsub job to icgrid",     action='store_true')
  parser.add_argument('-g',         '--gen_overlay',       help="default: don't compile the static region",         default=None)
  parser.add_argument('-hls',       '--gen_hls',           help="default: don't compile the static region",         action='store_true')
  parser.add_argument('-syn',       '--gen_syn',           help="default: don't perform out-of-context synthesis",  action='store_true')
  parser.add_argument('-impl',      '--gen_impl',          help="default: don't perform placement/routing/bit gen", action='store_true')
  parser.add_argument('-xclbin',    '--gen_xclbin',        help="default: don't generate xclbin",                   action='store_true')
  parser.add_argument('-runtime',   '--gen_runtime',       help="default: don't update the runtime driver",         action='store_true')
  parser.add_argument('-monolithic','--gen_monolithic',    help="default: don't update the runtime driver",         action='store_true')
  parser.add_argument('-ip',        '--gen_ip_repo',       help="default: don't generate ip_repo",                  action='store_true')
  parser.add_argument('-rpt',       '--gen_report',        help="default: don't generate the report",               action='store_true')
  parser.add_argument('-rpt_m',     '--gen_report_mono',   help="default: don't generate the report for monolithic",action='store_true')
  parser.add_argument('-op',        '--operator',          help="choose which function to be regenrated", type=str, default="no_func")
  parser.add_argument('-m',         '--monitor_on',        help="default: monitor_on=False", type=bool,             default=False)
  parser.add_argument('-incr',      '--gen_incremental',   help="default: don't do incremental compile",            action='store_true')
  parser.add_argument('-s_dcp',     '--syn_dcp',           help="default: syn_dcp=None",                            default=None)
  parser.add_argument('-rt',        '--routing_test',      help="default: routing_test=False",                      action='store_true')
  parser.add_argument('-pg',        '--gen_page_assign',   help="default: gen_page_assign=False",                   action='store_true')
  parser.add_argument('-freq',      '--frequency',         help="default: freq=200",                                default="200")
  parser.add_argument('-c',         '--check_impl_result', help="default: check_impl_result=False",                 action='store_true')


  args = parser.parse_args()
  benchmark_name = args.benchmark_name  
  input_file_name = './common/configure/configure.xml'
  prflow_params                    = utils.load_prflow_params(input_file_name)
  prflow_params['benchmark_name']  = benchmark_name
  prflow_params['run_qsub']        = args.run_qsub
  prflow_params['gen_overlay']     = args.gen_overlay
  prflow_params['gen_hls']         = args.gen_hls
  prflow_params['gen_syn']         = args.gen_syn
  prflow_params['gen_impl']        = args.gen_impl
  prflow_params['gen_xclbin']      = args.gen_xclbin
  prflow_params['gen_runtime']     = args.gen_runtime
  prflow_params['gen_monolithic']  = args.gen_monolithic
  prflow_params['gen_ip_repo']     = args.gen_ip_repo
  prflow_params['gen_report']      = args.gen_report
  prflow_params['gen_report_mono'] = args.gen_report_mono
  prflow_params['input_file_name'] = input_file_name
  prflow_params['workspace']       = './workspace'
  operator = args.operator
  monitor_on = args.monitor_on # maybe outdated
  prflow_params['gen_incremental'] = args.gen_incremental
  syn_dcp = args.syn_dcp # maybe outdated
  is_routing_test = args.routing_test # maybe outdated
  prflow_params['gen_page_assign'] = args.gen_page_assign
  freq = args.frequency # outdated
  prflow_params['check_impl_result'] = args.check_impl_result
  prflow_params['overlay_freq'] = "400" # fixed to highest frequency
  prflow_params['overlay_n'] = 'overlay_p23' # maybe just fix the overlay

  if prflow_params['gen_overlay'] == 'psnoc':
    overlay_inst = overlay.overlay(prflow_params)
    overlay_inst.run(operator)
    print ('psnoc')

  if prflow_params['gen_overlay'] == 'mono':
    overlay_inst = overlay.overlay(prflow_params)
    overlay_inst.run(operator, is_mono = True)
    print ('mono')

  if prflow_params['gen_hls'] == True:
    hls_inst = hls.hls(prflow_params)
    hls_inst.run(operator)

  if prflow_params['gen_syn'] == True:
    syn_inst = syn.syn(prflow_params)
    syn_inst.run(operator)

  if prflow_params['gen_impl'] == True:
    impl_inst = impl.impl(prflow_params)
    impl_inst.run(operator, syn_dcp)

  if prflow_params['gen_xclbin'] == True:
    xclbin_inst = xclbin.xclbin(prflow_params)
    xclbin_inst.run(operator)

  if prflow_params['gen_runtime'] == True:
    runtime_inst = runtime.runtime(prflow_params)
    runtime_inst.run(operator)

  if prflow_params['gen_monolithic'] == True:
    mono_inst = monolithic.monolithic(prflow_params)
    mono_inst.run(operator)

  if prflow_params['gen_ip_repo'] == True:
    ip_repo_inst = ip_repo.ip_repo(prflow_params)
    ip_repo_inst.run(operator)

  if prflow_params['gen_report'] == True:
    rpt_inst = report.report(prflow_params)
    rpt_inst.run(operator,is_routing_test)

  if prflow_params['gen_report_mono'] == True:
    rpt_inst = report_mono.report_mono(prflow_params)
    rpt_inst.run(operator,frequency = freq)

  if prflow_params['gen_incremental'] == True:
    incr_inst = incr.incr(prflow_params)
    incr_inst.run()

  if prflow_params['gen_page_assign'] == True:
    pg_inst = page_assign.page_assign(prflow_params)
    pg_inst.run(operator)

  if prflow_params['check_impl_result'] == True:
    pg_inst = check_impl_result.check_impl_result(prflow_params)
    pg_inst.run(operator)
