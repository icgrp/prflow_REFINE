#!/bin/bash


if [ ! -f ./input_src/BENCHMARK/__NoC_done__ ]; then
    scp -i ~/.ssh/id_rsa_zcu102 ./workspace/F005_bits_BENCHMARK/sd_card/* root@10.10.7.1:/run/media/mmcblk0p1/
    ssh -i ~/.ssh/id_rsa_zcu102 root@IP_ZCU102 "cd /run/media/mmcblk0p1/; ./run_app.sh > results.txt; scp -i ~/.ssh/id_rsa results.txt summary.csv USERNAME@IP_HOST:PROJECT_DIR/_bi_results/BENCHMARK/"

    # Record resource util, compile time, impl, results, timing
    make record_NoC_success
    python counter_analyze.py -b BENCHMARK --NoC_success
    if [ ! -f ./input_src/BENCHMARK/__NoC_done__ ]; then
        cd ./input_src/BENCHMARK/ && python gen_next_param.py
        cd -
        make incr_NoC
    else
        make incr_mono
    fi
else
    make incr_mono
fi