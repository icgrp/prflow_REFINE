#!/bin/bash


python counter_analyze.py -b BENCHMARK --NoC_timing_violate

if [ ! -f ./input_src/rendering/__NoC_done__ ]; then
    cd ./input_src/BENCHMARK/ && python gen_next_param.py
    cd -
    make incr_NoC
else
    make incr_mono
fi