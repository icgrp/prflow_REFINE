scp -i ~/.ssh/id_rsa_zcu102 ./workspace/F005_bits_BENCHMARK/sd_card/* root@10.10.7.1:/run/media/mmcblk0p1/
ssh -i ~/.ssh/id_rsa_zcu102 root@10.10.7.1 "cd /run/media/mmcblk0p1/; ./run_app.sh; ./run_app.sh; ./run_app.sh > results.txt; scp -i ~/.ssh/id_rsa results.txt summary.csv dopark@10.10.7.2:/home/dopark/workspace/zcu102_tuning/prflow_DSE_bi_22.1/_bi_results/BENCHMARK/"

python counter_analyzer.py -b BENCHMARK
cd ./input_src/BENCHMARK/gen_next_param.py
make incr -j$(nproc)