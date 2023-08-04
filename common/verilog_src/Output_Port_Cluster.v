`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/12/2018 07:49:30 PM
// Design Name: 
// Module Name: Output_Port_Cluster
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


module Output_Port_Cluster #(
    parameter PACKET_BITS = 97,
    parameter NUM_LEAF_BITS = 6,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter PAYLOAD_BITS = 64,  
    parameter NUM_IN_PORTS = 1, 
    parameter NUM_OUT_PORTS = 7,
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter FREESPACE_UPDATE_SIZE = 64,
    localparam OUT_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS+NUM_ADDR_BITS+NUM_ADDR_BITS+3
    )(
    input clk,
    input clk_user,

    input reset,
    input reset_user,    

    input [OUT_PORTS_REG_BITS*NUM_OUT_PORTS-1:0] out_control_reg,  
    output [PACKET_BITS*NUM_OUT_PORTS-1:0] internal_out,
    output [NUM_OUT_PORTS-1:0] empty,
    input [NUM_OUT_PORTS-1:0] rd_en_sel,
    
    output [NUM_OUT_PORTS-1:0] ack_b_out2user,
    input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] din_leaf_user2interface,
    input [NUM_OUT_PORTS-1:0] vld_user2b_out,
    
    input is_done_mode, // clk(_bft) domain
    input is_done_mode_user, // clk_user domain
    output [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_full_cnt,
    output [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_empty_cnt,
    input is_sending_full_cnt_reg,
    input [NUM_LEAF_BITS-1:0] self_leaf_reg,
    input [NUM_PORT_BITS-1:0] self_port_reg,
    input [1:0] cnt_type_reg,
    output output_port_cluster_stall_condition
    );

    wire [NUM_OUT_PORTS-1:0] output_port_stall_condition;
    assign output_port_cluster_stall_condition = |output_port_stall_condition;
    
    genvar gv_i;
    generate
    for(gv_i = 0; gv_i < NUM_OUT_PORTS; gv_i = gv_i + 1) begin : output_port_cluster
        Output_Port#(
            .PACKET_BITS(PACKET_BITS),
            .NUM_LEAF_BITS(NUM_LEAF_BITS),
            .NUM_PORT_BITS(NUM_PORT_BITS),
            .NUM_ADDR_BITS(NUM_ADDR_BITS),
            .PAYLOAD_BITS(PAYLOAD_BITS),
            .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),
            .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE)
        )OPort(
            .clk(clk),
            .clk_user(clk_user),
            .reset(reset),
            .reset_user(reset_user),
            .update_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+2]),
            .update_fifo_addr_en(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS+1]),
            .add_freespace_en(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS]),
            .dst_leaf(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS+NUM_LEAF_BITS-1:OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS]),
            .dst_port(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS+NUM_PORT_BITS-1:OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS]),
            .fifo_addr(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS]),
            .freespace(out_control_reg[OUT_PORTS_REG_BITS*gv_i+NUM_ADDR_BITS-1:OUT_PORTS_REG_BITS*gv_i]),
            .vld_user2b_out(vld_user2b_out[gv_i]),
            .rd_en_sel(rd_en_sel[gv_i]),
            .din_leaf_user2interface(din_leaf_user2interface[PAYLOAD_BITS*(gv_i+1)-1:PAYLOAD_BITS*gv_i]),
            .internal_out(internal_out[PACKET_BITS*(gv_i+1)-1:PACKET_BITS*gv_i]),
            .empty(empty[gv_i]),
            .ack_b_out2user(ack_b_out2user[gv_i]),

            .is_done_mode(is_done_mode),
            .is_done_mode_user(is_done_mode_user),
            .output_port_full_cnt(output_port_full_cnt[PAYLOAD_BITS*(gv_i+1)-1:PAYLOAD_BITS*gv_i]),
            .output_port_empty_cnt(output_port_empty_cnt[PAYLOAD_BITS*(gv_i+1)-1:PAYLOAD_BITS*gv_i]),
            .is_sending_full_cnt_reg(is_sending_full_cnt_reg),
            .self_leaf_reg(self_leaf_reg),
            .self_port_reg(self_port_reg),
            .cnt_type_reg(cnt_type_reg),
            .output_port_stall_condition(output_port_stall_condition[gv_i])
        );
    end
    endgenerate

endmodule
