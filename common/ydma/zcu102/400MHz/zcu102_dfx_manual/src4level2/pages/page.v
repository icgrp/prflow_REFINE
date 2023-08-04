module page(
    input wire clk_200,
    input wire clk_250,
    input wire clk_300,
    input wire clk_350,
    input wire clk_400,
    input wire [48 : 0] din_leaf_bft2interface,
    output reg  [48 : 0] dout_leaf_interface2bft,
    input wire resend,
    input wire reset_400,
    input wire ap_start
    );

always@(posedge clk_400)begin // fastest clk?
  if(reset_400) begin
    dout_leaf_interface2bft <= 0;
  end else if(resend) begin 
    dout_leaf_interface2bft <= din_leaf_bft2interface;
  end else begin 
    dout_leaf_interface2bft <= dout_leaf_interface2bft;
  end
end

   
endmodule

// module page(
//     input wire clk_200,
//     input wire clk_250,
//     input wire clk_300,
//     input wire clk_350,
//     input wire clk_400,
//     input wire [48 : 0] din_leaf_bft2interface,
//     output wire [48 : 0] dout_leaf_interface2bft,
//     input wire resend,
//     input wire reset_400,
//     input wire ap_start
//     );

//     wire ap_start_user;
//     wire [32-1 :0] dout_leaf_interface2user_1;
//     wire vld_interface2user_1;
//     wire ack_user2interface_1;
//     wire [32-1 :0] dout_leaf_interface2user_1_user;
//     wire vld_interface2user_1_user;
//     wire ack_user2interface_1_user;
//     wire [32-1 :0] din_leaf_user2interface_1;
//     wire vld_user2interface_1;
//     wire ack_interface2user_1;
//     wire [32-1 :0] din_leaf_user2interface_1_user;
//     wire vld_user2interface_1_user;
//     wire ack_interface2user_1_user;
//     wire clk_user;
//     assign clk_user = clk_400;
//     wire reset_ap_start_user;
    
//     wire [48:0] dout_leaf_interface2bft_tmp;
//     assign dout_leaf_interface2bft = resend ? 0 : dout_leaf_interface2bft_tmp;
    
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
//     )leaf_interface_inst(
//         .clk(clk_400),
//         .clk_user(clk_user),
//         .reset(reset_400),
//         .din_leaf_bft2interface(din_leaf_bft2interface),
//         .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp),
//         .ap_start_user(ap_start_user), // not used
//         .resend(resend),
//         .dout_leaf_interface2user({dout_leaf_interface2user_1}),
//         .vld_interface2user({vld_interface2user_1}),
//         .ack_user2interface({ack_user2interface_1}),
//         .ack_interface2user({ack_interface2user_1}),
//         .vld_user2interface({vld_user2interface_1}),
//         .din_leaf_user2interface({din_leaf_user2interface_1}),
//         .ap_start(ap_start),
//         .reset_ap_start_user(reset_ap_start_user)
//     );
    
//     assign dout_leaf_interface2user_1_user = dout_leaf_interface2user_1;
//     assign vld_interface2user_1_user = vld_interface2user_1;
//     assign ack_user2interface_1 = ack_user2interface_1_user;

//     assign din_leaf_user2interface_1 = din_leaf_user2interface_1_user;
//     assign vld_user2interface_1 = vld_user2interface_1_user;
//     assign ack_interface2user_1_user = ack_interface2user_1;

//     // update_knn2 update_knn2_inst(
//     //     .ap_clk(clk_user),
//     //     .ap_start(1'b1), // this should be fine
//     //     .ap_done(),
//     //     .ap_idle(),
//     //     .ap_ready(),
//     //     .Input_1_TDATA(dout_leaf_interface2user_1_user),
//     //     .Input_1_TVALID(vld_interface2user_1_user),
//     //     .Input_1_TREADY(ack_user2interface_1_user),
//     //     .Output_1_TDATA(din_leaf_user2interface_1_user),
//     //     .Output_1_TVALID(vld_user2interface_1_user),
//     //     .Output_1_TREADY(ack_interface2user_1_user),
//     //     .ap_rst_n(~reset_ap_start_user)
//     //     );  

// // always@(posedge clk_400)begin // fastest clk?
// //   if(reset_400) begin
// //     dout_leaf_interface2bft <= 0;
// //   end else if(resend) begin 
// //     dout_leaf_interface2bft <= din_leaf_bft2interface;
// //   end else begin 
// //     dout_leaf_interface2bft <= dout_leaf_interface2bft;
// //   end
// // end

   
// endmodule
