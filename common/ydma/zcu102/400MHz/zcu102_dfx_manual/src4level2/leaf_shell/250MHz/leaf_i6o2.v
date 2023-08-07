`timescale 1ns / 1ps
module leaf_i6o2(
    input wire clk_200,
    input wire clk_250,
    input wire clk_300,
    input wire clk_350,
    input wire clk_400,
    input wire [49-1 : 0] din_leaf_bft2interface,
    output wire [49-1 : 0] dout_leaf_interface2bft,
    input wire resend,
    input wire reset_400,
    input wire ap_start
    );

    wire ap_start_user;
    wire [32-1 :0] dout_leaf_interface2user_6, dout_leaf_interface2user_5, dout_leaf_interface2user_4, dout_leaf_interface2user_3, dout_leaf_interface2user_2, dout_leaf_interface2user_1;
    wire vld_interface2user_6, vld_interface2user_5, vld_interface2user_4, vld_interface2user_3, vld_interface2user_2, vld_interface2user_1;
    wire ack_user2interface_6, ack_user2interface_5, ack_user2interface_4, ack_user2interface_3, ack_user2interface_2, ack_user2interface_1;

    wire [32-1 :0] din_leaf_user2interface_2, din_leaf_user2interface_1;
    wire vld_user2interface_2, vld_user2interface_1;
    wire ack_interface2user_2, ack_interface2user_1;

    wire clk_user;
    assign clk_user = clk_250;
    wire reset_ap_start_user;

    wire [48:0] dout_leaf_interface2bft_tmp;
    assign dout_leaf_interface2bft = resend ? 0 : dout_leaf_interface2bft_tmp;

    leaf_interface #(
        .PACKET_BITS(49),
        .PAYLOAD_BITS(32),
        .NUM_LEAF_BITS(5),
        .NUM_PORT_BITS(4),
        .NUM_ADDR_BITS(7),
        .NUM_IN_PORTS(6),
        .NUM_OUT_PORTS(2),
        .NUM_BRAM_ADDR_BITS(7),
        .FREESPACE_UPDATE_SIZE(64)
    )leaf_interface_inst(
        .clk(clk_400),
        .clk_user(clk_user),
        .reset(reset_400),
        .din_leaf_bft2interface(din_leaf_bft2interface),
        .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp),
        .ap_start_user(ap_start_user), // not used
        .resend(resend),

        .dout_leaf_interface2user({dout_leaf_interface2user_6,dout_leaf_interface2user_5,dout_leaf_interface2user_4,dout_leaf_interface2user_3,dout_leaf_interface2user_2,dout_leaf_interface2user_1}),
        .vld_interface2user({vld_interface2user_6,vld_interface2user_5,vld_interface2user_4,vld_interface2user_3,vld_interface2user_2,vld_interface2user_1}),
        .ack_user2interface({ack_user2interface_6,ack_user2interface_5,ack_user2interface_4,ack_user2interface_3,ack_user2interface_2,ack_user2interface_1}),
        .ack_interface2user({ack_interface2user_2,ack_interface2user_1}),
        .vld_user2interface({vld_user2interface_2,vld_user2interface_1}),
        .din_leaf_user2interface({din_leaf_user2interface_2,din_leaf_user2interface_1}),

        .ap_start(ap_start),
        .reset_ap_start_user(reset_ap_start_user)
    );

    user_kernel_bb user_kernel_inst( 
        .clk_user(clk_250),
        .reset(reset_ap_start_user),
        .dout_leaf_interface2user_6(dout_leaf_interface2user_6),
        .dout_leaf_interface2user_5(dout_leaf_interface2user_5),
        .dout_leaf_interface2user_4(dout_leaf_interface2user_4),
        .dout_leaf_interface2user_3(dout_leaf_interface2user_3),
        .dout_leaf_interface2user_2(dout_leaf_interface2user_2),
        .dout_leaf_interface2user_1(dout_leaf_interface2user_1),
        .vld_interface2user_6(vld_interface2user_6),
        .vld_interface2user_5(vld_interface2user_5),
        .vld_interface2user_4(vld_interface2user_4),
        .vld_interface2user_3(vld_interface2user_3),
        .vld_interface2user_2(vld_interface2user_2),
        .vld_interface2user_1(vld_interface2user_1),
        .ack_user2interface_6(ack_user2interface_6),
        .ack_user2interface_5(ack_user2interface_5),
        .ack_user2interface_4(ack_user2interface_4),
        .ack_user2interface_3(ack_user2interface_3),
        .ack_user2interface_2(ack_user2interface_2),
        .ack_user2interface_1(ack_user2interface_1),

        .din_leaf_user2interface_2(din_leaf_user2interface_2),
        .din_leaf_user2interface_1(din_leaf_user2interface_1),
        .vld_user2interface_2(vld_user2interface_2),
        .vld_user2interface_1(vld_user2interface_1),
        .ack_interface2user_2(ack_interface2user_2),
        .ack_interface2user_1(ack_interface2user_1)
        );

endmodule

module user_kernel_bb(
    input wire clk_user,
    input wire reset,
    input wire [32-1:0] dout_leaf_interface2user_6,
    input wire [32-1:0] dout_leaf_interface2user_5,
    input wire [32-1:0] dout_leaf_interface2user_4,
    input wire [32-1:0] dout_leaf_interface2user_3,
    input wire [32-1:0] dout_leaf_interface2user_2,
    input wire [32-1:0] dout_leaf_interface2user_1,
    input wire vld_interface2user_6,
    input wire vld_interface2user_5,
    input wire vld_interface2user_4,
    input wire vld_interface2user_3,
    input wire vld_interface2user_2,
    input wire vld_interface2user_1,
    output wire ack_user2interface_6,
    output wire ack_user2interface_5,
    output wire ack_user2interface_4,
    output wire ack_user2interface_3,
    output wire ack_user2interface_2,
    output wire ack_user2interface_1,

    output wire [32-1:0] din_leaf_user2interface_2,
    output wire [32-1:0] din_leaf_user2interface_1,
    output wire vld_user2interface_2,
    output wire vld_user2interface_1,
    input wire ack_interface2user_2,
    input wire ack_interface2user_1
    );

endmodule
