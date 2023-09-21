export PLATFORM_REPO_PATHS=/opt/platforms/xilinx_zcu102_base_202210_1
export ROOTFS=/opt/platforms/xilinx-zynqmp-common-v2022.1
export kl_name=ydma
export MaxJobNum=$(nproc)
export PLATFORM=xilinx_zcu102_base_202210_1
#export MaxJobNum=10

source /tools/Xilinx/Vitis/2022.1/settings64.sh
# Embedded platform doesn't need XRT_DIR

unset LD_LIBRARY_PATH

source /opt/platforms/xilinx-zynqmp-common-v2022.1/environment-setup-cortexa72-cortexa53-xilinx-linux

make all
