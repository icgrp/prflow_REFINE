#!/bin/bash

export PLATFORM_REPO_PATHS=
export ROOTFS=
export kl_name=mono
export MaxJobNum=$(nproc)
export PLATFORM=
#export MaxJobNum=10

Xilinx_dir
# Embedded platform doesn't need XRT_DIR

unset LD_LIBRARY_PATH

sdk_dir

# Generate mono.dcp
cd ./mono_syn/
./run_vivado_tcl.sh syn_mono.tcl
cd ..

# Generate mono.bit
cd mono_impl
./run_vivado_tcl.sh impl_mono.tcl
cd ..

# Generate mono.xclbin
cd ./mono_xclbin
./run_mono_xclbin.sh
cd ..

# Generate sd card img
make all

