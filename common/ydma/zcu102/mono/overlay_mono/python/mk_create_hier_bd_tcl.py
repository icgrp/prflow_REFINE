#!/usr/bin/env python
import argparse
import os


prev_dir = os.path.abspath('..')
# kernel_freq = os.path.abspath('..').split('/')[-1].split('MHz')[0] + '000000'

with open('./tcl/create_hier_bd.tcl', 'r') as infile:
  lines = infile.readlines()

filedata = ''
for line in lines:
  if 'PRJ_BOARD_FREQ_DIR' in line:
    line = line.replace('PRJ_BOARD_FREQ_DIR', prev_dir)
  filedata += line

with open(prev_dir+'/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup/create_hier_bd.tcl', 'w') as outfile:
  outfile.write(filedata)