STILL WIP

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
If you want to generate a new overlay from scratch, please refer to [Generate Overlay](#gen_overlay).
First, in your `/<PROJECT_DIR>/`, create `/<PROJECT_DIR>/workspace` directory.
Then, you can download pre-generated overlay from [here](https://drive.google.com/drive/folders/16sRIMmyqjawautBHWOcVuaYvhOsECIMo?usp=drive_link).
You will have one .img file and .zip file. 

### Copy abstract shells
Extract the downloaded .zip file. You will have `F001_overlay` folder. Copy this folder under `/<PROJECT_DIR>/workspace/` so that you have `/<PROJECT_DIR>/workspace/F001_overlay`.


## Run on the device

<a name="create_img"></a>
1. Use .img file either you downloaded or you generated to create boot image.
   In Ubuntu, run Startup Disk Creator, select .img file, select your sd card and click ``Make Startup Disk''.

2. Safely unplug the SD card from the workstation and slide it into the ZCU102. Power on the device.

3. You can refer to [this post](https://dj-park.github.io/posts/2022/1/scp-emb/) set up the ip addresses for the workstation and the ZCU102.





<a name="gen_overlay"></a>
## Generate overlay
Please take a look at [this repo](https://github.com/icgrp/prflow_nested_dfx) for the overview.

In your `/<PROJECT_DIR>/`, to generate `/<PROJECT_DIR>/workspace/F001_overlay` directory, run the command below.
Note that this process can take >4 hours depending on the system CPU/RAM because of the sequentialized charateristic of
Xilinx Nested DFX technology.

```
make overlay -j$(nproc)
```

You will encounter the error shown below.

![](images/overlay_gen_error.png)

We consider this as a potential bug in Vivado.
In this case, cd to `/<PROJECT_DIR>/workspace/F001_overlay/ydma/zcu102/400MHz/zcu102_dfx_manual/` and open up **Vivado GUI** with
`vivado &`. In Tcl console, manually copy and paste the contents of the scripts that encountered the errors as shown below.
**You need to run one command at a time instead of entering multiple lines of tcl commands.**

<p align="center"> <img src="images/vivado_gui_tcl.png"> </p>

With the given floorplanning(\*.xdc files), scripts that cause this error are:

- `/<PROJECT_DIR>/workspace/F001_overlay/ydma/zcu102/400MHz/zcu102_dfx_manual/tcl/nested/pr_recombine_p20.tcl`
- `/<PROJECT_DIR>/workspace/F001_overlay/ydma/zcu102/400MHz/zcu102_dfx_manual/tcl/nested/pr_recombine_p20_p1.tcl`

Once you manually generate `p20.dcp` and `p20_p1.dcp`, 
in `/<PROJECT_DIR>/workspace/F001_overlay/ydma/zcu102/400MHz/zcu102_dfx_manual/`,
do 
```
make all -j8
```
to run the rest of the Makefile. Note that the number 8 is an arbitrary value so that the script doesn't overutilize the system memory.
Once the Makefile finishes, 
in the same directory, run the rest of the commands in
`/<PROJECT_DIR>/workspace/F001_overlay/run.sh` that were supposed to run.
For instance, copy/paste the lines below in the terminal.
```
./shell/run_xclbin.sh
cp -r ../package ./overlay_p23/
cp ./overlay_p23/*.xclbin ./overlay_p23/package/sd_card
cd overlay_p23
cp ../util_scripts/get_blocked_resources_abs_shell.py .
cp ../util_scripts/parse_ovly_util.py .
cp ../util_scripts/blocked_analysis.py .
python get_blocked_resources_abs_shell.py
python parse_ovly_util.py
python blocked_analysis.py
```

This conclues overlay generation and creates `/<PROJECT_DIR>/workspace/F001_overlay/` directory.
Use `/<PROJECT_DIR>/workspace/F001_overlay/ydma/zcu102/400MHz/zcu102_dfx_manual/overlay_p23/package/sd_card.img`
to generate the boot image.



