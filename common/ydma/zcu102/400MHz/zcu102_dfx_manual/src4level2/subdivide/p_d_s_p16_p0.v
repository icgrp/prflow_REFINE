module page_double_subdivide_p16_p0(
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

page_bb p0(
    .clk_200(clk_200_0),
    .clk_250(clk_250_0),
    .clk_300(clk_300_0),
    .clk_350(clk_350_0),
    .clk_400(clk_400_0),
    .din_leaf_bft2interface(din_leaf_bft2interface_0),
    .dout_leaf_interface2bft(dout_leaf_interface2bft_0),
    .resend(resend_0),
    .reset_400(reset_400_0),
    .ap_start(ap_start_0)
    );
    
page_bb p1(
    .clk_200(clk_200_1),
    .clk_250(clk_250_1),
    .clk_300(clk_300_1),
    .clk_350(clk_350_1),
    .clk_400(clk_400_1),
    .din_leaf_bft2interface(din_leaf_bft2interface_1),
    .dout_leaf_interface2bft(dout_leaf_interface2bft_1),
    .resend(resend_1),
    .reset_400(reset_400_1),
    .ap_start(ap_start_1)
    );

    // dummy logic is necessary for Vivado not to be confused 
    // about parent pblock and children pblock
    (* dont_touch = "true" *) reg dummy;

   
endmodule

module page_bb(
    input wire clk_200,
    input wire clk_250,
    input wire clk_300,
    input wire clk_350,
    input wire clk_400,
    input wire [48 : 0] din_leaf_bft2interface,
    output wire [48 : 0] dout_leaf_interface2bft,
    input wire resend,
    input wire reset_400,
    input wire ap_start
    );
    
endmodule
