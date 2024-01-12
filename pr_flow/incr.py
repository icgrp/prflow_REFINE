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
      if 'IP_ZCU102' in line:
        line = line.replace('IP_ZCU102', self.prflow_params['ip_zcu102'])
      if 'IP_HOST' in line:
        line = line.replace('IP_HOST', self.prflow_params['ip_host'])
      if 'USERNAME' in line:
        line = line.replace('USERNAME', self.prflow_params['username'])
      if 'PROJECT_DIR' in line:
        line = line.replace('PROJECT_DIR', self.prflow_params['project_dir'])
      filedata += line
    with open('./run_on_fpga.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_timing.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      if 'IP_ZCU102' in line:
        line = line.replace('IP_ZCU102', self.prflow_params['ip_zcu102'])
      if 'IP_HOST' in line:
        line = line.replace('IP_HOST', self.prflow_params['ip_host'])
      if 'USERNAME' in line:
        line = line.replace('USERNAME', self.prflow_params['username'])
      if 'PROJECT_DIR' in line:
        line = line.replace('PROJECT_DIR', self.prflow_params['project_dir'])
      filedata += line
    with open('./run_on_fpga_timing.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_mono.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      if 'IP_ZCU102' in line:
        line = line.replace('IP_ZCU102', self.prflow_params['ip_zcu102'])
      if 'IP_HOST' in line:
        line = line.replace('IP_HOST', self.prflow_params['ip_host'])
      if 'USERNAME' in line:
        line = line.replace('USERNAME', self.prflow_params['username'])
      if 'PROJECT_DIR' in line:
        line = line.replace('PROJECT_DIR', self.prflow_params['project_dir'])
      filedata += line
    with open('./run_on_fpga_mono.sh', 'w') as outfile:
      outfile.write(filedata)

    with open('./run_on_fpga_mono_failed.sh', 'r') as infile:
      lines = infile.readlines()
    filedata = ''
    for line in lines:
      if 'BENCHMARK' in line:
        line = line.replace('BENCHMARK', self.prflow_params['benchmark_name'])
      if 'IP_ZCU102' in line:
        line = line.replace('IP_ZCU102', self.prflow_params['ip_zcu102'])
      if 'IP_HOST' in line:
        line = line.replace('IP_HOST', self.prflow_params['ip_host'])
      if 'USERNAME' in line:
        line = line.replace('USERNAME', self.prflow_params['username'])
      if 'PROJECT_DIR' in line:
        line = line.replace('PROJECT_DIR', self.prflow_params['project_dir'])
      filedata += line
    with open('./run_on_fpga_mono_failed.sh', 'w') as outfile:
      outfile.write(filedata)
