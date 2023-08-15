# This tcl script creates a single hierarchical cell for non-Vitis-kernel cell in Vivado block diagram.
# This step is necessary to include non-Vitis-kernel cell as a reconfigurable module to remove static routing on PR regions.


open_project PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.xpr

update_compile_order -fileset sources_1
open_bd_design {PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/sources_1/bd/vitis_design/vitis_design.bd}

add_files -norecurse {PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_hls_deadlock_report_unit.vh PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_hls_deadlock_detector.vh}
add_files -norecurse {PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_aximm1_m_axi.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_aximm2_m_axi.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_start_for_Loop_VITIS_LOOP_32_2_proc2_U0.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_36_4_proc4.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_hls_deadlock_detection_unit.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_fifo_w64_d3_S.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_32_2_proc2.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_35_3_proc3.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_mono.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_start_for_Loop_VITIS_LOOP_36_4_proc4_U0.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_31_1_proc1_Pipeline_VITIS_LOOP_31_1.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_35_3_proc3_Pipeline_VITIS_LOOP_35_3.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_36_4_proc4_Pipeline_VITIS_LOOP_36_4.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_entry_proc.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_control_s_axi.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_31_1_proc1.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_Loop_VITIS_LOOP_32_2_proc2_Pipeline_VITIS_LOOP_32_2.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_fifo_w32_d3_S.v PRJ_BOARD_FREQ_DIR/overlay_mono/bd_src/ydma_flow_control_loop_pipe_sequential_init.v}
update_compile_order -fileset sources_1


create_bd_cell -type module -reference ydma_mono ydma_mono_0


delete_bd_objs [get_bd_nets ydma_1_interrupt]
connect_bd_net [get_bd_pins axi_intc_0_intr_1_interrupt_concat/In1] [get_bd_pins ydma_mono_0/interrupt]
disconnect_bd_intf_net [get_bd_intf_net ydma_1_m_axi_aximm1] [get_bd_intf_pins ydma_1/m_axi_aximm1]
disconnect_bd_intf_net [get_bd_intf_net ydma_1_m_axi_aximm2] [get_bd_intf_pins ydma_1/m_axi_aximm2]
connect_bd_intf_net [get_bd_intf_pins ydma_mono_0/m_axi_aximm1] -boundary_type upper [get_bd_intf_pins axi_ic_ps_e_S_AXI_HP0_FPD/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins ydma_mono_0/m_axi_aximm2] -boundary_type upper [get_bd_intf_pins axi_ic_ps_e_S_AXI_HP0_FPD/S01_AXI]

disconnect_bd_intf_net [get_bd_intf_net interconnect_axilite_M01_AXI] [get_bd_intf_pins ydma_1/s_axi_control]
connect_bd_intf_net [get_bd_intf_pins ydma_mono_0/s_axi_control] -boundary_type upper [get_bd_intf_pins interconnect_axilite/M01_AXI]

set_property -dict [list CONFIG.CLK_DOMAIN {vitis_design_clk_wiz_0_0_clk_out1} CONFIG.FREQ_HZ {300000000}] [get_bd_intf_pins ydma_mono_0/s_axi_control]
set_property -dict [list CONFIG.CLK_DOMAIN {vitis_design_clk_wiz_0_0_clk_out1} CONFIG.FREQ_HZ {300000000}] [get_bd_intf_pins ydma_mono_0/m_axi_aximm1]
set_property -dict [list CONFIG.CLK_DOMAIN {vitis_design_clk_wiz_0_0_clk_out1} CONFIG.FREQ_HZ {300000000}] [get_bd_intf_pins ydma_mono_0/m_axi_aximm2]
connect_bd_net [get_bd_pins ydma_mono_0/ap_rst_n] [get_bd_pins proc_sys_reset_1/peripheral_aresetn]


startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:6.0 clk_wiz_1
endgroup
connect_bd_net [get_bd_pins clk_wiz_1/clk_in1] [get_bd_pins ps_e/pl_clk0]
startgroup
set_property -dict [list CONFIG.CLKOUT2_USED {true} CONFIG.CLK_OUT1_PORT {clk_250} CONFIG.CLK_OUT2_PORT {clk_350} CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {250} CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {350} CONFIG.USE_LOCKED {false} CONFIG.RESET_TYPE {ACTIVE_LOW} CONFIG.MMCM_DIVCLK_DIVIDE {2} CONFIG.MMCM_CLKFBOUT_MULT_F {28.125} CONFIG.MMCM_CLKOUT0_DIVIDE_F {5.625} CONFIG.MMCM_CLKOUT1_DIVIDE {4} CONFIG.NUM_OUT_CLKS {2} CONFIG.RESET_PORT {resetn} CONFIG.CLKOUT1_JITTER {102.028} CONFIG.CLKOUT1_PHASE_ERROR {137.463} CONFIG.CLKOUT2_JITTER {96.661} CONFIG.CLKOUT2_PHASE_ERROR {137.463}] [get_bd_cells clk_wiz_1]
endgroup
connect_bd_net [get_bd_pins clk_wiz_1/resetn] [get_bd_pins ps_e/pl_resetn0]
connect_bd_net [get_bd_pins clk_wiz_1/clk_250] [get_bd_pins ydma_mono_0/clk_250]
connect_bd_net [get_bd_pins clk_wiz_1/clk_350] [get_bd_pins ydma_mono_0/clk_350]
connect_bd_net [get_bd_pins ydma_mono_0/clk_200] [get_bd_pins clk_wiz_0/clk_out5]
connect_bd_net [get_bd_pins ydma_mono_0/clk_300] [get_bd_pins clk_wiz_0/clk_out2]
connect_bd_net [get_bd_pins ydma_mono_0/clk_400] [get_bd_pins clk_wiz_0/clk_out6]

delete_bd_objs [get_bd_cells ydma_1]

assign_bd_address
set_property range 64K [get_bd_addr_segs {ps_e/Data/SEG_ydma_mono_0_reg0}]


validate_bd_design
reset_run vitis_design_xbar_1_synth_1
reset_run vitis_design_dpa_mon1_0_0_synth_1
reset_run vitis_design_dpa_mon1_1_0_synth_1
reset_run vitis_design_dpa_mon2_0_0_synth_1
reset_run vitis_design_dpa_mon2_1_0_synth_1
save_bd_design
reset_run synth_1
launch_runs synth_1 -jobs 8
# 8 jobs to be safe

wait_on_runs synth_1

