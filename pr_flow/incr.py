import os, json
from pr_flow.gen_basic import gen_basic

class incr(gen_basic):

  def run(self):
    os.system('cp ./common/script_src/run_on_fpga.sh ./')
    os.system('cp ./common/script_src/run_on_fpga_timing.sh ./')
    os.system('cp ./common/script_src/run_on_fpga_mono.sh ./')
    os.system('cp ./common/script_src/run_on_fpga_mono_failed.sh ./')


    with open('./run_on_fpga.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      filedata += line
    with open('./run_on_fpga.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_timing.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      filedata += line
    with open('./run_on_fpga_timing.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_mono.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      filedata += line
    with open('./run_on_fpga_mono.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_mono_failed.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      filedata += line
    with open('./run_on_fpga_mono_failed.sh', 'w') as outfile:
      outfile.write(filedata)
