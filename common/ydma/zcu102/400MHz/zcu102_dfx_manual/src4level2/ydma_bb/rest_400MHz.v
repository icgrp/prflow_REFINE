module rest_400MHz #(
        parameter    C_S_AXI_CONTROL_DATA_WIDTH = 32,
        parameter    C_S_AXI_CONTROL_ADDR_WIDTH = 7,
        parameter    C_S_AXI_DATA_WIDTH = 32,
        parameter    C_M_AXI_AXIMM1_ID_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_ADDR_WIDTH = 64,
        parameter    C_M_AXI_AXIMM1_DATA_WIDTH = 64,
        parameter    C_M_AXI_AXIMM1_AWUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_ARUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_WUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_RUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_BUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM1_USER_VALUE = 0,
        parameter    C_M_AXI_AXIMM1_PROT_VALUE = 0,
        parameter    C_M_AXI_AXIMM1_CACHE_VALUE = 3,
        parameter    C_M_AXI_DATA_WIDTH = 32,
        parameter    C_M_AXI_AXIMM2_ID_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_ADDR_WIDTH = 64,
        parameter    C_M_AXI_AXIMM2_DATA_WIDTH = 512,
        parameter    C_M_AXI_AXIMM2_AWUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_ARUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_WUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_RUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_BUSER_WIDTH = 1,
        parameter    C_M_AXI_AXIMM2_USER_VALUE = 0,
        parameter    C_M_AXI_AXIMM2_PROT_VALUE = 0,
        parameter    C_M_AXI_AXIMM2_CACHE_VALUE = 3,
        parameter C_S_AXI_CONTROL_WSTRB_WIDTH = (32 / 8),
        parameter C_S_AXI_WSTRB_WIDTH = (32 / 8),
        parameter C_M_AXI_AXIMM1_WSTRB_WIDTH = (64 / 8),
        parameter C_M_AXI_WSTRB_WIDTH = (32 / 8),
        parameter C_M_AXI_AXIMM2_WSTRB_WIDTH = (512 / 8)
        )(
        s_axi_control_AWVALID,
        s_axi_control_AWREADY,
        s_axi_control_AWADDR,
        s_axi_control_WVALID,
        s_axi_control_WREADY,
        s_axi_control_WDATA,
        s_axi_control_WSTRB,
        s_axi_control_ARVALID,
        s_axi_control_ARREADY,
        s_axi_control_ARADDR,
        s_axi_control_RVALID,
        s_axi_control_RREADY,
        s_axi_control_RDATA,
        s_axi_control_RRESP,
        s_axi_control_BVALID,
        s_axi_control_BREADY,
        s_axi_control_BRESP,

        // clk_200,
        // clk_250,
        // clk_300,
        // clk_350,
        ap_clk,
        ap_rst_n,

        // ap_rst_n_200,
        // ap_rst_n_250,
        // ap_rst_n_300,
        // ap_rst_n_350,

        event_done,
        interrupt,
        event_start,
        m_axi_aximm1_AWVALID,
        m_axi_aximm1_AWREADY,
        m_axi_aximm1_AWADDR,
        m_axi_aximm1_AWID,
        m_axi_aximm1_AWLEN,
        m_axi_aximm1_AWSIZE,
        m_axi_aximm1_AWBURST,
        m_axi_aximm1_AWLOCK,
        m_axi_aximm1_AWCACHE,
        m_axi_aximm1_AWPROT,
        m_axi_aximm1_AWQOS,
        m_axi_aximm1_AWREGION,
        m_axi_aximm1_AWUSER,
        m_axi_aximm1_WVALID,
        m_axi_aximm1_WREADY,
        m_axi_aximm1_WDATA,
        m_axi_aximm1_WSTRB,
        m_axi_aximm1_WLAST,
        m_axi_aximm1_WID,
        m_axi_aximm1_WUSER,
        m_axi_aximm1_ARVALID,
        m_axi_aximm1_ARREADY,
        m_axi_aximm1_ARADDR,
        m_axi_aximm1_ARID,
        m_axi_aximm1_ARLEN,
        m_axi_aximm1_ARSIZE,
        m_axi_aximm1_ARBURST,
        m_axi_aximm1_ARLOCK,
        m_axi_aximm1_ARCACHE,
        m_axi_aximm1_ARPROT,
        m_axi_aximm1_ARQOS,
        m_axi_aximm1_ARREGION,
        m_axi_aximm1_ARUSER,
        m_axi_aximm1_RVALID,
        m_axi_aximm1_RREADY,
        m_axi_aximm1_RDATA,
        m_axi_aximm1_RLAST,
        m_axi_aximm1_RID,
        m_axi_aximm1_RUSER,
        m_axi_aximm1_RRESP,
        m_axi_aximm1_BVALID,
        m_axi_aximm1_BREADY,
        m_axi_aximm1_BRESP,
        m_axi_aximm1_BID,
        m_axi_aximm1_BUSER,
        m_axi_aximm2_AWVALID,
        m_axi_aximm2_AWREADY,
        m_axi_aximm2_AWADDR,
        m_axi_aximm2_AWID,
        m_axi_aximm2_AWLEN,
        m_axi_aximm2_AWSIZE,
        m_axi_aximm2_AWBURST,
        m_axi_aximm2_AWLOCK,
        m_axi_aximm2_AWCACHE,
        m_axi_aximm2_AWPROT,
        m_axi_aximm2_AWQOS,
        m_axi_aximm2_AWREGION,
        m_axi_aximm2_AWUSER,
        m_axi_aximm2_WVALID,
        m_axi_aximm2_WREADY,
        m_axi_aximm2_WDATA,
        m_axi_aximm2_WSTRB,
        m_axi_aximm2_WLAST,
        m_axi_aximm2_WID,
        m_axi_aximm2_WUSER,
        m_axi_aximm2_ARVALID,
        m_axi_aximm2_ARREADY,
        m_axi_aximm2_ARADDR,
        m_axi_aximm2_ARID,
        m_axi_aximm2_ARLEN,
        m_axi_aximm2_ARSIZE,
        m_axi_aximm2_ARBURST,
        m_axi_aximm2_ARLOCK,
        m_axi_aximm2_ARCACHE,
        m_axi_aximm2_ARPROT,
        m_axi_aximm2_ARQOS,
        m_axi_aximm2_ARREGION,
        m_axi_aximm2_ARUSER,
        m_axi_aximm2_RVALID,
        m_axi_aximm2_RREADY,
        m_axi_aximm2_RDATA,
        m_axi_aximm2_RLAST,
        m_axi_aximm2_RID,
        m_axi_aximm2_RUSER,
        m_axi_aximm2_RRESP,
        m_axi_aximm2_BVALID,
        m_axi_aximm2_BREADY,
        m_axi_aximm2_BRESP,
        m_axi_aximm2_BID,
        m_axi_aximm2_BUSER,
        stall_start_ext,
        stall_done_ext,
        stall_start_str,
        stall_done_str,
        stall_start_int,
        stall_done_int,

        ap_rst_n_inv_400_p2,
        ap_rst_n_inv_400_p3,
        ap_rst_n_inv_400_p4,
        ap_rst_n_inv_400_p5,
        ap_rst_n_inv_400_p6,
        ap_rst_n_inv_400_p7,
        ap_rst_n_inv_400_p8,
        ap_rst_n_inv_400_p9,
        ap_rst_n_inv_400_p10,
        ap_rst_n_inv_400_p11,
        ap_rst_n_inv_400_p12,
        ap_rst_n_inv_400_p13,
        ap_rst_n_inv_400_p14,
        ap_rst_n_inv_400_p15,
        ap_rst_n_inv_400_p16,
        ap_rst_n_inv_400_p17,
        ap_rst_n_inv_400_p18,
        ap_rst_n_inv_400_p19,
        ap_rst_n_inv_400_p20,
        ap_rst_n_inv_400_p21,
        ap_rst_n_inv_400_p22,
        ap_rst_n_inv_400_p23,

        ap_start_400_p2,
        ap_start_400_p3,
        ap_start_400_p4,
        ap_start_400_p5,
        ap_start_400_p6,
        ap_start_400_p7,
        ap_start_400_p8,
        ap_start_400_p9,
        ap_start_400_p10,
        ap_start_400_p11,
        ap_start_400_p12,
        ap_start_400_p13,
        ap_start_400_p14,
        ap_start_400_p15,
        ap_start_400_p16,
        ap_start_400_p17,
        ap_start_400_p18,
        ap_start_400_p19,
        ap_start_400_p20,
        ap_start_400_p21,
        ap_start_400_p22,
        ap_start_400_p23,

        resend_2,
        resend_3,
        resend_4,
        resend_5,
        resend_6,
        resend_7,
        resend_8,
        resend_9,
        resend_10,
        resend_11,
        resend_12,
        resend_13,
        resend_14,
        resend_15,
        resend_16,
        resend_17,
        resend_18,
        resend_19,
        resend_20,
        resend_21,
        resend_22,
        resend_23,
        din_leaf_2,
        din_leaf_3,
        din_leaf_4,
        din_leaf_5,
        din_leaf_6,
        din_leaf_7,
        din_leaf_8,
        din_leaf_9,
        din_leaf_10,
        din_leaf_11,
        din_leaf_12,
        din_leaf_13,
        din_leaf_14,
        din_leaf_15,
        din_leaf_16,
        din_leaf_17,
        din_leaf_18,
        din_leaf_19,
        din_leaf_20,
        din_leaf_21,
        din_leaf_22,
        din_leaf_23,
        dout_leaf_2,
        dout_leaf_3,
        dout_leaf_4,
        dout_leaf_5,
        dout_leaf_6,
        dout_leaf_7,
        dout_leaf_8,
        dout_leaf_9,
        dout_leaf_10,
        dout_leaf_11,
        dout_leaf_12,
        dout_leaf_13,
        dout_leaf_14,
        dout_leaf_15,
        dout_leaf_16,
        dout_leaf_17,
        dout_leaf_18,
        dout_leaf_19,
        dout_leaf_20,
        dout_leaf_21,
        dout_leaf_22,
        dout_leaf_23
);


input   s_axi_control_AWVALID;
output   s_axi_control_AWREADY;
input  [C_S_AXI_CONTROL_ADDR_WIDTH - 1:0] s_axi_control_AWADDR;
input   s_axi_control_WVALID;
output   s_axi_control_WREADY;
input  [C_S_AXI_CONTROL_DATA_WIDTH - 1:0] s_axi_control_WDATA;
input  [C_S_AXI_CONTROL_WSTRB_WIDTH - 1:0] s_axi_control_WSTRB;
input   s_axi_control_ARVALID;
output   s_axi_control_ARREADY;
input  [C_S_AXI_CONTROL_ADDR_WIDTH - 1:0] s_axi_control_ARADDR;
output   s_axi_control_RVALID;
input   s_axi_control_RREADY;
output  [C_S_AXI_CONTROL_DATA_WIDTH - 1:0] s_axi_control_RDATA;
output  [1:0] s_axi_control_RRESP;
output   s_axi_control_BVALID;
input   s_axi_control_BREADY;
output  [1:0] s_axi_control_BRESP;

// input clk_200; // by dopark
// input clk_250; // by dopark
// input clk_300; // by dopark
// input clk_350; // by dopark
input   ap_clk;
input   ap_rst_n;

// input ap_rst_n_200; // by dopark
// input ap_rst_n_250; // by dopark
// input ap_rst_n_300; // by dopark
// input ap_rst_n_350; // by dopark
// DJP: resets for different clocks will be synchronized in leaf interface

output   event_done;
output   interrupt;
output   event_start;
output   m_axi_aximm1_AWVALID;
input   m_axi_aximm1_AWREADY;
output  [C_M_AXI_AXIMM1_ADDR_WIDTH - 1:0] m_axi_aximm1_AWADDR;
output  [C_M_AXI_AXIMM1_ID_WIDTH - 1:0] m_axi_aximm1_AWID;
output  [7:0] m_axi_aximm1_AWLEN;
output  [2:0] m_axi_aximm1_AWSIZE;
output  [1:0] m_axi_aximm1_AWBURST;
output  [1:0] m_axi_aximm1_AWLOCK;
output  [3:0] m_axi_aximm1_AWCACHE;
output  [2:0] m_axi_aximm1_AWPROT;
output  [3:0] m_axi_aximm1_AWQOS;
output  [3:0] m_axi_aximm1_AWREGION;
output  [C_M_AXI_AXIMM1_AWUSER_WIDTH - 1:0] m_axi_aximm1_AWUSER;
output   m_axi_aximm1_WVALID;
input   m_axi_aximm1_WREADY;
output  [C_M_AXI_AXIMM1_DATA_WIDTH - 1:0] m_axi_aximm1_WDATA;
output  [C_M_AXI_AXIMM1_WSTRB_WIDTH - 1:0] m_axi_aximm1_WSTRB;
output   m_axi_aximm1_WLAST;
output  [C_M_AXI_AXIMM1_ID_WIDTH - 1:0] m_axi_aximm1_WID;
output  [C_M_AXI_AXIMM1_WUSER_WIDTH - 1:0] m_axi_aximm1_WUSER;
output   m_axi_aximm1_ARVALID;
input   m_axi_aximm1_ARREADY;
output  [C_M_AXI_AXIMM1_ADDR_WIDTH - 1:0] m_axi_aximm1_ARADDR;
output  [C_M_AXI_AXIMM1_ID_WIDTH - 1:0] m_axi_aximm1_ARID;
output  [7:0] m_axi_aximm1_ARLEN;
output  [2:0] m_axi_aximm1_ARSIZE;
output  [1:0] m_axi_aximm1_ARBURST;
output  [1:0] m_axi_aximm1_ARLOCK;
output  [3:0] m_axi_aximm1_ARCACHE;
output  [2:0] m_axi_aximm1_ARPROT;
output  [3:0] m_axi_aximm1_ARQOS;
output  [3:0] m_axi_aximm1_ARREGION;
output  [C_M_AXI_AXIMM1_ARUSER_WIDTH - 1:0] m_axi_aximm1_ARUSER;
input   m_axi_aximm1_RVALID;
output   m_axi_aximm1_RREADY;
input  [C_M_AXI_AXIMM1_DATA_WIDTH - 1:0] m_axi_aximm1_RDATA;
input   m_axi_aximm1_RLAST;
input  [C_M_AXI_AXIMM1_ID_WIDTH - 1:0] m_axi_aximm1_RID;
input  [C_M_AXI_AXIMM1_RUSER_WIDTH - 1:0] m_axi_aximm1_RUSER;
input  [1:0] m_axi_aximm1_RRESP;
input   m_axi_aximm1_BVALID;
output   m_axi_aximm1_BREADY;
input  [1:0] m_axi_aximm1_BRESP;
input  [C_M_AXI_AXIMM1_ID_WIDTH - 1:0] m_axi_aximm1_BID;
input  [C_M_AXI_AXIMM1_BUSER_WIDTH - 1:0] m_axi_aximm1_BUSER;
output   m_axi_aximm2_AWVALID;
input   m_axi_aximm2_AWREADY;
output  [C_M_AXI_AXIMM2_ADDR_WIDTH - 1:0] m_axi_aximm2_AWADDR;
output  [C_M_AXI_AXIMM2_ID_WIDTH - 1:0] m_axi_aximm2_AWID;
output  [7:0] m_axi_aximm2_AWLEN;
output  [2:0] m_axi_aximm2_AWSIZE;
output  [1:0] m_axi_aximm2_AWBURST;
output  [1:0] m_axi_aximm2_AWLOCK;
output  [3:0] m_axi_aximm2_AWCACHE;
output  [2:0] m_axi_aximm2_AWPROT;
output  [3:0] m_axi_aximm2_AWQOS;
output  [3:0] m_axi_aximm2_AWREGION;
output  [C_M_AXI_AXIMM2_AWUSER_WIDTH - 1:0] m_axi_aximm2_AWUSER;
output   m_axi_aximm2_WVALID;
input   m_axi_aximm2_WREADY;
output  [C_M_AXI_AXIMM2_DATA_WIDTH - 1:0] m_axi_aximm2_WDATA;
output  [C_M_AXI_AXIMM2_WSTRB_WIDTH - 1:0] m_axi_aximm2_WSTRB;
output   m_axi_aximm2_WLAST;
output  [C_M_AXI_AXIMM2_ID_WIDTH - 1:0] m_axi_aximm2_WID;
output  [C_M_AXI_AXIMM2_WUSER_WIDTH - 1:0] m_axi_aximm2_WUSER;
output   m_axi_aximm2_ARVALID;
input   m_axi_aximm2_ARREADY;
output  [C_M_AXI_AXIMM2_ADDR_WIDTH - 1:0] m_axi_aximm2_ARADDR;
output  [C_M_AXI_AXIMM2_ID_WIDTH - 1:0] m_axi_aximm2_ARID;
output  [7:0] m_axi_aximm2_ARLEN;
output  [2:0] m_axi_aximm2_ARSIZE;
output  [1:0] m_axi_aximm2_ARBURST;
output  [1:0] m_axi_aximm2_ARLOCK;
output  [3:0] m_axi_aximm2_ARCACHE;
output  [2:0] m_axi_aximm2_ARPROT;
output  [3:0] m_axi_aximm2_ARQOS;
output  [3:0] m_axi_aximm2_ARREGION;
output  [C_M_AXI_AXIMM2_ARUSER_WIDTH - 1:0] m_axi_aximm2_ARUSER;
input   m_axi_aximm2_RVALID;
output   m_axi_aximm2_RREADY;
input  [C_M_AXI_AXIMM2_DATA_WIDTH - 1:0] m_axi_aximm2_RDATA;
input   m_axi_aximm2_RLAST;
input  [C_M_AXI_AXIMM2_ID_WIDTH - 1:0] m_axi_aximm2_RID;
input  [C_M_AXI_AXIMM2_RUSER_WIDTH - 1:0] m_axi_aximm2_RUSER;
input  [1:0] m_axi_aximm2_RRESP;
input   m_axi_aximm2_BVALID;
output   m_axi_aximm2_BREADY;
input  [1:0] m_axi_aximm2_BRESP;
input  [C_M_AXI_AXIMM2_ID_WIDTH - 1:0] m_axi_aximm2_BID;
input  [C_M_AXI_AXIMM2_BUSER_WIDTH - 1:0] m_axi_aximm2_BUSER;
output   stall_start_ext;
output   stall_done_ext;
output   stall_start_str;
output   stall_done_str;
output   stall_start_int;
output   stall_done_int;


(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p2;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p3;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p4;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p5;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p6;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p7;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p8;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p9;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p10;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p11;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p12;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p13;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p14;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p15;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p16;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p17;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p18;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p19;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p20;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p21;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p22;
(* dont_touch = "true" *) output reg ap_rst_n_inv_400_p23;

(* dont_touch = "true" *) output reg ap_start_400_p2;
(* dont_touch = "true" *) output reg ap_start_400_p3;
(* dont_touch = "true" *) output reg ap_start_400_p4;
(* dont_touch = "true" *) output reg ap_start_400_p5;
(* dont_touch = "true" *) output reg ap_start_400_p6;
(* dont_touch = "true" *) output reg ap_start_400_p7;
(* dont_touch = "true" *) output reg ap_start_400_p8;
(* dont_touch = "true" *) output reg ap_start_400_p9;
(* dont_touch = "true" *) output reg ap_start_400_p10;
(* dont_touch = "true" *) output reg ap_start_400_p11;
(* dont_touch = "true" *) output reg ap_start_400_p12;
(* dont_touch = "true" *) output reg ap_start_400_p13;
(* dont_touch = "true" *) output reg ap_start_400_p14;
(* dont_touch = "true" *) output reg ap_start_400_p15;
(* dont_touch = "true" *) output reg ap_start_400_p16;
(* dont_touch = "true" *) output reg ap_start_400_p17;
(* dont_touch = "true" *) output reg ap_start_400_p18;
(* dont_touch = "true" *) output reg ap_start_400_p19;
(* dont_touch = "true" *) output reg ap_start_400_p20;
(* dont_touch = "true" *) output reg ap_start_400_p21;
(* dont_touch = "true" *) output reg ap_start_400_p22;
(* dont_touch = "true" *) output reg ap_start_400_p23;

output wire resend_2;
output wire resend_3;
output wire resend_4;
output wire resend_5;
output wire resend_6;
output wire resend_7;
output wire resend_8;
output wire resend_9;
output wire resend_10;
output wire resend_11;
output wire resend_12;
output wire resend_13;
output wire resend_14;
output wire resend_15;
output wire resend_16;
output wire resend_17;
output wire resend_18;
output wire resend_19;
output wire resend_20;
output wire resend_21;
output wire resend_22;
output wire resend_23;
output wire [48:0] din_leaf_2;
output wire [48:0] din_leaf_3;
output wire [48:0] din_leaf_4;
output wire [48:0] din_leaf_5;
output wire [48:0] din_leaf_6;
output wire [48:0] din_leaf_7;
output wire [48:0] din_leaf_8;
output wire [48:0] din_leaf_9;
output wire [48:0] din_leaf_10;
output wire [48:0] din_leaf_11;
output wire [48:0] din_leaf_12;
output wire [48:0] din_leaf_13;
output wire [48:0] din_leaf_14;
output wire [48:0] din_leaf_15;
output wire [48:0] din_leaf_16;
output wire [48:0] din_leaf_17;
output wire [48:0] din_leaf_18;
output wire [48:0] din_leaf_19;
output wire [48:0] din_leaf_20;
output wire [48:0] din_leaf_21;
output wire [48:0] din_leaf_22;
output wire [48:0] din_leaf_23;

input wire [48:0] dout_leaf_2;
input wire [48:0] dout_leaf_3;
input wire [48:0] dout_leaf_4;
input wire [48:0] dout_leaf_5;
input wire [48:0] dout_leaf_6;
input wire [48:0] dout_leaf_7;
input wire [48:0] dout_leaf_8;
input wire [48:0] dout_leaf_9;
input wire [48:0] dout_leaf_10;
input wire [48:0] dout_leaf_11;
input wire [48:0] dout_leaf_12;
input wire [48:0] dout_leaf_13;
input wire [48:0] dout_leaf_14;
input wire [48:0] dout_leaf_15;
input wire [48:0] dout_leaf_16;
input wire [48:0] dout_leaf_17;
input wire [48:0] dout_leaf_18;
input wire [48:0] dout_leaf_19;
input wire [48:0] dout_leaf_20;
input wire [48:0] dout_leaf_21;
input wire [48:0] dout_leaf_22;
input wire [48:0] dout_leaf_23;





reg stall_start_ext;
reg stall_done_ext;
reg stall_start_str;
reg stall_done_str;
reg stall_start_int;
reg stall_done_int;

(* shreg_extract = "no" *) reg    ap_rst_reg_2;
(* shreg_extract = "no" *) reg    ap_rst_reg_1;
(* shreg_extract = "no" *) reg    ap_rst_n_inv;

// added for better routing, by dopark
(* dont_touch = "true" *) reg    ap_rst_n_inv_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_aximm1_m_axi_U;
(* dont_touch = "true" *) reg    ap_rst_n_inv_aximm2_m_axi_U;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p0;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p1;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p2;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p3;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p4;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p5;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p6;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p7;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p8;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p9;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p10;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p11;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p12;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p13;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p14;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p15;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p16;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p17;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p18;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p19;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p20;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p21;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p22;
// (* dont_touch = "true" *) reg    ap_rst_n_inv_p23;



(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p2_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p3_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p4_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p5_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p6_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p7_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p8_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p9_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p10_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p11_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p12_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p13_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p14_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p15_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p16_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p17_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p18_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p19_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p20_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p21_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p22_bft;
(* dont_touch = "true" *) reg    ap_rst_n_inv_400_p23_bft;

wire ap_start_400_p2_1;
wire ap_start_400_p3_1;
wire ap_start_400_p4_1;
wire ap_start_400_p5_1;
wire ap_start_400_p6_1;
wire ap_start_400_p7_1;
wire ap_start_400_p8_1;
wire ap_start_400_p9_1;
wire ap_start_400_p10_1;
wire ap_start_400_p11_1;
wire ap_start_400_p12_1;
wire ap_start_400_p13_1;
wire ap_start_400_p14_1;
wire ap_start_400_p15_1;
wire ap_start_400_p16_1;
wire ap_start_400_p17_1;
wire ap_start_400_p18_1;
wire ap_start_400_p19_1;
wire ap_start_400_p20_1;
wire ap_start_400_p21_1;
wire ap_start_400_p22_1;
wire ap_start_400_p23_1;


wire   [63:0] input1;
wire   [63:0] input2;
wire   [63:0] output1;
wire   [63:0] output2;
wire   [31:0] config_size;
wire   [31:0] input_size;
wire   [31:0] output_size;
wire   [31:0] num_total_cnt;
wire    ap_start;
wire    ap_ready;
wire    ap_done;
wire    ap_continue;
wire    ap_idle;
wire    aximm1_AWREADY;
wire    aximm1_WREADY;
wire    aximm1_ARREADY;
wire    aximm1_RVALID;
wire   [63:0] aximm1_RDATA;
wire    aximm1_RLAST;
wire   [0:0] aximm1_RID;
wire   [8:0] aximm1_RFIFONUM;
wire   [0:0] aximm1_RUSER;
wire   [1:0] aximm1_RRESP;
wire    aximm1_BVALID;
wire   [1:0] aximm1_BRESP;
wire   [0:0] aximm1_BID;
wire   [0:0] aximm1_BUSER;
wire    aximm2_AWREADY;
wire    aximm2_WREADY;
wire    aximm2_ARREADY;
wire    aximm2_RVALID;
wire   [511:0] aximm2_RDATA;
wire    aximm2_RLAST;
wire   [0:0] aximm2_RID;
wire   [8:0] aximm2_RFIFONUM;
wire   [0:0] aximm2_RUSER;
wire   [1:0] aximm2_RRESP;
wire    aximm2_BVALID;
wire   [1:0] aximm2_BRESP;
wire   [0:0] aximm2_BID;
wire   [0:0] aximm2_BUSER;
wire    entry_proc_U0_ap_start;
wire    entry_proc_U0_start_full_n;
wire    entry_proc_U0_ap_done;
wire    entry_proc_U0_ap_continue;
wire    entry_proc_U0_ap_idle;
wire    entry_proc_U0_ap_ready;
wire    entry_proc_U0_start_out;
wire    entry_proc_U0_start_write;
wire   [63:0] entry_proc_U0_output1_c_din;
wire    entry_proc_U0_output1_c_write;
wire   [63:0] entry_proc_U0_output2_c_din;
wire    entry_proc_U0_output2_c_write;
wire   [31:0] entry_proc_U0_output_size_c_din;
wire    entry_proc_U0_output_size_c_write;
wire   [31:0] entry_proc_U0_num_total_cnt_c_din;
wire    entry_proc_U0_num_total_cnt_c_write;
wire    entry_proc_U0_ap_ext_blocking_n;
wire    entry_proc_U0_ap_str_blocking_n;
wire    entry_proc_U0_ap_int_blocking_n;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_start;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_done;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_continue;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_idle;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWVALID;
wire   [63:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWADDR;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWID;
wire   [31:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWLEN;
wire   [2:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWSIZE;
wire   [1:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWBURST;
wire   [1:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWLOCK;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWCACHE;
wire   [2:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWPROT;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWQOS;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWREGION;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWUSER;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WVALID;
wire   [63:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WDATA;
wire   [7:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WSTRB;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WLAST;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WID;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WUSER;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARVALID;
wire   [63:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARADDR;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARID;
wire   [31:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARLEN;
wire   [2:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARSIZE;
wire   [1:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARBURST;
wire   [1:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARLOCK;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARCACHE;
wire   [2:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARPROT;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARQOS;
wire   [3:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARREGION;
wire   [0:0] Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARUSER;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_RREADY;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_BREADY;
wire   [63:0] Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_din;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_write;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_ext_blocking_n;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_str_blocking_n;
wire    Loop_VITIS_LOOP_31_1_proc1_U0_ap_int_blocking_n;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_start;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_done;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_continue;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_idle;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_ready;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_num_total_cnt_read;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_output1_read;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWVALID;
wire   [63:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWADDR;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWID;
wire   [31:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWLEN;
wire   [2:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWSIZE;
wire   [1:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWBURST;
wire   [1:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWLOCK;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWCACHE;
wire   [2:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWPROT;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWQOS;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWREGION;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWUSER;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WVALID;
wire   [63:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WDATA;
wire   [7:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WSTRB;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WLAST;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WID;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WUSER;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARVALID;
wire   [63:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARADDR;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARID;
wire   [31:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARLEN;
wire   [2:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARSIZE;
wire   [1:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARBURST;
wire   [1:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARLOCK;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARCACHE;
wire   [2:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARPROT;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARQOS;
wire   [3:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARREGION;
wire   [0:0] Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARUSER;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_RREADY;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_BREADY;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_v1_buffer_V_read;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_ext_blocking_n;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_str_blocking_n;
wire    Loop_VITIS_LOOP_32_2_proc2_U0_ap_int_blocking_n;
wire    ap_sync_continue;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_start;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_done;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_continue;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_idle;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWVALID;
wire   [63:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWADDR;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWID;
wire   [31:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWLEN;
wire   [2:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWSIZE;
wire   [1:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWBURST;
wire   [1:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWLOCK;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWCACHE;
wire   [2:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWPROT;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWQOS;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWREGION;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWUSER;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WVALID;
wire   [511:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WDATA;
wire   [63:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WSTRB;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WLAST;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WID;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WUSER;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARVALID;
wire   [63:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARADDR;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARID;
wire   [31:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARLEN;
wire   [2:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARSIZE;
wire   [1:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARBURST;
wire   [1:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARLOCK;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARCACHE;
wire   [2:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARPROT;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARQOS;
wire   [3:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARREGION;
wire   [0:0] Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARUSER;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_RREADY;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_BREADY;
wire   [511:0] Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_din;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_write;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_ext_blocking_n;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_str_blocking_n;
wire    Loop_VITIS_LOOP_35_3_proc3_U0_ap_int_blocking_n;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_start;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_done;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_continue;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_idle;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_ready;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_output_size_read;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_output2_read;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWVALID;
wire   [63:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWADDR;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWID;
wire   [31:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWLEN;
wire   [2:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWSIZE;
wire   [1:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWBURST;
wire   [1:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWLOCK;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWCACHE;
wire   [2:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWPROT;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWQOS;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWREGION;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWUSER;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WVALID;
wire   [511:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WDATA;
wire   [63:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WSTRB;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WLAST;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WID;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WUSER;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARVALID;
wire   [63:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARADDR;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARID;
wire   [31:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARLEN;
wire   [2:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARSIZE;
wire   [1:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARBURST;
wire   [1:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARLOCK;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARCACHE;
wire   [2:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARPROT;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARQOS;
wire   [3:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARREGION;
wire   [0:0] Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARUSER;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_RREADY;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_BREADY;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_v2_buffer_V_read;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_ext_blocking_n;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_str_blocking_n;
wire    Loop_VITIS_LOOP_36_4_proc4_U0_ap_int_blocking_n;
wire    output1_c_full_n;
wire   [63:0] output1_c_dout;
wire   [2:0] output1_c_num_data_valid;
wire   [2:0] output1_c_fifo_cap;
wire    output1_c_empty_n;
wire    output2_c_full_n;
wire   [63:0] output2_c_dout;
wire   [2:0] output2_c_num_data_valid;
wire   [2:0] output2_c_fifo_cap;
wire    output2_c_empty_n;
wire    output_size_c_full_n;
wire   [31:0] output_size_c_dout;
wire   [2:0] output_size_c_num_data_valid;
wire   [2:0] output_size_c_fifo_cap;
wire    output_size_c_empty_n;
wire    num_total_cnt_c_full_n;
wire   [31:0] num_total_cnt_c_dout;
wire   [2:0] num_total_cnt_c_num_data_valid;
wire   [2:0] num_total_cnt_c_fifo_cap;
wire    num_total_cnt_c_empty_n;
wire    v1_buffer_V_full_n;
wire   [63:0] v1_buffer_V_dout;
wire   [9:0] v1_buffer_V_num_data_valid;
wire   [9:0] v1_buffer_V_fifo_cap;
wire    v1_buffer_V_empty_n;
wire    v2_buffer_V_full_n;
wire   [511:0] v2_buffer_V_dout;
wire   [10:0] v2_buffer_V_num_data_valid;
wire   [10:0] v2_buffer_V_fifo_cap;
wire    v2_buffer_V_empty_n;
wire    ap_sync_done;
wire    ap_sync_ready;
reg    ap_sync_reg_entry_proc_U0_ap_ready;
wire    ap_sync_entry_proc_U0_ap_ready;
reg    ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready;
wire    ap_sync_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready;
reg    ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready;
wire    ap_sync_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready;
wire   [0:0] start_for_Loop_VITIS_LOOP_32_2_proc2_U0_din;
wire    start_for_Loop_VITIS_LOOP_32_2_proc2_U0_full_n;
wire   [0:0] start_for_Loop_VITIS_LOOP_32_2_proc2_U0_dout;
wire    start_for_Loop_VITIS_LOOP_32_2_proc2_U0_empty_n;
wire   [0:0] start_for_Loop_VITIS_LOOP_36_4_proc4_U0_din;
wire    start_for_Loop_VITIS_LOOP_36_4_proc4_U0_full_n;
wire   [0:0] start_for_Loop_VITIS_LOOP_36_4_proc4_U0_dout;
wire    start_for_Loop_VITIS_LOOP_36_4_proc4_U0_empty_n;
wire    ap_ext_blocking_cur_n;
wire    ap_str_blocking_cur_n;
wire    ap_int_blocking_cur_n;
wire    ap_ext_blocking_sub_n;
wire    ap_str_blocking_sub_n;
wire    ap_int_blocking_sub_n;
wire    ap_ext_blocking_n;
wire    ap_str_blocking_n;
wire    ap_int_blocking_n;
reg    ap_ext_blocking_n_reg;
reg    ap_str_blocking_n_reg;
reg    ap_int_blocking_n_reg;
wire    ap_ce_reg;

// power-on initialization
initial begin
#0 ap_rst_reg_2 = 1'b1;
#0 ap_rst_reg_1 = 1'b1;
#0 ap_rst_n_inv = 1'b1;
#0 ap_sync_reg_entry_proc_U0_ap_ready = 1'b0;
#0 ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready = 1'b0;
#0 ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready = 1'b0;

// added for better routing, by dopark
#0 ap_rst_n_inv_bft = 1'b1;
#0 ap_rst_n_inv_aximm1_m_axi_U = 1'b1;
#0 ap_rst_n_inv_aximm2_m_axi_U = 1'b1;
#0 ap_rst_n_inv_400_p0 = 1'b1;
#0 ap_rst_n_inv_400_p1 = 1'b1;

#0 ap_rst_n_inv_400_p2 = 1'b1;
#0 ap_rst_n_inv_400_p3 = 1'b1;
#0 ap_rst_n_inv_400_p4 = 1'b1;
#0 ap_rst_n_inv_400_p5 = 1'b1;
#0 ap_rst_n_inv_400_p6 = 1'b1;
#0 ap_rst_n_inv_400_p7 = 1'b1;
#0 ap_rst_n_inv_400_p8 = 1'b1;
#0 ap_rst_n_inv_400_p9 = 1'b1;
#0 ap_rst_n_inv_400_p10 = 1'b1;
#0 ap_rst_n_inv_400_p11 = 1'b1;
#0 ap_rst_n_inv_400_p12 = 1'b1;
#0 ap_rst_n_inv_400_p13 = 1'b1;
#0 ap_rst_n_inv_400_p14 = 1'b1;
#0 ap_rst_n_inv_400_p15 = 1'b1;
#0 ap_rst_n_inv_400_p16 = 1'b1;
#0 ap_rst_n_inv_400_p17 = 1'b1;
#0 ap_rst_n_inv_400_p18 = 1'b1;
#0 ap_rst_n_inv_400_p19 = 1'b1;
#0 ap_rst_n_inv_400_p20 = 1'b1;
#0 ap_rst_n_inv_400_p21 = 1'b1;
#0 ap_rst_n_inv_400_p22 = 1'b1;
#0 ap_rst_n_inv_400_p23 = 1'b1;

#0 ap_rst_n_inv_400_p2_bft = 1'b1;
#0 ap_rst_n_inv_400_p3_bft = 1'b1;
#0 ap_rst_n_inv_400_p4_bft = 1'b1;
#0 ap_rst_n_inv_400_p5_bft = 1'b1;
#0 ap_rst_n_inv_400_p6_bft = 1'b1;
#0 ap_rst_n_inv_400_p7_bft = 1'b1;
#0 ap_rst_n_inv_400_p8_bft = 1'b1;
#0 ap_rst_n_inv_400_p9_bft = 1'b1;
#0 ap_rst_n_inv_400_p10_bft = 1'b1;
#0 ap_rst_n_inv_400_p11_bft = 1'b1;
#0 ap_rst_n_inv_400_p12_bft = 1'b1;
#0 ap_rst_n_inv_400_p13_bft = 1'b1;
#0 ap_rst_n_inv_400_p14_bft = 1'b1;
#0 ap_rst_n_inv_400_p15_bft = 1'b1;
#0 ap_rst_n_inv_400_p16_bft = 1'b1;
#0 ap_rst_n_inv_400_p17_bft = 1'b1;
#0 ap_rst_n_inv_400_p18_bft = 1'b1;
#0 ap_rst_n_inv_400_p19_bft = 1'b1;
#0 ap_rst_n_inv_400_p20_bft = 1'b1;
#0 ap_rst_n_inv_400_p21_bft = 1'b1;
#0 ap_rst_n_inv_400_p22_bft = 1'b1;
#0 ap_rst_n_inv_400_p23_bft = 1'b1;
end

ydma_control_s_axi #(
    .C_S_AXI_ADDR_WIDTH( C_S_AXI_CONTROL_ADDR_WIDTH ),
    .C_S_AXI_DATA_WIDTH( C_S_AXI_CONTROL_DATA_WIDTH ))
control_s_axi_U(
    .AWVALID(s_axi_control_AWVALID),
    .AWREADY(s_axi_control_AWREADY),
    .AWADDR(s_axi_control_AWADDR),
    .WVALID(s_axi_control_WVALID),
    .WREADY(s_axi_control_WREADY),
    .WDATA(s_axi_control_WDATA),
    .WSTRB(s_axi_control_WSTRB),
    .ARVALID(s_axi_control_ARVALID),
    .ARREADY(s_axi_control_ARREADY),
    .ARADDR(s_axi_control_ARADDR),
    .RVALID(s_axi_control_RVALID),
    .RREADY(s_axi_control_RREADY),
    .RDATA(s_axi_control_RDATA),
    .RRESP(s_axi_control_RRESP),
    .BVALID(s_axi_control_BVALID),
    .BREADY(s_axi_control_BREADY),
    .BRESP(s_axi_control_BRESP),
    .ACLK(ap_clk),
    .ARESET(ap_rst_n_inv),
    .ACLK_EN(1'b1),
    .input1(input1),
    .input2(input2),
    .output1(output1),
    .output2(output2),
    .config_size(config_size),
    .input_size(input_size),
    .output_size(output_size),
    .num_total_cnt(num_total_cnt),
    .ap_start(ap_start),
    
    // below added by dopark
    .ap_start_400_p2(ap_start_400_p2_1),
    .ap_start_400_p3(ap_start_400_p3_1),
    .ap_start_400_p4(ap_start_400_p4_1),
    .ap_start_400_p5(ap_start_400_p5_1),
    .ap_start_400_p6(ap_start_400_p6_1),
    .ap_start_400_p7(ap_start_400_p7_1),
    .ap_start_400_p8(ap_start_400_p8_1),
    .ap_start_400_p9(ap_start_400_p9_1),
    .ap_start_400_p10(ap_start_400_p10_1),
    .ap_start_400_p11(ap_start_400_p11_1),
    .ap_start_400_p12(ap_start_400_p12_1),
    .ap_start_400_p13(ap_start_400_p13_1),
    .ap_start_400_p14(ap_start_400_p14_1),
    .ap_start_400_p15(ap_start_400_p15_1),
    .ap_start_400_p16(ap_start_400_p16_1),
    .ap_start_400_p17(ap_start_400_p17_1),
    .ap_start_400_p18(ap_start_400_p18_1),
    .ap_start_400_p19(ap_start_400_p19_1),
    .ap_start_400_p20(ap_start_400_p20_1),
    .ap_start_400_p21(ap_start_400_p21_1),
    .ap_start_400_p22(ap_start_400_p22_1),
    .ap_start_400_p23(ap_start_400_p23_1),

    .interrupt(interrupt),
    .event_start(event_start),
    .ap_ready(ap_ready),
    .ap_done(ap_done),
    .ap_continue(ap_continue),
    .ap_idle(ap_idle)
);

ydma_aximm1_m_axi #(
    .CONSERVATIVE( 1 ),
    .USER_MAXREQS( 69 ),
    .NUM_READ_OUTSTANDING( 16 ),
    .NUM_WRITE_OUTSTANDING( 16 ),
    .MAX_READ_BURST_LENGTH( 16 ),
    .MAX_WRITE_BURST_LENGTH( 16 ),
    .USER_RFIFONUM_WIDTH( 9 ),
    .C_M_AXI_ID_WIDTH( C_M_AXI_AXIMM1_ID_WIDTH ),
    .C_M_AXI_ADDR_WIDTH( C_M_AXI_AXIMM1_ADDR_WIDTH ),
    .C_M_AXI_DATA_WIDTH( C_M_AXI_AXIMM1_DATA_WIDTH ),
    .C_M_AXI_AWUSER_WIDTH( C_M_AXI_AXIMM1_AWUSER_WIDTH ),
    .C_M_AXI_ARUSER_WIDTH( C_M_AXI_AXIMM1_ARUSER_WIDTH ),
    .C_M_AXI_WUSER_WIDTH( C_M_AXI_AXIMM1_WUSER_WIDTH ),
    .C_M_AXI_RUSER_WIDTH( C_M_AXI_AXIMM1_RUSER_WIDTH ),
    .C_M_AXI_BUSER_WIDTH( C_M_AXI_AXIMM1_BUSER_WIDTH ),
    .C_USER_VALUE( C_M_AXI_AXIMM1_USER_VALUE ),
    .C_PROT_VALUE( C_M_AXI_AXIMM1_PROT_VALUE ),
    .C_CACHE_VALUE( C_M_AXI_AXIMM1_CACHE_VALUE ),
    .USER_DW( 64 ),
    .USER_AW( 64 ))
aximm1_m_axi_U(
    .AWVALID(m_axi_aximm1_AWVALID),
    .AWREADY(m_axi_aximm1_AWREADY),
    .AWADDR(m_axi_aximm1_AWADDR),
    .AWID(m_axi_aximm1_AWID),
    .AWLEN(m_axi_aximm1_AWLEN),
    .AWSIZE(m_axi_aximm1_AWSIZE),
    .AWBURST(m_axi_aximm1_AWBURST),
    .AWLOCK(m_axi_aximm1_AWLOCK),
    .AWCACHE(m_axi_aximm1_AWCACHE),
    .AWPROT(m_axi_aximm1_AWPROT),
    .AWQOS(m_axi_aximm1_AWQOS),
    .AWREGION(m_axi_aximm1_AWREGION),
    .AWUSER(m_axi_aximm1_AWUSER),
    .WVALID(m_axi_aximm1_WVALID),
    .WREADY(m_axi_aximm1_WREADY),
    .WDATA(m_axi_aximm1_WDATA),
    .WSTRB(m_axi_aximm1_WSTRB),
    .WLAST(m_axi_aximm1_WLAST),
    .WID(m_axi_aximm1_WID),
    .WUSER(m_axi_aximm1_WUSER),
    .ARVALID(m_axi_aximm1_ARVALID),
    .ARREADY(m_axi_aximm1_ARREADY),
    .ARADDR(m_axi_aximm1_ARADDR),
    .ARID(m_axi_aximm1_ARID),
    .ARLEN(m_axi_aximm1_ARLEN),
    .ARSIZE(m_axi_aximm1_ARSIZE),
    .ARBURST(m_axi_aximm1_ARBURST),
    .ARLOCK(m_axi_aximm1_ARLOCK),
    .ARCACHE(m_axi_aximm1_ARCACHE),
    .ARPROT(m_axi_aximm1_ARPROT),
    .ARQOS(m_axi_aximm1_ARQOS),
    .ARREGION(m_axi_aximm1_ARREGION),
    .ARUSER(m_axi_aximm1_ARUSER),
    .RVALID(m_axi_aximm1_RVALID),
    .RREADY(m_axi_aximm1_RREADY),
    .RDATA(m_axi_aximm1_RDATA),
    .RLAST(m_axi_aximm1_RLAST),
    .RID(m_axi_aximm1_RID),
    .RUSER(m_axi_aximm1_RUSER),
    .RRESP(m_axi_aximm1_RRESP),
    .BVALID(m_axi_aximm1_BVALID),
    .BREADY(m_axi_aximm1_BREADY),
    .BRESP(m_axi_aximm1_BRESP),
    .BID(m_axi_aximm1_BID),
    .BUSER(m_axi_aximm1_BUSER),
    .ACLK(ap_clk),
    .ARESET(ap_rst_n_inv),
    .ACLK_EN(1'b1),
    .I_ARVALID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARVALID),
    .I_ARREADY(aximm1_ARREADY),
    .I_ARADDR(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARADDR),
    .I_ARLEN(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARLEN),
    .I_RVALID(aximm1_RVALID),
    .I_RREADY(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_RREADY),
    .I_RDATA(aximm1_RDATA),
    .I_RFIFONUM(aximm1_RFIFONUM),
    .I_AWVALID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWVALID),
    .I_AWREADY(aximm1_AWREADY),
    .I_AWADDR(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWADDR),
    .I_AWLEN(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWLEN),
    .I_WVALID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WVALID),
    .I_WREADY(aximm1_WREADY),
    .I_WDATA(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WDATA),
    .I_WSTRB(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WSTRB),
    .I_BVALID(aximm1_BVALID),
    .I_BREADY(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_BREADY)
);

ydma_aximm2_m_axi #(
    .CONSERVATIVE( 1 ),
    .USER_MAXREQS( 69 ),
    .NUM_READ_OUTSTANDING( 16 ),
    .NUM_WRITE_OUTSTANDING( 16 ),
    .MAX_READ_BURST_LENGTH( 16 ),
    .MAX_WRITE_BURST_LENGTH( 16 ),
    .USER_RFIFONUM_WIDTH( 9 ),
    .C_M_AXI_ID_WIDTH( C_M_AXI_AXIMM2_ID_WIDTH ),
    .C_M_AXI_ADDR_WIDTH( C_M_AXI_AXIMM2_ADDR_WIDTH ),
    .C_M_AXI_DATA_WIDTH( C_M_AXI_AXIMM2_DATA_WIDTH ),
    .C_M_AXI_AWUSER_WIDTH( C_M_AXI_AXIMM2_AWUSER_WIDTH ),
    .C_M_AXI_ARUSER_WIDTH( C_M_AXI_AXIMM2_ARUSER_WIDTH ),
    .C_M_AXI_WUSER_WIDTH( C_M_AXI_AXIMM2_WUSER_WIDTH ),
    .C_M_AXI_RUSER_WIDTH( C_M_AXI_AXIMM2_RUSER_WIDTH ),
    .C_M_AXI_BUSER_WIDTH( C_M_AXI_AXIMM2_BUSER_WIDTH ),
    .C_USER_VALUE( C_M_AXI_AXIMM2_USER_VALUE ),
    .C_PROT_VALUE( C_M_AXI_AXIMM2_PROT_VALUE ),
    .C_CACHE_VALUE( C_M_AXI_AXIMM2_CACHE_VALUE ),
    .USER_DW( 512 ),
    .USER_AW( 64 ))
aximm2_m_axi_U(
    .AWVALID(m_axi_aximm2_AWVALID),
    .AWREADY(m_axi_aximm2_AWREADY),
    .AWADDR(m_axi_aximm2_AWADDR),
    .AWID(m_axi_aximm2_AWID),
    .AWLEN(m_axi_aximm2_AWLEN),
    .AWSIZE(m_axi_aximm2_AWSIZE),
    .AWBURST(m_axi_aximm2_AWBURST),
    .AWLOCK(m_axi_aximm2_AWLOCK),
    .AWCACHE(m_axi_aximm2_AWCACHE),
    .AWPROT(m_axi_aximm2_AWPROT),
    .AWQOS(m_axi_aximm2_AWQOS),
    .AWREGION(m_axi_aximm2_AWREGION),
    .AWUSER(m_axi_aximm2_AWUSER),
    .WVALID(m_axi_aximm2_WVALID),
    .WREADY(m_axi_aximm2_WREADY),
    .WDATA(m_axi_aximm2_WDATA),
    .WSTRB(m_axi_aximm2_WSTRB),
    .WLAST(m_axi_aximm2_WLAST),
    .WID(m_axi_aximm2_WID),
    .WUSER(m_axi_aximm2_WUSER),
    .ARVALID(m_axi_aximm2_ARVALID),
    .ARREADY(m_axi_aximm2_ARREADY),
    .ARADDR(m_axi_aximm2_ARADDR),
    .ARID(m_axi_aximm2_ARID),
    .ARLEN(m_axi_aximm2_ARLEN),
    .ARSIZE(m_axi_aximm2_ARSIZE),
    .ARBURST(m_axi_aximm2_ARBURST),
    .ARLOCK(m_axi_aximm2_ARLOCK),
    .ARCACHE(m_axi_aximm2_ARCACHE),
    .ARPROT(m_axi_aximm2_ARPROT),
    .ARQOS(m_axi_aximm2_ARQOS),
    .ARREGION(m_axi_aximm2_ARREGION),
    .ARUSER(m_axi_aximm2_ARUSER),
    .RVALID(m_axi_aximm2_RVALID),
    .RREADY(m_axi_aximm2_RREADY),
    .RDATA(m_axi_aximm2_RDATA),
    .RLAST(m_axi_aximm2_RLAST),
    .RID(m_axi_aximm2_RID),
    .RUSER(m_axi_aximm2_RUSER),
    .RRESP(m_axi_aximm2_RRESP),
    .BVALID(m_axi_aximm2_BVALID),
    .BREADY(m_axi_aximm2_BREADY),
    .BRESP(m_axi_aximm2_BRESP),
    .BID(m_axi_aximm2_BID),
    .BUSER(m_axi_aximm2_BUSER),
    .ACLK(ap_clk),
    .ARESET(ap_rst_n_inv),
    .ACLK_EN(1'b1),
    .I_ARVALID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARVALID),
    .I_ARREADY(aximm2_ARREADY),
    .I_ARADDR(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARADDR),
    .I_ARLEN(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARLEN),
    .I_RVALID(aximm2_RVALID),
    .I_RREADY(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_RREADY),
    .I_RDATA(aximm2_RDATA),
    .I_RFIFONUM(aximm2_RFIFONUM),
    .I_AWVALID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWVALID),
    .I_AWREADY(aximm2_AWREADY),
    .I_AWADDR(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWADDR),
    .I_AWLEN(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWLEN),
    .I_WVALID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WVALID),
    .I_WREADY(aximm2_WREADY),
    .I_WDATA(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WDATA),
    .I_WSTRB(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WSTRB),
    .I_BVALID(aximm2_BVALID),
    .I_BREADY(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_BREADY)
);

ydma_entry_proc entry_proc_U0(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst_n_inv),
    .ap_start(entry_proc_U0_ap_start),
    .start_full_n(entry_proc_U0_start_full_n),
    .ap_done(entry_proc_U0_ap_done),
    .ap_continue(entry_proc_U0_ap_continue),
    .ap_idle(entry_proc_U0_ap_idle),
    .ap_ready(entry_proc_U0_ap_ready),
    .start_out(entry_proc_U0_start_out),
    .start_write(entry_proc_U0_start_write),
    .output1(output1),
    .output1_c_din(entry_proc_U0_output1_c_din),
    .output1_c_num_data_valid(output1_c_num_data_valid),
    .output1_c_fifo_cap(output1_c_fifo_cap),
    .output1_c_full_n(output1_c_full_n),
    .output1_c_write(entry_proc_U0_output1_c_write),
    .output2(output2),
    .output2_c_din(entry_proc_U0_output2_c_din),
    .output2_c_num_data_valid(output2_c_num_data_valid),
    .output2_c_fifo_cap(output2_c_fifo_cap),
    .output2_c_full_n(output2_c_full_n),
    .output2_c_write(entry_proc_U0_output2_c_write),
    .output_size(output_size),
    .output_size_c_din(entry_proc_U0_output_size_c_din),
    .output_size_c_num_data_valid(output_size_c_num_data_valid),
    .output_size_c_fifo_cap(output_size_c_fifo_cap),
    .output_size_c_full_n(output_size_c_full_n),
    .output_size_c_write(entry_proc_U0_output_size_c_write),
    .num_total_cnt(num_total_cnt),
    .num_total_cnt_c_din(entry_proc_U0_num_total_cnt_c_din),
    .num_total_cnt_c_num_data_valid(num_total_cnt_c_num_data_valid),
    .num_total_cnt_c_fifo_cap(num_total_cnt_c_fifo_cap),
    .num_total_cnt_c_full_n(num_total_cnt_c_full_n),
    .num_total_cnt_c_write(entry_proc_U0_num_total_cnt_c_write),
    .ap_ext_blocking_n(entry_proc_U0_ap_ext_blocking_n),
    .ap_str_blocking_n(entry_proc_U0_ap_str_blocking_n),
    .ap_int_blocking_n(entry_proc_U0_ap_int_blocking_n)
);

ydma_Loop_VITIS_LOOP_31_1_proc1 Loop_VITIS_LOOP_31_1_proc1_U0(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst_n_inv),
    .ap_start(Loop_VITIS_LOOP_31_1_proc1_U0_ap_start),
    .ap_done(Loop_VITIS_LOOP_31_1_proc1_U0_ap_done),
    .ap_continue(Loop_VITIS_LOOP_31_1_proc1_U0_ap_continue),
    .ap_idle(Loop_VITIS_LOOP_31_1_proc1_U0_ap_idle),
    .ap_ready(Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready),
    .config_size(config_size),
    .input1(input1),
    .m_axi_aximm1_AWVALID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWVALID),
    .m_axi_aximm1_AWREADY(1'b0),
    .m_axi_aximm1_AWADDR(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWADDR),
    .m_axi_aximm1_AWID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWID),
    .m_axi_aximm1_AWLEN(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWLEN),
    .m_axi_aximm1_AWSIZE(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWSIZE),
    .m_axi_aximm1_AWBURST(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWBURST),
    .m_axi_aximm1_AWLOCK(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWLOCK),
    .m_axi_aximm1_AWCACHE(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWCACHE),
    .m_axi_aximm1_AWPROT(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWPROT),
    .m_axi_aximm1_AWQOS(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWQOS),
    .m_axi_aximm1_AWREGION(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWREGION),
    .m_axi_aximm1_AWUSER(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_AWUSER),
    .m_axi_aximm1_WVALID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WVALID),
    .m_axi_aximm1_WREADY(1'b0),
    .m_axi_aximm1_WDATA(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WDATA),
    .m_axi_aximm1_WSTRB(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WSTRB),
    .m_axi_aximm1_WLAST(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WLAST),
    .m_axi_aximm1_WID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WID),
    .m_axi_aximm1_WUSER(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_WUSER),
    .m_axi_aximm1_ARVALID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARVALID),
    .m_axi_aximm1_ARREADY(aximm1_ARREADY),
    .m_axi_aximm1_ARADDR(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARADDR),
    .m_axi_aximm1_ARID(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARID),
    .m_axi_aximm1_ARLEN(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARLEN),
    .m_axi_aximm1_ARSIZE(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARSIZE),
    .m_axi_aximm1_ARBURST(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARBURST),
    .m_axi_aximm1_ARLOCK(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARLOCK),
    .m_axi_aximm1_ARCACHE(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARCACHE),
    .m_axi_aximm1_ARPROT(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARPROT),
    .m_axi_aximm1_ARQOS(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARQOS),
    .m_axi_aximm1_ARREGION(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARREGION),
    .m_axi_aximm1_ARUSER(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_ARUSER),
    .m_axi_aximm1_RVALID(aximm1_RVALID),
    .m_axi_aximm1_RREADY(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_RREADY),
    .m_axi_aximm1_RDATA(aximm1_RDATA),
    .m_axi_aximm1_RLAST(aximm1_RLAST),
    .m_axi_aximm1_RID(aximm1_RID),
    .m_axi_aximm1_RFIFONUM(aximm1_RFIFONUM),
    .m_axi_aximm1_RUSER(aximm1_RUSER),
    .m_axi_aximm1_RRESP(aximm1_RRESP),
    .m_axi_aximm1_BVALID(1'b0),
    .m_axi_aximm1_BREADY(Loop_VITIS_LOOP_31_1_proc1_U0_m_axi_aximm1_BREADY),
    .m_axi_aximm1_BRESP(2'd0),
    .m_axi_aximm1_BID(1'd0),
    .m_axi_aximm1_BUSER(1'd0),
    .v1_buffer_V_din(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_din),
    .v1_buffer_V_num_data_valid(v1_buffer_V_num_data_valid),
    .v1_buffer_V_fifo_cap(v1_buffer_V_fifo_cap),
    .v1_buffer_V_full_n(v1_buffer_V_full_n),
    .v1_buffer_V_write(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_write),
    .ap_ext_blocking_n(Loop_VITIS_LOOP_31_1_proc1_U0_ap_ext_blocking_n),
    .ap_str_blocking_n(Loop_VITIS_LOOP_31_1_proc1_U0_ap_str_blocking_n),
    .ap_int_blocking_n(Loop_VITIS_LOOP_31_1_proc1_U0_ap_int_blocking_n)
);

ydma_Loop_VITIS_LOOP_32_2_proc2 Loop_VITIS_LOOP_32_2_proc2_U0(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst_n_inv),
    .ap_start(Loop_VITIS_LOOP_32_2_proc2_U0_ap_start),
    .ap_done(Loop_VITIS_LOOP_32_2_proc2_U0_ap_done),
    .ap_continue(Loop_VITIS_LOOP_32_2_proc2_U0_ap_continue),
    .ap_idle(Loop_VITIS_LOOP_32_2_proc2_U0_ap_idle),
    .ap_ready(Loop_VITIS_LOOP_32_2_proc2_U0_ap_ready),
    .num_total_cnt_dout(num_total_cnt_c_dout),
    .num_total_cnt_num_data_valid(num_total_cnt_c_num_data_valid),
    .num_total_cnt_fifo_cap(num_total_cnt_c_fifo_cap),
    .num_total_cnt_empty_n(num_total_cnt_c_empty_n),
    .num_total_cnt_read(Loop_VITIS_LOOP_32_2_proc2_U0_num_total_cnt_read),
    .output1_dout(output1_c_dout),
    .output1_num_data_valid(output1_c_num_data_valid),
    .output1_fifo_cap(output1_c_fifo_cap),
    .output1_empty_n(output1_c_empty_n),
    .output1_read(Loop_VITIS_LOOP_32_2_proc2_U0_output1_read),
    .m_axi_aximm1_AWVALID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWVALID),
    .m_axi_aximm1_AWREADY(aximm1_AWREADY),
    .m_axi_aximm1_AWADDR(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWADDR),
    .m_axi_aximm1_AWID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWID),
    .m_axi_aximm1_AWLEN(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWLEN),
    .m_axi_aximm1_AWSIZE(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWSIZE),
    .m_axi_aximm1_AWBURST(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWBURST),
    .m_axi_aximm1_AWLOCK(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWLOCK),
    .m_axi_aximm1_AWCACHE(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWCACHE),
    .m_axi_aximm1_AWPROT(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWPROT),
    .m_axi_aximm1_AWQOS(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWQOS),
    .m_axi_aximm1_AWREGION(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWREGION),
    .m_axi_aximm1_AWUSER(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_AWUSER),
    .m_axi_aximm1_WVALID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WVALID),
    .m_axi_aximm1_WREADY(aximm1_WREADY),
    .m_axi_aximm1_WDATA(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WDATA),
    .m_axi_aximm1_WSTRB(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WSTRB),
    .m_axi_aximm1_WLAST(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WLAST),
    .m_axi_aximm1_WID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WID),
    .m_axi_aximm1_WUSER(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_WUSER),
    .m_axi_aximm1_ARVALID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARVALID),
    .m_axi_aximm1_ARREADY(1'b0),
    .m_axi_aximm1_ARADDR(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARADDR),
    .m_axi_aximm1_ARID(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARID),
    .m_axi_aximm1_ARLEN(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARLEN),
    .m_axi_aximm1_ARSIZE(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARSIZE),
    .m_axi_aximm1_ARBURST(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARBURST),
    .m_axi_aximm1_ARLOCK(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARLOCK),
    .m_axi_aximm1_ARCACHE(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARCACHE),
    .m_axi_aximm1_ARPROT(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARPROT),
    .m_axi_aximm1_ARQOS(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARQOS),
    .m_axi_aximm1_ARREGION(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARREGION),
    .m_axi_aximm1_ARUSER(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_ARUSER),
    .m_axi_aximm1_RVALID(1'b0),
    .m_axi_aximm1_RREADY(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_RREADY),
    .m_axi_aximm1_RDATA(64'd0),
    .m_axi_aximm1_RLAST(1'b0),
    .m_axi_aximm1_RID(1'd0),
    .m_axi_aximm1_RFIFONUM(9'd0),
    .m_axi_aximm1_RUSER(1'd0),
    .m_axi_aximm1_RRESP(2'd0),
    .m_axi_aximm1_BVALID(aximm1_BVALID),
    .m_axi_aximm1_BREADY(Loop_VITIS_LOOP_32_2_proc2_U0_m_axi_aximm1_BREADY),
    .m_axi_aximm1_BRESP(aximm1_BRESP),
    .m_axi_aximm1_BID(aximm1_BID),
    .m_axi_aximm1_BUSER(aximm1_BUSER),
    .v1_buffer_V_dout(v1_buffer_V_dout),
    .v1_buffer_V_num_data_valid(v1_buffer_V_num_data_valid),
    .v1_buffer_V_fifo_cap(v1_buffer_V_fifo_cap),
    .v1_buffer_V_empty_n(v1_buffer_V_empty_n),
    .v1_buffer_V_read(Loop_VITIS_LOOP_32_2_proc2_U0_v1_buffer_V_read),
    .ap_ext_blocking_n(Loop_VITIS_LOOP_32_2_proc2_U0_ap_ext_blocking_n),
    .ap_str_blocking_n(Loop_VITIS_LOOP_32_2_proc2_U0_ap_str_blocking_n),
    .ap_int_blocking_n(Loop_VITIS_LOOP_32_2_proc2_U0_ap_int_blocking_n)
);

ydma_Loop_VITIS_LOOP_35_3_proc3 Loop_VITIS_LOOP_35_3_proc3_U0(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst_n_inv),
    .ap_start(Loop_VITIS_LOOP_35_3_proc3_U0_ap_start),
    .ap_done(Loop_VITIS_LOOP_35_3_proc3_U0_ap_done),
    .ap_continue(Loop_VITIS_LOOP_35_3_proc3_U0_ap_continue),
    .ap_idle(Loop_VITIS_LOOP_35_3_proc3_U0_ap_idle),
    .ap_ready(Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready),
    .input_size(input_size),
    .input2(input2),
    .m_axi_aximm2_AWVALID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWVALID),
    .m_axi_aximm2_AWREADY(1'b0),
    .m_axi_aximm2_AWADDR(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWADDR),
    .m_axi_aximm2_AWID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWID),
    .m_axi_aximm2_AWLEN(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWLEN),
    .m_axi_aximm2_AWSIZE(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWSIZE),
    .m_axi_aximm2_AWBURST(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWBURST),
    .m_axi_aximm2_AWLOCK(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWLOCK),
    .m_axi_aximm2_AWCACHE(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWCACHE),
    .m_axi_aximm2_AWPROT(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWPROT),
    .m_axi_aximm2_AWQOS(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWQOS),
    .m_axi_aximm2_AWREGION(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWREGION),
    .m_axi_aximm2_AWUSER(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_AWUSER),
    .m_axi_aximm2_WVALID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WVALID),
    .m_axi_aximm2_WREADY(1'b0),
    .m_axi_aximm2_WDATA(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WDATA),
    .m_axi_aximm2_WSTRB(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WSTRB),
    .m_axi_aximm2_WLAST(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WLAST),
    .m_axi_aximm2_WID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WID),
    .m_axi_aximm2_WUSER(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_WUSER),
    .m_axi_aximm2_ARVALID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARVALID),
    .m_axi_aximm2_ARREADY(aximm2_ARREADY),
    .m_axi_aximm2_ARADDR(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARADDR),
    .m_axi_aximm2_ARID(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARID),
    .m_axi_aximm2_ARLEN(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARLEN),
    .m_axi_aximm2_ARSIZE(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARSIZE),
    .m_axi_aximm2_ARBURST(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARBURST),
    .m_axi_aximm2_ARLOCK(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARLOCK),
    .m_axi_aximm2_ARCACHE(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARCACHE),
    .m_axi_aximm2_ARPROT(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARPROT),
    .m_axi_aximm2_ARQOS(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARQOS),
    .m_axi_aximm2_ARREGION(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARREGION),
    .m_axi_aximm2_ARUSER(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_ARUSER),
    .m_axi_aximm2_RVALID(aximm2_RVALID),
    .m_axi_aximm2_RREADY(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_RREADY),
    .m_axi_aximm2_RDATA(aximm2_RDATA),
    .m_axi_aximm2_RLAST(aximm2_RLAST),
    .m_axi_aximm2_RID(aximm2_RID),
    .m_axi_aximm2_RFIFONUM(aximm2_RFIFONUM),
    .m_axi_aximm2_RUSER(aximm2_RUSER),
    .m_axi_aximm2_RRESP(aximm2_RRESP),
    .m_axi_aximm2_BVALID(1'b0),
    .m_axi_aximm2_BREADY(Loop_VITIS_LOOP_35_3_proc3_U0_m_axi_aximm2_BREADY),
    .m_axi_aximm2_BRESP(2'd0),
    .m_axi_aximm2_BID(1'd0),
    .m_axi_aximm2_BUSER(1'd0),
    .v2_buffer_V_din(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_din),
    .v2_buffer_V_num_data_valid(v2_buffer_V_num_data_valid),
    .v2_buffer_V_fifo_cap(v2_buffer_V_fifo_cap),
    .v2_buffer_V_full_n(v2_buffer_V_full_n),
    .v2_buffer_V_write(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_write),
    .ap_ext_blocking_n(Loop_VITIS_LOOP_35_3_proc3_U0_ap_ext_blocking_n),
    .ap_str_blocking_n(Loop_VITIS_LOOP_35_3_proc3_U0_ap_str_blocking_n),
    .ap_int_blocking_n(Loop_VITIS_LOOP_35_3_proc3_U0_ap_int_blocking_n)
);

ydma_Loop_VITIS_LOOP_36_4_proc4 Loop_VITIS_LOOP_36_4_proc4_U0(
    .ap_clk(ap_clk),
    .ap_rst(ap_rst_n_inv),
    .ap_start(Loop_VITIS_LOOP_36_4_proc4_U0_ap_start),
    .ap_done(Loop_VITIS_LOOP_36_4_proc4_U0_ap_done),
    .ap_continue(Loop_VITIS_LOOP_36_4_proc4_U0_ap_continue),
    .ap_idle(Loop_VITIS_LOOP_36_4_proc4_U0_ap_idle),
    .ap_ready(Loop_VITIS_LOOP_36_4_proc4_U0_ap_ready),
    .output_size_dout(output_size_c_dout),
    .output_size_num_data_valid(output_size_c_num_data_valid),
    .output_size_fifo_cap(output_size_c_fifo_cap),
    .output_size_empty_n(output_size_c_empty_n),
    .output_size_read(Loop_VITIS_LOOP_36_4_proc4_U0_output_size_read),
    .output2_dout(output2_c_dout),
    .output2_num_data_valid(output2_c_num_data_valid),
    .output2_fifo_cap(output2_c_fifo_cap),
    .output2_empty_n(output2_c_empty_n),
    .output2_read(Loop_VITIS_LOOP_36_4_proc4_U0_output2_read),
    .m_axi_aximm2_AWVALID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWVALID),
    .m_axi_aximm2_AWREADY(aximm2_AWREADY),
    .m_axi_aximm2_AWADDR(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWADDR),
    .m_axi_aximm2_AWID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWID),
    .m_axi_aximm2_AWLEN(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWLEN),
    .m_axi_aximm2_AWSIZE(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWSIZE),
    .m_axi_aximm2_AWBURST(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWBURST),
    .m_axi_aximm2_AWLOCK(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWLOCK),
    .m_axi_aximm2_AWCACHE(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWCACHE),
    .m_axi_aximm2_AWPROT(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWPROT),
    .m_axi_aximm2_AWQOS(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWQOS),
    .m_axi_aximm2_AWREGION(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWREGION),
    .m_axi_aximm2_AWUSER(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_AWUSER),
    .m_axi_aximm2_WVALID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WVALID),
    .m_axi_aximm2_WREADY(aximm2_WREADY),
    .m_axi_aximm2_WDATA(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WDATA),
    .m_axi_aximm2_WSTRB(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WSTRB),
    .m_axi_aximm2_WLAST(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WLAST),
    .m_axi_aximm2_WID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WID),
    .m_axi_aximm2_WUSER(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_WUSER),
    .m_axi_aximm2_ARVALID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARVALID),
    .m_axi_aximm2_ARREADY(1'b0),
    .m_axi_aximm2_ARADDR(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARADDR),
    .m_axi_aximm2_ARID(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARID),
    .m_axi_aximm2_ARLEN(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARLEN),
    .m_axi_aximm2_ARSIZE(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARSIZE),
    .m_axi_aximm2_ARBURST(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARBURST),
    .m_axi_aximm2_ARLOCK(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARLOCK),
    .m_axi_aximm2_ARCACHE(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARCACHE),
    .m_axi_aximm2_ARPROT(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARPROT),
    .m_axi_aximm2_ARQOS(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARQOS),
    .m_axi_aximm2_ARREGION(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARREGION),
    .m_axi_aximm2_ARUSER(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_ARUSER),
    .m_axi_aximm2_RVALID(1'b0),
    .m_axi_aximm2_RREADY(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_RREADY),
    .m_axi_aximm2_RDATA(512'd0),
    .m_axi_aximm2_RLAST(1'b0),
    .m_axi_aximm2_RID(1'd0),
    .m_axi_aximm2_RFIFONUM(9'd0),
    .m_axi_aximm2_RUSER(1'd0),
    .m_axi_aximm2_RRESP(2'd0),
    .m_axi_aximm2_BVALID(aximm2_BVALID),
    .m_axi_aximm2_BREADY(Loop_VITIS_LOOP_36_4_proc4_U0_m_axi_aximm2_BREADY),
    .m_axi_aximm2_BRESP(aximm2_BRESP),
    .m_axi_aximm2_BID(aximm2_BID),
    .m_axi_aximm2_BUSER(aximm2_BUSER),
    .v2_buffer_V_dout(v2_buffer_V_dout),
    .v2_buffer_V_num_data_valid(v2_buffer_V_num_data_valid),
    .v2_buffer_V_fifo_cap(v2_buffer_V_fifo_cap),
    .v2_buffer_V_empty_n(v2_buffer_V_empty_n),
    .v2_buffer_V_read(Loop_VITIS_LOOP_36_4_proc4_U0_v2_buffer_V_read),
    .ap_ext_blocking_n(Loop_VITIS_LOOP_36_4_proc4_U0_ap_ext_blocking_n),
    .ap_str_blocking_n(Loop_VITIS_LOOP_36_4_proc4_U0_ap_str_blocking_n),
    .ap_int_blocking_n(Loop_VITIS_LOOP_36_4_proc4_U0_ap_int_blocking_n)
);

ydma_fifo_w64_d3_S output1_c_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(entry_proc_U0_output1_c_din),
    .if_full_n(output1_c_full_n),
    .if_write(entry_proc_U0_output1_c_write),
    .if_dout(output1_c_dout),
    .if_num_data_valid(output1_c_num_data_valid),
    .if_fifo_cap(output1_c_fifo_cap),
    .if_empty_n(output1_c_empty_n),
    .if_read(Loop_VITIS_LOOP_32_2_proc2_U0_output1_read)
);

ydma_fifo_w64_d3_S output2_c_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(entry_proc_U0_output2_c_din),
    .if_full_n(output2_c_full_n),
    .if_write(entry_proc_U0_output2_c_write),
    .if_dout(output2_c_dout),
    .if_num_data_valid(output2_c_num_data_valid),
    .if_fifo_cap(output2_c_fifo_cap),
    .if_empty_n(output2_c_empty_n),
    .if_read(Loop_VITIS_LOOP_36_4_proc4_U0_output2_read)
);

ydma_fifo_w32_d3_S output_size_c_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(entry_proc_U0_output_size_c_din),
    .if_full_n(output_size_c_full_n),
    .if_write(entry_proc_U0_output_size_c_write),
    .if_dout(output_size_c_dout),
    .if_num_data_valid(output_size_c_num_data_valid),
    .if_fifo_cap(output_size_c_fifo_cap),
    .if_empty_n(output_size_c_empty_n),
    .if_read(Loop_VITIS_LOOP_36_4_proc4_U0_output_size_read)
);

ydma_fifo_w32_d3_S num_total_cnt_c_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(entry_proc_U0_num_total_cnt_c_din),
    .if_full_n(num_total_cnt_c_full_n),
    .if_write(entry_proc_U0_num_total_cnt_c_write),
    .if_dout(num_total_cnt_c_dout),
    .if_num_data_valid(num_total_cnt_c_num_data_valid),
    .if_fifo_cap(num_total_cnt_c_fifo_cap),
    .if_empty_n(num_total_cnt_c_empty_n),
    .if_read(Loop_VITIS_LOOP_32_2_proc2_U0_num_total_cnt_read)
);
/*
ydma_fifo_w64_d512_A v1_buffer_V_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_din),
    .if_full_n(v1_buffer_V_full_n),
    .if_write(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_write),
    .if_dout(v1_buffer_V_dout),
    .if_num_data_valid(v1_buffer_V_num_data_valid),
    .if_fifo_cap(v1_buffer_V_fifo_cap),
    .if_empty_n(v1_buffer_V_empty_n),
    .if_read(Loop_VITIS_LOOP_32_2_proc2_U0_v1_buffer_V_read)
);

ydma_fifo_w512_d1024_A v2_buffer_V_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_din),
    .if_full_n(v2_buffer_V_full_n),
    .if_write(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_write),
    .if_dout(v2_buffer_V_dout),
    .if_num_data_valid(v2_buffer_V_num_data_valid),
    .if_fifo_cap(v2_buffer_V_fifo_cap),
    .if_empty_n(v2_buffer_V_empty_n),
    .if_read(Loop_VITIS_LOOP_36_4_proc4_U0_v2_buffer_V_read)
);
*/
ydma_start_for_Loop_VITIS_LOOP_32_2_proc2_U0 start_for_Loop_VITIS_LOOP_32_2_proc2_U0_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(start_for_Loop_VITIS_LOOP_32_2_proc2_U0_din),
    .if_full_n(start_for_Loop_VITIS_LOOP_32_2_proc2_U0_full_n),
    .if_write(entry_proc_U0_start_write),
    .if_dout(start_for_Loop_VITIS_LOOP_32_2_proc2_U0_dout),
    .if_empty_n(start_for_Loop_VITIS_LOOP_32_2_proc2_U0_empty_n),
    .if_read(Loop_VITIS_LOOP_32_2_proc2_U0_ap_ready)
);

ydma_start_for_Loop_VITIS_LOOP_36_4_proc4_U0 start_for_Loop_VITIS_LOOP_36_4_proc4_U0_U(
    .clk(ap_clk),
    .reset(ap_rst_n_inv),
    .if_read_ce(1'b1),
    .if_write_ce(1'b1),
    .if_din(start_for_Loop_VITIS_LOOP_36_4_proc4_U0_din),
    .if_full_n(start_for_Loop_VITIS_LOOP_36_4_proc4_U0_full_n),
    .if_write(entry_proc_U0_start_write),
    .if_dout(start_for_Loop_VITIS_LOOP_36_4_proc4_U0_dout),
    .if_empty_n(start_for_Loop_VITIS_LOOP_36_4_proc4_U0_empty_n),
    .if_read(Loop_VITIS_LOOP_36_4_proc4_U0_ap_ready)
);


wire [48:0] din_leaf_0_bft;
wire [48:0] din_leaf_1_bft;
wire [48:0] din_leaf_2_bft;
wire [48:0] din_leaf_3_bft;
wire [48:0] din_leaf_4_bft;
wire [48:0] din_leaf_5_bft;
wire [48:0] din_leaf_6_bft;
wire [48:0] din_leaf_7_bft;
wire [48:0] din_leaf_8_bft;
wire [48:0] din_leaf_9_bft;
wire [48:0] din_leaf_10_bft;
wire [48:0] din_leaf_11_bft;
wire [48:0] din_leaf_12_bft;
wire [48:0] din_leaf_13_bft;
wire [48:0] din_leaf_14_bft;
wire [48:0] din_leaf_15_bft;
wire [48:0] din_leaf_16_bft;
wire [48:0] din_leaf_17_bft;
wire [48:0] din_leaf_18_bft;
wire [48:0] din_leaf_19_bft;
wire [48:0] din_leaf_20_bft;
wire [48:0] din_leaf_21_bft;
wire [48:0] din_leaf_22_bft;
wire [48:0] din_leaf_23_bft;
// wire [48:0] din_leaf_24_bft;
// wire [48:0] din_leaf_25_bft;
// wire [48:0] din_leaf_26_bft;
// wire [48:0] din_leaf_27_bft;
// wire [48:0] din_leaf_28_bft;
// wire [48:0] din_leaf_29_bft;
// wire [48:0] din_leaf_30_bft;
// wire [48:0] din_leaf_31_bft;

reg [48:0] din_leaf_0_reg;
reg [48:0] din_leaf_1_reg;
reg [48:0] din_leaf_2_reg;
reg [48:0] din_leaf_3_reg;
reg [48:0] din_leaf_4_reg;
reg [48:0] din_leaf_5_reg;
reg [48:0] din_leaf_6_reg;
reg [48:0] din_leaf_7_reg;
reg [48:0] din_leaf_8_reg;
reg [48:0] din_leaf_9_reg;
reg [48:0] din_leaf_10_reg;
reg [48:0] din_leaf_11_reg;
reg [48:0] din_leaf_12_reg;
reg [48:0] din_leaf_13_reg;
reg [48:0] din_leaf_14_reg;
reg [48:0] din_leaf_15_reg;
reg [48:0] din_leaf_16_reg;
reg [48:0] din_leaf_17_reg;
reg [48:0] din_leaf_18_reg;
reg [48:0] din_leaf_19_reg;
reg [48:0] din_leaf_20_reg;
reg [48:0] din_leaf_21_reg;
reg [48:0] din_leaf_22_reg;
reg [48:0] din_leaf_23_reg;
// reg [48:0] din_leaf_24_reg;
// reg [48:0] din_leaf_25_reg;
// reg [48:0] din_leaf_26_reg;
// reg [48:0] din_leaf_27_reg;
// reg [48:0] din_leaf_28_reg;
// reg [48:0] din_leaf_29_reg;
// reg [48:0] din_leaf_30_reg;
// reg [48:0] din_leaf_31_reg;

wire [48:0] din_leaf_0;
wire [48:0] din_leaf_1;
// wire [48:0] din_leaf_2;
// wire [48:0] din_leaf_3;
// wire [48:0] din_leaf_4;
// wire [48:0] din_leaf_5;
// wire [48:0] din_leaf_6;
// wire [48:0] din_leaf_7;
// wire [48:0] din_leaf_8;
// wire [48:0] din_leaf_9;
// wire [48:0] din_leaf_10;
// wire [48:0] din_leaf_11;
// wire [48:0] din_leaf_12;
// wire [48:0] din_leaf_13;
// wire [48:0] din_leaf_14;
// wire [48:0] din_leaf_15;
// wire [48:0] din_leaf_16;
// wire [48:0] din_leaf_17;
// wire [48:0] din_leaf_18;
// wire [48:0] din_leaf_19;
// wire [48:0] din_leaf_20;
// wire [48:0] din_leaf_21;
// wire [48:0] din_leaf_22;
// wire [48:0] din_leaf_23;
// wire [48:0] din_leaf_24;
// wire [48:0] din_leaf_25;
// wire [48:0] din_leaf_26;
// wire [48:0] din_leaf_27;
// wire [48:0] din_leaf_28;
// wire [48:0] din_leaf_29;
// wire [48:0] din_leaf_30;
// wire [48:0] din_leaf_31;



wire [48:0] dout_leaf_0_bft;
wire [48:0] dout_leaf_1_bft;
wire [48:0] dout_leaf_2_bft;
wire [48:0] dout_leaf_3_bft;
wire [48:0] dout_leaf_4_bft;
wire [48:0] dout_leaf_5_bft;
wire [48:0] dout_leaf_6_bft;
wire [48:0] dout_leaf_7_bft;
wire [48:0] dout_leaf_8_bft;
wire [48:0] dout_leaf_9_bft;
wire [48:0] dout_leaf_10_bft;
wire [48:0] dout_leaf_11_bft;
wire [48:0] dout_leaf_12_bft;
wire [48:0] dout_leaf_13_bft;
wire [48:0] dout_leaf_14_bft;
wire [48:0] dout_leaf_15_bft;
wire [48:0] dout_leaf_16_bft;
wire [48:0] dout_leaf_17_bft;
wire [48:0] dout_leaf_18_bft;
wire [48:0] dout_leaf_19_bft;
wire [48:0] dout_leaf_20_bft;
wire [48:0] dout_leaf_21_bft;
wire [48:0] dout_leaf_22_bft;
wire [48:0] dout_leaf_23_bft;
// wire [48:0] dout_leaf_24_bft;
// wire [48:0] dout_leaf_25_bft;
// wire [48:0] dout_leaf_26_bft;
// wire [48:0] dout_leaf_27_bft;
// wire [48:0] dout_leaf_28_bft;
// wire [48:0] dout_leaf_29_bft;
// wire [48:0] dout_leaf_30_bft;
// wire [48:0] dout_leaf_31_bft;

reg [48:0] dout_leaf_0_reg;
reg [48:0] dout_leaf_1_reg;
reg [48:0] dout_leaf_2_reg;
reg [48:0] dout_leaf_3_reg;
reg [48:0] dout_leaf_4_reg;
reg [48:0] dout_leaf_5_reg;
reg [48:0] dout_leaf_6_reg;
reg [48:0] dout_leaf_7_reg;
reg [48:0] dout_leaf_8_reg;
reg [48:0] dout_leaf_9_reg;
reg [48:0] dout_leaf_10_reg;
reg [48:0] dout_leaf_11_reg;
reg [48:0] dout_leaf_12_reg;
reg [48:0] dout_leaf_13_reg;
reg [48:0] dout_leaf_14_reg;
reg [48:0] dout_leaf_15_reg;
reg [48:0] dout_leaf_16_reg;
reg [48:0] dout_leaf_17_reg;
reg [48:0] dout_leaf_18_reg;
reg [48:0] dout_leaf_19_reg;
reg [48:0] dout_leaf_20_reg;
reg [48:0] dout_leaf_21_reg;
reg [48:0] dout_leaf_22_reg;
reg [48:0] dout_leaf_23_reg;
// reg [48:0] dout_leaf_24_reg;
// reg [48:0] dout_leaf_25_reg;
// reg [48:0] dout_leaf_26_reg;
// reg [48:0] dout_leaf_27_reg;
// reg [48:0] dout_leaf_28_reg;
// reg [48:0] dout_leaf_29_reg;
// reg [48:0] dout_leaf_30_reg;
// reg [48:0] dout_leaf_31_reg;

wire [48:0] dout_leaf_0;
wire [48:0] dout_leaf_1;
// wire [48:0] dout_leaf_2;
// wire [48:0] dout_leaf_3;
// wire [48:0] dout_leaf_4;
// wire [48:0] dout_leaf_5;
// wire [48:0] dout_leaf_6;
// wire [48:0] dout_leaf_7;
// wire [48:0] dout_leaf_8;
// wire [48:0] dout_leaf_9;
// wire [48:0] dout_leaf_10;
// wire [48:0] dout_leaf_11;
// wire [48:0] dout_leaf_12;
// wire [48:0] dout_leaf_13;
// wire [48:0] dout_leaf_14;
// wire [48:0] dout_leaf_15;
// wire [48:0] dout_leaf_16;
// wire [48:0] dout_leaf_17;
// wire [48:0] dout_leaf_18;
// wire [48:0] dout_leaf_19;
// wire [48:0] dout_leaf_20;
// wire [48:0] dout_leaf_21;
// wire [48:0] dout_leaf_22;
// wire [48:0] dout_leaf_23;
// wire [48:0] dout_leaf_24;
// wire [48:0] dout_leaf_25;
// wire [48:0] dout_leaf_26;
// wire [48:0] dout_leaf_27;
// wire [48:0] dout_leaf_28;
// wire [48:0] dout_leaf_29;
// wire [48:0] dout_leaf_30;
// wire [48:0] dout_leaf_31;



wire resend_0_bft;
wire resend_1_bft;
wire resend_2_bft;
wire resend_3_bft;
wire resend_4_bft;
wire resend_5_bft;
wire resend_6_bft;
wire resend_7_bft;
wire resend_8_bft;
wire resend_9_bft;
wire resend_10_bft;
wire resend_11_bft;
wire resend_12_bft;
wire resend_13_bft;
wire resend_14_bft;
wire resend_15_bft;
wire resend_16_bft;
wire resend_17_bft;
wire resend_18_bft;
wire resend_19_bft;
wire resend_20_bft;
wire resend_21_bft;
wire resend_22_bft;
wire resend_23_bft;
wire resend_24_bft;
wire resend_25_bft;
wire resend_26_bft;
wire resend_27_bft;
wire resend_28_bft;
wire resend_29_bft;
wire resend_30_bft;
wire resend_31_bft;

reg resend_0_reg;
reg resend_1_reg;
reg resend_2_reg;
reg resend_3_reg;
reg resend_4_reg;
reg resend_5_reg;
reg resend_6_reg;
reg resend_7_reg;
reg resend_8_reg;
reg resend_9_reg;
reg resend_10_reg;
reg resend_11_reg;
reg resend_12_reg;
reg resend_13_reg;
reg resend_14_reg;
reg resend_15_reg;
reg resend_16_reg;
reg resend_17_reg;
reg resend_18_reg;
reg resend_19_reg;
reg resend_20_reg;
reg resend_21_reg;
reg resend_22_reg;
reg resend_23_reg;
// reg resend_24_reg;
// reg resend_25_reg;
// reg resend_26_reg;
// reg resend_27_reg;
// reg resend_28_reg;
// reg resend_29_reg;
// reg resend_30_reg;
// reg resend_31_reg;

wire resend_0;
wire resend_1;
// wire resend_2;
// wire resend_3;
// wire resend_4;
// wire resend_5;
// wire resend_6;
// wire resend_7;
// wire resend_8;
// wire resend_9;
// wire resend_10;
// wire resend_11;
// wire resend_12;
// wire resend_13;
// wire resend_14;
// wire resend_15;
// wire resend_16;
// wire resend_17;
// wire resend_18;
// wire resend_19;
// wire resend_20;
// wire resend_21;
// wire resend_22;
// wire resend_23;
// wire resend_24;
// wire resend_25;
// wire resend_26;
// wire resend_27;
// wire resend_28;
// wire resend_29;
// wire resend_30;
// wire resend_31;



wire [31:0] tdata1;
wire        tvalid1;
wire        tready1;

wire [31:0] tdata2;
wire        tvalid2;
wire        tready2;

wire [63:0] tdata3;
wire        tvalid3;
wire        tready3;

wire [7:0] is_done_output_size;
wire is_done_output_size_valid;
wire is_done_output_size_ack;

wire [31:0] output_size_I1;
wire  output_size_valid_I1;
wire [15:0] num_cnt_read_I1;
wire  num_cnt_read_valid_I1;


config_parser config_parser_inst(
    .ap_clk(ap_clk),
    .ap_rst_n(ap_rst_n),
    .ap_start(1'b1),
    .ap_done(),
    .ap_idle(),
    .ap_ready(),
    .input1_TDATA(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_din),
    .input1_TVALID(Loop_VITIS_LOOP_31_1_proc1_U0_v1_buffer_V_write),
    .input1_TREADY(v1_buffer_V_full_n),
    .input2_TDATA(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_din),
    .input2_TVALID(Loop_VITIS_LOOP_35_3_proc3_U0_v2_buffer_V_write),
    .input2_TREADY(v2_buffer_V_full_n),

    .input3_TDATA(is_done_output_size),
    .input3_TVALID(is_done_output_size_valid),
    .input3_TREADY(is_done_output_size_ack),

    .output1_TDATA(tdata3), // config data
    .output1_TVALID(tvalid3),
    .output1_TREADY(~resend_0),
    .output2_TDATA(tdata1), // data
    .output2_TVALID(tvalid1),
    .output2_TREADY(tready1),
    .output3_TDATA(output_size_I1),
    .output3_TVALID(output_size_valid_I1),
    .output3_TREADY(1'b1), // always ready
    .output4_TDATA(num_cnt_read_I1),
    .output4_TVALID(num_cnt_read_valid_I1),
    .output4_TREADY(1'b1) // always ready
);

data32to512 data32to512_inst(
    .ap_clk(ap_clk),
    .ap_rst_n(ap_rst_n),
    .ap_start(1'b1),
    .ap_done(),
    .ap_idle(),
    .ap_ready(),
    .Input_1_V_TDATA(tdata2),
    .Input_1_V_TVALID(tvalid2),
    .Input_1_V_TREADY(tready2),
    .Output_1_V_TDATA(v2_buffer_V_dout),
    .Output_1_V_TVALID(v2_buffer_V_empty_n),
    .Output_1_V_TREADY(Loop_VITIS_LOOP_36_4_proc4_U0_v2_buffer_V_read)
);

InterfaceWrapper1 InterfaceWrapper1_inst(
    .clk(ap_clk),
    .din_leaf_bft2interface(din_leaf_1),
    .dout_leaf_interface2bft(dout_leaf_1),
    .resend(resend_1),
    .Input_1_V_V(tdata1),
    .Input_1_V_V_ap_vld(tvalid1),
    .Input_1_V_V_ap_ack(tready1),
    .Output_1_V_V(tdata2),
    .Output_1_V_V_ap_vld(tvalid2),
    .Output_1_V_V_ap_ack(tready2),
    
    .cnt(v1_buffer_V_dout),
    .cnt_vld(v1_buffer_V_empty_n),
    .cnt_ack(Loop_VITIS_LOOP_32_2_proc2_U0_v1_buffer_V_read),
    
    .output_size(output_size_I1),
    .output_size_valid(output_size_valid_I1),
    .num_cnt_read(num_cnt_read_I1), // added
    .num_cnt_read_valid(num_cnt_read_valid_I1), // added        
    .is_done_output_size(is_done_output_size), // added
    .is_done_output_size_valid(is_done_output_size_valid), // added
    
    .reset(ap_rst_n_inv_400_p1),
    .ap_start(ap_start)
    );


assign din_leaf_0 = din_leaf_0_reg;
assign din_leaf_1 = din_leaf_1_reg;
assign din_leaf_2 = din_leaf_2_reg;
assign din_leaf_3 = din_leaf_3_reg;
assign din_leaf_4 = din_leaf_4_reg;
assign din_leaf_5 = din_leaf_5_reg;
assign din_leaf_6 = din_leaf_6_reg;
assign din_leaf_7 = din_leaf_7_reg;
assign din_leaf_8 = din_leaf_8_reg;
assign din_leaf_9 = din_leaf_9_reg;
assign din_leaf_10 = din_leaf_10_reg;
assign din_leaf_11 = din_leaf_11_reg;
assign din_leaf_12 = din_leaf_12_reg;
assign din_leaf_13 = din_leaf_13_reg;
assign din_leaf_14 = din_leaf_14_reg;
assign din_leaf_15 = din_leaf_15_reg;
assign din_leaf_16 = din_leaf_16_reg;
assign din_leaf_17 = din_leaf_17_reg;
assign din_leaf_18 = din_leaf_18_reg;
assign din_leaf_19 = din_leaf_19_reg;
assign din_leaf_20 = din_leaf_20_reg;
assign din_leaf_21 = din_leaf_21_reg;
assign din_leaf_22 = din_leaf_22_reg;
assign din_leaf_23 = din_leaf_23_reg;

assign resend_0 = resend_0_reg;
assign resend_1 = resend_1_reg;
assign resend_2 = resend_2_reg;
assign resend_3 = resend_3_reg;
assign resend_4 = resend_4_reg;
assign resend_5 = resend_5_reg;
assign resend_6 = resend_6_reg;
assign resend_7 = resend_7_reg;
assign resend_8 = resend_8_reg;
assign resend_9 = resend_9_reg;
assign resend_10 = resend_10_reg;
assign resend_11 = resend_11_reg;
assign resend_12 = resend_12_reg;
assign resend_13 = resend_13_reg;
assign resend_14 = resend_14_reg;
assign resend_15 = resend_15_reg;
assign resend_16 = resend_16_reg;
assign resend_17 = resend_17_reg;
assign resend_18 = resend_18_reg;
assign resend_19 = resend_19_reg;
assign resend_20 = resend_20_reg;
assign resend_21 = resend_21_reg;
assign resend_22 = resend_22_reg;
assign resend_23 = resend_23_reg;

assign dout_leaf_0_bft = dout_leaf_0_reg;
assign dout_leaf_1_bft = dout_leaf_1_reg;
assign dout_leaf_2_bft = dout_leaf_2_reg;
assign dout_leaf_3_bft = dout_leaf_3_reg;
assign dout_leaf_4_bft = dout_leaf_4_reg;
assign dout_leaf_5_bft = dout_leaf_5_reg;
assign dout_leaf_6_bft = dout_leaf_6_reg;
assign dout_leaf_7_bft = dout_leaf_7_reg;
assign dout_leaf_8_bft = dout_leaf_8_reg;
assign dout_leaf_9_bft = dout_leaf_9_reg;
assign dout_leaf_10_bft = dout_leaf_10_reg;
assign dout_leaf_11_bft = dout_leaf_11_reg;
assign dout_leaf_12_bft = dout_leaf_12_reg;
assign dout_leaf_13_bft = dout_leaf_13_reg;
assign dout_leaf_14_bft = dout_leaf_14_reg;
assign dout_leaf_15_bft = dout_leaf_15_reg;
assign dout_leaf_16_bft = dout_leaf_16_reg;
assign dout_leaf_17_bft = dout_leaf_17_reg;
assign dout_leaf_18_bft = dout_leaf_18_reg;
assign dout_leaf_19_bft = dout_leaf_19_reg;
assign dout_leaf_20_bft = dout_leaf_20_reg;
assign dout_leaf_21_bft = dout_leaf_21_reg;
assign dout_leaf_22_bft = dout_leaf_22_reg;
assign dout_leaf_23_bft = dout_leaf_23_reg;


    always @ (posedge ap_clk) begin 
        if (ap_rst_n_inv == 1'b1) begin
            din_leaf_0_reg <= 0;
            din_leaf_1_reg <= 0;
            din_leaf_2_reg <= 0;
            din_leaf_3_reg <= 0;
            din_leaf_4_reg <= 0;
            din_leaf_5_reg <= 0;
            din_leaf_6_reg <= 0;
            din_leaf_7_reg <= 0;
            din_leaf_8_reg <= 0;
            din_leaf_9_reg <= 0;
            din_leaf_10_reg <= 0;
            din_leaf_11_reg <= 0;
            din_leaf_12_reg <= 0;
            din_leaf_13_reg <= 0;
            din_leaf_14_reg <= 0;
            din_leaf_15_reg <= 0;
            din_leaf_16_reg <= 0;
            din_leaf_17_reg <= 0;
            din_leaf_18_reg <= 0;
            din_leaf_19_reg <= 0;
            din_leaf_20_reg <= 0;
            din_leaf_21_reg <= 0;
            din_leaf_22_reg <= 0;
            din_leaf_23_reg <= 0;

            resend_0_reg <= 0;
            resend_1_reg <= 0;
            resend_2_reg <= 0;
            resend_3_reg <= 0;
            resend_4_reg <= 0;
            resend_5_reg <= 0;
            resend_6_reg <= 0;
            resend_7_reg <= 0;
            resend_8_reg <= 0;
            resend_9_reg <= 0;
            resend_10_reg <= 0;
            resend_11_reg <= 0;
            resend_12_reg <= 0;
            resend_13_reg <= 0;
            resend_14_reg <= 0;
            resend_15_reg <= 0;
            resend_16_reg <= 0;
            resend_17_reg <= 0;
            resend_18_reg <= 0;
            resend_19_reg <= 0;
            resend_20_reg <= 0;
            resend_21_reg <= 0;
            resend_22_reg <= 0;
            resend_23_reg <= 0;

            dout_leaf_0_reg <= 0;
            dout_leaf_1_reg <= 0;
            dout_leaf_2_reg <= 0;
            dout_leaf_3_reg <= 0;
            dout_leaf_4_reg <= 0;
            dout_leaf_5_reg <= 0;
            dout_leaf_6_reg <= 0;
            dout_leaf_7_reg <= 0;
            dout_leaf_8_reg <= 0;
            dout_leaf_9_reg <= 0;
            dout_leaf_10_reg <= 0;
            dout_leaf_11_reg <= 0;
            dout_leaf_12_reg <= 0;
            dout_leaf_13_reg <= 0;
            dout_leaf_14_reg <= 0;
            dout_leaf_15_reg <= 0;
            dout_leaf_16_reg <= 0;
            dout_leaf_17_reg <= 0;
            dout_leaf_18_reg <= 0;
            dout_leaf_19_reg <= 0;
            dout_leaf_20_reg <= 0;
            dout_leaf_21_reg <= 0;
            dout_leaf_22_reg <= 0;
            dout_leaf_23_reg <= 0;
        end
        else begin
            din_leaf_0_reg <= din_leaf_0_bft;
            din_leaf_1_reg <= din_leaf_1_bft;
            din_leaf_2_reg <= din_leaf_2_bft; 
            din_leaf_3_reg <= din_leaf_3_bft; 
            din_leaf_4_reg <= din_leaf_4_bft; 
            din_leaf_5_reg <= din_leaf_5_bft; 
            din_leaf_6_reg <= din_leaf_6_bft; 
            din_leaf_7_reg <= din_leaf_7_bft; 
            din_leaf_8_reg <= din_leaf_8_bft; 
            din_leaf_9_reg <= din_leaf_9_bft; 
            din_leaf_10_reg <= din_leaf_10_bft; 
            din_leaf_11_reg <= din_leaf_11_bft; 
            din_leaf_12_reg <= din_leaf_12_bft; 
            din_leaf_13_reg <= din_leaf_13_bft; 
            din_leaf_14_reg <= din_leaf_14_bft; 
            din_leaf_15_reg <= din_leaf_15_bft; 
            din_leaf_16_reg <= din_leaf_16_bft; 
            din_leaf_17_reg <= din_leaf_17_bft; 
            din_leaf_18_reg <= din_leaf_18_bft; 
            din_leaf_19_reg <= din_leaf_19_bft; 
            din_leaf_20_reg <= din_leaf_20_bft; 
            din_leaf_21_reg <= din_leaf_21_bft; 
            din_leaf_22_reg <= din_leaf_22_bft; 
            din_leaf_23_reg <= din_leaf_23_bft; 

            resend_0_reg <= resend_0_bft;
            resend_1_reg <= resend_1_bft;
            resend_2_reg <= resend_2_bft; 
            resend_3_reg <= resend_3_bft; 
            resend_4_reg <= resend_4_bft; 
            resend_5_reg <= resend_5_bft; 
            resend_6_reg <= resend_6_bft; 
            resend_7_reg <= resend_7_bft; 
            resend_8_reg <= resend_8_bft; 
            resend_9_reg <= resend_9_bft; 
            resend_10_reg <= resend_10_bft; 
            resend_11_reg <= resend_11_bft; 
            resend_12_reg <= resend_12_bft; 
            resend_13_reg <= resend_13_bft; 
            resend_14_reg <= resend_14_bft; 
            resend_15_reg <= resend_15_bft; 
            resend_16_reg <= resend_16_bft; 
            resend_17_reg <= resend_17_bft; 
            resend_18_reg <= resend_18_bft; 
            resend_19_reg <= resend_19_bft; 
            resend_20_reg <= resend_20_bft; 
            resend_21_reg <= resend_21_bft; 
            resend_22_reg <= resend_22_bft; 
            resend_23_reg <= resend_23_bft; 

            dout_leaf_0_reg <= {tvalid3, tdata3[47:0]};
            dout_leaf_1_reg <= dout_leaf_1; 
            dout_leaf_2_reg <= dout_leaf_2; 
            dout_leaf_3_reg <= dout_leaf_3;
            dout_leaf_4_reg <= dout_leaf_4; 
            dout_leaf_5_reg <= dout_leaf_5; 
            dout_leaf_6_reg <= dout_leaf_6;
            dout_leaf_7_reg <= dout_leaf_7; 
            dout_leaf_8_reg <= dout_leaf_8; 
            dout_leaf_9_reg <= dout_leaf_9;
            dout_leaf_10_reg <= dout_leaf_10; 
            dout_leaf_11_reg <= dout_leaf_11; 
            dout_leaf_12_reg <= dout_leaf_12;
            dout_leaf_13_reg <= dout_leaf_13; 
            dout_leaf_14_reg <= dout_leaf_14; 
            dout_leaf_15_reg <= dout_leaf_15;
            dout_leaf_16_reg <= dout_leaf_16; 
            dout_leaf_17_reg <= dout_leaf_17; 
            dout_leaf_18_reg <= dout_leaf_18;
            dout_leaf_19_reg <= dout_leaf_19;
            dout_leaf_20_reg <= dout_leaf_20; 
            dout_leaf_21_reg <= dout_leaf_21; 
            dout_leaf_22_reg <= dout_leaf_22;
            dout_leaf_23_reg <= dout_leaf_23;
        end
    end


(* DONT_TOUCH = "yes" *) bft bft_inst(
    .clk(ap_clk),
    .dout_leaf_0(dout_leaf_0_bft),
    .dout_leaf_1(dout_leaf_1_bft),
    .dout_leaf_2(dout_leaf_2_bft),
    .dout_leaf_3(dout_leaf_3_bft),
    .dout_leaf_4(dout_leaf_4_bft),
    .dout_leaf_5(dout_leaf_5_bft),
    .dout_leaf_6(dout_leaf_6_bft),
    .dout_leaf_7(dout_leaf_7_bft),
    .dout_leaf_8(dout_leaf_8_bft),
    .dout_leaf_9(dout_leaf_9_bft),
    .dout_leaf_10(dout_leaf_10_bft),
    .dout_leaf_11(dout_leaf_11_bft),
    .dout_leaf_12(dout_leaf_12_bft),
    .dout_leaf_13(dout_leaf_13_bft),
    .dout_leaf_14(dout_leaf_14_bft),
    .dout_leaf_15(dout_leaf_15_bft),
    .dout_leaf_16(dout_leaf_16_bft),
    .dout_leaf_17(dout_leaf_17_bft),
    .dout_leaf_18(dout_leaf_18_bft),
    .dout_leaf_19(dout_leaf_19_bft),
    .dout_leaf_20(dout_leaf_20_bft),
    .dout_leaf_21(dout_leaf_21_bft),
    .dout_leaf_22(dout_leaf_22_bft),
    .dout_leaf_23(dout_leaf_23_bft),
    // .dout_leaf_24(dout_leaf_24_bft),
    // .dout_leaf_25(dout_leaf_25_bft),
    // .dout_leaf_26(dout_leaf_26_bft),
    // .dout_leaf_27(dout_leaf_27_bft),
    // .dout_leaf_28(dout_leaf_28_bft),
    // .dout_leaf_29(dout_leaf_29_bft),
    // .dout_leaf_30(dout_leaf_30_bft),
    // .dout_leaf_31(dout_leaf_31_bft),
    .din_leaf_0(din_leaf_0_bft),
    .din_leaf_1(din_leaf_1_bft),
    .din_leaf_2(din_leaf_2_bft),
    .din_leaf_3(din_leaf_3_bft),
    .din_leaf_4(din_leaf_4_bft),
    .din_leaf_5(din_leaf_5_bft),
    .din_leaf_6(din_leaf_6_bft),
    .din_leaf_7(din_leaf_7_bft),
    .din_leaf_8(din_leaf_8_bft),
    .din_leaf_9(din_leaf_9_bft),
    .din_leaf_10(din_leaf_10_bft),
    .din_leaf_11(din_leaf_11_bft),
    .din_leaf_12(din_leaf_12_bft),
    .din_leaf_13(din_leaf_13_bft),
    .din_leaf_14(din_leaf_14_bft),
    .din_leaf_15(din_leaf_15_bft),
    .din_leaf_16(din_leaf_16_bft),
    .din_leaf_17(din_leaf_17_bft),
    .din_leaf_18(din_leaf_18_bft),
    .din_leaf_19(din_leaf_19_bft),
    .din_leaf_20(din_leaf_20_bft),
    .din_leaf_21(din_leaf_21_bft),
    .din_leaf_22(din_leaf_22_bft),
    .din_leaf_23(din_leaf_23_bft),
    // .din_leaf_24(din_leaf_24_bft),
    // .din_leaf_25(din_leaf_25_bft),
    // .din_leaf_26(din_leaf_26_bft),
    // .din_leaf_27(din_leaf_27_bft),
    // .din_leaf_28(din_leaf_28_bft),
    // .din_leaf_29(din_leaf_29_bft),
    // .din_leaf_30(din_leaf_30_bft),
    // .din_leaf_31(din_leaf_31_bft),
   .resend_0(resend_0_bft),
   .resend_1(resend_1_bft),
   .resend_2(resend_2_bft),
   .resend_3(resend_3_bft),
   .resend_4(resend_4_bft),
   .resend_5(resend_5_bft),
   .resend_6(resend_6_bft),
   .resend_7(resend_7_bft),
   .resend_8(resend_8_bft),
   .resend_9(resend_9_bft),
   .resend_10(resend_10_bft),
   .resend_11(resend_11_bft),
   .resend_12(resend_12_bft),
   .resend_13(resend_13_bft),
   .resend_14(resend_14_bft),
   .resend_15(resend_15_bft),
   .resend_16(resend_16_bft),
   .resend_17(resend_17_bft),
   .resend_18(resend_18_bft),
   .resend_19(resend_19_bft),
   .resend_20(resend_20_bft),
   .resend_21(resend_21_bft),
   .resend_22(resend_22_bft),
   .resend_23(resend_23_bft),
   // .resend_24(resend_24_bft),
   // .resend_25(resend_25_bft),
   // .resend_26(resend_26_bft),
   // .resend_27(resend_27_bft),
   // .resend_28(resend_28_bft),
   // .resend_29(resend_29_bft),
   // .resend_30(resend_30_bft),
   // .resend_31(resend_31_bft)
    .reset(ap_rst_n_inv_bft),
    .reset_0(ap_rst_n_inv_400_p0),
    .reset_1(ap_rst_n_inv_400_p1),
    .reset_2(ap_rst_n_inv_400_p2_bft),
    .reset_3(ap_rst_n_inv_400_p3_bft),
    .reset_4(ap_rst_n_inv_400_p4_bft),
    .reset_5(ap_rst_n_inv_400_p5_bft),
    .reset_6(ap_rst_n_inv_400_p6_bft),
    .reset_7(ap_rst_n_inv_400_p7_bft),
    .reset_8(ap_rst_n_inv_400_p8_bft),
    .reset_9(ap_rst_n_inv_400_p9_bft),
    .reset_10(ap_rst_n_inv_400_p10_bft),
    .reset_11(ap_rst_n_inv_400_p11_bft),
    .reset_12(ap_rst_n_inv_400_p12_bft),
    .reset_13(ap_rst_n_inv_400_p13_bft),
    .reset_14(ap_rst_n_inv_400_p14_bft),
    .reset_15(ap_rst_n_inv_400_p15_bft),
    .reset_16(ap_rst_n_inv_400_p16_bft),
    .reset_17(ap_rst_n_inv_400_p17_bft),
    .reset_18(ap_rst_n_inv_400_p18_bft),
    .reset_19(ap_rst_n_inv_400_p19_bft),
    .reset_20(ap_rst_n_inv_400_p20_bft),
    .reset_21(ap_rst_n_inv_400_p21_bft),
    .reset_22(ap_rst_n_inv_400_p22_bft),
    .reset_23(ap_rst_n_inv_400_p23_bft)
    );



always @ (posedge ap_clk) begin
    if (ap_rst_n_inv == 1'b1) begin
        ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready <= 1'b0;
    end else begin
        if (((ap_sync_ready & ap_start) == 1'b1)) begin
            ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready <= 1'b0;
        end else begin
            ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready <= ap_sync_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst_n_inv == 1'b1) begin
        ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready <= 1'b0;
    end else begin
        if (((ap_sync_ready & ap_start) == 1'b1)) begin
            ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready <= 1'b0;
        end else begin
            ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready <= ap_sync_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready;
        end
    end
end

always @ (posedge ap_clk) begin
    if (ap_rst_n_inv == 1'b1) begin
        ap_sync_reg_entry_proc_U0_ap_ready <= 1'b0;
    end else begin
        if (((ap_sync_ready & ap_start) == 1'b1)) begin
            ap_sync_reg_entry_proc_U0_ap_ready <= 1'b0;
        end else begin
            ap_sync_reg_entry_proc_U0_ap_ready <= ap_sync_entry_proc_U0_ap_ready;
        end
    end
end

always @ (posedge ap_clk) begin
    ap_ext_blocking_n_reg <= ap_ext_blocking_n;
end

always @ (posedge ap_clk) begin
    ap_int_blocking_n_reg <= ap_int_blocking_n;
end

always @ (posedge ap_clk) begin
    ap_rst_n_inv <= ap_rst_reg_1;

    // added by dopark
    ap_rst_n_inv_bft <= ap_rst_reg_1;
    ap_rst_n_inv_aximm1_m_axi_U <= ap_rst_reg_1;
    ap_rst_n_inv_aximm2_m_axi_U <= ap_rst_reg_1;

    ap_rst_n_inv_400_p0 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p1 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p2 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p3 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p4 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p5 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p6 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p7 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p8 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p9 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p10 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p11 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p12 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p13 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p14 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p15 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p16 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p17 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p18 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p19 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p20 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p21 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p22 <= ap_rst_reg_1;
    ap_rst_n_inv_400_p23 <= ap_rst_reg_1;

    ap_rst_n_inv_400_p2_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p3_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p4_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p5_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p6_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p7_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p8_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p9_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p10_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p11_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p12_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p13_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p14_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p15_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p16_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p17_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p18_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p19_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p20_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p21_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p22_bft <= ap_rst_reg_1;
    ap_rst_n_inv_400_p23_bft <= ap_rst_reg_1;

end

always @ (posedge ap_clk) begin
    ap_rst_reg_1 <= ap_rst_reg_2;
end

always @ (posedge ap_clk) begin
    ap_rst_reg_2 <= ~ap_rst_n;
end

(* dont_touch = "true" *) reg ap_start_400_p2_2;
(* dont_touch = "true" *) reg ap_start_400_p3_2;
(* dont_touch = "true" *) reg ap_start_400_p4_2;
(* dont_touch = "true" *) reg ap_start_400_p5_2;
(* dont_touch = "true" *) reg ap_start_400_p6_2;
(* dont_touch = "true" *) reg ap_start_400_p7_2;
(* dont_touch = "true" *) reg ap_start_400_p8_2;
(* dont_touch = "true" *) reg ap_start_400_p9_2;
(* dont_touch = "true" *) reg ap_start_400_p10_2;
(* dont_touch = "true" *) reg ap_start_400_p11_2;
(* dont_touch = "true" *) reg ap_start_400_p12_2;
(* dont_touch = "true" *) reg ap_start_400_p13_2;
(* dont_touch = "true" *) reg ap_start_400_p14_2;
(* dont_touch = "true" *) reg ap_start_400_p15_2;
(* dont_touch = "true" *) reg ap_start_400_p16_2;
(* dont_touch = "true" *) reg ap_start_400_p17_2;
(* dont_touch = "true" *) reg ap_start_400_p18_2;
(* dont_touch = "true" *) reg ap_start_400_p19_2;
(* dont_touch = "true" *) reg ap_start_400_p20_2;
(* dont_touch = "true" *) reg ap_start_400_p21_2;
(* dont_touch = "true" *) reg ap_start_400_p22_2;
(* dont_touch = "true" *) reg ap_start_400_p23_2;

// This results in two cycles delay for PR pages' ap_starts
// But it should be fine.
// added by dopark
always @ (posedge ap_clk) begin
    ap_start_400_p2_2 <= ap_start_400_p2_1;
    ap_start_400_p3_2 <= ap_start_400_p3_1;
    ap_start_400_p4_2 <= ap_start_400_p4_1;
    ap_start_400_p5_2 <= ap_start_400_p5_1;
    ap_start_400_p6_2 <= ap_start_400_p6_1;
    ap_start_400_p7_2 <= ap_start_400_p7_1;
    ap_start_400_p8_2 <= ap_start_400_p8_1;
    ap_start_400_p9_2 <= ap_start_400_p9_1;
    ap_start_400_p10_2 <= ap_start_400_p10_1;
    ap_start_400_p11_2 <= ap_start_400_p11_1;
    ap_start_400_p12_2 <= ap_start_400_p12_1;
    ap_start_400_p13_2 <= ap_start_400_p13_1;
    ap_start_400_p14_2 <= ap_start_400_p14_1;
    ap_start_400_p15_2 <= ap_start_400_p15_1;
    ap_start_400_p16_2 <= ap_start_400_p16_1;
    ap_start_400_p17_2 <= ap_start_400_p17_1;
    ap_start_400_p18_2 <= ap_start_400_p18_1;
    ap_start_400_p19_2 <= ap_start_400_p19_1;
    ap_start_400_p20_2 <= ap_start_400_p20_1;
    ap_start_400_p21_2 <= ap_start_400_p21_1;
    ap_start_400_p22_2 <= ap_start_400_p22_1;
    ap_start_400_p23_2 <= ap_start_400_p23_1;

    ap_start_400_p2 <= ap_start_400_p2_2;
    ap_start_400_p3 <= ap_start_400_p3_2;
    ap_start_400_p4 <= ap_start_400_p4_2;
    ap_start_400_p5 <= ap_start_400_p5_2;
    ap_start_400_p6 <= ap_start_400_p6_2;
    ap_start_400_p7 <= ap_start_400_p7_2;
    ap_start_400_p8 <= ap_start_400_p8_2;
    ap_start_400_p9 <= ap_start_400_p9_2;
    ap_start_400_p10 <= ap_start_400_p10_2;
    ap_start_400_p11 <= ap_start_400_p11_2;
    ap_start_400_p12 <= ap_start_400_p12_2;
    ap_start_400_p13 <= ap_start_400_p13_2;
    ap_start_400_p14 <= ap_start_400_p14_2;
    ap_start_400_p15 <= ap_start_400_p15_2;
    ap_start_400_p16 <= ap_start_400_p16_2;
    ap_start_400_p17 <= ap_start_400_p17_2;
    ap_start_400_p18 <= ap_start_400_p18_2;
    ap_start_400_p19 <= ap_start_400_p19_2;
    ap_start_400_p20 <= ap_start_400_p20_2;
    ap_start_400_p21 <= ap_start_400_p21_2;
    ap_start_400_p22 <= ap_start_400_p22_2;
    ap_start_400_p23 <= ap_start_400_p23_2;
end




always @ (posedge ap_clk) begin
    ap_str_blocking_n_reg <= ap_str_blocking_n;
end

always @ (*) begin
    if (((ap_ext_blocking_n_reg == 1'b0) & (ap_ext_blocking_n == 1'b1))) begin
        stall_done_ext = 1'b1;
    end else begin
        stall_done_ext = 1'b0;
    end
end

always @ (*) begin
    if (((ap_int_blocking_n_reg == 1'b0) & (ap_int_blocking_n == 1'b1))) begin
        stall_done_int = 1'b1;
    end else begin
        stall_done_int = 1'b0;
    end
end

always @ (*) begin
    if (((ap_str_blocking_n_reg == 1'b0) & (ap_str_blocking_n == 1'b1))) begin
        stall_done_str = 1'b1;
    end else begin
        stall_done_str = 1'b0;
    end
end

always @ (*) begin
    if (((ap_ext_blocking_n_reg == 1'b1) & (ap_ext_blocking_n == 1'b0))) begin
        stall_start_ext = 1'b1;
    end else begin
        stall_start_ext = 1'b0;
    end
end

always @ (*) begin
    if (((ap_int_blocking_n_reg == 1'b1) & (ap_int_blocking_n == 1'b0))) begin
        stall_start_int = 1'b1;
    end else begin
        stall_start_int = 1'b0;
    end
end

always @ (*) begin
    if (((ap_str_blocking_n_reg == 1'b1) & (ap_str_blocking_n == 1'b0))) begin
        stall_start_str = 1'b1;
    end else begin
        stall_start_str = 1'b0;
    end
end

assign Loop_VITIS_LOOP_31_1_proc1_U0_ap_continue = 1'b1;

assign Loop_VITIS_LOOP_31_1_proc1_U0_ap_start = ((ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready ^ 1'b1) & ap_start);

assign Loop_VITIS_LOOP_32_2_proc2_U0_ap_continue = ap_sync_continue;

assign Loop_VITIS_LOOP_32_2_proc2_U0_ap_start = start_for_Loop_VITIS_LOOP_32_2_proc2_U0_empty_n;

assign Loop_VITIS_LOOP_35_3_proc3_U0_ap_continue = 1'b1;

assign Loop_VITIS_LOOP_35_3_proc3_U0_ap_start = ((ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready ^ 1'b1) & ap_start);

assign Loop_VITIS_LOOP_36_4_proc4_U0_ap_continue = ap_sync_continue;

assign Loop_VITIS_LOOP_36_4_proc4_U0_ap_start = start_for_Loop_VITIS_LOOP_36_4_proc4_U0_empty_n;

assign ap_done = ap_sync_done;

assign ap_ext_blocking_cur_n = 1'b1;

assign ap_ext_blocking_n = (ap_ext_blocking_sub_n & ap_ext_blocking_cur_n);

assign ap_ext_blocking_sub_n = (entry_proc_U0_ap_ext_blocking_n & Loop_VITIS_LOOP_36_4_proc4_U0_ap_ext_blocking_n & Loop_VITIS_LOOP_35_3_proc3_U0_ap_ext_blocking_n & Loop_VITIS_LOOP_32_2_proc2_U0_ap_ext_blocking_n & Loop_VITIS_LOOP_31_1_proc1_U0_ap_ext_blocking_n);

assign ap_idle = (entry_proc_U0_ap_idle & Loop_VITIS_LOOP_36_4_proc4_U0_ap_idle & Loop_VITIS_LOOP_35_3_proc3_U0_ap_idle & Loop_VITIS_LOOP_32_2_proc2_U0_ap_idle & Loop_VITIS_LOOP_31_1_proc1_U0_ap_idle);

assign ap_int_blocking_cur_n = 1'b1;

assign ap_int_blocking_n = (ap_int_blocking_sub_n & ap_int_blocking_cur_n);

assign ap_int_blocking_sub_n = (entry_proc_U0_ap_int_blocking_n & Loop_VITIS_LOOP_36_4_proc4_U0_ap_int_blocking_n & Loop_VITIS_LOOP_35_3_proc3_U0_ap_int_blocking_n & Loop_VITIS_LOOP_32_2_proc2_U0_ap_int_blocking_n & Loop_VITIS_LOOP_31_1_proc1_U0_ap_int_blocking_n);

assign ap_ready = ap_sync_ready;

assign ap_str_blocking_cur_n = 1'b1;

assign ap_str_blocking_n = (ap_str_blocking_sub_n & ap_str_blocking_cur_n);

assign ap_str_blocking_sub_n = (entry_proc_U0_ap_str_blocking_n & Loop_VITIS_LOOP_36_4_proc4_U0_ap_str_blocking_n & Loop_VITIS_LOOP_35_3_proc3_U0_ap_str_blocking_n & Loop_VITIS_LOOP_32_2_proc2_U0_ap_str_blocking_n & Loop_VITIS_LOOP_31_1_proc1_U0_ap_str_blocking_n);

assign ap_sync_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready = (ap_sync_reg_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready | Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready);

assign ap_sync_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready = (ap_sync_reg_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready | Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready);

assign ap_sync_continue = (ap_sync_done & ap_continue);

assign ap_sync_done = (Loop_VITIS_LOOP_36_4_proc4_U0_ap_done & Loop_VITIS_LOOP_32_2_proc2_U0_ap_done);

assign ap_sync_entry_proc_U0_ap_ready = (entry_proc_U0_ap_ready | ap_sync_reg_entry_proc_U0_ap_ready);

assign ap_sync_ready = (ap_sync_entry_proc_U0_ap_ready & ap_sync_Loop_VITIS_LOOP_35_3_proc3_U0_ap_ready & ap_sync_Loop_VITIS_LOOP_31_1_proc1_U0_ap_ready);

assign aximm1_BID = 1'd0;

assign aximm1_BRESP = 2'd0;

assign aximm1_BUSER = 1'd0;

assign aximm1_RID = 1'd0;

assign aximm1_RLAST = 1'b0;

assign aximm1_RRESP = 2'd0;

assign aximm1_RUSER = 1'd0;

assign aximm2_BID = 1'd0;

assign aximm2_BRESP = 2'd0;

assign aximm2_BUSER = 1'd0;

assign aximm2_RID = 1'd0;

assign aximm2_RLAST = 1'b0;

assign aximm2_RRESP = 2'd0;

assign aximm2_RUSER = 1'd0;

assign entry_proc_U0_ap_continue = 1'b1;

assign entry_proc_U0_ap_start = ((ap_sync_reg_entry_proc_U0_ap_ready ^ 1'b1) & ap_start);

assign entry_proc_U0_start_full_n = (start_for_Loop_VITIS_LOOP_36_4_proc4_U0_full_n & start_for_Loop_VITIS_LOOP_32_2_proc2_U0_full_n);

assign event_done = ap_done;

assign start_for_Loop_VITIS_LOOP_32_2_proc2_U0_din = 1'b1;

assign start_for_Loop_VITIS_LOOP_36_4_proc4_U0_din = 1'b1;


reg find_df_deadlock = 0;
// synthesis translate_off
`include "ydma_hls_deadlock_detector.vh"
// synthesis translate_on

endmodule //ydma

