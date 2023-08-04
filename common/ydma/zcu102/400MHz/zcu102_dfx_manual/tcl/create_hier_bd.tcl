# This tcl script creates a single hierarchical cell for non-Vitis-kernel cell in Vivado block diagram.
# This step is necessary to include non-Vitis-kernel cell as a reconfigurable module to remove static routing on PR regions.

open_project PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.xpr

open_bd_design {PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd}

add_files -norecurse {PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_hls_deadlock_report_unit.vh PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_hls_deadlock_detector.vh}
add_files -norecurse {PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_31_1_proc1_Pipeline_VITIS_LOOP_31_1.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/write_b_in.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/converge_ctrl.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/bft.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Output_Port_Cluster.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Stream_Flow_Control_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_35_3_proc3.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/SynFIFO.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_31_1_proc1.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/leaf_interface_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/write_b_out.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_32_2_proc2.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_flow_control_loop_pipe_sequential_init.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Config_Controls_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/stream_shell.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_fifo_w64_d3_S.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Input_Port_Cluster_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ExtractCtrl.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/page_quad_bb.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_start_for_Loop_VITIS_LOOP_32_2_proc2_U0.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Input_Port_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/page_bb.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_36_4_proc4.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_32_2_proc2_Pipeline_VITIS_LOOP_32_2.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/single_ram.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Output_Port_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_v1_buffer_V_RAM_AUTO_1R1W.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_entry_proc.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_control_s_axi.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/rest_400MHz.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_36_4_proc4_Pipeline_VITIS_LOOP_36_4.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/PR_pages_top.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Output_Port_Cluster_ydma.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_regslice_both.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_start_for_Loop_VITIS_LOOP_36_4_proc4_U0.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_Loop_VITIS_LOOP_35_3_proc3_Pipeline_VITIS_LOOP_35_3.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_config_parser_Pipeline_VITIS_LOOP_41_2.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/read_b_in.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/data32to512_data32to512_Pipeline_VITIS_LOOP_175_1.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/data32to512_regslice_both.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/Output_Port.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_aximm1_m_axi.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/data32to512_flow_control_loop_pipe_sequential_init.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_config_parser_Pipeline_VITIS_LOOP_70_6.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/leaf_interface_wrapper1.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_config_parser_Pipeline_VITIS_LOOP_61_5.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_fifo_w32_d3_S.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_aximm2_m_axi.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_fifo_w512_d1024_A.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_config_parser_Pipeline_VITIS_LOOP_54_4.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ram0.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_fifo_w64_d512_A.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/data32to512.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/page_double_bb.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_hls_deadlock_detection_unit.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/ydma_flow_control_loop_pipe_sequential_init.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/config_parser_config_parser_Pipeline_VITIS_LOOP_35_1.v PRJ_BOARD_FREQ_DIR/zcu102_dfx_manual/src4level2/ydma_bb/rise_detect.v}

set_property source_mgmt_mode All [current_project]
create_bd_cell -type module -reference rest_400MHz rest_400MHz_0
create_bd_cell -type module -reference PR_pages_top PR_pages_top_0

delete_bd_objs [get_bd_nets ydma_1_interrupt]
connect_bd_net [get_bd_pins rest_400MHz_0/interrupt] [get_bd_pins interrupt_concat/In0]

delete_bd_objs [get_bd_intf_nets ydma_1_m_axi_aximm2]
connect_bd_intf_net [get_bd_intf_pins rest_400MHz_0/m_axi_aximm2] -boundary_type upper [get_bd_intf_pins System_DPA/MON_M_AXI1]
connect_bd_intf_net [get_bd_intf_pins rest_400MHz_0/m_axi_aximm2] -boundary_type upper [get_bd_intf_pins interconnect_axifull_2_user_slr1/S02_AXI]
delete_bd_objs [get_bd_intf_nets ydma_1_m_axi_aximm1]
connect_bd_intf_net [get_bd_intf_pins rest_400MHz_0/m_axi_aximm1] -boundary_type upper [get_bd_intf_pins System_DPA/MON_M_AXI]
connect_bd_intf_net -boundary_type upper [get_bd_intf_pins interconnect_axifull_2_user_slr1/S01_AXI] [get_bd_intf_pins rest_400MHz_0/m_axi_aximm1]
delete_bd_objs [get_bd_intf_nets interconnect_axilite_user_slr1_M01_AXI]
connect_bd_intf_net [get_bd_intf_pins rest_400MHz_0/s_axi_control] -boundary_type upper [get_bd_intf_pins interconnect_axilite_user_slr1/M01_AXI]
connect_bd_intf_net -boundary_type upper [get_bd_intf_pins System_DPA/MON_S_AXI] [get_bd_intf_pins interconnect_axilite_user_slr1/M01_AXI]

set_property -dict [list CONFIG.CLK_DOMAIN {pfm_dynamic_clkwiz_kernel5_clk_out} CONFIG.FREQ_HZ {400000000}] [get_bd_intf_pins rest_400MHz_0/m_axi_aximm1]
set_property -dict [list CONFIG.CLK_DOMAIN {pfm_dynamic_clkwiz_kernel5_clk_out} CONFIG.FREQ_HZ {400000000}] [get_bd_intf_pins rest_400MHz_0/m_axi_aximm2]
set_property -dict [list CONFIG.CLK_DOMAIN {pfm_dynamic_clkwiz_kernel5_clk_out} CONFIG.FREQ_HZ {400000000}] [get_bd_intf_pins rest_400MHz_0/s_axi_control]
connect_bd_net [get_bd_ports clkwiz_kernel5_clk_out] [get_bd_pins rest_400MHz_0/ap_clk]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n] [get_bd_pins reset_controllers/peripheral_aresetn]


# carefully generate clock with clocking wizard!
startgroup
create_bd_cell -type ip -vlnv xilinx.com:ip:clk_wiz:6.0 clk_wiz_0
endgroup
set_property -dict [list CONFIG.PRIM_IN_FREQ.VALUE_SRC USER] [get_bd_cells clk_wiz_0]
set_property -dict [list CONFIG.PRIM_IN_FREQ {75} CONFIG.CLKOUT2_USED {true} CONFIG.CLK_OUT1_PORT {clk_250} CONFIG.CLK_OUT2_PORT {clk_350} CONFIG.CLKOUT1_REQUESTED_OUT_FREQ {250} CONFIG.CLKOUT2_REQUESTED_OUT_FREQ {350} CONFIG.USE_LOCKED {false} CONFIG.RESET_TYPE {ACTIVE_LOW} CONFIG.CLKIN1_JITTER_PS {133.33} CONFIG.MMCM_DIVCLK_DIVIDE {1} CONFIG.MMCM_CLKFBOUT_MULT_F {18.750} CONFIG.MMCM_CLKIN1_PERIOD {13.333} CONFIG.MMCM_CLKIN2_PERIOD {10.0} CONFIG.MMCM_CLKOUT0_DIVIDE_F {5.625} CONFIG.MMCM_CLKOUT1_DIVIDE {4} CONFIG.NUM_OUT_CLKS {2} CONFIG.RESET_PORT {resetn} CONFIG.CLKOUT1_JITTER {90.608} CONFIG.CLKOUT1_PHASE_ERROR {104.999} CONFIG.CLKOUT2_JITTER {85.589} CONFIG.CLKOUT2_PHASE_ERROR {104.999}] [get_bd_cells clk_wiz_0]
connect_bd_net [get_bd_ports clkwiz_sysclks_clk_out2] [get_bd_pins clk_wiz_0/clk_in1]
connect_bd_net [get_bd_pins clk_wiz_0/resetn] [get_bd_pins reset_controllers/peripheral_aresetn]


connect_bd_net [get_bd_ports clkwiz_kernel5_clk_out] [get_bd_pins PR_pages_top_0/clk_400]
connect_bd_net [get_bd_pins clk_wiz_0/clk_350] [get_bd_pins PR_pages_top_0/clk_350]
connect_bd_net [get_bd_ports clkwiz_kernel2_clk_out1] [get_bd_pins PR_pages_top_0/clk_300]
connect_bd_net [get_bd_pins PR_pages_top_0/clk_250] [get_bd_pins clk_wiz_0/clk_250]
connect_bd_net [get_bd_ports clkwiz_kernel4_clk_out] [get_bd_pins PR_pages_top_0/clk_200]


connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p2] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p2]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p3] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p3]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p4] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p4]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p5] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p5]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p6] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p6]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p7] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p7]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p8] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p8]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p9] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p9]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p10] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p10]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p11] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p11]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p12] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p12]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p13] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p13]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p14] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p14]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p15] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p15]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p16] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p16]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p17] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p17]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p18] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p18]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p19] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p19]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p20] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p20]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p21] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p21]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p22] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p22]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_rst_n_inv_400_p23] [get_bd_pins PR_pages_top_0/ap_rst_n_inv_400_p23]

connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p2] [get_bd_pins PR_pages_top_0/ap_start_400_p2]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p3] [get_bd_pins PR_pages_top_0/ap_start_400_p3]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p4] [get_bd_pins PR_pages_top_0/ap_start_400_p4]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p5] [get_bd_pins PR_pages_top_0/ap_start_400_p5]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p6] [get_bd_pins PR_pages_top_0/ap_start_400_p6]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p7] [get_bd_pins PR_pages_top_0/ap_start_400_p7]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p8] [get_bd_pins PR_pages_top_0/ap_start_400_p8]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p9] [get_bd_pins PR_pages_top_0/ap_start_400_p9]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p10] [get_bd_pins PR_pages_top_0/ap_start_400_p10]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p11] [get_bd_pins PR_pages_top_0/ap_start_400_p11]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p12] [get_bd_pins PR_pages_top_0/ap_start_400_p12]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p13] [get_bd_pins PR_pages_top_0/ap_start_400_p13]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p14] [get_bd_pins PR_pages_top_0/ap_start_400_p14]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p15] [get_bd_pins PR_pages_top_0/ap_start_400_p15]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p16] [get_bd_pins PR_pages_top_0/ap_start_400_p16]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p17] [get_bd_pins PR_pages_top_0/ap_start_400_p17]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p18] [get_bd_pins PR_pages_top_0/ap_start_400_p18]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p19] [get_bd_pins PR_pages_top_0/ap_start_400_p19]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p20] [get_bd_pins PR_pages_top_0/ap_start_400_p20]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p21] [get_bd_pins PR_pages_top_0/ap_start_400_p21]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p22] [get_bd_pins PR_pages_top_0/ap_start_400_p22]
connect_bd_net [get_bd_pins rest_400MHz_0/ap_start_400_p23] [get_bd_pins PR_pages_top_0/ap_start_400_p23]


connect_bd_net [get_bd_pins rest_400MHz_0/resend_2] [get_bd_pins PR_pages_top_0/resend_2]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_3] [get_bd_pins PR_pages_top_0/resend_3]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_4] [get_bd_pins PR_pages_top_0/resend_4]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_5] [get_bd_pins PR_pages_top_0/resend_5]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_6] [get_bd_pins PR_pages_top_0/resend_6]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_7] [get_bd_pins PR_pages_top_0/resend_7]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_8] [get_bd_pins PR_pages_top_0/resend_8]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_9] [get_bd_pins PR_pages_top_0/resend_9]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_10] [get_bd_pins PR_pages_top_0/resend_10]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_11] [get_bd_pins PR_pages_top_0/resend_11]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_12] [get_bd_pins PR_pages_top_0/resend_12]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_13] [get_bd_pins PR_pages_top_0/resend_13]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_14] [get_bd_pins PR_pages_top_0/resend_14]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_15] [get_bd_pins PR_pages_top_0/resend_15]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_16] [get_bd_pins PR_pages_top_0/resend_16]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_17] [get_bd_pins PR_pages_top_0/resend_17]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_18] [get_bd_pins PR_pages_top_0/resend_18]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_19] [get_bd_pins PR_pages_top_0/resend_19]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_20] [get_bd_pins PR_pages_top_0/resend_20]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_21] [get_bd_pins PR_pages_top_0/resend_21]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_22] [get_bd_pins PR_pages_top_0/resend_22]
connect_bd_net [get_bd_pins rest_400MHz_0/resend_23] [get_bd_pins PR_pages_top_0/resend_23]

connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_2] [get_bd_pins PR_pages_top_0/din_leaf_2]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_3] [get_bd_pins PR_pages_top_0/din_leaf_3]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_4] [get_bd_pins PR_pages_top_0/din_leaf_4]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_5] [get_bd_pins PR_pages_top_0/din_leaf_5]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_6] [get_bd_pins PR_pages_top_0/din_leaf_6]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_7] [get_bd_pins PR_pages_top_0/din_leaf_7]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_8] [get_bd_pins PR_pages_top_0/din_leaf_8]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_9] [get_bd_pins PR_pages_top_0/din_leaf_9]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_10] [get_bd_pins PR_pages_top_0/din_leaf_10]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_11] [get_bd_pins PR_pages_top_0/din_leaf_11]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_12] [get_bd_pins PR_pages_top_0/din_leaf_12]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_13] [get_bd_pins PR_pages_top_0/din_leaf_13]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_14] [get_bd_pins PR_pages_top_0/din_leaf_14]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_15] [get_bd_pins PR_pages_top_0/din_leaf_15]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_16] [get_bd_pins PR_pages_top_0/din_leaf_16]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_17] [get_bd_pins PR_pages_top_0/din_leaf_17]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_18] [get_bd_pins PR_pages_top_0/din_leaf_18]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_19] [get_bd_pins PR_pages_top_0/din_leaf_19]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_20] [get_bd_pins PR_pages_top_0/din_leaf_20]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_21] [get_bd_pins PR_pages_top_0/din_leaf_21]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_22] [get_bd_pins PR_pages_top_0/din_leaf_22]
connect_bd_net [get_bd_pins rest_400MHz_0/din_leaf_23] [get_bd_pins PR_pages_top_0/din_leaf_23]

connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_2] [get_bd_pins rest_400MHz_0/dout_leaf_2]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_3] [get_bd_pins rest_400MHz_0/dout_leaf_3]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_4] [get_bd_pins rest_400MHz_0/dout_leaf_4]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_5] [get_bd_pins rest_400MHz_0/dout_leaf_5]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_6] [get_bd_pins rest_400MHz_0/dout_leaf_6]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_7] [get_bd_pins rest_400MHz_0/dout_leaf_7]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_8] [get_bd_pins rest_400MHz_0/dout_leaf_8]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_9] [get_bd_pins rest_400MHz_0/dout_leaf_9]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_10] [get_bd_pins rest_400MHz_0/dout_leaf_10]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_11] [get_bd_pins rest_400MHz_0/dout_leaf_11]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_12] [get_bd_pins rest_400MHz_0/dout_leaf_12]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_13] [get_bd_pins rest_400MHz_0/dout_leaf_13]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_14] [get_bd_pins rest_400MHz_0/dout_leaf_14]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_15] [get_bd_pins rest_400MHz_0/dout_leaf_15]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_16] [get_bd_pins rest_400MHz_0/dout_leaf_16]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_17] [get_bd_pins rest_400MHz_0/dout_leaf_17]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_18] [get_bd_pins rest_400MHz_0/dout_leaf_18]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_19] [get_bd_pins rest_400MHz_0/dout_leaf_19]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_20] [get_bd_pins rest_400MHz_0/dout_leaf_20]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_21] [get_bd_pins rest_400MHz_0/dout_leaf_21]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_22] [get_bd_pins rest_400MHz_0/dout_leaf_22]
connect_bd_net [get_bd_pins PR_pages_top_0/dout_leaf_23] [get_bd_pins rest_400MHz_0/dout_leaf_23]


delete_bd_objs [get_bd_cells ydma_1]


group_bd_cells hier_0 [get_bd_cells axi_mmu_4] [get_bd_cells axi_mmu_5] [get_bd_cells rest_400MHz_0] [get_bd_cells axi_gpio_null] [get_bd_cells axi_vip_hpm0fpd] [get_bd_cells axi_vip_ctrl_userpf] [get_bd_cells axi_register_slice_hpm0fpd] [get_bd_cells axi_vip_2] [get_bd_cells axi_vip_3] [get_bd_cells axi_mmu_2] [get_bd_cells axi_vip_4] [get_bd_cells axi_vip_5] [get_bd_cells axi_mmu_3] [get_bd_cells debug_bridge_xsdbm] [get_bd_cells axi_interconnect_hpm0fpd] [get_bd_cells reset_controllers] [get_bd_cells interconnect_axifull_2_user_slr1] [get_bd_cells interconnect_axifull_1_user_slr1] [get_bd_cells interrupt_concat] [get_bd_cells interconnect_axilite_user_slr1] [get_bd_cells axi_interconnect_0] [get_bd_cells axi_interconnect_1] [get_bd_cells System_DPA]

assign_bd_address -target_address_space /hier_0/rest_400MHz_0/m_axi_aximm1 [get_bd_addr_segs interconnect_aximm_ddrmem3_M00_AXI/Reg] -force
assign_bd_address -target_address_space /hier_0/rest_400MHz_0/m_axi_aximm2 [get_bd_addr_segs interconnect_aximm_ddrmem3_M00_AXI/Reg] -force
assign_bd_address -target_address_space /regslice_control_userpf_M_AXI [get_bd_addr_segs hier_0/rest_400MHz_0/s_axi_control/reg0] -force
set_property range 64K [get_bd_addr_segs {regslice_control_userpf_M_AXI/SEG_rest_400MHz_0_reg0}]
validate_bd_design

startgroup
set curdesign [current_bd_design]
create_bd_design -cell [get_bd_cells /hier_0] hier_0

current_bd_design $curdesign
set new_cell [create_bd_cell -type container -reference hier_0 hier_0_temp]
replace_bd_cell [get_bd_cells /hier_0] $new_cell
delete_bd_objs  [get_bd_cells /hier_0]
set_property name hier_0 $new_cell
endgroup

open_bd_design {PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd}

generate_target all [get_files -of_objects [get_reconfig_modules my_rm] PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd]


catch { config_ip_cache -export [get_ips -all hier_0_inst_0_xbar_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_hub_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_mon0_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_mon1_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_mon2_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_trace_s2mm_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_gpio_null_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_mmu_2_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_mmu_3_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_mmu_4_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_mmu_5_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_register_slice_hpm0fpd_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_2_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_3_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_4_0] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_5_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_ctrl_userpf_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_axi_vip_hpm0fpd_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_debug_bridge_xsdbm_0] }
catch { config_ip_cache -export [get_ips -all bd_93c6_xsdbm_0] }

catch { config_ip_cache -export [get_ips -all bd_93c6_lut_buffer_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_xbar_1] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_xbar_2] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_control_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel2_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel3_0] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel4_0] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel5_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_psreset_gate_pr_kernel6_0] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_rest_400MHz_0_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_20] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m00_regslice_8] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m01_regslice_4] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m02_regslice_4] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m03_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m04_regslice_0] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_14] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_15] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_16] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_17] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_18] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_us_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_rs_w_1] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s01_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_us_cc_df_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s02_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s02_data_fifo_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_cc_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s03_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_us_1] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_cc_1] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m00_regslice_6] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_ds_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_rs_w_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s00_regslice_19] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m00_regslice_7] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m01_regslice_3] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_cc_2] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_m02_regslice_3] }

catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_cc_3] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_mon1_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_dpa_mon2_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_debug_bridge_xsdbm_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_xbar_1] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_rest_400MHz_0_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s01_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_us_cc_df_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s02_regslice_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_s02_data_fifo_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_cc_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_ds_0] }
catch { config_ip_cache -export [get_ips -all hier_0_inst_0_auto_rs_w_0] }
catch { config_ip_cache -export [get_ips -all pfm_dynamic_PR_pages_top_0_0] }
catch { config_ip_cache -export [get_ips -all pfm_dynamic_clk_wiz_0_0] }


export_ip_user_files -of_objects [get_files -of_objects [get_reconfig_modules my_rm] PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd] -no_script -sync -force -quiet
create_ip_run [get_files -of_objects [get_reconfig_modules my_rm] PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd]
reset_run my_rm_synth_1
launch_runs my_rm_synth_1 hier_0_inst_0_dpa_mon1_0_synth_1 hier_0_inst_0_dpa_mon2_0_synth_1 hier_0_inst_0_debug_bridge_xsdbm_0_synth_1 hier_0_inst_0_xbar_1_synth_1 hier_0_inst_0_rest_400MHz_0_0_synth_1 hier_0_inst_0_s01_regslice_0_synth_1 hier_0_inst_0_auto_us_cc_df_0_synth_1 hier_0_inst_0_s02_regslice_0_synth_1 hier_0_inst_0_s02_data_fifo_0_synth_1 hier_0_inst_0_auto_cc_0_synth_1 hier_0_inst_0_auto_ds_0_synth_1 hier_0_inst_0_auto_rs_w_0_synth_1 pfm_dynamic_PR_pages_top_0_0_synth_1 pfm_dynamic_clk_wiz_0_0_synth_1 -jobs 8
wait_on_runs my_rm_synth_1 hier_0_inst_0_dpa_mon1_0_synth_1 hier_0_inst_0_dpa_mon2_0_synth_1 hier_0_inst_0_debug_bridge_xsdbm_0_synth_1 hier_0_inst_0_xbar_1_synth_1 hier_0_inst_0_rest_400MHz_0_0_synth_1 hier_0_inst_0_s01_regslice_0_synth_1 hier_0_inst_0_auto_us_cc_df_0_synth_1 hier_0_inst_0_s02_regslice_0_synth_1 hier_0_inst_0_s02_data_fifo_0_synth_1 hier_0_inst_0_auto_cc_0_synth_1 hier_0_inst_0_auto_ds_0_synth_1 hier_0_inst_0_auto_rs_w_0_synth_1 pfm_dynamic_PR_pages_top_0_0_synth_1 pfm_dynamic_clk_wiz_0_0_synth_1


export_simulation -of_objects [get_files -of_objects [get_reconfig_modules my_rm] PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.srcs/my_rm/bd/pfm_dynamic/pfm_dynamic.bd] -directory PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.ip_user_files/sim_scripts -ip_user_files_dir PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.ip_user_files -ipstatic_source_dir PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.ip_user_files/ipstatic -lib_map_path [list {modelsim=PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.cache/compile_simlib/modelsim} {questa=PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.cache/compile_simlib/questa} {xcelium=PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.cache/compile_simlib/xcelium} {vcs=PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.cache/compile_simlib/vcs} {riviera=PRJ_BOARD_FREQ_DIR/_x/link/vivado/vpl/prj/prj.cache/compile_simlib/riviera}] -use_ip_compiled_libs -force -quiet

save_bd_design