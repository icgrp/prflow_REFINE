/*
 Copyright (c) 2020, Xilinx
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name of FINN nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

module mva_0_memstream
#(
//parameters to enable/disable axi-mm, set number of streams, set readmemh for memory, set per-stream offsets in memory, set per-stream widths
    parameter CONFIG_EN = 1,
    parameter NSTREAMS = 1,//1 up to 6 // changed

    parameter MEM_DEPTH = 60, // changed
    parameter MEM_WIDTH = 1280, // changed
    parameter MEM_INIT = "/home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_test/operators/", // changed
    parameter RAM_STYLE = "auto", // changed

    //widths per stream
	parameter STRM0_WIDTH = 1280, // changed
	parameter STRM1_WIDTH = 32,
	parameter STRM2_WIDTH = 32,
	parameter STRM3_WIDTH = 32,
	parameter STRM4_WIDTH = 32,
	parameter STRM5_WIDTH = 32,

	//depths per stream
	parameter STRM0_DEPTH = 60, // changed
	parameter STRM1_DEPTH = 2304,
	parameter STRM2_DEPTH = 2304,
	parameter STRM3_DEPTH = 2304,
	parameter STRM4_DEPTH = 2304,
	parameter STRM5_DEPTH = 2304,

	//offsets for each stream
	parameter STRM0_OFFSET = 0,
	parameter STRM1_OFFSET = 2304,
	parameter STRM2_OFFSET = 4608,
	parameter STRM3_OFFSET = 6912,
	parameter STRM4_OFFSET = 9216,
	parameter STRM5_OFFSET = 11520,

    parameter AXILITE_ADDR_WIDTH = 2+$clog2(MEM_DEPTH*(1<<$clog2((MEM_WIDTH+31)/32)))
)

(
    input aclk,
    input aresetn,

    output awready,
    input                       awvalid,
    input [AXILITE_ADDR_WIDTH-1:0]      awaddr,
    input [2:0]                 awprot,
    //write data
    output                  wready,
    input                       wvalid,
    input [31:0]      wdata,
    input [3:0]  wstrb,
    //burst response
    input                       bready,
    output                  bvalid,
    output [1:0]            bresp,

    //Read channels
    //read address
    output                  arready,
    input                       arvalid,
    input [AXILITE_ADDR_WIDTH-1:0]      araddr,
    input [2:0]                 arprot,
    //read data
    input                       rready,
    output                  rvalid,
    output [1:0]            rresp,
    output [31:0] rdata,

    //multiple output AXI Streams, TDATA width rounded to multiple of 8 bits
    input m_axis_0_afull,
    input m_axis_0_tready,
    output m_axis_0_tvalid,
    output [((STRM0_WIDTH+7)/8)*8-1:0] m_axis_0_tdata,

    input m_axis_1_afull,
    input m_axis_1_tready,
    output m_axis_1_tvalid,
    output [((STRM1_WIDTH+7)/8)*8-1:0] m_axis_1_tdata,

    input m_axis_2_afull,
    input m_axis_2_tready,
    output m_axis_2_tvalid,
    output [((STRM2_WIDTH+7)/8)*8-1:0] m_axis_2_tdata,

    input m_axis_3_afull,
    input m_axis_3_tready,
    output m_axis_3_tvalid,
    output [((STRM3_WIDTH+7)/8)*8-1:0] m_axis_3_tdata,

    input m_axis_4_afull,
    input m_axis_4_tready,
    output m_axis_4_tvalid,
    output [((STRM4_WIDTH+7)/8)*8-1:0] m_axis_4_tdata,

    input m_axis_5_afull,
    input m_axis_5_tready,
    output m_axis_5_tvalid,
    output [((STRM5_WIDTH+7)/8)*8-1:0] m_axis_5_tdata


);

wire [31:0] config_address;
wire config_ce;
wire config_we;
wire config_rack;
wire [MEM_WIDTH-1:0] config_d0;
wire [MEM_WIDTH-1:0] config_q0;

generate
if(NSTREAMS <= 2) begin: singleblock


memstream_singleblock
#(
    .CONFIG_EN(CONFIG_EN),
    .NSTREAMS(NSTREAMS),
    .MEM_DEPTH(MEM_DEPTH),
    .MEM_WIDTH(MEM_WIDTH),
    .MEM_INIT(MEM_INIT),
    .RAM_STYLE(RAM_STYLE),

    //widths per stream
    .STRM0_WIDTH(STRM0_WIDTH),
    .STRM1_WIDTH(STRM1_WIDTH),

    //depths per stream
    .STRM0_DEPTH(STRM0_DEPTH),
    .STRM1_DEPTH(STRM1_DEPTH),

    //offsets for each stream
    .STRM0_OFFSET(STRM0_OFFSET),
    .STRM1_OFFSET(STRM1_OFFSET)
)
mem
(
    .aclk(aclk),
    .aresetn(aresetn),

    .config_address(config_address),
    .config_ce(config_ce),
    .config_we(config_we),
    .config_d0(config_d0),
    .config_q0(config_q0),
    .config_rack(config_rack),

    .m_axis_0_tready(m_axis_0_tready),
    .m_axis_0_tvalid(m_axis_0_tvalid),
    .m_axis_0_tdata(m_axis_0_tdata),

    .m_axis_1_tready(m_axis_1_tready),
    .m_axis_1_tvalid(m_axis_1_tvalid),
    .m_axis_1_tdata(m_axis_1_tdata)
);

assign m_axis_2_tvalid = 0;
assign m_axis_2_tdata = 0;
assign m_axis_3_tvalid = 0;
assign m_axis_3_tdata = 0;
assign m_axis_4_tvalid = 0;
assign m_axis_4_tdata = 0;
assign m_axis_5_tvalid = 0;
assign m_axis_5_tdata = 0;

end else begin: multiblock


memstream_multiblock
#(
    .CONFIG_EN(CONFIG_EN),
    .NSTREAMS(NSTREAMS),
    .MEM_DEPTH(MEM_DEPTH),
    .MEM_WIDTH(MEM_WIDTH),
    .MEM_INIT(MEM_INIT),
    .RAM_STYLE(RAM_STYLE),

    //widths per stream
    .STRM0_WIDTH(STRM0_WIDTH),
    .STRM1_WIDTH(STRM1_WIDTH),
    .STRM2_WIDTH(STRM2_WIDTH),
    .STRM3_WIDTH(STRM3_WIDTH),
    .STRM4_WIDTH(STRM4_WIDTH),
    .STRM5_WIDTH(STRM5_WIDTH),

    //depths per stream
    .STRM0_DEPTH(STRM0_DEPTH),
    .STRM1_DEPTH(STRM1_DEPTH),
    .STRM2_DEPTH(STRM2_DEPTH),
    .STRM3_DEPTH(STRM3_DEPTH),
    .STRM4_DEPTH(STRM4_DEPTH),
    .STRM5_DEPTH(STRM5_DEPTH),

    //offsets for each stream
    .STRM0_OFFSET(STRM0_OFFSET),
    .STRM1_OFFSET(STRM1_OFFSET),
    .STRM2_OFFSET(STRM2_OFFSET),
    .STRM3_OFFSET(STRM3_OFFSET),
    .STRM4_OFFSET(STRM4_OFFSET),
    .STRM5_OFFSET(STRM5_OFFSET)
)
mem
(
    .aclk(aclk),
    .aresetn(aresetn),

    .config_address(config_address),
    .config_ce(config_ce),
    .config_we(config_we),
    .config_d0(config_d0),
    .config_q0(config_q0),

    .m_axis_0_afull(m_axis_0_afull),
    .m_axis_0_tready(m_axis_0_tready),
    .m_axis_0_tvalid(m_axis_0_tvalid),
    .m_axis_0_tdata(m_axis_0_tdata),

    .m_axis_1_afull(m_axis_1_afull),
    .m_axis_1_tready(m_axis_1_tready),
    .m_axis_1_tvalid(m_axis_1_tvalid),
    .m_axis_1_tdata(m_axis_1_tdata),

    .m_axis_2_afull(m_axis_2_afull),
    .m_axis_2_tready(m_axis_2_tready),
    .m_axis_2_tvalid(m_axis_2_tvalid),
    .m_axis_2_tdata(m_axis_2_tdata),

    .m_axis_3_afull(m_axis_3_afull),
    .m_axis_3_tready(m_axis_3_tready),
    .m_axis_3_tvalid(m_axis_3_tvalid),
    .m_axis_3_tdata(m_axis_3_tdata),

    .m_axis_4_afull(m_axis_4_afull),
    .m_axis_4_tready(m_axis_4_tready),
    .m_axis_4_tvalid(m_axis_4_tvalid),
    .m_axis_4_tdata(m_axis_4_tdata),

    .m_axis_5_afull(m_axis_5_afull),
    .m_axis_5_tready(m_axis_5_tready),
    .m_axis_5_tvalid(m_axis_5_tvalid),
    .m_axis_5_tdata(m_axis_5_tdata)

);


end
endgenerate

axi4lite_if
#(
    .ADDR_WIDTH(AXILITE_ADDR_WIDTH),
    .DATA_WIDTH(32),
    .IP_DATA_WIDTH(MEM_WIDTH)
)
config_if
(
    //system signals
    .aclk(aclk),
    .aresetn(aresetn),

    //Write channels
    //write address
    .awready(awready),
    .awvalid(awvalid),
    .awaddr(awaddr),
    .awprot(awprot),
    //write data
    .wready(wready),
    .wvalid(wvalid),
    .wdata(wdata),
    .wstrb(wstrb),
    //burst response
    .bready(bready),
    .bvalid(bvalid),
    .bresp(bresp),

    //Read channels
    //read address
    .arready(arready),
    .arvalid(arvalid),
    .araddr(araddr),
    .arprot(arprot),
    //read data
    .rready(rready),
    .rvalid(rvalid),
    .rresp(rresp),
    .rdata(rdata),

    //IP-side interface
    .ip_en(config_ce),
    .ip_wen(config_we),
    .ip_addr(config_address),
    .ip_wdata(config_d0),
    .ip_rack(config_rack),
    .ip_rdata(config_q0)
);

endmodule


module axi4lite_if
#(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,//AXI4 spec requires this to be strictly 32 or 64
    parameter IP_DATA_WIDTH = 64//can be any power-of-2 multiple of DATA_WIDTH
)
(
//system signals
input aclk,
input aresetn,//active low, asynchronous assertion and synchronous deassertion

//Write channels
//write address
output reg                  awready,
input                       awvalid,
input [ADDR_WIDTH-1:0]      awaddr,
input [2:0]                 awprot,
//write data
output reg                  wready,
input                       wvalid,
input [DATA_WIDTH-1:0]      wdata,
input [(DATA_WIDTH/8)-1:0]  wstrb,
//burst response
input                       bready,
output reg                  bvalid,
output reg [1:0]            bresp,//NOTE: 00 = OKAY, 10 = SLVERR (write error)

//Read channels
//read address
output reg                  arready,
input                       arvalid,
input [ADDR_WIDTH-1:0]      araddr,
input [2:0]                 arprot,
//read data
input                       rready,
output reg                  rvalid,
output reg [1:0]            rresp,//NOTE: 00 = OKAY, 10 = SLVERR (read error)
output reg [DATA_WIDTH-1:0] rdata,

//IP-side interface
output reg                  ip_en,
output reg                  ip_wen,
output reg [ADDR_WIDTH-1:0] ip_addr,
output [IP_DATA_WIDTH-1:0]  ip_wdata,
input                       ip_rack,
input [IP_DATA_WIDTH-1:0]      ip_rdata
);

localparam RESP_OKAY = 2'b00;
localparam RESP_SLVERR = 2'b10;
//get ceil(log2(ceil(IP_DATA_WIDTH/DATA_WIDTH)))
localparam NFOLDS_LOG = $clog2((IP_DATA_WIDTH + DATA_WIDTH - 1) / DATA_WIDTH);

reg                      internal_ren;
reg                      internal_wen;
reg                      internal_wack;
reg [ADDR_WIDTH-1:0]     internal_raddr;
reg [ADDR_WIDTH-1:0]     internal_waddr;
reg [DATA_WIDTH-1:0]     internal_wdata;
wire [DATA_WIDTH-1:0]    internal_rdata;
reg                      internal_error = 0;

//check DATA_WIDTH
initial begin
    if(DATA_WIDTH != 32 & DATA_WIDTH != 64) begin
        $display("AXI4Lite DATA_WIDTH must be 32 or 64");
        $finish;
    end
end

//transaction state machine
localparam  STATE_IDLE  = 0,
            STATE_READ  = 1,
            STATE_WRITE = 2;

reg [1:0] state;

always @(posedge aclk or negedge aresetn)
    if(~aresetn)
        state <= STATE_IDLE;
    else case(state)
        STATE_IDLE:
            if(awvalid & wvalid)
                state <= STATE_WRITE;
            else if(arvalid)
                state <= STATE_READ;
        STATE_READ:
            if(rvalid & rready)
                state <= STATE_IDLE;
        STATE_WRITE:
            if(bvalid & bready)
                state <= STATE_IDLE;
        default: state <= STATE_IDLE;
    endcase

//write-related internal signals
always @(*) begin
    internal_waddr = awaddr >> $clog2(DATA_WIDTH/8);
    internal_wdata = wdata;
    internal_wen = (state == STATE_IDLE) & awvalid & wvalid;
end

always @(posedge aclk) begin
    awready <= internal_wen;
    wready <= internal_wen;
end

//read-related internal signals
always @(*) begin
    internal_raddr = araddr >> $clog2(DATA_WIDTH/8);
    internal_ren = (state == STATE_IDLE) & ~internal_wen & arvalid;
end

always @(posedge aclk)
    arready <= internal_ren;

wire write_to_last_fold;

always @(posedge aclk) begin
    ip_wen <= write_to_last_fold;
    ip_en <= internal_ren | write_to_last_fold;
    if(internal_ren | write_to_last_fold)
        ip_addr <= internal_ren ? (internal_raddr >> NFOLDS_LOG) : (internal_waddr >> NFOLDS_LOG);
    internal_wack <= internal_wen;
end

genvar i;
reg [(1<<NFOLDS_LOG)*DATA_WIDTH-1:0] ip_wdata_wide;
generate
if(NFOLDS_LOG == 0) begin: no_fold
    assign write_to_last_fold = internal_wen;
    assign internal_rdata = ip_rdata;
    always @(posedge aclk)
        ip_wdata_wide <= internal_wdata;
end else begin: fold
    reg [NFOLDS_LOG-1:0] internal_rfold;
    assign write_to_last_fold = internal_wen & (internal_waddr[NFOLDS_LOG-1:0] == {(NFOLDS_LOG){1'b1}});
    assign internal_rdata = ip_rdata >> (internal_rfold*DATA_WIDTH);
    always @(posedge aclk)
        if(internal_ren)
            internal_rfold <= internal_raddr[NFOLDS_LOG-1:0];
    for(i=0; i<(1<<NFOLDS_LOG); i = i+1) begin: gen_wdata
        always @(posedge aclk)
            if(internal_waddr[NFOLDS_LOG-1:0] == i)
                ip_wdata_wide[(i+1)*DATA_WIDTH-1:i*DATA_WIDTH] <= internal_wdata;
    end
end
endgenerate
assign ip_wdata = ip_wdata_wide[IP_DATA_WIDTH-1:0];

//write response on AXI4L bus
always @(posedge aclk or negedge aresetn)
    if(~aresetn) begin
        bvalid <= 0;//AXI4 spec requires BVALID pulled LOW during reset
        bresp <= RESP_OKAY;
    end else if(internal_wack) begin
        bvalid <= 1;
        bresp <= internal_error ? RESP_SLVERR : RESP_OKAY;
    end else if(bready) begin
        bvalid <= 0;
        bresp <= RESP_OKAY;
    end

//read response on AXI4L bus
always @(posedge aclk or negedge aresetn)
    if(~aresetn) begin
        rvalid <= 0;//AXI4 spec requires RVALID pulled LOW during reset
        rdata <= 0;
        rresp <= RESP_OKAY;
    end else if(ip_rack) begin
        rvalid <= 1;
        rdata <= internal_rdata;
        rresp <= internal_error ? RESP_SLVERR : RESP_OKAY;
    end else if(rready) begin
        rvalid <= 0;
        rdata <= 0;
        rresp <= RESP_OKAY;
    end

endmodule


module memstream_multiblock
#(
//parameters to enable/disable axi-mm, set number of streams, set readmemh for memory, set per-stream offsets in memory, set per-stream widths
    parameter CONFIG_EN = 1,
    parameter NSTREAMS = 6,//1 up to 6

    parameter MEM_DEPTH = 13824,
    parameter MEM_WIDTH = 32,
    parameter MEM_INIT = "./",
    parameter RAM_STYLE = "auto",

    //widths per stream
    parameter STRM0_WIDTH = 32,
    parameter STRM1_WIDTH = 32,
    parameter STRM2_WIDTH = 32,
    parameter STRM3_WIDTH = 32,
    parameter STRM4_WIDTH = 32,
    parameter STRM5_WIDTH = 32,

    //depths per stream
    parameter STRM0_DEPTH = 2304,
    parameter STRM1_DEPTH = 2304,
    parameter STRM2_DEPTH = 2304,
    parameter STRM3_DEPTH = 2304,
    parameter STRM4_DEPTH = 2304,
    parameter STRM5_DEPTH = 2304,

    //offsets for each stream
    parameter STRM0_OFFSET = 0,
    parameter STRM1_OFFSET = 2304,
    parameter STRM2_OFFSET = 4608,
    parameter STRM3_OFFSET = 6912,
    parameter STRM4_OFFSET = 9216,
    parameter STRM5_OFFSET = 11520
)

(
    input aclk,
    input aresetn,

    //optional configuration interface compatible with ap_memory
    input [31:0] config_address,
    input config_ce,
    input config_we,
    input [31:0] config_d0,
    output [31:0] config_q0,
    output config_rack,

    //multiple output AXI Streams, TDATA width rounded to multiple of 8 bits
    input m_axis_0_afull,
    input m_axis_0_tready,
    output m_axis_0_tvalid,
    output [((STRM0_WIDTH+7)/8)*8-1:0] m_axis_0_tdata,

    input m_axis_1_afull,
    input m_axis_1_tready,
    output m_axis_1_tvalid,
    output [((STRM1_WIDTH+7)/8)*8-1:0] m_axis_1_tdata,

    input m_axis_2_afull,
    input m_axis_2_tready,
    output m_axis_2_tvalid,
    output [((STRM2_WIDTH+7)/8)*8-1:0] m_axis_2_tdata,

    input m_axis_3_afull,
    input m_axis_3_tready,
    output m_axis_3_tvalid,
    output [((STRM3_WIDTH+7)/8)*8-1:0] m_axis_3_tdata,

    input m_axis_4_afull,
    input m_axis_4_tready,
    output m_axis_4_tvalid,
    output [((STRM4_WIDTH+7)/8)*8-1:0] m_axis_4_tdata,

    input m_axis_5_afull,
    input m_axis_5_tready,
    output m_axis_5_tvalid,
    output [((STRM5_WIDTH+7)/8)*8-1:0] m_axis_5_tdata


);

//calculate number of RAMB18 blocks we need depth-wise
localparam NMEMBLOCKS = (MEM_DEPTH+1023) / 1024; //ceil(MEM_DEPTH/1024)

//calculate width of address for each block
localparam BLOCKADRWIDTH = NMEMBLOCKS > 1 ? 10 : $clog2(MEM_DEPTH);

//determine whether a stream needs to multiplex between memory blocks
localparam STRM0_MUX = ((STRM0_OFFSET/1024) != ((STRM0_OFFSET+STRM0_DEPTH)/1024));
localparam STRM1_MUX = ((STRM1_OFFSET/1024) != ((STRM1_OFFSET+STRM1_DEPTH)/1024));
localparam STRM2_MUX = ((STRM2_OFFSET/1024) != ((STRM2_OFFSET+STRM2_DEPTH)/1024));
localparam STRM3_MUX = ((STRM3_OFFSET/1024) != ((STRM3_OFFSET+STRM3_DEPTH)/1024));
localparam STRM4_MUX = ((STRM4_OFFSET/1024) != ((STRM4_OFFSET+STRM4_DEPTH)/1024));
localparam STRM5_MUX = ((STRM5_OFFSET/1024) != ((STRM5_OFFSET+STRM5_DEPTH)/1024));

//determine what the base block of each stream is
localparam STRM0_BLOCK = (STRM0_OFFSET/1024);
localparam STRM1_BLOCK = (STRM1_OFFSET/1024);
localparam STRM2_BLOCK = (STRM2_OFFSET/1024);
localparam STRM3_BLOCK = (STRM3_OFFSET/1024);
localparam STRM4_BLOCK = (STRM4_OFFSET/1024);
localparam STRM5_BLOCK = (STRM5_OFFSET/1024);

//determine what the end block of each stream is
localparam STRM0_END_BLOCK = ((STRM0_OFFSET+STRM0_DEPTH-1)/1024);
localparam STRM1_END_BLOCK = ((STRM1_OFFSET+STRM1_DEPTH-1)/1024);
localparam STRM2_END_BLOCK = ((STRM2_OFFSET+STRM2_DEPTH-1)/1024);
localparam STRM3_END_BLOCK = ((STRM3_OFFSET+STRM3_DEPTH-1)/1024);
localparam STRM4_END_BLOCK = ((STRM4_OFFSET+STRM4_DEPTH-1)/1024);
localparam STRM5_END_BLOCK = ((STRM5_OFFSET+STRM5_DEPTH-1)/1024);

//determine the number of blocks spanned by each stream
localparam STRM0_NBLOCKS = STRM0_END_BLOCK - STRM0_BLOCK + 1;
localparam STRM1_NBLOCKS = STRM1_END_BLOCK - STRM1_BLOCK + 1;
localparam STRM2_NBLOCKS = STRM2_END_BLOCK - STRM2_BLOCK + 1;
localparam STRM3_NBLOCKS = STRM3_END_BLOCK - STRM3_BLOCK + 1;
localparam STRM4_NBLOCKS = STRM4_END_BLOCK - STRM4_BLOCK + 1;
localparam STRM5_NBLOCKS = STRM5_END_BLOCK - STRM5_BLOCK + 1;

//TODO: check that memory width is equal to the widest stream
//TODO: check that the stream depths and offsets make sense, and that the memory depth is sufficient (or calculate depth here?)
initial begin
    if((NSTREAMS < 1) | (NSTREAMS > 6)) begin
        $display("Invalid setting for NSTREAMS, please set in range [1,6]");
        $finish();
    end
end

//invert reset
wire rst;
assign rst = ~aresetn;

//WARNING: pipeline depth is larger than the number of streams per port so we have in-flight writes that may see not-ready when they get executed
//solution: use prog-full to make sure we have an equal number of free slots in the stream to the read pipeline depth

reg [$clog2(MEM_DEPTH)-1:0] strm0_addr = STRM0_OFFSET;
reg [$clog2(MEM_DEPTH)-1:0] strm1_addr = STRM1_OFFSET;
reg [$clog2(MEM_DEPTH)-1:0] strm2_addr = STRM2_OFFSET;
reg [$clog2(MEM_DEPTH)-1:0] strm3_addr = STRM3_OFFSET;
reg [$clog2(MEM_DEPTH)-1:0] strm4_addr = STRM4_OFFSET;
reg [$clog2(MEM_DEPTH)-1:0] strm5_addr = STRM5_OFFSET;

reg strm0_incr_en;
reg strm1_incr_en;
reg strm2_incr_en;
reg strm3_incr_en;
reg strm4_incr_en;
reg strm5_incr_en;

wire strm0_rst;
wire strm1_rst;
wire strm2_rst;
wire strm3_rst;
wire strm4_rst;
wire strm5_rst;

reg strm0_ready;
reg strm1_ready;
reg strm2_ready;
reg strm3_ready;
reg strm4_ready;
reg strm5_ready;

//arbiter: work on one stream at a time
//multiplex each port between (up to) half of the streams
reg [1:0] current_stream_porta = 0;
reg [1:0] current_stream_portb = 0;

always @(posedge aclk) begin
    if(rst)
        current_stream_porta <= 0;
    else case(current_stream_porta)
        0: current_stream_porta <= strm2_ready ? 1 : strm4_ready ? 2 : 0;
        1: current_stream_porta <= strm4_ready ? 2 : strm0_ready ? 0 : 1;
        2: current_stream_porta <= strm0_ready ? 0 : strm2_ready ? 1 : 2;
    endcase
    if(rst)
        current_stream_portb <= 0;
    else case(current_stream_portb)
        0: current_stream_portb <= strm3_ready ? 1 : strm5_ready ? 2 : 0;
        1: current_stream_portb <= strm5_ready ? 2 : strm1_ready ? 0 : 1;
        2: current_stream_portb <= strm1_ready ? 0 : strm3_ready ? 1 : 2;
    endcase
end

always @(posedge aclk) begin
    if(rst) begin
        strm0_incr_en <= 0;
        strm1_incr_en <= 0;
        strm2_incr_en <= 0;
        strm3_incr_en <= 0;
        strm4_incr_en <= 0;
        strm5_incr_en <= 0;
    end else begin
        strm0_incr_en <= (current_stream_porta == 0) & strm0_ready;
        strm1_incr_en <= (current_stream_portb == 0) & strm1_ready;
        strm2_incr_en <= (current_stream_porta == 1) & strm2_ready;
        strm3_incr_en <= (current_stream_portb == 1) & strm3_ready;
        strm4_incr_en <= (current_stream_porta == 2) & strm4_ready;
        strm5_incr_en <= (current_stream_portb == 2) & strm5_ready;
    end
end

assign strm0_rst = strm0_incr_en & (strm0_addr == (STRM0_OFFSET + STRM0_DEPTH-1));
assign strm1_rst = strm1_incr_en & (strm1_addr == (STRM1_OFFSET + STRM1_DEPTH-1));
assign strm2_rst = strm2_incr_en & (strm2_addr == (STRM2_OFFSET + STRM2_DEPTH-1));
assign strm3_rst = strm3_incr_en & (strm3_addr == (STRM3_OFFSET + STRM3_DEPTH-1));
assign strm4_rst = strm4_incr_en & (strm4_addr == (STRM4_OFFSET + STRM4_DEPTH-1));
assign strm5_rst = strm5_incr_en & (strm5_addr == (STRM5_OFFSET + STRM5_DEPTH-1));

always @(posedge aclk) begin
    strm0_ready <= ~m_axis_0_afull;
    strm1_ready <= ~m_axis_1_afull & (NSTREAMS >= 2);
    strm2_ready <= ~m_axis_2_afull & (NSTREAMS >= 3);
    strm3_ready <= ~m_axis_3_afull & (NSTREAMS >= 4);
    strm4_ready <= ~m_axis_4_afull & (NSTREAMS >= 5);
    strm5_ready <= ~m_axis_5_afull & (NSTREAMS >= 6);
end

//one address counter per stream; more LUTs but keeps routing short and local
always @(posedge aclk) begin
    if(strm0_rst | rst)
        strm0_addr <= STRM0_OFFSET;
    else if(strm0_incr_en)
        strm0_addr <= strm0_addr + 1;
    if(strm1_rst | rst)
        strm1_addr <= STRM1_OFFSET;
    else if(strm1_incr_en)
        strm1_addr <= strm1_addr + 1;
    if(strm2_rst | rst)
        strm2_addr <= STRM2_OFFSET;
    else if(strm2_incr_en)
        strm2_addr <= strm2_addr + 1;
    if(strm3_rst | rst)
        strm3_addr <= STRM3_OFFSET;
    else if(strm3_incr_en)
        strm3_addr <= strm3_addr + 1;
    if(strm4_rst | rst)
        strm4_addr <= STRM4_OFFSET;
    else if(strm4_incr_en)
        strm4_addr <= strm4_addr + 1;
    if(strm5_rst | rst)
        strm5_addr <= STRM5_OFFSET;
    else if(strm5_incr_en)
        strm5_addr <= strm5_addr + 1;
end

reg [$clog2(MEM_DEPTH)-1:0] addra;
wire [MEM_WIDTH*NMEMBLOCKS-1:0] rdqa;

reg [$clog2(MEM_DEPTH)-1:0] addrb;
wire [MEM_WIDTH*NMEMBLOCKS-1:0] rdqb;

wire [NMEMBLOCKS-1:0] we;

reg [1:0] addr_select_porta;
reg [1:0] addr_select_portb;

//multiplex addresses of various streams into address ports of memory
always @(posedge aclk) begin
    addr_select_porta <= current_stream_porta;
    case(addr_select_porta)
        0: addra <= strm0_addr;
        1: addra <= strm2_addr;
        2: addra <= strm4_addr;
    endcase
    addr_select_portb <= current_stream_portb;
    case(addr_select_portb)
        0: addrb <= strm1_addr;
        1: addrb <= strm3_addr;
        2: addrb <= strm5_addr;
    endcase
end

genvar g;
generate for(g=0; g<NMEMBLOCKS; g=g+1) begin: blockports

assign we[g] = (CONFIG_EN == 1) & config_ce & config_we & (config_address[31:BLOCKADRWIDTH] == g);

ramb18_wf_dualport
#(
    .ID(g),
    .DWIDTH(MEM_WIDTH),
    .AWIDTH(BLOCKADRWIDTH),
    .MEM_INIT(MEM_INIT),
  .RAM_STYLE(RAM_STYLE)
)
ram
(
    .clk(aclk),

    .wea(we[g]),
    .ena(1'b1),
    .enqa(1'b1),
    .addra(we[g] ? config_address[BLOCKADRWIDTH-1:0] : addra[BLOCKADRWIDTH-1:0]),
    .wdataa(config_d0),
    .rdqa(rdqa[(g+1)*MEM_WIDTH-1:g*MEM_WIDTH]),

    .web(1'b0),
    .enb(1'b1),
    .enqb(1'b1),
    .addrb(addrb[BLOCKADRWIDTH-1:0]),
    .wdatab('d0),
    .rdqb(rdqb[(g+1)*MEM_WIDTH-1:g*MEM_WIDTH])
);

end
endgenerate

integer i;

generate if(NMEMBLOCKS > 1) begin: multiblock

wire [MEM_WIDTH-1:0] rdqmux[5:0];

reg [$clog2(MEM_DEPTH)-BLOCKADRWIDTH-1:0] rdblocka[2:0];
reg [$clog2(MEM_DEPTH)-BLOCKADRWIDTH-1:0] rdblockb[2:0];

always @(posedge aclk) begin
    rdblocka[0] <= addra[$clog2(MEM_DEPTH)-1:BLOCKADRWIDTH];
    rdblockb[0] <= addrb[$clog2(MEM_DEPTH)-1:BLOCKADRWIDTH];
    for(i=0; i<2; i=i+1) begin
        rdblocka[i+1] <= rdblocka[i];
        rdblockb[i+1] <= rdblockb[i];
    end
end

if(NSTREAMS >= 1) begin: en_strm0
    if(STRM0_MUX == 1) begin: mux0
        mux #(STRM0_NBLOCKS, MEM_WIDTH) m(rdqa[(STRM0_BLOCK+STRM0_NBLOCKS)*MEM_WIDTH-1:STRM0_BLOCK*MEM_WIDTH],rdqmux[0],rdblocka[1] - STRM0_BLOCK);
    end else begin: nomux0
        assign rdqmux[0] = rdqa[(STRM0_BLOCK+1)*MEM_WIDTH-1:STRM0_BLOCK*MEM_WIDTH];
    end
    assign m_axis_0_tdata = rdqmux[0][STRM0_WIDTH-1:0];
end

if(NSTREAMS >= 2) begin: en_strm1
    if(STRM1_MUX == 1) begin: mux1
        mux #(STRM1_NBLOCKS, MEM_WIDTH) m(rdqb[(STRM1_BLOCK+STRM1_NBLOCKS)*MEM_WIDTH-1:STRM1_BLOCK*MEM_WIDTH],rdqmux[1],rdblockb[1] - STRM1_BLOCK);
    end else begin: nomux1
        assign rdqmux[1] = rdqb[(STRM1_BLOCK+1)*MEM_WIDTH-1:STRM1_BLOCK*MEM_WIDTH];
    end
    assign m_axis_1_tdata = rdqmux[1][STRM1_WIDTH-1:0];
end

if(NSTREAMS >= 3) begin: en_strm2
    if(STRM2_MUX == 1) begin: mux2
        mux #(STRM2_NBLOCKS, MEM_WIDTH) m(rdqa[(STRM2_BLOCK+STRM2_NBLOCKS)*MEM_WIDTH-1:STRM2_BLOCK*MEM_WIDTH],rdqmux[2],rdblocka[1] - STRM2_BLOCK);
    end else begin: nomux2
        assign rdqmux[2] = rdqa[(STRM2_BLOCK+1)*MEM_WIDTH-1:STRM2_BLOCK*MEM_WIDTH];
    end
    assign m_axis_2_tdata = rdqmux[2][STRM2_WIDTH-1:0];
end

if(NSTREAMS >= 4) begin: en_strm3
    if(STRM3_MUX == 1) begin: mux3
        mux #(STRM3_NBLOCKS, MEM_WIDTH) m(rdqb[(STRM3_BLOCK+STRM3_NBLOCKS)*MEM_WIDTH-1:STRM3_BLOCK*MEM_WIDTH],rdqmux[3],rdblockb[1] - STRM3_BLOCK);
    end else begin: nomux3
        assign rdqmux[3] = rdqb[(STRM3_BLOCK+1)*MEM_WIDTH-1:STRM3_BLOCK*MEM_WIDTH];
    end
    assign m_axis_3_tdata = rdqmux[3][STRM3_WIDTH-1:0];
end

if(NSTREAMS >= 5) begin: en_strm4
    if(STRM4_MUX == 1) begin: mux4
        mux #(STRM4_NBLOCKS, MEM_WIDTH) m(rdqa[(STRM4_BLOCK+STRM4_NBLOCKS)*MEM_WIDTH-1:STRM4_BLOCK*MEM_WIDTH],rdqmux[4],rdblocka[1] - STRM4_BLOCK);
    end else begin: nomux4
        assign rdqmux[4] = rdqa[(STRM4_BLOCK+1)*MEM_WIDTH-1:STRM4_BLOCK*MEM_WIDTH];
    end
    assign m_axis_4_tdata = rdqmux[4][STRM4_WIDTH-1:0];
end

if(NSTREAMS >= 6) begin: en_strm5
    if(STRM5_MUX == 1) begin: mux5
        mux #(STRM5_NBLOCKS, MEM_WIDTH) m(rdqb[(STRM5_BLOCK+STRM5_NBLOCKS)*MEM_WIDTH-1:STRM5_BLOCK*MEM_WIDTH],rdqmux[5],rdblockb[1] - STRM5_BLOCK);
    end else begin: nomux5
        assign rdqmux[5] = rdqb[(STRM5_BLOCK+1)*MEM_WIDTH-1:STRM5_BLOCK*MEM_WIDTH];
    end
    assign m_axis_5_tdata = rdqmux[5][STRM5_WIDTH-1:0];
end

end else begin: singleblock

if(NSTREAMS >= 1) begin: en_strm0_direct
    assign m_axis_0_tdata = rdqa[STRM0_WIDTH-1:0];
end
if(NSTREAMS >= 2) begin: en_strm1_direct
    assign m_axis_1_tdata = rdqb[STRM1_WIDTH-1:0];
end
if(NSTREAMS >= 3) begin: en_strm2_direct
    assign m_axis_2_tdata = rdqa[STRM2_WIDTH-1:0];
end
if(NSTREAMS >= 4) begin: en_strm3_direct
    assign m_axis_3_tdata = rdqb[STRM3_WIDTH-1:0];
end
if(NSTREAMS >= 5) begin: en_strm4_direct
    assign m_axis_4_tdata = rdqa[STRM4_WIDTH-1:0];
end
if(NSTREAMS >= 6) begin: en_strm5_direct
    assign m_axis_5_tdata = rdqb[STRM5_WIDTH-1:0];
end

end
endgenerate

//output to AXI Streams
reg tvalid_pipe0[2:0];
reg tvalid_pipe1[2:0];
reg tvalid_pipe2[2:0];
reg tvalid_pipe3[2:0];
reg tvalid_pipe4[2:0];
reg tvalid_pipe5[2:0];

assign m_axis_0_tvalid = tvalid_pipe0[2];
assign m_axis_1_tvalid = tvalid_pipe1[2];
assign m_axis_2_tvalid = tvalid_pipe2[2];
assign m_axis_3_tvalid = tvalid_pipe3[2];
assign m_axis_4_tvalid = tvalid_pipe4[2];
assign m_axis_5_tvalid = tvalid_pipe5[2];


always @(posedge aclk) begin
    tvalid_pipe0[0] <= strm0_incr_en;
    tvalid_pipe1[0] <= strm1_incr_en;
    tvalid_pipe2[0] <= strm2_incr_en;
    tvalid_pipe3[0] <= strm3_incr_en;
    tvalid_pipe4[0] <= strm4_incr_en;
    tvalid_pipe5[0] <= strm5_incr_en;
    for(i=0; i<2; i=i+1) begin: srl
        tvalid_pipe0[i+1] <= tvalid_pipe0[i];
        tvalid_pipe1[i+1] <= tvalid_pipe1[i];
        tvalid_pipe2[i+1] <= tvalid_pipe2[i];
        tvalid_pipe3[i+1] <= tvalid_pipe3[i];
        tvalid_pipe4[i+1] <= tvalid_pipe4[i];
        tvalid_pipe5[i+1] <= tvalid_pipe5[i];
    end
end

//dummy read, for now
assign config_q0 = 0;
assign config_rack = config_ce & ~config_we;

endmodule


module memstream_singleblock
#(
    parameter CONFIG_EN = 1,
    parameter NSTREAMS = 2,//1 up to 2

    parameter MEM_DEPTH = 512,
    parameter MEM_WIDTH = 32,
    parameter MEM_INIT = "./",
    parameter RAM_STYLE = "auto",

    //widths per stream
    parameter STRM0_WIDTH = 32,
    parameter STRM1_WIDTH = 32,

    //depths per stream
    parameter STRM0_DEPTH = 256,
    parameter STRM1_DEPTH = 256,

    //offsets for each stream
    parameter STRM0_OFFSET = 0,
    parameter STRM1_OFFSET = 256
)

(
    input aclk,
    input aresetn,

    //optional configuration interface compatible with ap_memory
    input [31:0] config_address,
    input config_ce,
    input config_we,
    input [MEM_WIDTH-1:0] config_d0,
    output [MEM_WIDTH-1:0] config_q0,
    output config_rack,

    //multiple output AXI Streams, TDATA width rounded to multiple of 8 bits
    input m_axis_0_tready,
    output m_axis_0_tvalid,
    output [((STRM0_WIDTH+7)/8)*8-1:0] m_axis_0_tdata,

    input m_axis_1_tready,
    output m_axis_1_tvalid,
    output [((STRM1_WIDTH+7)/8)*8-1:0] m_axis_1_tdata

);


//TODO: check that memory width is equal to the widest stream
//TODO: check that the stream depths and offsets make sense, and that the memory depth is sufficient (or calculate depth here?)
initial begin
    if((NSTREAMS < 1) | (NSTREAMS > 2)) begin
        $display("Invalid setting for NSTREAMS, please set in range [1,2]");
        $finish();
    end
end

//invert reset
wire rst;
assign rst = ~aresetn;

wire strm0_incr_en;
wire strm1_incr_en;

assign strm0_incr_en = m_axis_0_tready | ~m_axis_0_tvalid;
assign strm1_incr_en = m_axis_1_tready | ~m_axis_1_tvalid;

reg rack_shift[1:0];

generate
if(MEM_DEPTH > 1) begin: use_ram

//calculate width of memory address, with a minimum of 1 bit
localparam BLOCKADRWIDTH = $clog2(MEM_DEPTH);

reg [BLOCKADRWIDTH-1:0] strm0_addr = STRM0_OFFSET;
wire strm0_rst;
assign strm0_rst = strm0_incr_en & (strm0_addr == (STRM0_OFFSET + STRM0_DEPTH-1));

//one address counter per stream; more LUTs but keeps routing short and local
always @(posedge aclk) begin
    if(strm0_rst | rst)
        strm0_addr <= STRM0_OFFSET;
    else if(strm0_incr_en)
        strm0_addr <= strm0_addr + 1;
end

if(NSTREAMS == 1) begin: sdp

ramb18_sdp
#(
    .ID(0),
    .DWIDTH(MEM_WIDTH),
    .AWIDTH(BLOCKADRWIDTH),
    .DEPTH(MEM_DEPTH),
    .MEM_INIT(MEM_INIT),
    .RAM_STYLE(RAM_STYLE)
)
ram
(
    .clk(aclk),

    .ena(config_ce),
    .wea(config_we),
    .addra(config_address[BLOCKADRWIDTH-1:0]),
    .wdataa(config_d0),

    .enb(strm0_incr_en | config_ce),
    .enqb(strm0_incr_en | rack_shift[0]),
    .addrb(config_ce ? config_address[BLOCKADRWIDTH-1:0] : strm0_addr),
    .rdqb(m_axis_0_tdata)
);


end else begin: tdp

reg [BLOCKADRWIDTH-1:0] strm1_addr = STRM1_OFFSET;
wire strm1_rst;
assign strm1_rst = strm1_incr_en & (strm1_addr == (STRM1_OFFSET + STRM1_DEPTH-1));

always @(posedge aclk) begin
    if(strm1_rst | rst)
        strm1_addr <= STRM1_OFFSET;
    else if(strm1_incr_en)
        strm1_addr <= strm1_addr + 1;
end

ramb18_wf_dualport
#(
    .ID(0),
    .DWIDTH(MEM_WIDTH),
    .AWIDTH(BLOCKADRWIDTH),
    .DEPTH(MEM_DEPTH),
    .MEM_INIT(MEM_INIT),
    .RAM_STYLE(RAM_STYLE)
)
ram
(
    .clk(aclk),

    .wea(config_we),
    .ena(strm0_incr_en | config_ce),
    .enqa(strm0_incr_en | config_ce_r),
    .addra(config_we ? config_address[BLOCKADRWIDTH-1:0] : strm0_addr),
    .wdataa(config_d0),
    .rdqa(m_axis_0_tdata),

    .web(1'b0),
    .enb(strm1_incr_en),
    .enqb(strm1_incr_en),
    .addrb(strm1_addr),
    .wdatab('d0),
    .rdqb(m_axis_1_tdata)
);

end

end else begin: bypass

reg [MEM_WIDTH-1:0] singleval[0:0];
initial begin
    `ifdef SYNTHESIS
        $readmemh({MEM_INIT,"memblock_synth_0.dat"}, singleval, 0, 0);
    `else
        $readmemh({MEM_INIT,"memblock_sim_0.dat"}, singleval, 0, 0);
    `endif
end

always @(posedge aclk)
    if(config_ce & config_we)
        singleval[0] <= config_d0;

assign m_axis_0_tdata = singleval[0];
assign m_axis_1_tdata = singleval[0];

end
endgenerate

//signal valid after 2 tready cycles after initialization
//then stay valid
reg [1:0] tvalid_pipe0 = 2'd0;
reg [1:0] tvalid_pipe1 = 2'd0;

assign m_axis_0_tvalid = tvalid_pipe0[1];
assign m_axis_1_tvalid = tvalid_pipe1[1];

always @(posedge aclk) begin
    if(rst) begin
        tvalid_pipe0 <= 0;
    end else if(strm0_incr_en) begin
        tvalid_pipe0[0] <= 1;
        tvalid_pipe0[1] <= tvalid_pipe0[0];
    end
end

always @(posedge aclk) begin
    if(rst) begin
        tvalid_pipe1 <= 0;
    end else if(strm1_incr_en) begin
        tvalid_pipe1[0] <= 1;
        tvalid_pipe1[1] <= tvalid_pipe1[0];
    end
end

always @(posedge aclk) begin
    rack_shift[0] <= config_ce & ~config_we;
    rack_shift[1] <= rack_shift[0];
end

assign config_rack = rack_shift[1];
assign config_q0 = m_axis_0_tdata;

endmodule


module ramb18_sdp
#(
    parameter ID = 0,
    parameter DWIDTH = 18,
    parameter AWIDTH = 10,
    parameter DEPTH = 2**AWIDTH,
    parameter MEM_INIT = "",
    parameter RAM_STYLE = "auto"
)
(
    input clk,

    input ena,
    input wea,
    input [AWIDTH-1:0] addra,
    input [DWIDTH-1:0] wdataa,

    input enb,
    input enqb,
    input [AWIDTH-1:0] addrb,
    output reg [DWIDTH-1:0] rdqb
);

(* ram_style = RAM_STYLE *) reg [DWIDTH-1:0] mem[0:DEPTH-1];
reg [DWIDTH-1:0] rdatab;

`ifdef SYNTHESIS
reg [7:0] idx = ID;
`else
reg [15:0] idx;
`endif

//initialize memory
initial begin
  //note the hacky way of adding a filename memblock_ID.dat to the path provided in MEM_INIT
  //ID can go up to 99
  if (ID < 0 && ID > 99) begin
    $display("ID out of range [0-99]");
    $finish();
  end
    //MEM_INIT path must be terminated by /
  `ifdef SYNTHESIS
  if (ID < 10)
    $readmemh({MEM_INIT,"memblock_synth_",idx+8'd48,".dat"}, mem, 0, DEPTH-1);
  else
    $readmemh({MEM_INIT,"memblock_synth_",(idx/10)+8'd48,(idx%10)+8'd48,".dat"}, mem, 0, DEPTH-1);
  `else
  $sformat(idx,"%0d",ID);
  if (ID < 10)
    $readmemh({MEM_INIT,"memblock_sim_",idx[7:0],".dat"}, mem, 0, DEPTH-1);
  else
    $readmemh({MEM_INIT,"memblock_sim_",idx,".dat"}, mem, 0, DEPTH-1);
  `endif
end

//memory ports, with output pipeline register
always @(posedge clk) begin
    if(wea)
        mem[addra] <= wdataa;
    if(enb)
        rdatab <= mem[addrb];
    if(enqb)
        rdqb <= rdatab;
end

endmodule


module ramb18_wf_dualport
#(
    parameter ID = 0,
    parameter DWIDTH = 18,
    parameter AWIDTH = 10,
    parameter DEPTH = 2**AWIDTH,
    parameter MEM_INIT = "",
    parameter RAM_STYLE = "auto"
)
(
    input clk,

    input wea,
    input ena,
    input enqa,
    input [AWIDTH-1:0] addra,
    input [DWIDTH-1:0] wdataa,
    output reg [DWIDTH-1:0] rdqa,

    input web,
    input enb,
    input enqb,
    input [AWIDTH-1:0] addrb,
    input [DWIDTH-1:0] wdatab,
    output reg [DWIDTH-1:0] rdqb
);

(* ram_style = RAM_STYLE *) reg [DWIDTH-1:0] mem[0:DEPTH-1];
reg [DWIDTH-1:0] rdataa;
reg [DWIDTH-1:0] rdatab;

`ifdef SYNTHESIS
reg [7:0] idx = ID;
`else
reg [15:0] idx;
`endif

//initialize memory
initial begin
  //note the hacky way of adding a filename memblock_ID.dat to the path provided in MEM_INIT
  //ID can go up to 99
  if (ID < 0 && ID > 99) begin
    $display("ID out of range [0-99]");
    $finish();
  end
    //MEM_INIT path must be terminated by /
  `ifdef SYNTHESIS
  if (ID < 10)
    $readmemh({MEM_INIT,"memblock_",idx+8'd48,".dat"}, mem, 0, DEPTH-1);
  else
    $readmemh({MEM_INIT,"memblock_",(idx/10)+8'd48,(idx%10)+8'd48,".dat"}, mem, 0, DEPTH-1);
  `else
  $sformat(idx,"%0d",ID);
  if (ID < 10)
    $readmemh({MEM_INIT,"memblock_",idx[7:0],".dat"}, mem, 0, DEPTH-1);
  else
    $readmemh({MEM_INIT,"memblock_",idx,".dat"}, mem, 0, DEPTH-1);
  `endif
end

//memory ports, with output pipeline register
always @(posedge clk) begin
    if(ena) begin
        if(wea)
            mem[addra] <= wdataa;
        rdataa <= mem[addra];
    end
    if(enqa)
        rdqa <= rdataa;
end
always @(posedge clk) begin
    if(enb) begin
        if(web)
            mem[addrb] <= wdatab;
        rdatab <= mem[addrb];
    end
    if(enqb)
        rdqb <= rdatab;
end

endmodule