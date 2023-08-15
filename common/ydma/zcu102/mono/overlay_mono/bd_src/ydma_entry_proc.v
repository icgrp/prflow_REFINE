// ==============================================================
// RTL generated by Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.1 (64-bit)
// Version: 2022.1
// Copyright (C) Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// 
// ===========================================================

`timescale 1 ns / 1 ps 

module ydma_entry_proc (
        ap_clk,
        ap_rst,
        ap_start,
        start_full_n,
        ap_done,
        ap_continue,
        ap_idle,
        ap_ready,
        start_out,
        start_write,
        output1,
        output1_c_din,
        output1_c_num_data_valid,
        output1_c_fifo_cap,
        output1_c_full_n,
        output1_c_write,
        output2,
        output2_c_din,
        output2_c_num_data_valid,
        output2_c_fifo_cap,
        output2_c_full_n,
        output2_c_write,
        output_size,
        output_size_c_din,
        output_size_c_num_data_valid,
        output_size_c_fifo_cap,
        output_size_c_full_n,
        output_size_c_write,
        num_total_cnt,
        num_total_cnt_c_din,
        num_total_cnt_c_num_data_valid,
        num_total_cnt_c_fifo_cap,
        num_total_cnt_c_full_n,
        num_total_cnt_c_write,
        ap_ext_blocking_n,
        ap_str_blocking_n,
        ap_int_blocking_n
);

parameter    ap_ST_fsm_state1 = 1'd1;

input   ap_clk;
input   ap_rst;
input   ap_start;
input   start_full_n;
output   ap_done;
input   ap_continue;
output   ap_idle;
output   ap_ready;
output   start_out;
output   start_write;
input  [63:0] output1;
output  [63:0] output1_c_din;
input  [2:0] output1_c_num_data_valid;
input  [2:0] output1_c_fifo_cap;
input   output1_c_full_n;
output   output1_c_write;
input  [63:0] output2;
output  [63:0] output2_c_din;
input  [2:0] output2_c_num_data_valid;
input  [2:0] output2_c_fifo_cap;
input   output2_c_full_n;
output   output2_c_write;
input  [31:0] output_size;
output  [31:0] output_size_c_din;
input  [2:0] output_size_c_num_data_valid;
input  [2:0] output_size_c_fifo_cap;
input   output_size_c_full_n;
output   output_size_c_write;
input  [31:0] num_total_cnt;
output  [31:0] num_total_cnt_c_din;
input  [2:0] num_total_cnt_c_num_data_valid;
input  [2:0] num_total_cnt_c_fifo_cap;
input   num_total_cnt_c_full_n;
output   num_total_cnt_c_write;
output   ap_ext_blocking_n;
output   ap_str_blocking_n;
output   ap_int_blocking_n;

reg ap_done;
reg ap_idle;
reg start_write;
reg output1_c_write;
reg output2_c_write;
reg output_size_c_write;
reg num_total_cnt_c_write;

reg    real_start;
reg    start_once_reg;
reg    ap_done_reg;
(* fsm_encoding = "none" *) reg   [0:0] ap_CS_fsm;
wire    ap_CS_fsm_state1;
reg    internal_ap_ready;
reg    output1_c_blk_n;
reg    output2_c_blk_n;
reg    output_size_c_blk_n;
reg    num_total_cnt_c_blk_n;
reg    ap_block_state1;
reg   [0:0] ap_NS_fsm;
reg    ap_ST_fsm_state1_blk;
wire    ap_int_blocking_cur_n;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 start_once_reg = 1'b0;
#0 ap_done_reg = 1'b0;
#0 ap_CS_fsm = 1'd1;
end

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
        if ((ap_continue == 1'b1)) begin
            ap_done_reg <= 1'b0;
        end else if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
            ap_done_reg <= 1'b1;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst == 1'b1) begin
        start_once_reg <= 1'b0;
    end else begin
        if (((real_start == 1'b1) & (internal_ap_ready == 1'b0))) begin
            start_once_reg <= 1'b1;
        end else if ((internal_ap_ready == 1'b1)) begin
            start_once_reg <= 1'b0;
        end
    end
end

always @ (*) begin
    if (((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1))) begin
        ap_ST_fsm_state1_blk = 1'b1;
    end else begin
        ap_ST_fsm_state1_blk = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_done = 1'b1;
    end else begin
        ap_done = ap_done_reg;
    end
end

always @ (*) begin
    if (((real_start == 1'b0) & (1'b1 == ap_CS_fsm_state1))) begin
        ap_idle = 1'b1;
    end else begin
        ap_idle = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        internal_ap_ready = 1'b1;
    end else begin
        internal_ap_ready = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        num_total_cnt_c_blk_n = num_total_cnt_c_full_n;
    end else begin
        num_total_cnt_c_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        num_total_cnt_c_write = 1'b1;
    end else begin
        num_total_cnt_c_write = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output1_c_blk_n = output1_c_full_n;
    end else begin
        output1_c_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output1_c_write = 1'b1;
    end else begin
        output1_c_write = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output2_c_blk_n = output2_c_full_n;
    end else begin
        output2_c_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output2_c_write = 1'b1;
    end else begin
        output2_c_write = 1'b0;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output_size_c_blk_n = output_size_c_full_n;
    end else begin
        output_size_c_blk_n = 1'b1;
    end
end

always @ (*) begin
    if ((~((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1)) & (1'b1 == ap_CS_fsm_state1))) begin
        output_size_c_write = 1'b1;
    end else begin
        output_size_c_write = 1'b0;
    end
end

always @ (*) begin
    if (((start_full_n == 1'b0) & (start_once_reg == 1'b0))) begin
        real_start = 1'b0;
    end else begin
        real_start = ap_start;
    end
end

always @ (*) begin
    if (((real_start == 1'b1) & (start_once_reg == 1'b0))) begin
        start_write = 1'b1;
    end else begin
        start_write = 1'b0;
    end
end

always @ (*) begin
    case (ap_CS_fsm)
        ap_ST_fsm_state1 : begin
            ap_NS_fsm = ap_ST_fsm_state1;
        end
        default : begin
            ap_NS_fsm = 'bx;
        end
    endcase
end

assign ap_CS_fsm_state1 = ap_CS_fsm[32'd0];

always @ (*) begin
    ap_block_state1 = ((real_start == 1'b0) | (num_total_cnt_c_full_n == 1'b0) | (output_size_c_full_n == 1'b0) | (output2_c_full_n == 1'b0) | (output1_c_full_n == 1'b0) | (ap_done_reg == 1'b1));
end

assign ap_ext_blocking_n = (1'b1 & 1'b1);

assign ap_int_blocking_cur_n = (output_size_c_blk_n & output2_c_blk_n & output1_c_blk_n & num_total_cnt_c_blk_n);

assign ap_int_blocking_n = (ap_int_blocking_cur_n & 1'b1);

assign ap_ready = internal_ap_ready;

assign ap_str_blocking_n = (1'b1 & 1'b1);

assign num_total_cnt_c_din = num_total_cnt;

assign output1_c_din = output1;

assign output2_c_din = output2;

assign output_size_c_din = output_size;

assign start_out = real_start;

endmodule //ydma_entry_proc
