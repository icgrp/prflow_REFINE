#!/bin/bash 
cd /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/StreamingFIFO_25_tbcxkyrg/project_StreamingFIFO_25/sol1/impl/verilog
vivado -mode batch -source package_ip.tcl
cd /home/dopark/workspace/finn_v21.1
