all: package/sd_card.img
#all:${kl_name}.xclbin 

app.exe: ./mono_host/host/host.cpp
	${CXX} -Wall -g -std=c++11 ./mono_host/host/host.cpp -o app.exe \
		-I/usr/include/xrt \
		-I${XILINX_HLS}/include \
		-lOpenCL \
		-lpthread \
		-lrt \
		-lstdc++


package/sd_card.img: app.exe ./mono_xclbin/mono.xclbin xrt.ini run_app.sh
	v++ -p -t hw --config ./zcu102.cfg ./mono_xclbin/mono.xclbin \
		--package.out_dir package \
		--package.rootfs ${ROOTFS}/rootfs.ext4 \
		--package.sd_file ${ROOTFS}/Image \
		--package.sd_file ./mono_xclbin/mono.xclbin \
		--package.sd_file xrt.ini \
		--package.sd_file app.exe \
		--package.sd_file run_app.sh


clean:
	rm -rf *xclbin* *.exe *json *xo *ltx *csv *log *summary _x package *.json .run .Xil .ipcache *.jou

# Unless specified, use the current directory name as the v++ build target
TARGET ?= $(notdir $(CURDIR))
