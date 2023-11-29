#!/bin/bash


python counter_analyze.py -b BENCHMARK --NoC_timing_violate
# If NoC ver. violated timing and DSE is over, revert back to
# the most recent successful param and generate src codes with the line below.
cd ./input_src/BENCHMARK/ && python gen_next_param.py
cd -

if [ ! -f ./input_src/BENCHMARK/__NoC_done__ ]; then
    make incr_NoC
else
    make incr_mono
fi