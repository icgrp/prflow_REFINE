# Monitor points
set_property HDL_ATTRIBUTE.DPA_MONITOR true [get_bd_intf_pins /ydma_1/m_axi_aximm1]
set_property HDL_ATTRIBUTE.DPA_MONITOR true [get_bd_cells /ydma_1]
set_property HDL_ATTRIBUTE.DPA_MONITOR true [get_bd_intf_pins /ydma_1/m_axi_aximm2]

# Platform options
set_property HDL_ATTRIBUTE.DPA_AXILITE_MASTER true [get_bd_intf_pins /interconnect_axilite/M02_AXI]
set_property HDL_ATTRIBUTE.DPA_TRACE_SLAVE true [get_bd_intf_pins /interconnect_axifull/S01_AXI]

#Trace Dictionaries
set default_trace [dict create \
  MEM_SPACE HP3_DDR_LOW \
  MEM_INDEX 0 \
  MEM_TYPE HP \
  SLAVE /interconnect_axifull/S01_AXI \
];


# Call debug/profiling automation
set dpa_dict [list \
              [get_bd_intf_pins ydma_1/M_AXI_AXIMM1]  {TYPE data DETAIL all CLK_SRC /ydma_1/ap_clk RST_SRC /ydma_1/ap_rst_n MIN_ADDRESS {0xC0000000 0x0} MAX_ADDRESS {0xFFFFFFFFF 0x7FFFFFFF} MEMORY {HP HP0} PRINTABLE_KEY {[get_bd_intf_pins ydma_1/M_AXI_AXIMM1]} INS_MODE user} \
              [get_bd_cells /ydma_1]  {TYPE exec DETAIL all CLK_SRC /ydma_1/ap_clk RST_SRC /ydma_1/ap_rst_n PRINTABLE_KEY {[get_bd_cells /ydma_1]} INS_MODE user} \
              [get_bd_intf_pins ydma_1/M_AXI_AXIMM2]  {TYPE data DETAIL all CLK_SRC /ydma_1/ap_clk RST_SRC /ydma_1/ap_rst_n MIN_ADDRESS {0xC0000000 0x0} MAX_ADDRESS {0xFFFFFFFFF 0x7FFFFFFF} MEMORY {HP HP0} PRINTABLE_KEY {[get_bd_intf_pins ydma_1/M_AXI_AXIMM2]} INS_MODE user} \
             ]
set dpa_opts [list \
              SETTINGS  {HW_EMU false IS_EMBEDDED true VERSAL_DFX 0} \
              AIE_TRACE  {FIFO_DEPTH 4096 PACKET_RATE 0 CLK_SELECT default PROFILE_STREAMS 0 MEM_TYPE DDR MEM_SPACE MEM_SPACE_NOT_FOUND MEM_INDEX {}} \
              SYSTEM_DEADLOCK  {DEADLOCK_OPTION disable} \
              AXILITE  {MASTER /interconnect_axilite/M02_AXI CLK_SRC /ydma_1/ap_clk RST_SRC /ydma_1/ap_rst_n} \
              TRACE_OFFLOAD  $default_trace \
             ]

set_param bd.enable_dpa 1
set_param bd.debug_profile.script /home/dopark/workspace/zcu102_tuning/prflow_DSE_bi_22.1/workspace/F007_overlay_mono/ydma/zcu102/mono/_x/link/vivado/vpl/.local/debug_profile_automation.tcl
apply_bd_automation -rule xilinx.com:bd_rule:debug_profile -opts $dpa_opts -dict $dpa_dict

# Write debug_ip_layout
debug_profile::write_debug_ip_layout false "xilinx.com:xd:xilinx_zcu102_base_202210_1:202210.1" "/home/dopark/workspace/zcu102_tuning/prflow_DSE_bi_22.1/workspace/F007_overlay_mono/ydma/zcu102/mono/_x/link/int"
