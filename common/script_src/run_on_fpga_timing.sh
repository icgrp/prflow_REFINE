#!/bin/bash


python counter_analyze.py -b BENCHMARK --NoC_timing_violate
cd ./input_src/BENCHMARK/ && python gen_next_param.py
cd -

if [ ! -f ./input_src/rendering/__NoC_done__ ]; then
    make incr_NoC
else
    make incr_mono
fi