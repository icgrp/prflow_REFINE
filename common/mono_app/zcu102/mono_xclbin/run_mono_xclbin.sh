#!/bin/bash -e
source /tools/Xilinx/Vitis/2022.1/settings64.sh
bitstream=../mono_impl/mono.bit
xmlfile=ydma.xml
xclbin=mono.xclbin

xclbinutil --add-section DEBUG_IP_LAYOUT:JSON:../../../F007_overlay_mono/ydma/zcu102/mono/_x/link/int/debug_ip_layout.rtd \
--add-section BITSTREAM:RAW:${bitstream} \
--force --target hw --key-value SYS:dfx_enable:false --add-section :JSON:../../../F007_overlay_mono/ydma/zcu102/mono/_x/link/int/ydma.rtd \
--add-section CLOCK_FREQ_TOPOLOGY:JSON:../../../F007_overlay_mono/ydma/zcu102/mono/_x/link/int/ydma_xml.rtd \
--add-section BUILD_METADATA:JSON:../../../F007_overlay_mono/ydma/zcu102/mono/_x/link/int/ydma_build.rtd \
--add-section EMBEDDED_METADATA:RAW:${xmlfile} \
--add-section SYSTEM_METADATA:RAW:../../../F007_overlay_mono/ydma/zcu102/mono/_x/link/int/systemDiagramModelSlrBaseAddress.json \
--key-value SYS:PlatformVBNV:xilinx.com_xd_xilinx_zcu102_base_202210_1_202210_1 \
--output ${xclbin}