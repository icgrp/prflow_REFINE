#!/usr/bin/env python
import re
from pr_flow.gen_basic import gen_basic
from datetime import datetime
date_format = "%H:%M:%S"

class report_mono(gen_basic):

  def gen_compile_time_report(self, operators_list, frequency):
    # v++ -l log file
    log_dir = self.mono_dir + '/logs/'
    vitis_log_file = log_dir + 'v++.log'
    vivado_log_file = log_dir + 'vivado.log'

    # HLS is done in parallel, take the max
    elapsed_hls_max = 0
    for operator_name in operators_list:
      try:
        file_name = self.hls_dir + '/runLog' + operator_name + '.log'
        file_in = open(file_name, 'r')
        for line in file_in:
          elapsed_hls = int(re.findall(r"\d+", line)[0])
        file_in.close()

        if(elapsed_hls  > elapsed_hls_max):
          elapsed_hls_max = elapsed_hls

      except:
        print ('Something is wrong with '+file_name) 

    # v++ -l log file
    with open(vitis_log_file,"r") as infile:
        for line in infile:
            if(line.startswith("INFO: [v++ 60-1548] Creating build summary session")):
                time_start = line.split(" at ")[1].strip()
                time_start = time_start.split()[3]
                #print(time_start) # e.g.: 22:29:52
            if(line.endswith("Step vpl: Started\n")):
                time_end = line.split(" Run run_link:")[0].strip()
                time_end = time_end.split()[3]
                time_end = time_end[1:-1]
                #print(time_end) # e.g.: 22:30:01

        # setup time before synthesis(9~10s, add to synthesis time)
        syn_extra = datetime.strptime(time_end, date_format) - datetime.strptime(time_start, date_format)
        #print(syn_extra)
    
    # vivado.log for more details
    with open(vivado_log_file,"r") as infile:
        for line in infile:
            if("Start of session at:" in line):
                time_viv_start = line.split()[8] # magic number to extract time, e.g.: "22:30:03"
                #print(time_viv_start)
            if("synth_1 finished" in line):
                time_syn_end = line.split()[3] # magic number to extract time, e.g.: "22:33:12"
                #print(time_syn_end)
            if("write_bitstream: Time" in line):
                time_bits = line.split()[9] # magic number to extract time, e.g.: "00:00:15"
                #print(time_bits)
            if("Exiting Vivado" in line): # multiple times... but last one
                time_viv_end = line.split()[9]
        #print(time_viv_end) # e.g.: 22:36:08
    
    elapsed_syn = (datetime.strptime(time_syn_end, date_format) - \
                   datetime.strptime(time_viv_start, date_format) + \
                   syn_extra).seconds
    elapsed_bits = datetime.strptime(time_bits, date_format).minute*60 + \
                   datetime.strptime(time_bits, date_format).second
    elapsed_pnr = (datetime.strptime(time_viv_end, date_format) - \
                   datetime.strptime(time_syn_end, date_format)).seconds - \
                   elapsed_bits
    elapsed_total = elapsed_hls_max + elapsed_syn + elapsed_pnr + elapsed_bits

    print("HLS\t" + "Syn\t" + "P/R\t" + "Bits\t" + "Total")
    print("-------------------------------------------")
    print(str(elapsed_hls_max) + "\t" + \
          str(elapsed_syn) + "\t" + \
          str(elapsed_pnr) + "\t" + \
          str(elapsed_bits) + "\t" + \
          str(elapsed_total))

  def run(self, operators_str, frequency="200"):
    operators_list = operators_str.split() 
    self.gen_compile_time_report(operators_list, frequency)
