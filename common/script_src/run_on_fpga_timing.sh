python counter_analyze.py -b BENCHMARK --NoC_timing_violate
cd ./input_src/BENCHMARK/ && python gen_next_param.py
cd -
make incr_NoC -j$(nproc)