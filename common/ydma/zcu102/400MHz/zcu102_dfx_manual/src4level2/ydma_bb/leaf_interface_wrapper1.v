`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company:
// Engineer:
//
// Create Date: 03/23/2018 02:46:07 PM
// Design Name:
// Module Name: leaf_empty
// Project Name:
// Target Devices:
// Tool Versions:
// Description:
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////

module InterfaceWrapper1(
    input wire clk,
    input wire [48 : 0] din_leaf_bft2interface,
    output wire [48 : 0] dout_leaf_interface2bft,
    input wire resend,
    
    input [31:0]  Input_1_V_V,
    input         Input_1_V_V_ap_vld,
    output        Input_1_V_V_ap_ack,
    output [31:0] Output_1_V_V,
    output        Output_1_V_V_ap_vld,
    input         Output_1_V_V_ap_ack,

    output [63:0] cnt,
    output        cnt_vld,
    input         cnt_ack,    
    input [31:0]  output_size,
    input         output_size_valid,
    input [15:0]  num_cnt_read,
    input         num_cnt_read_valid,
    output [7:0]  is_done_output_size,
    output        is_done_output_size_valid,

    input wire reset,
    input wire ap_start
    );

    wire [48:0] dout_leaf_interface2bft_tmp;
    assign dout_leaf_interface2bft = resend ? 0 : dout_leaf_interface2bft_tmp;

    leaf_interface_ydma #(
        .PACKET_BITS(49),
        .PAYLOAD_BITS(32), 
        .NUM_LEAF_BITS(5),
        .NUM_PORT_BITS(4),
        .NUM_ADDR_BITS(7),
        .NUM_IN_PORTS(1),
        .NUM_OUT_PORTS(1),
        .NUM_BRAM_ADDR_BITS(7),
        .FREESPACE_UPDATE_SIZE(64)
    )leaf_interface_ydma_inst(
        .clk(clk),
        .reset(reset),
        .din_leaf_bft2interface(din_leaf_bft2interface),
        .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp),
        .resend(resend),

        .dout_leaf_interface2user({Output_1_V_V}),
        .vld_interface2user({Output_1_V_V_ap_vld}),
        .ack_user2interface({Output_1_V_V_ap_ack}),

        .ack_interface2user({Input_1_V_V_ap_ack}),
        .vld_user2interface({Input_1_V_V_ap_vld}),
        .din_leaf_user2interface({Input_1_V_V}),

        .cnt(cnt), // added
        .cnt_vld(cnt_vld), // added
        .cnt_ack(cnt_ack), // added
        .output_size(output_size), // added
        .output_size_valid(output_size_valid), // added
        .num_cnt_read(num_cnt_read), // added
        .num_cnt_read_valid(num_cnt_read_valid), // added        
        .is_done_output_size(is_done_output_size), // added
        .is_done_output_size_valid(is_done_output_size_valid), // added

        .ap_start(ap_start)
    );
    
    
endmodule
