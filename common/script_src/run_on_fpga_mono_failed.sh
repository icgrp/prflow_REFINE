#!/bin/bash

python counter_analyze.py -b BENCHMARK --monolithic_fail

if [ ! -f ./input_src/BENCHMARK/__mono_done__ ]; then
    cd ./input_src/BENCHMARK/ && python gen_next_param.py
    cd -
    make incr_mono
else
    echo "Design space exploration done!"
fi