#!/bin/bash

scp -i ~/.ssh/id_rsa_zcu102 ./workspace/F007_mono_BENCHMARK/zcu102/package/sd_card/* root@10.10.7.1:/run/media/mmcblk0p1/
ssh -i ~/.ssh/id_rsa_zcu102 root@10.10.7.1 "sbin/reboot"
# Wait for the board to boot up
sleep 20
ssh -i ~/.ssh/id_rsa_zcu102 root@10.10.7.1 "cd /run/media/mmcblk0p1/; rm __static_loaded__; ./run_app.sh; ./run_app.sh; ./run_app.sh > results.txt; scp -i ~/.ssh/id_rsa results.txt summary.csv dopark@10.10.7.2:/home/dopark/workspace/zcu102_tuning/prflow_DSE_bi_22.1/_bi_results/BENCHMARK/"

python counter_analyze.py -b BENCHMARK --monolithic_success
cd ./input_src/BENCHMARK/ && python gen_next_param.py
cd -

if [ ! -f ./input_src/BENCHMARK/__mono_done__ ]; then
    make incr_mono -j$(nproc)
else
    echo "Design space exploration done!"
fi