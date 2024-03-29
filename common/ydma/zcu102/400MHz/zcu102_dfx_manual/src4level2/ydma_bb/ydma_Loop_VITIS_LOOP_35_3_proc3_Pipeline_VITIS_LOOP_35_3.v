// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.1 (64-bit)
// Version: 2022.1
// Copyright (C) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module ydma_Loop_VITIS_LOOP_35_3_proc3_Pipeline_VITIS_LOOP_35_3 (
        ap_clk,
        ap_rst,
        ap_start,
        ap_done,
        ap_idle,
        ap_ready,
        m_axi_aximm2_AWVALID,
        m_axi_aximm2_AWREADY,
        m_axi_aximm2_AWADDR,
        m_axi_aximm2_AWID,
        m_axi_aximm2_AWLEN,
        m_axi_aximm2_AWSIZE,
        m_axi_aximm2_AWBURST,
        m_axi_aximm2_AWLOCK,
        m_axi_aximm2_AWCACHE,
        m_axi_aximm2_AWPROT,
        m_axi_aximm2_AWQOS,
        m_axi_aximm2_AWREGION,
        m_axi_aximm2_AWUSER,
        m_axi_aximm2_WVALID,
        m_axi_aximm2_WREADY,
        m_axi_aximm2_WDATA,
        m_axi_aximm2_WSTRB,
        m_axi_aximm2_WLAST,
        m_axi_aximm2_WID,
        m_axi_aximm2_WUSER,
        m_axi_aximm2_ARVALID,
        m_axi_aximm2_ARREADY,
        m_axi_aximm2_ARADDR,
        m_axi_aximm2_ARID,
        m_axi_aximm2_ARLEN,
        m_axi_aximm2_ARSIZE,
        m_axi_aximm2_ARBURST,
        m_axi_aximm2_ARLOCK,
        m_axi_aximm2_ARCACHE,
        m_axi_aximm2_ARPROT,
        m_axi_aximm2_ARQOS,
        m_axi_aximm2_ARREGION,
        m_axi_aximm2_ARUSER,
        m_axi_aximm2_RVALID,
        m_axi_aximm2_RREADY,
        m_axi_aximm2_RDATA,
        m_axi_aximm2_RLAST,
        m_axi_aximm2_RID,
        m_axi_aximm2_RFIFONUM,
        m_axi_aximm2_RUSER,
        m_axi_aximm2_RRESP,
        m_axi_aximm2_BVALID,
        m_axi_aximm2_BREADY,
        m_axi_aximm2_BRESP,
        m_axi_aximm2_BID,
        m_axi_aximm2_BUSER,
        v2_buffer_V_din,
        v2_buffer_V_num_data_valid,
        v2_buffer_V_fifo_cap,
        v2_buffer_V_full_n,
        v2_buffer_V_write,
        sext_ln35,
        input_size,
        ap_ext_blocking_n,
        ap_str_blocking_n,
        ap_int_blocking_n
);

parameter    ap_ST_fsm_pp0_stage0 = 1'd1;

input   ap_clk;
input   ap_rst;
input   ap_start;
output   ap_done;
output   ap_idle;
output   ap_ready;
output   m_axi_aximm2_AWVALID;
input   m_axi_aximm2_AWREADY;
output  [63:0] m_axi_aximm2_AWADDR;
output  [0:0] m_axi_aximm2_AWID;
output  [31:0] m_axi_aximm2_AWLEN;
output  [2:0] m_axi_aximm2_AWSIZE;
output  [1:0] m_axi_aximm2_AWBURST;
output  [1:0] m_axi_aximm2_AWLOCK;
output  [3:0] m_axi_aximm2_AWCACHE;
output  [2:0] m_axi_aximm2_AWPROT;
output  [3:0] m_axi_aximm2_AWQOS;
output  [3:0] m_axi_aximm2_AWREGION;
output  [0:0] m_axi_aximm2_AWUSER;
output   m_axi_aximm2_WVALID;
input   m_axi_aximm2_WREADY;
output  [511:0] m_axi_aximm2_WDATA;
output  [63:0] m_axi_aximm2_WSTRB;
output   m_axi_aximm2_WLAST;
output  [0:0] m_axi_aximm2_WID;
output  [0:0] m_axi_aximm2_WUSER;
output   m_axi_aximm2_ARVALID;
input   m_axi_aximm2_ARREADY;
output  [63:0] m_axi_aximm2_ARADDR;
output  [0:0] m_axi_aximm2_ARID;
output  [31:0] m_axi_aximm2_ARLEN;
output  [2:0] m_axi_aximm2_ARSIZE;
output  [1:0] m_axi_aximm2_ARBURST;
output  [1:0] m_axi_aximm2_ARLOCK;
output  [3:0] m_axi_aximm2_ARCACHE;
output  [2:0] m_axi_aximm2_ARPROT;
output  [3:0] m_axi_aximm2_ARQOS;
output  [3:0] m_axi_aximm2_ARREGION;
output  [0:0] m_axi_aximm2_ARUSER;
input   m_axi_aximm2_RVALID;
output   m_axi_aximm2_RREADY;
input  [511:0] m_axi_aximm2_RDATA;
input   m_axi_aximm2_RLAST;
input  [0:0] m_axi_aximm2_RID;
input  [8:0] m_axi_aximm2_RFIFONUM;
input  [0:0] m_axi_aximm2_RUSER;
input  [1:0] m_axi_aximm2_RRESP;
input   m_axi_aximm2_BVALID;
output   m_axi_aximm2_BREADY;
input  [1:0] m_axi_aximm2_BRESP;
input  [0:0] m_axi_aximm2_BID;
input  [0:0] m_axi_aximm2_BUSER;
output  [511:0] v2_buffer_V_din;
input  [10:0] v2_buffer_V_num_data_valid;
input  [10:0] v2_buffer_V_fifo_cap;
input   v2_buffer_V_full_n;
output   v2_buffer_V_write;
input  [57:0] sext_ln35;
input  [31:0] input_size;
output   ap_ext_blocking_n;
output   ap_str_blocking_n;
output   ap_int_blocking_n;

reg ap_idle;
reg m_axi_aximm2_RREADY;
reg v2_buffer_V_write;

(* fsm_encoding = "none" *) reg   [0:0] ap_CS_fsm;
wire    ap_CS_fsm_pp0_stage0;
wire    ap_enable_reg_pp0_iter0;
reg    ap_enable_reg_pp0_iter1;
reg    ap_enable_reg_pp0_iter2;
reg    ap_idle_pp0;
wire    ap_block_state1_pp0_stage0_iter0;
reg   [0:0] icmp_ln35_reg_129;
reg    ap_block_state2_pp0_stage0_iter1;
reg    ap_block_state3_pp0_stage0_iter2;
reg    ap_block_pp0_stage0_subdone;
wire   [0:0] icmp_ln35_fu_94_p2;
reg    ap_condition_exit_pp0_iter0_stage0;
wire    ap_loop_exit_ready;
reg    ap_ready_int;
reg    aximm2_blk_n_R;
wire    ap_block_pp0_stage0;
reg    v2_buffer_V_blk_n;
reg    ap_block_pp0_stage0_11001;
reg   [511:0] aximm2_addr_read_reg_133;
reg    ap_condition_exit_pp0_iter1_stage0;
reg   [30:0] i_fu_50;
wire   [30:0] add_ln35_fu_100_p2;
wire    ap_loop_init;
reg   [30:0] ap_sig_allocacmp_i_load;
reg    ap_block_pp0_stage0_01001;
wire   [31:0] zext_ln35_fu_90_p1;
reg    ap_done_reg;
wire    ap_continue_int;
reg    ap_done_int;
reg    ap_loop_exit_ready_pp0_iter1_reg;
reg   [0:0] ap_NS_fsm;
wire    ap_ext_blocking_cur_n;
wire    ap_int_blocking_cur_n;
wire    ap_enable_pp0;
wire    ap_start_int;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_CS_fsm = 1'd1;
#0 ap_enable_reg_pp0_iter1 = 1'b0;
#0 ap_enable_reg_pp0_iter2 = 1'b0;
#0 ap_done_reg = 1'b0;
end

ydma_flow_control_loop_pipe_sequential_init flow_control_loop_pipe_sequential_init_U(
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
        end else if (((1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_exit_ready_pp0_iter1_reg == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_enable_reg_pp0_iter1 <= 1'b0;
    end else begin
        if (((1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
            ap_enable_reg_pp0_iter1 <= ap_start_int;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        ap_enable_reg_pp0_iter2 <= 1'b0;
    end else begin
        if ((1'b1 == ap_condition_exit_pp0_iter1_stage0)) begin
            ap_enable_reg_pp0_iter2 <= 1'b0;
        end else if ((1'b0 == ap_block_pp0_stage0_subdone)) begin
            ap_enable_reg_pp0_iter2 <= ap_enable_reg_pp0_iter1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_11001))) begin
        if (((ap_enable_reg_pp0_iter0 == 1'b1) & (icmp_ln35_fu_94_p2 == 1'd1))) begin
            i_fu_50 <= add_ln35_fu_100_p2;
        end else if ((ap_loop_init == 1'b1)) begin
            i_fu_50 <= 31'd0;
        end
    end
end

always @ (posedge ap_clk) begin
    if (((1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_11001))) begin
        ap_loop_exit_ready_pp0_iter1_reg <= ap_loop_exit_ready;
        icmp_ln35_reg_129 <= icmp_ln35_fu_94_p2;
    end
end

always @ (posedge ap_clk) begin
    if (((icmp_ln35_reg_129 == 1'd1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_11001))) begin
        aximm2_addr_read_reg_133 <= m_axi_aximm2_RDATA;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (icmp_ln35_fu_94_p2 == 1'd0) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b1;
    end else begin
        ap_condition_exit_pp0_iter0_stage0 = 1'b0;
    end
end

always @ (*) begin
    if (((icmp_ln35_reg_129 == 1'd0) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
        ap_condition_exit_pp0_iter1_stage0 = 1'b1;
    end else begin
        ap_condition_exit_pp0_iter1_stage0 = 1'b0;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_exit_ready_pp0_iter1_reg == 1'b1) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
        ap_done_int = 1'b1;
    end else begin
        ap_done_int = ap_done_reg;
    end
end

always @ (*) begin
    if (((ap_idle_pp0 == 1'b1) & (ap_start_int == 1'b0) & (1'b1 == ap_CS_fsm_pp0_stage0))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter2 == 1'b0) & (ap_enable_reg_pp0_iter1 == 1'b0) & (ap_enable_reg_pp0_iter0 == 1'b0))) begin
        ap_idle_pp0 = 1'b1;
    end else begin
        ap_idle_pp0 = 1'b0;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter0 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_subdone))) begin
        ap_ready_int = 1'b1;
    end else begin
        ap_ready_int = 1'b0;
    end
end

always @ (*) begin
    if (((1'b1 == ap_CS_fsm_pp0_stage0) & (ap_loop_init == 1'b1) & (1'b0 == ap_block_pp0_stage0))) begin
        ap_sig_allocacmp_i_load = 31'd0;
    end else begin
        ap_sig_allocacmp_i_load = i_fu_50;
    end
end

always @ (*) begin
    if (((icmp_ln35_reg_129 == 1'd1) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0))) begin
        aximm2_blk_n_R = m_axi_aximm2_RVALID;
    end else begin
        aximm2_blk_n_R = 1'b1;
    end
end

always @ (*) begin
    if (((icmp_ln35_reg_129 == 1'd1) & (ap_enable_reg_pp0_iter1 == 1'b1) & (1'b1 == ap_CS_fsm_pp0_stage0) & (1'b0 == ap_block_pp0_stage0_11001))) begin
        m_axi_aximm2_RREADY = 1'b1;
    end else begin
        m_axi_aximm2_RREADY = 1'b0;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter2 == 1'b1) & (1'b0 == ap_block_pp0_stage0))) begin
        v2_buffer_V_blk_n = v2_buffer_V_full_n;
    end else begin
        v2_buffer_V_blk_n = 1'b1;
    end
end

always @ (*) begin
    if (((ap_enable_reg_pp0_iter2 == 1'b1) & (1'b0 == ap_block_pp0_stage0_11001))) begin
        v2_buffer_V_write = 1'b1;
    end else begin
        v2_buffer_V_write = 1'b0;
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

assign add_ln35_fu_100_p2 = (ap_sig_allocacmp_i_load + 31'd1);

assign ap_CS_fsm_pp0_stage0 = ap_CS_fsm[32'd0];

assign ap_block_pp0_stage0 = ~(1'b1 == 1'b1);

always @ (*) begin
    ap_block_pp0_stage0_01001 = (((v2_buffer_V_full_n == 1'b0) & (ap_enable_reg_pp0_iter2 == 1'b1)) | ((icmp_ln35_reg_129 == 1'd1) & (m_axi_aximm2_RVALID == 1'b0) & (ap_enable_reg_pp0_iter1 == 1'b1)));
end

always @ (*) begin
    ap_block_pp0_stage0_11001 = (((v2_buffer_V_full_n == 1'b0) & (ap_enable_reg_pp0_iter2 == 1'b1)) | ((icmp_ln35_reg_129 == 1'd1) & (m_axi_aximm2_RVALID == 1'b0) & (ap_enable_reg_pp0_iter1 == 1'b1)));
end

always @ (*) begin
    ap_block_pp0_stage0_subdone = (((v2_buffer_V_full_n == 1'b0) & (ap_enable_reg_pp0_iter2 == 1'b1)) | ((icmp_ln35_reg_129 == 1'd1) & (m_axi_aximm2_RVALID == 1'b0) & (ap_enable_reg_pp0_iter1 == 1'b1)));
end

assign ap_block_state1_pp0_stage0_iter0 = ~(1'b1 == 1'b1);

always @ (*) begin
    ap_block_state2_pp0_stage0_iter1 = ((icmp_ln35_reg_129 == 1'd1) & (m_axi_aximm2_RVALID == 1'b0));
end

always @ (*) begin
    ap_block_state3_pp0_stage0_iter2 = (v2_buffer_V_full_n == 1'b0);
end

assign ap_enable_pp0 = (ap_idle_pp0 ^ 1'b1);

assign ap_enable_reg_pp0_iter0 = ap_start_int;

assign ap_ext_blocking_cur_n = aximm2_blk_n_R;

assign ap_ext_blocking_n = (ap_ext_blocking_cur_n & 1'b1);

assign ap_int_blocking_cur_n = v2_buffer_V_blk_n;

assign ap_int_blocking_n = (ap_int_blocking_cur_n & 1'b1);

assign ap_loop_exit_ready = ap_condition_exit_pp0_iter0_stage0;

assign ap_str_blocking_n = (1'b1 & 1'b1);

assign icmp_ln35_fu_94_p2 = (($signed(zext_ln35_fu_90_p1) < $signed(input_size)) ? 1'b1 : 1'b0);

assign m_axi_aximm2_ARADDR = 64'd0;

assign m_axi_aximm2_ARBURST = 2'd0;

assign m_axi_aximm2_ARCACHE = 4'd0;

assign m_axi_aximm2_ARID = 1'd0;

assign m_axi_aximm2_ARLEN = 32'd0;

assign m_axi_aximm2_ARLOCK = 2'd0;

assign m_axi_aximm2_ARPROT = 3'd0;

assign m_axi_aximm2_ARQOS = 4'd0;

assign m_axi_aximm2_ARREGION = 4'd0;

assign m_axi_aximm2_ARSIZE = 3'd0;

assign m_axi_aximm2_ARUSER = 1'd0;

assign m_axi_aximm2_ARVALID = 1'b0;

assign m_axi_aximm2_AWADDR = 64'd0;

assign m_axi_aximm2_AWBURST = 2'd0;

assign m_axi_aximm2_AWCACHE = 4'd0;

assign m_axi_aximm2_AWID = 1'd0;

assign m_axi_aximm2_AWLEN = 32'd0;

assign m_axi_aximm2_AWLOCK = 2'd0;

assign m_axi_aximm2_AWPROT = 3'd0;

assign m_axi_aximm2_AWQOS = 4'd0;

assign m_axi_aximm2_AWREGION = 4'd0;

assign m_axi_aximm2_AWSIZE = 3'd0;

assign m_axi_aximm2_AWUSER = 1'd0;

assign m_axi_aximm2_AWVALID = 1'b0;

assign m_axi_aximm2_BREADY = 1'b0;

assign m_axi_aximm2_WDATA = 512'd0;

assign m_axi_aximm2_WID = 1'd0;

assign m_axi_aximm2_WLAST = 1'b0;

assign m_axi_aximm2_WSTRB = 64'd0;

assign m_axi_aximm2_WUSER = 1'd0;

assign m_axi_aximm2_WVALID = 1'b0;

assign v2_buffer_V_din = aximm2_addr_read_reg_133;

assign zext_ln35_fu_90_p1 = ap_sig_allocacmp_i_load;

endmodule //ydma_Loop_VITIS_LOOP_35_3_proc3_Pipeline_VITIS_LOOP_35_3
