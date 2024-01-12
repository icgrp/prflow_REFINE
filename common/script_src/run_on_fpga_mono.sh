#!/bin/bash


if [ ! -f ./input_src/BENCHMARK/__mono_done__ ]; then
    scp -i ~/.ssh/id_rsa_zcu102 ./workspace/F007_mono_BENCHMARK/zcu102/package/sd_card/* root@IP_ZCU102:/run/media/mmcblk0p1/
    ssh -i ~/.ssh/id_rsa_zcu102 root@IP_ZCU102 "/sbin/reboot"
    # Wait for the board to boot up
    sleep 80
    ssh -i ~/.ssh/id_rsa_zcu102 root@IP_ZCU102 "cd /run/media/mmcblk0p1/; rm -rf __static_loaded__;./run_app.sh > results.txt; scp -i ~/.ssh/id_rsa results.txt summary.csv USERNAME@IP_HOST:PROJECT_DIR/_bi_results/BENCHMARK/"

    # Record resource util, compile time, impl, results, timing
    make record_mono_success
    python counter_analyze.py -b BENCHMARK --monolithic_success
    cd ./input_src/BENCHMARK/ && python gen_next_param.py
    cd -
    make incr_mono
else
    echo "Design space exploration done!"
fi