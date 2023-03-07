module page_double(
    input wire clk_0,
    input wire [48 : 0] din_leaf_bft2interface_0,
    output reg  [48 : 0] dout_leaf_interface2bft_0,
    input wire resend_0,
    input wire reset_0,
    input wire ap_start_0,

    input wire clk_1,
    input wire [48 : 0] din_leaf_bft2interface_1,
    output reg  [48 : 0] dout_leaf_interface2bft_1,
    input wire resend_1,
    input wire reset_1,
    input wire ap_start_1
    );

always@(posedge clk_0)begin
  if(reset_0) begin
    dout_leaf_interface2bft_0 <= 0;
  end else if(resend_0) begin 
    dout_leaf_interface2bft_0 <= din_leaf_bft2interface_0;
  end else begin 
    dout_leaf_interface2bft_0 <= dout_leaf_interface2bft_0;
  end
end

always@(posedge clk_1)begin
  if(reset_1) begin
    dout_leaf_interface2bft_1 <= 0;
  end else if(resend_1) begin 
    dout_leaf_interface2bft_1 <= din_leaf_bft2interface_1;
  end else begin 
    dout_leaf_interface2bft_1 <= dout_leaf_interface2bft_1;
  end
end

endmodule