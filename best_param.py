import json
import argparse
import sys, os

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # parser.add_argument('-b',         '--bottleneck', required = True)
    # args = parser.parse_args()
    # bottleneck = args.bottleneck

    benchmark = 'rendering'


    prev_summary_list = [x for x in os.listdir("./input_src/" + benchmark + "/params/visited/")\
                                 if (x.startswith('summary_') and x.endswith('.csv'))]

    best_latency = sys.maxsize
    idx = -1
    for summary_file in prev_summary_list:
        with open("./input_src/" + benchmark + "/params/visited/" + summary_file, "r") as infile:
            lines = infile.readlines()

            next_line = False
            # Parse results
            for line in lines:
                if line.startswith('Kernel,Number Of Enqueues'):
                    next_line = True
                elif next_line == True:
                    kernel_name, num_enqueue, latency, _, _, _, _ = line.split(',') 
                    break
        if latency < best_latency:
            best_latency = latency
            idx = int(summary_file.split('_')[1].split('.')[0])

    print("Best idx: " + str(idx))
    # os.system('cp ./input_src/' + benchmark + '/params/visited/prev_param_' + str(idx) + '.json ' +\
    #              './input_src/' + benchmark + '/params/cur_param.json')
