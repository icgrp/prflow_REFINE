#!/bin/bash
cd ../../
root_dir=$(pwd)
cd -


export PLATFORM_REPO_PATHS=
export ROOTFS=
export kl_name=ydma
export MaxJobNum=$(nproc)
export PLATFORM=
#export MaxJobNum=10

Xilinx_dir
# Embedded platform doesn't need XRT_DIR

unset LD_LIBRARY_PATH

sdk_dir

# Make sure everything is up to date
# make app.exe
# make clean
make all
# make $1 
# make ${kl_name}.xo
