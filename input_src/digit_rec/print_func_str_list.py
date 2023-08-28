import json, math, os
import argparse

with open("./operators/flow_calc_1.cpp", "r") as infile:
    lines = infile.readlines()
    for line in lines:
        print('    func_str_list.append(\'' + line.replace('\t',' ').replace('\n','') + '\')')