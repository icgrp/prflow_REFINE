// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.1 (64-bit)
// Version: 2022.1
// Copyright (C) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module data_redir_m_rasterization1_odd_m (
        ap_clk,
        ap_rst,
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        triangle_2d_x0,
        triangle_2d_y0,
        triangle_2d_x1,
        triangle_2d_y1,
        triangle_2d_x2,
        triangle_2d_y2,
        triangle_2d_z,
        Output_1_TDATA,
        Output_1_TVALID,
        Output_1_TREADY
);

parameter    ap_ST_fsm_state1 = 9'd1;
parameter    ap_ST_fsm_state2 = 9'd2;
parameter    ap_ST_fsm_state3 = 9'd4;
parameter    ap_ST_fsm_state4 = 9'd8;
parameter    ap_ST_fsm_state5 = 9'd16;
parameter    ap_ST_fsm_state6 = 9'd32;
parameter    ap_ST_fsm_state7 = 9'd64;
parameter    ap_ST_fsm_state8 = 9'd128;
parameter    ap_ST_fsm_state9 = 9'd256;

input   ap_clk;
input   ap_rst;
input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
input  [7:0] triangle_2d_x0;
input  [7:0] triangle_2d_y0;
input  [7:0] triangle_2d_x1;
input  [7:0] triangle_2d_y1;
input  [7:0] triangle_2d_x2;
input  [7:0] triangle_2d_y2;
input  [7:0] triangle_2d_z;
output  [31:0] Output_1_TDATA;
output   Output_1_TVALID;
input   Output_1_TREADY;

reg ap_done;
reg ap_idle;
reg ap_ready;
reg[31:0] Output_1_TDATA;
reg Output_1_TVALID;

(* fsm_encoding = "none" *) reg   [8:0] ap_CS_fsm;
wire    ap_CS_fsm_state1;
reg   [15:0] max_index_V;
reg   [7:0] max_min_V_7;
reg   [7:0] max_min_V_6;
reg   [7:0] max_min_V_5;
reg   [7:0] max_min_V_4;
reg   [7:0] max_min_V;
reg    Output_1_TDATA_blk_n;
wire   [0:0] icmp_ln206_fu_195_p2;
wire    ap_CS_fsm_state6;
wire    ap_CS_fsm_state7;
wire    ap_CS_fsm_state8;
wire    ap_CS_fsm_state2;
wire    ap_CS_fsm_state3;
wire    ap_CS_fsm_state4;
wire    ap_CS_fsm_state5;
reg   [0:0] tmp_reg_602;
wire   [7:0] triangle_2d_same_y1_V_fu_209_p3;
reg   [7:0] triangle_2d_same_y1_V_reg_610;
wire   [7:0] triangle_2d_same_y0_V_fu_219_p3;
reg   [7:0] triangle_2d_same_y0_V_reg_621;
wire   [7:0] rhs_5_fu_259_p3;
reg   [7:0] rhs_5_reg_631;
wire   [7:0] lhs_5_fu_303_p3;
reg   [7:0] lhs_5_reg_637;
wire   [7:0] rhs_6_fu_354_p3;
reg   [7:0] rhs_6_reg_643;
wire   [7:0] lhs_6_fu_392_p3;
reg   [7:0] lhs_6_reg_649;
wire   [7:0] trunc_ln232_fu_427_p1;
reg   [7:0] trunc_ln232_reg_655;
wire   [15:0] mul_ln232_fu_457_p2;
reg    ap_block_state1;
reg    ap_block_state1_io;
wire   [31:0] p_Result_2_fu_317_p5;
wire   [31:0] p_Result_3_fu_406_p5;
wire   [31:0] p_Result_4_fu_469_p4;
wire   [31:0] zext_ln391_1_fu_487_p1;
wire   [31:0] p_Result_s_fu_504_p4;
wire   [31:0] zext_ln391_fu_539_p1;
wire   [8:0] zext_ln232_fu_113_p1;
wire   [8:0] zext_ln1542_fu_117_p1;
wire   [8:0] zext_ln232_1_fu_127_p1;
wire   [8:0] zext_ln1542_1_fu_131_p1;
wire  signed [8:0] ret_V_15_fu_121_p2;
wire  signed [8:0] ret_V_16_fu_135_p2;
wire   [8:0] zext_ln1542_2_fu_155_p1;
wire   [8:0] zext_ln1542_3_fu_165_p1;
wire  signed [8:0] ret_V_18_fu_159_p2;
wire  signed [8:0] ret_V_19_fu_169_p2;
wire   [17:0] ret_V_17_fu_149_p2;
wire   [17:0] ret_V_20_fu_183_p2;
wire   [17:0] ret_V_fu_189_p2;
wire   [7:0] triangle_2d_same_x0_V_fu_224_p3;
wire   [7:0] triangle_2d_same_x1_V_fu_214_p3;
wire   [0:0] icmp_ln1073_1_fu_235_p2;
wire   [0:0] icmp_ln1073_2_fu_247_p2;
wire   [0:0] icmp_ln1073_fu_229_p2;
wire   [7:0] select_ln35_fu_240_p3;
wire   [7:0] select_ln42_fu_252_p3;
wire   [0:0] icmp_ln1081_1_fu_279_p2;
wire   [0:0] icmp_ln1081_2_fu_291_p2;
wire   [0:0] icmp_ln1081_fu_273_p2;
wire   [7:0] select_ln55_fu_284_p3;
wire   [7:0] select_ln62_fu_296_p3;
wire   [0:0] icmp_ln1073_4_fu_334_p2;
wire   [0:0] icmp_ln1073_5_fu_344_p2;
wire   [0:0] icmp_ln1073_3_fu_330_p2;
wire   [7:0] select_ln35_1_fu_338_p3;
wire   [7:0] select_ln42_1_fu_348_p3;
wire   [0:0] icmp_ln1081_4_fu_372_p2;
wire   [0:0] icmp_ln1081_5_fu_382_p2;
wire   [0:0] icmp_ln1081_3_fu_368_p2;
wire   [7:0] select_ln55_1_fu_376_p3;
wire   [7:0] select_ln62_1_fu_386_p3;
wire   [8:0] zext_ln232_2_fu_415_p1;
wire   [8:0] zext_ln232_3_fu_418_p1;
wire  signed [8:0] ret_V_13_fu_421_p2;
wire   [8:0] zext_ln232_4_fu_437_p1;
wire   [8:0] zext_ln232_5_fu_440_p1;
wire  signed [8:0] ret_V_14_fu_443_p2;
wire   [24:0] p_Result_5_fu_478_p5;
wire   [24:0] p_Result_1_fu_527_p5;
wire    ap_CS_fsm_state9;
reg   [8:0] ap_NS_fsm;
reg    ap_ST_fsm_state1_blk;
reg    ap_ST_fsm_state2_blk;
reg    ap_ST_fsm_state3_blk;
reg    ap_ST_fsm_state4_blk;
reg    ap_ST_fsm_state5_blk;
reg    ap_ST_fsm_state6_blk;
reg    ap_ST_fsm_state7_blk;
reg    ap_ST_fsm_state8_blk;
wire    ap_ST_fsm_state9_blk;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_CS_fsm = 9'd1;
#0 max_index_V = 16'd0;
#0 max_min_V_7 = 8'd0;
#0 max_min_V_6 = 8'd0;
#0 max_min_V_5 = 8'd0;
#0 max_min_V_4 = 8'd0;
#0 max_min_V = 8'd0;
end

data_redir_m_mul_9s_9s_18_1_1 #(
    .ID( 1 ),
    .NUM_STAGE( 1 ),
    .din0_WIDTH( 9 ),
    .din1_WIDTH( 9 ),
    .dout_WIDTH( 18 ))
mul_9s_9s_18_1_1_U8(
    .din0(ret_V_15_fu_121_p2),
    .din1(ret_V_16_fu_135_p2),
    .dout(ret_V_17_fu_149_p2)
);

data_redir_m_mul_9s_9s_18_1_1 #(
    .ID( 1 ),
    .NUM_STAGE( 1 ),
    .din0_WIDTH( 9 ),
    .din1_WIDTH( 9 ),
    .dout_WIDTH( 18 ))
mul_9s_9s_18_1_1_U9(
    .din0(ret_V_18_fu_159_p2),
    .din1(ret_V_19_fu_169_p2),
    .dout(ret_V_20_fu_183_p2)
);

data_redir_m_mul_9s_9s_16_1_1 #(
    .ID( 1 ),
    .NUM_STAGE( 1 ),
    .din0_WIDTH( 9 ),
    .din1_WIDTH( 9 ),
    .dout_WIDTH( 16 ))
mul_9s_9s_16_1_1_U10(
    .din0(ret_V_13_fu_421_p2),
    .din1(ret_V_14_fu_443_p2),
    .dout(mul_ln232_fu_457_p2)
);

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_CS_fsm <= ap_ST_fsm_state1;
    end else begin
        ap_CS_fsm <= ap_NS_fsm;
    end
end

always @ (posedge ap_clk) begin
    if ((1'b1 == ap_CS_fsm_state2)) begin
        lhs_5_reg_637 <= lhs_5_fu_303_p3;
        rhs_5_reg_631 <= rhs_5_fu_259_p3;
        triangle_2d_same_y0_V_reg_621 <= triangle_2d_same_y0_V_fu_219_p3;
        triangle_2d_same_y1_V_reg_610 <= triangle_2d_same_y1_V_fu_209_p3;
    end
end

always @ (posedge ap_clk) begin
    if ((1'b1 == ap_CS_fsm_state3)) begin
        lhs_6_reg_649 <= lhs_6_fu_392_p3;
        rhs_6_reg_643 <= rhs_6_fu_354_p3;
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_state4) & (1'b1 == Output_1_TREADY))) begin
        max_index_V <= mul_ln232_fu_457_p2;
        max_min_V <= trunc_ln232_fu_427_p1;
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_state3) & (1'b1 == Output_1_TREADY))) begin
        max_min_V_4 <= lhs_6_fu_392_p3;
        max_min_V_5 <= rhs_6_fu_354_p3;
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_state2) & (1'b1 == Output_1_TREADY))) begin
        max_min_V_6 <= lhs_5_fu_303_p3;
        max_min_V_7 <= rhs_5_fu_259_p3;
    end
end

always @ (posedge ap_clk) begin
    if (((icmp_ln206_fu_195_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state1))) begin
        tmp_reg_602 <= ret_V_fu_189_p2[32'd17];
    end
end

always @ (posedge ap_clk) begin
    if ((1'b1 == ap_CS_fsm_state4)) begin
        trunc_ln232_reg_655 <= trunc_ln232_fu_427_p1;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state8) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = zext_ln391_fu_539_p1;
    end else if (((1'b1 == ap_CS_fsm_state7) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = p_Result_s_fu_504_p4;
    end else if (((1'b1 == ap_CS_fsm_state6) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = 32'd0;
    end else if (((1'b1 == ap_CS_fsm_state5) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = zext_ln391_1_fu_487_p1;
    end else if (((1'b1 == ap_CS_fsm_state4) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = p_Result_4_fu_469_p4;
    end else if (((1'b1 == ap_CS_fsm_state3) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = p_Result_3_fu_406_p5;
    end else if (((1'b1 == ap_CS_fsm_state2) & (1'b1 == Output_1_TREADY))) begin
        Output_1_TDATA = p_Result_2_fu_317_p5;
    end else if ((~((ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY))) & (icmp_ln206_fu_195_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state1))) begin
        Output_1_TDATA = 32'd1;
    end else begin
        Output_1_TDATA = 'bx;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state5) | (1'b1 == ap_CS_fsm_state4) | (1'b1 == ap_CS_fsm_state3) | (1'b1 == ap_CS_fsm_state2) | (1'b1 == ap_CS_fsm_state8) | (1'b1 == ap_CS_fsm_state7) | (1'b1 == ap_CS_fsm_state6) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state1) & (ap_start == 1'b1)))) begin
        Output_1_TDATA_blk_n = Output_1_TREADY;
    end else begin
        Output_1_TDATA_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((((1'b1 == ap_CS_fsm_state5) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state4) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state3) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state2) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state8) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state7) & (1'b1 == Output_1_TREADY)) | ((1'b1 == ap_CS_fsm_state6) & (1'b1 == Output_1_TREADY)) | (~((1'b1 == ap_block_state1_io) | (ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY))) & (icmp_ln206_fu_195_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state1)))) begin
        Output_1_TVALID = 1'b1;
    end else begin
        Output_1_TVALID = 1'b0;
    end
end

always @ (*) begin
    if (((1'b1 == ap_block_state1_io) | (ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY)))) begin
        ap_ST_fsm_state1_blk = 1'b1;
    end else begin
        ap_ST_fsm_state1_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state2_blk = 1'b1;
    end else begin
        ap_ST_fsm_state2_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state3_blk = 1'b1;
    end else begin
        ap_ST_fsm_state3_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state4_blk = 1'b1;
    end else begin
        ap_ST_fsm_state4_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state5_blk = 1'b1;
    end else begin
        ap_ST_fsm_state5_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state6_blk = 1'b1;
    end else begin
        ap_ST_fsm_state6_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state7_blk = 1'b1;
    end else begin
        ap_ST_fsm_state7_blk = 1'b0;
    end
end

always @ (*) begin
    if ((1'b0 == Output_1_TREADY)) begin
        ap_ST_fsm_state8_blk = 1'b1;
    end else begin
        ap_ST_fsm_state8_blk = 1'b0;
    end
end

assign ap_ST_fsm_state9_blk = 1'b0;

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state9) | ((1'b1 == ap_CS_fsm_state1) & (ap_start == 1'b0)))) begin
        ap_done = 1'b1;
    end else begin
        ap_done = 1'b0;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_state1) & (ap_start == 1'b0))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if ((1'b1 == ap_CS_fsm_state9)) begin
        ap_ready = 1'b1;
    end else begin
        ap_ready = 1'b0;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_state1 : begin
            if ((~((1'b1 == ap_block_state1_io) | (ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY))) & (icmp_ln206_fu_195_p2 == 1'd1) & (1'b1 == ap_CS_fsm_state1))) begin
                ap_NS_fsm = ap_ST_fsm_state6;
            end else if ((~((1'b1 == ap_block_state1_io) | (ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY))) & (icmp_ln206_fu_195_p2 == 1'd0) & (1'b1 == ap_CS_fsm_state1))) begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state1;
            end
        end
        ap_ST_fsm_state2 : begin
            if (((1'b1 == ap_CS_fsm_state2) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state2;
            end
        end
        ap_ST_fsm_state3 : begin
            if (((1'b1 == ap_CS_fsm_state3) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state3;
            end
        end
        ap_ST_fsm_state4 : begin
            if (((1'b1 == ap_CS_fsm_state4) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state5;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state4;
            end
        end
        ap_ST_fsm_state5 : begin
            if (((1'b1 == ap_CS_fsm_state5) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state9;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state5;
            end
        end
        ap_ST_fsm_state6 : begin
            if (((1'b1 == ap_CS_fsm_state6) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state7;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state6;
            end
        end
        ap_ST_fsm_state7 : begin
            if (((1'b1 == ap_CS_fsm_state7) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state8;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state7;
            end
        end
        ap_ST_fsm_state8 : begin
            if (((1'b1 == ap_CS_fsm_state8) & (1'b1 == Output_1_TREADY))) begin
                ap_NS_fsm = ap_ST_fsm_state9;
            end else begin
                ap_NS_fsm = ap_ST_fsm_state8;
            end
        end
        ap_ST_fsm_state9 : begin
            ap_NS_fsm = ap_ST_fsm_state1;
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign ap_CS_fsm_state1 = ap_CS_fsm[32'd0];

assign ap_CS_fsm_state2 = ap_CS_fsm[32'd1];

assign ap_CS_fsm_state3 = ap_CS_fsm[32'd2];

assign ap_CS_fsm_state4 = ap_CS_fsm[32'd3];

assign ap_CS_fsm_state5 = ap_CS_fsm[32'd4];

assign ap_CS_fsm_state6 = ap_CS_fsm[32'd5];

assign ap_CS_fsm_state7 = ap_CS_fsm[32'd6];

assign ap_CS_fsm_state8 = ap_CS_fsm[32'd7];

assign ap_CS_fsm_state9 = ap_CS_fsm[32'd8];

always @ (*) begin
    ap_block_state1 = ((ap_start == 1'b0) | ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY)));
end

always @ (*) begin
    ap_block_state1_io = ((icmp_ln206_fu_195_p2 == 1'd1) & (1'b0 == Output_1_TREADY));
end

assign icmp_ln1073_1_fu_235_p2 = ((triangle_2d_same_x0_V_fu_224_p3 < triangle_2d_x2) ? 1'b1 : 1'b0);

assign icmp_ln1073_2_fu_247_p2 = ((triangle_2d_same_x1_V_fu_214_p3 < triangle_2d_x2) ? 1'b1 : 1'b0);

assign icmp_ln1073_3_fu_330_p2 = ((triangle_2d_same_y0_V_reg_621 < triangle_2d_same_y1_V_reg_610) ? 1'b1 : 1'b0);

assign icmp_ln1073_4_fu_334_p2 = ((triangle_2d_same_y0_V_reg_621 < triangle_2d_y2) ? 1'b1 : 1'b0);

assign icmp_ln1073_5_fu_344_p2 = ((triangle_2d_same_y1_V_reg_610 < triangle_2d_y2) ? 1'b1 : 1'b0);

assign icmp_ln1073_fu_229_p2 = ((triangle_2d_same_x0_V_fu_224_p3 < triangle_2d_same_x1_V_fu_214_p3) ? 1'b1 : 1'b0);

assign icmp_ln1081_1_fu_279_p2 = ((triangle_2d_same_x0_V_fu_224_p3 > triangle_2d_x2) ? 1'b1 : 1'b0);

assign icmp_ln1081_2_fu_291_p2 = ((triangle_2d_same_x1_V_fu_214_p3 > triangle_2d_x2) ? 1'b1 : 1'b0);

assign icmp_ln1081_3_fu_368_p2 = ((triangle_2d_same_y0_V_reg_621 > triangle_2d_same_y1_V_reg_610) ? 1'b1 : 1'b0);

assign icmp_ln1081_4_fu_372_p2 = ((triangle_2d_same_y0_V_reg_621 > triangle_2d_y2) ? 1'b1 : 1'b0);

assign icmp_ln1081_5_fu_382_p2 = ((triangle_2d_same_y1_V_reg_610 > triangle_2d_y2) ? 1'b1 : 1'b0);

assign icmp_ln1081_fu_273_p2 = ((triangle_2d_same_x0_V_fu_224_p3 > triangle_2d_same_x1_V_fu_214_p3) ? 1'b1 : 1'b0);

assign icmp_ln206_fu_195_p2 = ((ret_V_17_fu_149_p2 == ret_V_20_fu_183_p2) ? 1'b1 : 1'b0);

assign lhs_5_fu_303_p3 = ((icmp_ln1081_fu_273_p2[0:0] == 1'b1) ? select_ln55_fu_284_p3 : select_ln62_fu_296_p3);

assign lhs_6_fu_392_p3 = ((icmp_ln1081_3_fu_368_p2[0:0] == 1'b1) ? select_ln55_1_fu_376_p3 : select_ln62_1_fu_386_p3);

assign p_Result_1_fu_527_p5 = {{{{{{1'd0}, {max_min_V}}}, {max_min_V_4}}}, {max_min_V_5}};

assign p_Result_2_fu_317_p5 = {{{{triangle_2d_same_x1_V_fu_214_p3}, {triangle_2d_same_y0_V_fu_219_p3}}, {triangle_2d_same_x0_V_fu_224_p3}}, {8'd0}};

assign p_Result_3_fu_406_p5 = {{{{triangle_2d_z}, {triangle_2d_y2}}, {triangle_2d_x2}}, {triangle_2d_same_y1_V_reg_610}};

assign p_Result_4_fu_469_p4 = {{{lhs_5_reg_637}, {rhs_5_reg_631}}, {mul_ln232_fu_457_p2}};

assign p_Result_5_fu_478_p5 = {{{{{{1'd0}, {trunc_ln232_reg_655}}}, {lhs_6_reg_649}}}, {rhs_6_reg_643}};

assign p_Result_s_fu_504_p4 = {{{max_min_V_6}, {max_min_V_7}}, {max_index_V}};

assign ret_V_13_fu_421_p2 = (zext_ln232_2_fu_415_p1 - zext_ln232_3_fu_418_p1);

assign ret_V_14_fu_443_p2 = (zext_ln232_4_fu_437_p1 - zext_ln232_5_fu_440_p1);

assign ret_V_15_fu_121_p2 = (zext_ln232_fu_113_p1 - zext_ln1542_fu_117_p1);

assign ret_V_16_fu_135_p2 = (zext_ln232_1_fu_127_p1 - zext_ln1542_1_fu_131_p1);

assign ret_V_18_fu_159_p2 = (zext_ln1542_2_fu_155_p1 - zext_ln1542_1_fu_131_p1);

assign ret_V_19_fu_169_p2 = (zext_ln1542_3_fu_165_p1 - zext_ln1542_fu_117_p1);

assign ret_V_fu_189_p2 = (ret_V_17_fu_149_p2 - ret_V_20_fu_183_p2);

assign rhs_5_fu_259_p3 = ((icmp_ln1073_fu_229_p2[0:0] == 1'b1) ? select_ln35_fu_240_p3 : select_ln42_fu_252_p3);

assign rhs_6_fu_354_p3 = ((icmp_ln1073_3_fu_330_p2[0:0] == 1'b1) ? select_ln35_1_fu_338_p3 : select_ln42_1_fu_348_p3);

assign select_ln35_1_fu_338_p3 = ((icmp_ln1073_4_fu_334_p2[0:0] == 1'b1) ? triangle_2d_same_y0_V_reg_621 : triangle_2d_y2);

assign select_ln35_fu_240_p3 = ((icmp_ln1073_1_fu_235_p2[0:0] == 1'b1) ? triangle_2d_same_x0_V_fu_224_p3 : triangle_2d_x2);

assign select_ln42_1_fu_348_p3 = ((icmp_ln1073_5_fu_344_p2[0:0] == 1'b1) ? triangle_2d_same_y1_V_reg_610 : triangle_2d_y2);

assign select_ln42_fu_252_p3 = ((icmp_ln1073_2_fu_247_p2[0:0] == 1'b1) ? triangle_2d_same_x1_V_fu_214_p3 : triangle_2d_x2);

assign select_ln55_1_fu_376_p3 = ((icmp_ln1081_4_fu_372_p2[0:0] == 1'b1) ? triangle_2d_same_y0_V_reg_621 : triangle_2d_y2);

assign select_ln55_fu_284_p3 = ((icmp_ln1081_1_fu_279_p2[0:0] == 1'b1) ? triangle_2d_same_x0_V_fu_224_p3 : triangle_2d_x2);

assign select_ln62_1_fu_386_p3 = ((icmp_ln1081_5_fu_382_p2[0:0] == 1'b1) ? triangle_2d_same_y1_V_reg_610 : triangle_2d_y2);

assign select_ln62_fu_296_p3 = ((icmp_ln1081_2_fu_291_p2[0:0] == 1'b1) ? triangle_2d_same_x1_V_fu_214_p3 : triangle_2d_x2);

assign triangle_2d_same_x0_V_fu_224_p3 = ((tmp_reg_602[0:0] == 1'b1) ? triangle_2d_x1 : triangle_2d_x0);

assign triangle_2d_same_x1_V_fu_214_p3 = ((tmp_reg_602[0:0] == 1'b1) ? triangle_2d_x0 : triangle_2d_x1);

assign triangle_2d_same_y0_V_fu_219_p3 = ((tmp_reg_602[0:0] == 1'b1) ? triangle_2d_y1 : triangle_2d_y0);

assign triangle_2d_same_y1_V_fu_209_p3 = ((tmp_reg_602[0:0] == 1'b1) ? triangle_2d_y0 : triangle_2d_y1);

assign trunc_ln232_fu_427_p1 = ret_V_13_fu_421_p2[7:0];

assign zext_ln1542_1_fu_131_p1 = triangle_2d_y0;

assign zext_ln1542_2_fu_155_p1 = triangle_2d_y2;

assign zext_ln1542_3_fu_165_p1 = triangle_2d_x1;

assign zext_ln1542_fu_117_p1 = triangle_2d_x0;

assign zext_ln232_1_fu_127_p1 = triangle_2d_y1;

assign zext_ln232_2_fu_415_p1 = lhs_5_reg_637;

assign zext_ln232_3_fu_418_p1 = rhs_5_reg_631;

assign zext_ln232_4_fu_437_p1 = lhs_6_reg_649;

assign zext_ln232_5_fu_440_p1 = rhs_6_reg_643;

assign zext_ln232_fu_113_p1 = triangle_2d_x2;

assign zext_ln391_1_fu_487_p1 = p_Result_5_fu_478_p5;

assign zext_ln391_fu_539_p1 = p_Result_1_fu_527_p5;

endmodule //data_redir_m_rasterization1_odd_m