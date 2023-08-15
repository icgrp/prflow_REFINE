#!/usr/bin/env python
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('workspace')
parser.add_argument('-t', '--top', type=str, default="no_func", help="set top function name for out of context synthesis")
parser.add_argument('-f', '--file_name', type=str, default="no_func", help="set output file name prefix")


args = parser.parse_args()
workspace = args.workspace
top_name  = args.top
file_name = args.file_name





# prepare the tcl file to restore the top dcp file
file_in = open(workspace+'/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup/'+file_name+'.tcl', 'r')
file_out = open(workspace+'/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup/gen_overlay_mono_syn.tcl', 'w')

copy_enable = True
for line in file_in:
  if copy_enable:
    if (line.startswith('set rc [catch {')):
      file_out.write('# ' + line)
    elif (line.startswith('OPTRACE "link_design" END')):
      file_out.write(line)
      copy_enable = False
    # elif (line.replace('reconfig_partitions', '') != line):
    elif ('/impl_1/vitis_design_wrapper.tcl' in line):
      line = line.replace('/impl_1/vitis_design_wrapper.tcl','/impl_1_backup/vitis_design_wrapper.tcl')
      file_out.write(line)
    elif (line.startswith('  link_design -top')):
      file_out.write(line)
      file_out.write('write_checkpoint -force overlay_mono_syn.dcp\n')
    else:
      file_out.write(line)
      
file_in.close()
file_out.close()
