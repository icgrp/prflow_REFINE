// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.1 (64-bit)
// Version: 2022.1
// Copyright (C) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module coloringFB_top_m_coloringFB_top_m_Pipeline_RECV (
        ap_clk,
        ap_rst,
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        Input_2_TVALID,
        Output_1_TREADY,
        Input_2_TDATA,
        Input_2_TREADY,
        Output_1_TDATA,
        Output_1_TVALID
);

parameter    ap_ST_fsm_state1 = 4'd1;
parameter    ap_ST_fsm_state2 = 4'd2;
parameter    ap_ST_fsm_state3 = 4'd4;
parameter    ap_ST_fsm_state4 = 4'd8;

input   ap_clk;
input   ap_rst;
input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
input   Input_2_TVALID;
input   Output_1_TREADY;
input  [127:0] Input_2_TDATA;
output   Input_2_TREADY;
output  [511:0] Output_1_TDATA;
output   Output_1_TVALID;

reg ap_idle;
reg Input_2_TREADY;
reg Output_1_TVALID;

(* fsm_encoding = "none" *) reg   [3:0] ap_CS_fsm;
wire    ap_CS_fsm_state1;
wire   [0:0] tmp_fu_67_p3;
reg    ap_block_state1_pp0_stage0_iter0;
reg    ap_condition_exit_pp0_iter0_stage0;
wire    ap_loop_exit_ready;
reg    ap_ready_int;
wire    ap_CS_fsm_state4;
reg    ap_block_state4_pp0_stage3_iter0;
reg    Input_2_TDATA_blk_n;
wire    ap_CS_fsm_state2;
wire    ap_CS_fsm_state3;
reg    Output_1_TDATA_blk_n;
reg   [127:0] tmp_5_reg_106;
reg   [127:0] tmp_6_reg_111;
reg    ap_block_state2_pp0_stage1_iter0;
reg   [127:0] tmp_7_reg_116;
reg    ap_block_state3_pp0_stage2_iter0;
reg   [5:0] k_fu_42;
wire   [5:0] k_3_fu_75_p2;
wire    ap_loop_init;
reg   [5:0] ap_sig_allocacmp_k_2;
reg    ap_done_reg;
wire    ap_continue_int;
reg    ap_done_int;
reg   [3:0] ap_NS_fsm;
reg    ap_ST_fsm_state1_blk;
reg    ap_ST_fsm_state2_blk;
reg    ap_ST_fsm_state3_blk;
reg    ap_ST_fsm_state4_blk;
wire    ap_start_int;
reg    ap_condition_144;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_CS_fsm = 4'd1;
#0 ap_done_reg = 1'b0;
end

coloringFB_top_m_flow_control_loop_pipe_sequential_init flow_control_loop_pipe_sequential_init_U(
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
        ap_CS_fsm <= ap_ST_fsm_state1;
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
        end else if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (ap_loop_exit_ready == 1'b1) & (1'b1 == ap_CS_fsm_state1))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if ((1'b1 == ap_condition_144)) begin
        if ((tmp_fu_67_p3 == 1'd0)) begin
            k_fu_42 <= k_3_fu_75_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            k_fu_42 <= 6'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (tmp_fu_67_p3 == 1'd0) & (1'b1 == ap_CS_fsm_state1))) begin
        tmp_5_reg_106 <= Input_2_TDATA;
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_state2) & (1'b1 == Input_2_TVALID))) begin
        tmp_6_reg_111 <= Input_2_TDATA;
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_state3) & (1'b1 == Input_2_TVALID))) begin
        tmp_7_reg_116 <= Input_2_TDATA;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state3) | (1'b1 == ap_CS_fsm_state2) | (1'b1 == ap_CS_fsm_state4) | ((tmp_fu_67_p3 == 1'd0) & (1'b1 == ap_CS_fsm_state1) & (ap_start_int == 1'b1)))) begin
        Input_2_TDATA_blk_n = Input_2_TVALID;
    end else begin
        Input_2_TDATA_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((((1'b1 == ap_CS_fsm_state3) & (1'b1 == Input_2_TVALID)) | ((1'b1 == ap_CS_fsm_state2) & (1'b1 == Input_2_TVALID)) | (~((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID)) & (1'b1 == ap_CS_fsm_state4)) | (~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (tmp_fu_67_p3 == 1'd0) & (1'b1 == ap_CS_fsm_state1)))) begin
        Input_2_TREADY = 1'b1;
    end else begin
        Input_2_TREADY = 1'b0;
    end
end

always @ (*) begin
    if ((1'b1 == ap_CS_fsm_state4)) begin
        Output_1_TDATA_blk_n = Output_1_TREADY;
    end else begin
        Output_1_TDATA_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((~((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID)) & (1'b1 == ap_CS_fsm_state4))) begin
        Output_1_TVALID = 1'b1;
    end else begin
        Output_1_TVALID = 1'b0;
    end
end

always @ (*) begin
    if (((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0)))) begin
        ap_ST_fsm_state1_blk = 1'b1;
    end else begin
        ap_ST_fsm_state1_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Input_2_TVALID)) begin
        ap_ST_fsm_state2_blk = 1'b1;
    end else begin
        ap_ST_fsm_state2_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Input_2_TVALID)) begin
        ap_ST_fsm_state3_blk = 1'b1;
    end else begin
        ap_ST_fsm_state3_blk = 1'b0;
    end
end

always @ (*) begin
    if (((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID))) begin
        ap_ST_fsm_state4_blk = 1'b1;
    end else begin
        ap_ST_fsm_state4_blk = 1'b0;
    end
end

always @ (*) begin
    if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (tmp_fu_67_p3 == 1'd1) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b1;
    end else begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b0;
    end
end

always @ (*) begin
    if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (ap_loop_exit_ready == 1'b1) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_done_int = 1'b1;
    end else begin
        ap_done_int = ap_done_reg;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state1) & (ap_start_int == 1'b0))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if ((~((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID)) & (1'b1 == ap_CS_fsm_state4))) begin
        ap_ready_int = 1'b1;
    end else begin
        ap_ready_int = 1'b0;
    end
end

always @ (*) begin
    if (((ap_loop_init == 1'b1) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_sig_allocacmp_k_2 = 6'd0;
    end else begin
        ap_sig_allocacmp_k_2 = k_fu_42;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_state1 : begin
            if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (tmp_fu_67_p3 == 1'd1) & (1'b1 == ap_CS_fsm_state1))) begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end else if ((~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (1'b1 == ap_CS_fsm_state1))) begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end
        end
        ap_ST_fsm_state2 : begin
            if (((1'b1 == ap_CS_fsm_state2) & (1'b1 == Input_2_TVALID))) begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end
        end
        ap_ST_fsm_state3 : begin
            if (((1'b1 == ap_CS_fsm_state3) & (1'b1 == Input_2_TVALID))) begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end
        end
        ap_ST_fsm_state4 : begin
            if ((~((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID)) & (1'b1 == ap_CS_fsm_state4))) begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign Output_1_TDATA = {{{{Input_2_TDATA}, {tmp_7_reg_116}}, {tmp_6_reg_111}}, {tmp_5_reg_106}};

assign ap_CS_fsm_state1 = ap_CS_fsm[32'd0];

assign ap_CS_fsm_state2 = ap_CS_fsm[32'd1];

assign ap_CS_fsm_state3 = ap_CS_fsm[32'd2];

assign ap_CS_fsm_state4 = ap_CS_fsm[32'd3];

always @ (*) begin
    ap_block_state1_pp0_stage0_iter0 = ((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0)));
end

always @ (*) begin
    ap_block_state2_pp0_stage1_iter0 = (1'b0 == Input_2_TVALID);
end

always @ (*) begin
    ap_block_state3_pp0_stage2_iter0 = (1'b0 == Input_2_TVALID);
end

always @ (*) begin
    ap_block_state4_pp0_stage3_iter0 = ((1'b0 == Output_1_TREADY) | (1'b0 == Input_2_TVALID));
end

always @ (*) begin
    ap_condition_144 = (~((ap_start_int == 1'b0) | ((1'b0 == Input_2_TVALID) & (tmp_fu_67_p3 == 1'd0))) & (1'b1 == ap_CS_fsm_state1));
end

assign ap_loop_exit_ready = ap_condition_exit_pp0_iter0_stage0;

assign k_3_fu_75_p2 = (ap_sig_allocacmp_k_2 + 6'd16);

assign tmp_fu_67_p3 = ap_sig_allocacmp_k_2[32'd5];

endmodule //coloringFB_top_m_coloringFB_top_m_Pipeline_RECV