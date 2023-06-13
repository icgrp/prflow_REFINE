
set config_proj_name project_ConvolutionInputGenerator_0
puts "HLS project: $config_proj_name"
set config_hwsrcdir "/home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/ConvolutionInputGenerator_0_gssp6tm5"
puts "HW source dir: $config_hwsrcdir"
set config_proj_part "xczu9eg-ffvb1156-2-e"
set config_bnnlibdir "$::env(FINN_ROOT)/deps/finn-hlslib"
puts "finn-hlslib dir: $config_bnnlibdir"
set config_customhlsdir "$::env(FINN_ROOT)/custom_hls"
puts "custom HLS dir: $config_customhlsdir"
set config_toplevelfxn "ConvolutionInputGenerator_0"
set config_clkperiod 10.0

open_project $config_proj_name
add_files $config_hwsrcdir/top_ConvolutionInputGenerator_0.cpp -cflags "-std=c++14 -I$config_bnnlibdir -I$config_customhlsdir"

set_top $config_toplevelfxn
open_solution sol1
set_part $config_proj_part

set_param hls.enable_hidden_option_error false
config_compile -disable_unroll_code_size_check -pipeline_style flp
config_interface -m_axi_addr64
config_rtl -module_auto_prefix


create_clock -period $config_clkperiod -name default
csynth_design
export_design -format ip_catalog
exit 0
