module page_double(
    input wire clk_200_0,
    input wire clk_250_0,
    input wire clk_300_0,
    input wire clk_350_0,
    input wire clk_400_0,
    input wire [48 : 0] din_leaf_bft2interface_0,
    output reg  [48 : 0] dout_leaf_interface2bft_0,
    input wire resend_0,
    input wire reset_400_0,
    input wire ap_start_0,

    input wire clk_200_1,
    input wire clk_250_1,
    input wire clk_300_1,
    input wire clk_350_1,
    input wire clk_400_1,
    input wire [48 : 0] din_leaf_bft2interface_1,
    output reg  [48 : 0] dout_leaf_interface2bft_1,
    input wire resend_1,
    input wire reset_400_1,
    input wire ap_start_1
    );

always@(posedge clk_400_0)begin // fastest clk?
  if(reset_400_0) begin
    dout_leaf_interface2bft_0 <= 0;
  end else if(resend_0) begin 
    dout_leaf_interface2bft_0 <= din_leaf_bft2interface_0;
  end else begin 
    dout_leaf_interface2bft_0 <= dout_leaf_interface2bft_0;
  end
end

always@(posedge clk_400_1)begin // fastest clk?
  if(reset_400_1) begin
    dout_leaf_interface2bft_1 <= 0;
  end else if(resend_1) begin 
    dout_leaf_interface2bft_1 <= din_leaf_bft2interface_1;
  end else begin 
    dout_leaf_interface2bft_1 <= dout_leaf_interface2bft_1;
  end
end

endmodule

// module page_double(
//     input wire clk_200_0,
//     input wire clk_250_0,
//     input wire clk_300_0,
//     input wire clk_350_0,
//     input wire clk_400_0,
//     input wire [48 : 0] din_leaf_bft2interface_0,
//     output wire [48 : 0] dout_leaf_interface2bft_0,
//     input wire resend_0,
//     input wire reset_400_0,
//     input wire ap_start_0,

//     input wire clk_200_1,
//     input wire clk_250_1,
//     input wire clk_300_1,
//     input wire clk_350_1,
//     input wire clk_400_1,
//     input wire [48 : 0] din_leaf_bft2interface_1,
//     output wire [48 : 0] dout_leaf_interface2bft_1,
//     input wire resend_1,
//     input wire reset_400_1,
//     input wire ap_start_1
//     );


//     wire ap_start_user_0;
//     wire [32-1 :0] dout_leaf_interface2user_1_0;
//     wire vld_interface2user_1_0;
//     wire ack_user2interface_1_0;
//     wire [32-1 :0] dout_leaf_interface2user_1_user_0;
//     wire vld_interface2user_1_user_0;
//     wire ack_user2interface_1_user_0;
//     wire [32-1 :0] din_leaf_user2interface_1_0;
//     wire vld_user2interface_1_0;
//     wire ack_interface2user_1_0;
//     wire [32-1 :0] din_leaf_user2interface_1_user_0;
//     wire vld_user2interface_1_user_0;
//     wire ack_interface2user_1_user_0;
//     wire clk_user_0;
//     assign clk_user_0 = clk_400_0;
//     wire reset_ap_start_user_0;
    
//     wire [48:0] dout_leaf_interface2bft_tmp_0;
//     assign dout_leaf_interface2bft_0 = resend_0 ? 0 : dout_leaf_interface2bft_tmp_0;
    
//     (* dont_touch = "true" *) leaf_interface #(
//         .PACKET_BITS(49),
//         .PAYLOAD_BITS(32),
//         .NUM_LEAF_BITS(5),
//         .NUM_PORT_BITS(4),
//         .NUM_ADDR_BITS(7),
//         .NUM_IN_PORTS(1),
//         .NUM_OUT_PORTS(1),
//         .NUM_BRAM_ADDR_BITS(7),
//         .FREESPACE_UPDATE_SIZE(64)
//     )leaf_interface_0_inst(
//         .clk(clk_400_0),
//         .clk_user(clk_user_0),
//         .reset(reset_400_0),
//         .din_leaf_bft2interface(din_leaf_bft2interface_0),
//         .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp_0),
//         .ap_start_user(ap_start_user_0), // not used
//         .resend(resend_0),
//         .dout_leaf_interface2user({dout_leaf_interface2user_1_0}),
//         .vld_interface2user({vld_interface2user_1_0}),
//         .ack_user2interface({ack_user2interface_1_0}),
//         .ack_interface2user({ack_interface2user_1_0}),
//         .vld_user2interface({vld_user2interface_1_0}),
//         .din_leaf_user2interface({din_leaf_user2interface_1_0}),
//         .ap_start(ap_start_0),
//         .reset_ap_start_user(reset_ap_start_user_0)
//     );
    
//     assign dout_leaf_interface2user_1_user_0 = dout_leaf_interface2user_1_0;
//     assign vld_interface2user_1_user_0 = vld_interface2user_1_0;
//     assign ack_user2interface_1_0 = ack_user2interface_1_user_0;

//     assign din_leaf_user2interface_1_0 = din_leaf_user2interface_1_user_0;
//     assign vld_user2interface_1_0 = vld_user2interface_1_user_0;
//     assign ack_interface2user_1_user_0 = ack_interface2user_1_0;

//     // update_knn2 update_knn2_0_inst(
//     //     .ap_clk(clk_user_0),
//     //     .ap_start(1'b1), // this should be fine
//     //     .ap_done(),
//     //     .ap_idle(),
//     //     .ap_ready(),
//     //     .Input_1_TDATA(dout_leaf_interface2user_1_user_0),
//     //     .Input_1_TVALID(vld_interface2user_1_user_0),
//     //     .Input_1_TREADY(ack_user2interface_1_user_0),
//     //     .Output_1_TDATA(din_leaf_user2interface_1_user_0),
//     //     .Output_1_TVALID(vld_user2interface_1_user_0),
//     //     .Output_1_TREADY(ack_interface2user_1_user_0),
//     //     .ap_rst_n(~reset_ap_start_user_0)
//     //     );  


//     wire ap_start_user_1;
//     wire [32-1 :0] dout_leaf_interface2user_1_1;
//     wire vld_interface2user_1_1;
//     wire ack_user2interface_1_1;
//     wire [32-1 :0] dout_leaf_interface2user_1_user_1;
//     wire vld_interface2user_1_user_1;
//     wire ack_user2interface_1_user_1;
//     wire [32-1 :0] din_leaf_user2interface_1_1;
//     wire vld_user2interface_1_1;
//     wire ack_interface2user_1_1;
//     wire [32-1 :0] din_leaf_user2interface_1_user_1;
//     wire vld_user2interface_1_user_1;
//     wire ack_interface2user_1_user_1;
//     wire clk_user_1;
//     assign clk_user_1 = clk_400_1;
//     wire reset_ap_start_user_1;
    
//     wire [48:0] dout_leaf_interface2bft_tmp_1;
//     assign dout_leaf_interface2bft_1 = resend_1 ? 0 : dout_leaf_interface2bft_tmp_1;
    
//     (* dont_touch = "true" *) leaf_interface #(
//         .PACKET_BITS(49),
//         .PAYLOAD_BITS(32),
//         .NUM_LEAF_BITS(5),
//         .NUM_PORT_BITS(4),
//         .NUM_ADDR_BITS(7),
//         .NUM_IN_PORTS(1),
//         .NUM_OUT_PORTS(1),
//         .NUM_BRAM_ADDR_BITS(7),
//         .FREESPACE_UPDATE_SIZE(64)
//     )leaf_interface_1_inst(
//         .clk(clk_400_1),
//         .clk_user(clk_user_1),
//         .reset(reset_400_1),
//         .din_leaf_bft2interface(din_leaf_bft2interface_1),
//         .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp_1),
//         .ap_start_user(ap_start_user_1), // not used
//         .resend(resend_1),
//         .dout_leaf_interface2user({dout_leaf_interface2user_1_1}),
//         .vld_interface2user({vld_interface2user_1_1}),
//         .ack_user2interface({ack_user2interface_1_1}),
//         .ack_interface2user({ack_interface2user_1_1}),
//         .vld_user2interface({vld_user2interface_1_1}),
//         .din_leaf_user2interface({din_leaf_user2interface_1_1}),
//         .ap_start(ap_start_1),
//         .reset_ap_start_user(reset_ap_start_user_1)
//     );
    
//     assign dout_leaf_interface2user_1_user_1 = dout_leaf_interface2user_1_1;
//     assign vld_interface2user_1_user_1 = vld_interface2user_1_1;
//     assign ack_user2interface_1_1 = ack_user2interface_1_user_1;

//     assign din_leaf_user2interface_1_1 = din_leaf_user2interface_1_user_1;
//     assign vld_user2interface_1_1 = vld_user2interface_1_user_1;
//     assign ack_interface2user_1_user_1 = ack_interface2user_1_1;

//     // update_knn2 update_knn2_1_inst(
//     //     .ap_clk(clk_user_1),
//     //     .ap_start(1'b1), // this should be fine
//     //     .ap_done(),
//     //     .ap_idle(),
//     //     .ap_ready(),
//     //     .Input_1_TDATA(dout_leaf_interface2user_1_user_1),
//     //     .Input_1_TVALID(vld_interface2user_1_user_1),
//     //     .Input_1_TREADY(ack_user2interface_1_user_1),
//     //     .Output_1_TDATA(din_leaf_user2interface_1_user_1),
//     //     .Output_1_TVALID(vld_user2interface_1_user_1),
//     //     .Output_1_TREADY(ack_interface2user_1_user_1),
//     //     .ap_rst_n(~reset_ap_start_user_1)
//     //     );  


// // always@(posedge clk_400_0)begin // fastest clk?
// //   if(reset_400_0) begin
// //     dout_leaf_interface2bft_0 <= 0;
// //   end else if(resend_0) begin 
// //     dout_leaf_interface2bft_0 <= din_leaf_bft2interface_0;
// //   end else begin 
// //     dout_leaf_interface2bft_0 <= dout_leaf_interface2bft_0;
// //   end
// // end

// // always@(posedge clk_400_1)begin // fastest clk?
// //   if(reset_400_1) begin
// //     dout_leaf_interface2bft_1 <= 0;
// //   end else if(resend_1) begin 
// //     dout_leaf_interface2bft_1 <= din_leaf_bft2interface_1;
// //   end else begin 
// //     dout_leaf_interface2bft_1 <= dout_leaf_interface2bft_1;
// //   end
// // end

// endmodule