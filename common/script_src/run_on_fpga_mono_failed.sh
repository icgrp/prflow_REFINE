#!/bin/bash

python counter_analyze.py -b BENCHMARK --monolithic_fail
cd ./input_src/BENCHMARK/ && python gen_next_param.py
cd -

if [ ! -f ./input_src/BENCHMARK/__mono_done__ ]; then
    make incr_mono -j$(nproc)
else
    echo "Design space exploration done!"
fi