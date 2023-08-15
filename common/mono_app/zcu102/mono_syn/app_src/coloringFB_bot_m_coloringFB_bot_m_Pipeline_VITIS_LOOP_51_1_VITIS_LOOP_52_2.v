// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.1 (64-bit)
// Version: 2022.1
// Copyright (C) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module coloringFB_bot_m_coloringFB_bot_m_Pipeline_VITIS_LOOP_51_1_VITIS_LOOP_52_2 (
        ap_clk,
        ap_rst,
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        Output_1_TREADY,
        Output_1_TDATA,
        Output_1_TVALID,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q0,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce1,
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q1
);

parameter    ap_ST_fsm_pp0_stage0 = 1'd1;

input   ap_clk;
input   ap_rst;
input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
input   Output_1_TREADY;
output  [127:0] Output_1_TDATA;
output   Output_1_TVALID;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q1;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address0;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce0;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q0;
output  [11:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address1;
output   coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce1;
input  [7:0] coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q1;

reg ap_idle;
reg Output_1_TVALID;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce1;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce0;
reg coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce1;

(* fsm_encoding = "none" *) reg   [0:0] ap_CS_fsm;
wire    ap_CS_fsm_pp0_stage0;
wire    ap_enable_reg_pp0_iter0;
reg    ap_enable_reg_pp0_iter1;
reg    ap_idle_pp0;
wire    ap_block_state1_pp0_stage0_iter0;
reg    ap_block_state2_pp0_stage0_iter1;
reg    ap_block_pp0_stage0_subdone;
wire   [0:0] icmp_ln51_fu_315_p2;
reg    ap_condition_exit_pp0_iter0_stage0;
wire    ap_loop_exit_ready;
reg    ap_ready_int;
reg    Output_1_TDATA_blk_n;
wire    ap_block_pp0_stage0;
reg    ap_block_pp0_stage0_11001;
wire   [63:0] zext_ln232_fu_385_p1;
wire   [63:0] zext_ln232_1_fu_411_p1;
reg   [7:0] j_fu_78;
wire   [7:0] add_ln52_fu_423_p2;
wire    ap_loop_init;
reg   [7:0] ap_sig_allocacmp_j_load;
reg   [8:0] i_fu_82;
wire   [8:0] select_ln51_1_fu_355_p3;
reg   [8:0] ap_sig_allocacmp_i_load;
reg   [11:0] indvar_flatten_fu_86;
wire   [11:0] add_ln51_1_fu_321_p2;
reg   [11:0] ap_sig_allocacmp_indvar_flatten_load;
reg    ap_block_pp0_stage0_01001;
wire   [0:0] tmp_fu_339_p3;
wire   [8:0] add_ln51_fu_333_p2;
wire   [7:0] select_ln51_fu_347_p3;
wire   [7:0] trunc_ln53_fu_363_p1;
wire   [3:0] lshr_ln1_fu_367_p4;
wire   [11:0] tmp_s_fu_377_p3;
wire   [3:0] or_ln232_fu_397_p2;
wire   [11:0] tmp_1_fu_403_p3;
reg    ap_done_reg;
wire    ap_continue_int;
reg    ap_done_int;
reg   [0:0] ap_NS_fsm;
wire    ap_enable_pp0;
wire    ap_start_int;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_CS_fsm = 1'd1;
#0 ap_enable_reg_pp0_iter1 = 1'b0;
#0 ap_done_reg = 1'b0;
end

coloringFB_bot_m_flow_control_loop_pipe_sequential_init flow_control_loop_pipe_sequential_init_U(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst),
    .ap_start(ap_start),
    .ap_ready(ap_ready),
    .ap_done(ap_done),
    .ap_start_int(ap_start_int),
    .ap_loop_init(ap_loop_init),
    .ap_ready_int(ap_ready_int),
    .ap_loop_exit_ready(ap_condition_exit_pp0_iter0_stage0),
    .ap_loop_exit_done(ap_done_int),
    .ap_continue_int(ap_continue_int),
    .ap_done_int(ap_done_int)
);

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_CS_fsm <= ap_ST_fsm_pp0_stage0;
    end else begin
        ap_CS_fsm <= ap_NS_fsm;
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_done_reg <= 1'b0;
    end else begin
        if ((ap_continue_int == 1'b1)) begin
            ap_done_reg <= 1'b0;
        end else if (((ap_loop_exit_ready == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_enable_reg_pp0_iter1 <= 1'b0;
    end else begin
        if ((1'b1 == ap_condition_exit_pp0_iter0_stage0)) begin
            ap_enable_reg_pp0_iter1 <= 1'b0;
        end else if (((1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
            ap_enable_reg_pp0_iter1 <= ap_start_int;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln51_fu_315_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            i_fu_82 <= select_ln51_1_fu_355_p3;
        end else if ((ap_loop_init == 1'b1)) begin
            i_fu_82 <= 9'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln51_fu_315_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            indvar_flatten_fu_86 <= add_ln51_1_fu_321_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            indvar_flatten_fu_86 <= 12'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        if (((icmp_ln51_fu_315_p2 == 1'd0) & (ap_enable_reg_pp0_iter0 == 1'b1))) begin
            j_fu_78 <= add_ln52_fu_423_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            j_fu_78 <= 8'd0;
        end
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        Output_1_TDATA_blk_n = Output_1_TREADY;
    end else begin
        Output_1_TDATA_blk_n = 1'b1;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        Output_1_TVALID = 1'b1;
    end else begin
        Output_1_TVALID = 1'b0;
    end
end

always @ (*) begin
    if (((icmp_ln51_fu_315_p2 == 1'd1) & (1'b0 == ap_block_pp0_stage0_subdone) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b1;
    end else begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b0;
    end
end

always @ (*) begin
    if (((ap_loop_exit_ready == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_done_int = 1'b1;
    end else begin
        ap_done_int = ap_done_reg;
    end
end

always @ (*) begin
    if (((ap_start_int == 1'b0) & (ap_idle_pp0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter1 == 1'b0) & (ap_enable_reg_pp0_iter0 == 1'b0))) begin
        ap_idle_pp0 = 1'b1;
    end else begin
        ap_idle_pp0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_subdone) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_ready_int = 1'b1;
    end else begin
        ap_ready_int = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_init == 1'b1))) begin
        ap_sig_allocacmp_i_load = 9'd0;
    end else begin
        ap_sig_allocacmp_i_load = i_fu_82;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_init == 1'b1))) begin
        ap_sig_allocacmp_indvar_flatten_load = 12'd0;
    end else begin
        ap_sig_allocacmp_indvar_flatten_load = indvar_flatten_fu_86;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0) & (1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_init == 1'b1))) begin
        ap_sig_allocacmp_j_load = 8'd0;
    end else begin
        ap_sig_allocacmp_j_load = j_fu_78;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_ce1 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce0 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == ap_block_pp0_stage0_11001) & (ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce1 = 1'b1;
    end else begin
        coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_ce1 = 1'b0;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_pp0_stage0 : begin
            ap_NS_fsm = ap_ST_fsm_pp0_stage0;
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign Output_1_TDATA = {{{{{{{{{{{{{{{{coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q0}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q0}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_q1}}, {coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_q1}};

assign add_ln51_1_fu_321_p2 = (ap_sig_allocacmp_indvar_flatten_load + 12'd1);

assign add_ln51_fu_333_p2 = (ap_sig_allocacmp_i_load + 9'd1);

assign add_ln52_fu_423_p2 = (select_ln51_fu_347_p3 + 8'd16);

assign ap_CS_fsm_pp0_stage0 = ap_CS_fsm[32'd0];

assign ap_block_pp0_stage0 = ~(1'b1 == 1'b1);

always @ (*) begin
    ap_block_pp0_stage0_01001 = ((1'b0 == Output_1_TREADY) & (ap_enable_reg_pp0_iter1 == 1'b1));
end

always @ (*) begin
    ap_block_pp0_stage0_11001 = ((1'b0 == Output_1_TREADY) & (ap_enable_reg_pp0_iter1 == 1'b1));
end

always @ (*) begin
    ap_block_pp0_stage0_subdone = ((1'b0 == Output_1_TREADY) & (ap_enable_reg_pp0_iter1 == 1'b1));
end

assign ap_block_state1_pp0_stage0_iter0 = ~(1'b1 == 1'b1);

always @ (*) begin
    ap_block_state2_pp0_stage0_iter1 = (1'b0 == Output_1_TREADY);
end

assign ap_enable_pp0 = (ap_idle_pp0 ^ 1'b1);

assign ap_enable_reg_pp0_iter0 = ap_start_int;

assign ap_loop_exit_ready = ap_condition_exit_pp0_iter0_stage0;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_1_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_2_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_3_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_4_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_5_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_6_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_7_address1 = zext_ln232_fu_385_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address0 = zext_ln232_1_fu_411_p1;

assign coloringFB_bot_m_stream_ap_uint_32_0_stream_ap_uint_128_0_frame_buffer_address1 = zext_ln232_fu_385_p1;

assign icmp_ln51_fu_315_p2 = ((ap_sig_allocacmp_indvar_flatten_load == 12'd2048) ? 1'b1 : 1'b0);

assign lshr_ln1_fu_367_p4 = {{select_ln51_fu_347_p3[6:3]}};

assign or_ln232_fu_397_p2 = (lshr_ln1_fu_367_p4 | 4'd1);

assign select_ln51_1_fu_355_p3 = ((tmp_fu_339_p3[0:0] == 1'b1) ? add_ln51_fu_333_p2 : ap_sig_allocacmp_i_load);

assign select_ln51_fu_347_p3 = ((tmp_fu_339_p3[0:0] == 1'b1) ? 8'd0 : ap_sig_allocacmp_j_load);

assign tmp_1_fu_403_p3 = {{trunc_ln53_fu_363_p1}, {or_ln232_fu_397_p2}};

assign tmp_fu_339_p3 = ap_sig_allocacmp_j_load[32'd7];

assign tmp_s_fu_377_p3 = {{trunc_ln53_fu_363_p1}, {lshr_ln1_fu_367_p4}};

assign trunc_ln53_fu_363_p1 = select_ln51_1_fu_355_p3[7:0];

assign zext_ln232_1_fu_411_p1 = tmp_1_fu_403_p3;

assign zext_ln232_fu_385_p1 = tmp_s_fu_377_p3;

endmodule //coloringFB_bot_m_coloringFB_bot_m_Pipeline_VITIS_LOOP_51_1_VITIS_LOOP_52_2