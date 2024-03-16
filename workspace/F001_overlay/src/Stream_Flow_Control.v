`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/13/2018 05:35:43 PM
// Design Name: 
// Module Name: Stream_Flow_Control
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
`define INPUT_PORT_MAX_NUM 8
`define OUTPUT_PORT_MIN_NUM 9

module Stream_Flow_Control_IDX_LEAF_INTERFACE#(
    parameter PACKET_BITS = 97,
    parameter NUM_LEAF_BITS = 6,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter PAYLOAD_BITS = 64, 
    parameter NUM_IN_PORTS = 7, 
    parameter NUM_OUT_PORTS = 7,
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter FREESPACE_UPDATE_SIZE = 64,
    parameter STALL_CNT = 0,
    parameter DATA_USER_IN_TOTAL = 32,
    parameter DATA_USER_OUT_TOTAL = 32,
    localparam OUT_PORTS_REG_BITS=NUM_LEAF_BITS+NUM_PORT_BITS+NUM_ADDR_BITS+NUM_ADDR_BITS+3,
    localparam IN_PORTS_REG_BITS=NUM_LEAF_BITS+NUM_PORT_BITS,
    localparam REG_CONTROL_BITS=OUT_PORTS_REG_BITS*NUM_OUT_PORTS+IN_PORTS_REG_BITS*NUM_IN_PORTS    
    )(
    input resend,
    input clk,
    input clk_user,
    input reset,
    input reset_user,

    input [PACKET_BITS-1:0] stream_in,
    output [PACKET_BITS-1:0] stream_out,
    input [REG_CONTROL_BITS-1:0] control_reg,
    
    //data to USER
    output [DATA_USER_IN_TOTAL-1:0] dout_leaf_interface2user,
    output [NUM_IN_PORTS-1:0] vld_interface2user,
    input [NUM_IN_PORTS-1:0] ack_user2interface,
    
    //data from USER
    output [NUM_OUT_PORTS-1:0] ack_interface2user,
    input [NUM_OUT_PORTS-1:0] vld_user2interface,
    input [DATA_USER_OUT_TOTAL-1:0] din_leaf_user2interface,
    
    input is_done, // clk(_bft) domain
    input is_done_user, // clk_user domain
    input [NUM_LEAF_BITS-1:0] self_leaf, // clk_user domain

    input input_port_cluster_stall_condition_others,
    input output_port_cluster_stall_condition_others,
    output input_port_cluster_stall_condition_self,
    output output_port_cluster_stall_condition_self

    // output reg is_done_mode_user,

    // input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] full_cnt_Input,
    // input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] empty_cnt_Input,
    // input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] read_cnt_Input,
    // input [NUM_IN_PORTS-1:0] stall_condition_Input,

    // input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] full_cnt_Output,
    // input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] empty_cnt_Output,
    // input [NUM_OUT_PORTS-1:0] stall_condition_Output
    );
    

    //////////////////////
    // clk(_bft) domain //
    //////////////////////

    wire [NUM_IN_PORTS-1:0] freespace_update;
    wire [NUM_OUT_PORTS-1:0] empty;
    wire [PACKET_BITS*NUM_IN_PORTS-1:0] packet_from_input_ports;
    wire [PACKET_BITS*NUM_OUT_PORTS-1:0] packet_from_output_ports;
    wire [NUM_OUT_PORTS-1:0] rd_en_sel;
    
    // wire [PACKET_BITS-1:0] stream_out_tmp;
    // assign stream_out = !(is_done_mode || is_done) ? stream_out_tmp : // data
    //                     ((stream_out_tmp[38:34] != 0) ? stream_out_tmp : 0); // valid counter packet


    converge_ctrl#(
        .PACKET_BITS(PACKET_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS)
    )ConCtrl(
        .clk(clk),
        .reset(reset),
        .outport_sel(rd_en_sel),
        .stream_out(stream_out),
        .freespace_update(freespace_update),
        .packet_from_input_ports(packet_from_input_ports),
        .packet_from_output_ports(packet_from_output_ports),
        .empty(empty),
        .resend(resend)
    );

    reg is_done_mode;
    always@(posedge clk) begin
        if(reset) is_done_mode <= 0;
        else begin
            if (!is_done_mode) begin
                if(is_done) is_done_mode <= 1;
                else is_done_mode <= 0;
            end
            else is_done_mode <= is_done_mode; // stays 1
        end
    end

    /////////////////////
    // clk_user domain //
    /////////////////////

     reg is_done_mode_user;
    always@(posedge clk_user) begin
        if(reset_user) is_done_mode_user <= 0;
        else begin
            if (!is_done_mode_user) begin
                if(is_done_user) is_done_mode_user <= 1;
                else is_done_mode_user <= 0;
            end
            else is_done_mode_user <= is_done_mode_user; // stays 1
        end
    end


    wire [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_full_cnt;
    wire [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_empty_cnt;
    wire [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_read_cnt;
    wire [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_full_cnt;
    wire [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_empty_cnt;
    wire input_port_cluster_stall_condition;
    wire output_port_cluster_stall_condition;
    wire is_sending_full_cnt_reg;
    wire [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] cnt_val;
    wire [NUM_LEAF_BITS-1:0] self_leaf_reg;
    wire [NUM_PORT_BITS-1:0] self_port_reg;
    wire [1:0] cnt_type_reg; // 3: full counter, 2: empty counter, 1: read coutner, 0: stall counter

    assign input_port_cluster_stall_condition_self = input_port_cluster_stall_condition;
    assign output_port_cluster_stall_condition_self = output_port_cluster_stall_condition;


    send_IO_queue_cnt #(
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .STALL_CNT(STALL_CNT)
    ) send_IO_queue_cnt_inst(
        .clk_user(clk_user),
        .reset_user(reset_user),
        .is_done_user(is_done_user),
        .is_done_mode_user(is_done_mode_user),
        .input_port_full_cnt(input_port_full_cnt), // clk(_bft) domain
        .input_port_empty_cnt(input_port_empty_cnt),
        .input_port_read_cnt(input_port_read_cnt),
        .output_port_full_cnt(output_port_full_cnt),
        .output_port_empty_cnt(output_port_empty_cnt), // clk(_bft) domain
        .input_port_cluster_stall_condition(input_port_cluster_stall_condition_self || input_port_cluster_stall_condition_others),
        .output_port_cluster_stall_condition(output_port_cluster_stall_condition_self || output_port_cluster_stall_condition_others),
        .self_leaf(self_leaf),

        .is_sending_full_cnt_reg(is_sending_full_cnt_reg), // output
        .cnt_val(cnt_val), // output
        .self_leaf_reg(self_leaf_reg),
        .self_port_reg(self_port_reg),
        .cnt_type_reg(cnt_type_reg)
    );

    // Input_Port and Output_Port

    Input_Port_Cluster_IDX_LEAF_INTERFACE # (
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),
        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),
        .DATA_USER_IN_TOTAL(DATA_USER_IN_TOTAL)
    )ipc(
        .clk(clk),
        .clk_user(clk_user),
        .reset(reset),
        .reset_user(reset_user),

        .freespace_update(freespace_update),
        .packet_from_input_ports(packet_from_input_ports),
        .stream_in(stream_in),
        .in_control_reg(control_reg[IN_PORTS_REG_BITS*NUM_IN_PORTS-1:0]),
        
        .dout2user(dout_leaf_interface2user),
        .vld2user(vld_interface2user),
        .ack_user2b_in(ack_user2interface),

        .is_done_mode(is_done_mode || is_done), // 1bit
        .is_done_mode_user(is_done_mode_user), // 1bit
        .input_port_full_cnt(input_port_full_cnt),  // clk(_bft) domain
        .input_port_empty_cnt(input_port_empty_cnt), // clk_user
        .input_port_read_cnt(input_port_read_cnt), // clk_user
        .input_port_cluster_stall_condition(input_port_cluster_stall_condition) // 1bit, clk_user
    );


    Output_Port_Cluster_IDX_LEAF_INTERFACE #(
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),
        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),
        .DATA_USER_OUT_TOTAL(DATA_USER_OUT_TOTAL)
    )opc(
        .clk(clk),
        .clk_user(clk_user),
        .reset(reset),
        .reset_user(reset_user),
        .out_control_reg(control_reg[REG_CONTROL_BITS-1:IN_PORTS_REG_BITS*NUM_IN_PORTS]),
        .internal_out(packet_from_output_ports),
        .empty(empty),
        .rd_en_sel(rd_en_sel),
        .ack_b_out2user(ack_interface2user),
        .din_leaf_user2interface(din_leaf_user2interface),
        .vld_user2b_out(vld_user2interface),

        .is_done_mode(is_done_mode || is_done), // 1bit
        .is_done_mode_user(is_done_mode_user), // 1bit
        .output_port_full_cnt(output_port_full_cnt), // clk_user
        .output_port_empty_cnt(output_port_empty_cnt), // clk(_bft) domain

        .is_sending_full_cnt_reg(is_sending_full_cnt_reg), // clk_user
        .self_leaf_reg(self_leaf_reg), // clk_user
        .self_port_reg(self_port_reg), // clk_user
        .cnt_type_reg(cnt_type_reg), // clk_user

        .vld_cnt(is_sending_full_cnt_reg),
        .cnt_val(cnt_val),

        .output_port_cluster_stall_condition(output_port_cluster_stall_condition) // 1bit. clk_user
    );


endmodule