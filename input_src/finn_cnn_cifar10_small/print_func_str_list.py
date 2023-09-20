import json, math, os
import argparse

with open("./operators/out_data_collect.cpp", "r") as infile:
    lines = infile.readlines()
    for line in lines:
        print('    func_str_list.append(\'' + line.replace('\t',' ').replace('\n','') + '\')')