import json, math, os
import argparse

with open("./operators/output_collect.h", "r") as infile:
    lines = infile.readlines()
    for line in lines:
        print('    func_str_list.append(\'' + line.replace('\t',' ').replace('\n','') + '\')')