module page_quad_subdivide_p4(
    input wire clk_200_0,
    input wire clk_250_0,
    input wire clk_300_0,
    input wire clk_350_0,
    input wire clk_400_0,
    input wire [48 : 0] din_leaf_bft2interface_0,
    output wire  [48 : 0] dout_leaf_interface2bft_0,
    input wire resend_0,
    input wire reset_400_0,
    input wire ap_start_0,

    input wire clk_200_1,
    input wire clk_250_1,
    input wire clk_300_1,
    input wire clk_350_1,
    input wire clk_400_1,
    input wire [48 : 0] din_leaf_bft2interface_1,
    output wire  [48 : 0] dout_leaf_interface2bft_1,
    input wire resend_1,
    input wire reset_400_1,
    input wire ap_start_1,

    input wire clk_200_2,
    input wire clk_250_2,
    input wire clk_300_2,
    input wire clk_350_2,
    input wire clk_400_2,
    input wire [48 : 0] din_leaf_bft2interface_2,
    output wire  [48 : 0] dout_leaf_interface2bft_2,
    input wire resend_2,
    input wire reset_400_2,
    input wire ap_start_2,

    input wire clk_200_3,
    input wire clk_250_3,
    input wire clk_300_3,
    input wire clk_350_3,
    input wire clk_400_3,
    input wire [48 : 0] din_leaf_bft2interface_3,
    output wire  [48 : 0] dout_leaf_interface2bft_3,
    input wire resend_3,
    input wire reset_400_3,
    input wire ap_start_3
    );

page_double_bb p0(
    .clk_200_0(clk_200_0),
    .clk_250_0(clk_250_0),
    .clk_300_0(clk_300_0),
    .clk_350_0(clk_350_0),
    .clk_400_0(clk_400_0),
    .din_leaf_bft2interface_0(din_leaf_bft2interface_0),
    .dout_leaf_interface2bft_0(dout_leaf_interface2bft_0),
    .resend_0(resend_0),
    .reset_400_0(reset_400_0),
    .ap_start_0(ap_start_0),

    .clk_200_1(clk_200_1),
    .clk_250_1(clk_250_1),
    .clk_300_1(clk_300_1),
    .clk_350_1(clk_350_1),
    .clk_400_1(clk_400_1),
    .din_leaf_bft2interface_1(din_leaf_bft2interface_1),
    .dout_leaf_interface2bft_1(dout_leaf_interface2bft_1),
    .resend_1(resend_1),
    .reset_400_1(reset_400_1),
    .ap_start_1(ap_start_1)
    );

page_double_bb p1(
    .clk_200_0(clk_200_2),
    .clk_250_0(clk_250_2),
    .clk_300_0(clk_300_2),
    .clk_350_0(clk_350_2),
    .clk_400_0(clk_400_2),
    .din_leaf_bft2interface_0(din_leaf_bft2interface_2),
    .dout_leaf_interface2bft_0(dout_leaf_interface2bft_2),
    .resend_0(resend_2),
    .reset_400_0(reset_400_2),
    .ap_start_0(ap_start_2),

    .clk_200_1(clk_200_3),
    .clk_250_1(clk_250_3),
    .clk_300_1(clk_300_3),
    .clk_350_1(clk_350_3),
    .clk_400_1(clk_400_3),
    .din_leaf_bft2interface_1(din_leaf_bft2interface_3),
    .dout_leaf_interface2bft_1(dout_leaf_interface2bft_3),
    .resend_1(resend_3),
    .reset_400_1(reset_400_3),
    .ap_start_1(ap_start_3)
    );

    // dummy logic is necessary for Vivado not to be confused 
    // about parent pblock and children pblock
    (* dont_touch = "true" *) reg dummy;

   
endmodule

module page_double_bb(
    input wire clk_200_0,
    input wire clk_250_0,
    input wire clk_300_0,
    input wire clk_350_0,
    input wire clk_400_0,
    input wire [48 : 0] din_leaf_bft2interface_0,
    output wire  [48 : 0] dout_leaf_interface2bft_0,
    input wire resend_0,
    input wire reset_400_0,
    input wire ap_start_0,

    input wire clk_200_1,
    input wire clk_250_1,
    input wire clk_300_1,
    input wire clk_350_1,
    input wire clk_400_1,
    input wire [48 : 0] din_leaf_bft2interface_1,
    output wire  [48 : 0] dout_leaf_interface2bft_1,
    input wire resend_1,
    input wire reset_400_1,
    input wire ap_start_1
    );
   
endmodule
