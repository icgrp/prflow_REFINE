# REFINE: Runtime Execution Feedback for INcremental Evolution on FPGA Designs

The starting code is forked from [this repo](https://github.com/icgrp/prflow_nested_dfx)
[[PARK/FPT2022](https://ic.ese.upenn.edu/abstracts/nested_dfx_fpt2022.html)].

## Setup
The framework is developed with Ubuntu 20.04 with kernel 5.4.0, Vitis 2022.1 
and Xilinx ZCU102 evaluation board.

### Vitis
If you install Vitis on **/tools/Xilinx**, you should set **Xilinx_dir** 
in [./common/configure/configure.xml](./common/configure/configure.xml) as below.
```xml
  <spec name = "Xilinx_dir"         value = "/tools/Xilinx/Vitis/2022.1/settings64.sh" />
```

### Common image
The ZYNQMP common image file can be downloaded from the [Vitis Embedded Platforms](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/embedded-platforms/2022-1.html)
page.
Locate the image to the directory of your choice(e.g. /opt/platforms/), and adjust the configuration in 
[./common/configure/zcu102/configure.xml](./common/configure/zcu102/configure.xml) as below.
```xml
  <spec name = "sdk_dir"             value = "/opt/platforms/xilinx-zynqmp-common-v2022.1/environment-setup-cortexa72-cortexa53-xilinx-linux" />
```

### ZCU102 Base DFX platform
You can create ZCU102 Base DFX paltform from 
[Vitis Embedded Platform Source repo(2022.1 branch)](https://github.com/Xilinx/Vitis_Embedded_Platform_Source/tree/2022.1).
We slightly modified the floorplanning of ZCU102 Base DFX platform
to reserve more area for the dynamic region.
This can be done by replacing 
[this file](https://github.com/Xilinx/Vitis_Embedded_Platform_Source/blob/2022.1/Xilinx_Official_Platforms/xilinx_zcu102_base_dfx/hw/sources/constraints/static_impl_early.xdc) 
to our [modified xdc file](./common/etc/static_impl_early_22_1.xdc).
You can follow the instructions to generate the ZCU102 DFX platform.
For instance, 
```bash
cd ./Xilinx_Official_Platforms/xilinx_zcu102_base_dfx/
make all PREBUILT_LINUX_PATH=/opt/platforms/xilinx-zynqmp-common-v2022.1/
```

Once you successfully generated ZCU102 DFX platform, locate the generated platform to the directory of your choice(e.g. /opt/platforms/),
and adjust the configurations in [./common/configure/zcu102/configure.xml](./common/configure/zcu102/configure.xml) as below.
```xml
  <spec name = "PLATFORM_REPO_PATHS" value=  "/opt/platforms/xilinx_zcu102_base_dfx_202210_1" />
  <spec name = "ROOTFS"              value = "/opt/platforms/xilinx-zynqmp-common-v2022.1" />
  <spec name = "PLATFORM"            value = "xilinx_zcu102_base_dfx_202210_1" />
```

## Pre-generated overlay
[Generate Overlay](##-Generate-Overlay)
test

test

test

test


## Generated overlay
blah
