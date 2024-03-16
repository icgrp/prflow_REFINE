`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/11/2018 11:23:36 PM
// Design Name: 
// Module Name: Input_Port
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


module Input_Port#(
    parameter PACKET_BITS = 97,
    parameter NUM_LEAF_BITS = 6,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter PAYLOAD_BITS = 64, 
    parameter NUM_IN_PORTS = 1, 
    parameter NUM_OUT_PORTS = 1,
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter PORT_No = 2,
    parameter FREESPACE_UPDATE_SIZE = 64,
    parameter DATA_USER_IN = 32,
    localparam BRAM_DEPTH = 2**(NUM_BRAM_ADDR_BITS-1)*(PAYLOAD_BITS+1)
    )(
    input clk,
    input clk_user,
    input reset,
    input reset_user,    

    //internal interface
    output freespace_update,
    output [PACKET_BITS-1:0] packet_from_input_port,
    input [PACKET_BITS-1:0] din_leaf_bft2interface,
    input [NUM_LEAF_BITS-1:0] src_leaf,
    input [NUM_PORT_BITS-1:0] src_port,
    
    //user interface
    output [DATA_USER_IN-1:0] dout2user,
    output vld2user,
    input ack_user2b_in,
    
    input is_done_mode, // clk(_bft) domain
    input is_done_mode_user, // clk_user domain
    output reg [PAYLOAD_BITS-1:0] input_port_full_cnt,
    output reg [PAYLOAD_BITS-1:0] input_port_empty_cnt,
    output reg [PAYLOAD_BITS-1:0] input_port_read_cnt,
    output input_port_stall_condition
    );

    wire vldBit;
    wire [NUM_PORT_BITS-1:0] port;
    wire [NUM_ADDR_BITS-1:0] addr;
    wire [PAYLOAD_BITS-1:0] payload;
    
    wire [PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-PAYLOAD_BITS-1:0] red_bits;
    wire [PAYLOAD_BITS-1:0] update_data;
    
    wire [NUM_ADDR_BITS-1:0] addra;
    //wire [NUM_BRAM_ADDR_BITS-1:0] addra_extend;
    wire [PAYLOAD_BITS:0] dina;
    wire wea;
    wire wea_0;
    wire wea_1;
    
    
    wire [NUM_ADDR_BITS-2:0] addrb_0;
    //wire [NUM_BRAM_ADDR_BITS-1:0] addrb_extend_0;
    wire [PAYLOAD_BITS:0] doutb_0;
    wire web_0;
    
        
    wire [NUM_ADDR_BITS-2:0] addrb_1;
    //wire [NUM_BRAM_ADDR_BITS-1:0] addrb_extend_1;
    wire [PAYLOAD_BITS:0] doutb_1;
    wire web_1;

    
    assign wea_0 = addra[0] ? 0 : wea;
    assign wea_1 = addra[0] ? wea : 0;
    
    
/*    generate
        if(NUM_BRAM_ADDR_BITS>NUM_ADDR_BITS) begin
            wire [NUM_BRAM_ADDR_BITS-NUM_ADDR_BITS-1:0] redundent_bits;
            assign redundent_bits = 0;
            assign addra_extend = {redundent_bits, addra};
            assign addrb_extend_0 = {redundent_bits, addrb_0};
            assign addrb_extend_1 = {redundent_bits, addrb_1};
        end else begin
            assign addra_extend = addra;
            assign addrb_extend_0 = addrb_0;
            assign addrb_extend_1 = addrb_1;
        end
    endgenerate
    */
    
    assign red_bits = 0;
    assign update_data = 1;
    assign packet_from_input_port = {1'b1, src_leaf, src_port, red_bits, update_data};
    
    
    assign vldBit = din_leaf_bft2interface[PACKET_BITS-1]; // 1 bit
    assign port = din_leaf_bft2interface[PACKET_BITS-2-NUM_LEAF_BITS:PACKET_BITS-2-NUM_LEAF_BITS-NUM_PORT_BITS+1];
    assign addr = din_leaf_bft2interface[PAYLOAD_BITS+NUM_ADDR_BITS-1:PAYLOAD_BITS];
    assign payload = din_leaf_bft2interface[PAYLOAD_BITS-1:0];


    // write bram_in, it manipulates write port of b_in
    

    write_b_in #(
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PORT_No(PORT_No)
        )wbi(
        .clk(clk), 
        .reset(reset), 
        .port(port), 
        .addr(addr), 
        .vldBit(vldBit), 
        .payload(payload), 
        .wea(wea), 
        .addra(addra), 
        .dina(dina)
        );

    // bram_in
    /*
    bram_in b_in(
        .clka(clk_bft), 
        .wea(b_in_wea), 
        .addra(b_in_addra), 
        .dina(b_in_dina), 
        .douta(),
        .clkb(clk_user), 
        .web(b_in_web), 
        .addrb(b_in_addrb), 
        .dinb(65'd0), 
        .doutb(b_in_doutb)
        );

       */ 
    wire [PAYLOAD_BITS:0] b_in_dinb;
    assign b_in_dinb = 0;
    
          
    xpm_memory_tdpram # (
      // Common module parameters
      .MEMORY_SIZE        (BRAM_DEPTH),            //positive integer
      .MEMORY_PRIMITIVE   ("block"),          //string; "auto", "distributed", "block" or "ultra";
      .CLOCKING_MODE      ("common_clock"),  //string; "common_clock", "independent_clock" 
      .MEMORY_INIT_FILE   ("none"),          //string; "none" or "<filename>.mem" 
      .MEMORY_INIT_PARAM  (""    ),          //string;
      .USE_MEM_INIT       (1),               //integer; 0,1
      .WAKEUP_TIME        ("disable_sleep"), //string; "disable_sleep" or "use_sleep_pin" 
      .MESSAGE_CONTROL    (0),               //integer; 0,1
      .ECC_MODE           ("no_ecc"),        //string; "no_ecc", "encode_only", "decode_only" or "both_encode_and_decode" 
      .AUTO_SLEEP_TIME    (0),               //Do not Change

      // Port A module parameters
      .WRITE_DATA_WIDTH_A (PAYLOAD_BITS+1),              //positive integer
      .READ_DATA_WIDTH_A  (PAYLOAD_BITS+1),              //positive integer
      .BYTE_WRITE_WIDTH_A (PAYLOAD_BITS+1),              //integer; 8, 9, or WRITE_DATA_WIDTH_A value
      .ADDR_WIDTH_A       (NUM_BRAM_ADDR_BITS-1),               //positive integer
      .READ_RESET_VALUE_A ("0"),             //string
      .READ_LATENCY_A     (1),               //non-negative integer
      .WRITE_MODE_A       ("read_first"),     //string; "write_first", "read_first", "no_change" 

      // Port B module parameters
      .WRITE_DATA_WIDTH_B (PAYLOAD_BITS+1),              //positive integer
      .READ_DATA_WIDTH_B  (PAYLOAD_BITS+1),              //positive integer
      .BYTE_WRITE_WIDTH_B (PAYLOAD_BITS+1),              //integer; 8, 9, or WRITE_DATA_WIDTH_B value
      .ADDR_WIDTH_B       (NUM_BRAM_ADDR_BITS-1),               //positive integer
      .READ_RESET_VALUE_B ("0"),             //vector of READ_DATA_WIDTH_B bits
      .READ_LATENCY_B     (1),               //non-negative integer
      .WRITE_MODE_B       ("read_first")      //string; "write_first", "read_first", "no_change" 

    ) xpm_memory_tdpram_inst_0 (
      // Common module ports
      .sleep          (1'b0),
      // Port A module ports
      .clka           (clk),
      .rsta           (reset),
      .ena            (1'b1),
      .regcea         (1'b1),
      .wea            (wea_0),
      .addra          (addra[NUM_ADDR_BITS-1:1]),
      .dina           (dina),
      .injectsbiterra (1'b0),
      .injectdbiterra (1'b0),
      .douta          (),
      .sbiterra       (),
      .dbiterra       (),
      // Port B module ports
      .clkb           (clk),
      .rstb           (reset),
      .enb            (1'b1),
      .regceb         (1'b1),
      .web            (web_0),
      .addrb          (addrb_0),
      .dinb           (0),
      .injectsbiterrb (1'b0),
      .injectdbiterrb (1'b0),
      .doutb          (doutb_0),
      .sbiterrb       (),
      .dbiterrb       ()
    );
    
    /*
    single_ram#(
        .PAYLOAD_BITS(PAYLOAD_BITS), 
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS-1),
        .NUM_ADDR_BITS(NUM_ADDR_BITS-1),
        .RAM_TYPE("block")
        )ram_1(
        .clk(clk),
        .reset(reset),
        .wea(wea_0),
        .web(web_0),
        .addra(addra[NUM_ADDR_BITS-1:1]),
        .addrb(addrb_0),
        .dina(dina),
        .dinb(33'b0),
        .doutb(doutb_0)
        );
        */
        
        
    xpm_memory_tdpram # (
      // Common module parameters
      .MEMORY_SIZE        (BRAM_DEPTH),            //positive integer
      .MEMORY_PRIMITIVE   ("block"),          //string; "auto", "distributed", "block" or "ultra";
      .CLOCKING_MODE      ("common_clock"),  //string; "common_clock", "independent_clock" 
      .MEMORY_INIT_FILE   ("none"),          //string; "none" or "<filename>.mem" 
      .MEMORY_INIT_PARAM  (""    ),          //string;
      .USE_MEM_INIT       (1),               //integer; 0,1
      .WAKEUP_TIME        ("disable_sleep"), //string; "disable_sleep" or "use_sleep_pin" 
      .MESSAGE_CONTROL    (0),               //integer; 0,1
      .ECC_MODE           ("no_ecc"),        //string; "no_ecc", "encode_only", "decode_only" or "both_encode_and_decode" 
      .AUTO_SLEEP_TIME    (0),               //Do not Change

      // Port A module parameters
      .WRITE_DATA_WIDTH_A (PAYLOAD_BITS+1),              //positive integer
      .READ_DATA_WIDTH_A  (PAYLOAD_BITS+1),              //positive integer
      .BYTE_WRITE_WIDTH_A (PAYLOAD_BITS+1),              //integer; 8, 9, or WRITE_DATA_WIDTH_A value
      .ADDR_WIDTH_A       (NUM_BRAM_ADDR_BITS-1),               //positive integer
      .READ_RESET_VALUE_A ("0"),             //string
      .READ_LATENCY_A     (1),               //non-negative integer
      .WRITE_MODE_A       ("read_first"),     //string; "write_first", "read_first", "no_change" 

      // Port B module parameters
      .WRITE_DATA_WIDTH_B (PAYLOAD_BITS+1),              //positive integer
      .READ_DATA_WIDTH_B  (PAYLOAD_BITS+1),              //positive integer
      .BYTE_WRITE_WIDTH_B (PAYLOAD_BITS+1),              //integer; 8, 9, or WRITE_DATA_WIDTH_B value
      .ADDR_WIDTH_B       (NUM_BRAM_ADDR_BITS-1),               //positive integer
      .READ_RESET_VALUE_B ("0"),             //vector of READ_DATA_WIDTH_B bits
      .READ_LATENCY_B     (1),               //non-negative integer
      .WRITE_MODE_B       ("read_first")      //string; "write_first", "read_first", "no_change" 

    ) xpm_memory_tdpram_inst_1 (
      // Common module ports
      .sleep          (1'b0),
      // Port A module ports
      .clka           (clk),
      .rsta           (reset),
      .ena            (1'b1),
      .regcea         (1'b1),
      .wea            (wea_1),
      .addra          (addra[NUM_ADDR_BITS-1:1]),
      .dina           (dina),
      .injectsbiterra (1'b0),
      .injectdbiterra (1'b0),
      .douta          (),
      .sbiterra       (),
      .dbiterra       (),
      // Port B module ports
      .clkb           (clk),
      .rstb           (reset),
      .enb            (1'b1),
      .regceb         (1'b1),
      .web            (web_1),
      .addrb          (addrb_1),
      .dinb           (0),
      .injectsbiterrb (1'b0),
      .injectdbiterrb (1'b0),
      .doutb          (doutb_1),
      .sbiterrb       (),
      .dbiterrb       ()
    );
    
    /*
    single_ram#(
        .PAYLOAD_BITS(PAYLOAD_BITS), 
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS-1),
        .NUM_ADDR_BITS(NUM_ADDR_BITS-1),
        .RAM_TYPE("block")
        )ram_2(
        .clk(clk),
        .reset(reset),
        .wea(wea_1),
        .web(web_1),
        .addra(addra[NUM_ADDR_BITS-1:1]),
        .addrb(addrb_1),
        .dina(dina),
        .dinb(33'b0),
        .doutb(doutb_1)
        );
        */
        
        
    wire [PAYLOAD_BITS-1:0] din_bram2fifo;
    wire vld_bram2fifo;
    wire ack_fifo2bram;

    // read bram_in,it manipulates read port
    read_b_in #(
        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS)        
        )rbi(
        .clk(clk), 
        .reset(reset), 
        .ack_user2b_in(ack_fifo2bram), 
        .doutb_0(doutb_0),
        .doutb_1(doutb_1),
        .addrb_0(addrb_0), 
        .addrb_1(addrb_1), 
        .dout_leaf_interface2user(din_bram2fifo), 
        .vld_bram_in2user(vld_bram2fifo), 
        .freespace_update(freespace_update), 
        .web_0(web_0),
        .web_1(web_1));

    wire input_fifo_empty;
    data_converter # (
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .DATA_USER_IN(DATA_USER_IN)
        ) data_converter_inst(
        .clk(clk),
        .clk_user(clk_user),
        .reset(reset),
        .reset_user(reset_user),
        .din_bram2fifo(din_bram2fifo),
        .vld_bram2fifo(vld_bram2fifo),
        .ack_fifo2bram(ack_fifo2bram), // ~full
        .dout_interface2user(dout2user),
        .vld_interface2user(vld2user),
        .ack_user2interface(ack_user2b_in),
        .empty(input_fifo_empty)
        );


    /////////////////////////
    // counter logic below //
    /////////////////////////
    // User is ready to receive data but input queue is empty
    assign input_port_stall_condition = (!is_done_mode_user) && ack_user2b_in && input_fifo_empty;

    // count the number of input queue's full, clk(_bft) domain
    always@(posedge clk) begin
        if(reset) input_port_full_cnt <= 0;
        else begin
            if(!ack_fifo2bram && !is_done_mode) input_port_full_cnt <= input_port_full_cnt + 1;
            else input_port_full_cnt <= input_port_full_cnt;
        end
    end

    // count the number of input queue's empty, clk_user domain
    always@(posedge clk_user) begin
        if(reset_user) input_port_empty_cnt <= 0;
        else begin
            if(input_fifo_empty && !is_done_mode_user) input_port_empty_cnt <= input_port_empty_cnt + 1;
            else input_port_empty_cnt <= input_port_empty_cnt;
        end
    end

    // count the number of input read, clk_user domain
    always@(posedge clk_user) begin
        if(reset_user) input_port_read_cnt <= 0;
        else begin
            if(vld2user && ack_user2b_in && !is_done_mode_user) input_port_read_cnt <= input_port_read_cnt + 1;
            else input_port_read_cnt <= input_port_read_cnt;
        end
    end

    
endmodule


module data_converter # (
    parameter PAYLOAD_BITS = 64,
    parameter DATA_USER_IN = 32
    )(
    input clk,
    input clk_user,
    input reset,
    input reset_user,
    
    input [PAYLOAD_BITS-1:0] din_bram2fifo,
    input vld_bram2fifo,
    output ack_fifo2bram,
    output [DATA_USER_IN-1:0] dout_interface2user,
    output reg vld_interface2user,
    input ack_user2interface,
    output empty
    );

    wire wr_en;
    wire [PAYLOAD_BITS-1:0] fifo_in;
    wire full;
    reg rd_en;
    wire [DATA_USER_IN-1:0] fifo_out;
    // wire empty;
    
    assign ack_fifo2bram = ~full;
    // assign wr_en = (~full) && vld_bram2fifo && !wr_rst_busy && !rd_rst_busy;
    assign wr_en = (~full) && vld_bram2fifo;

    assign fifo_in = din_bram2fifo;

    wire wr_rst_busy, rd_rst_busy;
    
    // Important: ensure depth of read/write is minimum 16 => FIFO_WRITE_DEPTH is set to 128
    xpm_fifo_async # (
      // .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
      .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
      .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
      .RELATED_CLOCKS            (0),                // 250MHz and 350MHz are related clock?
      // .FIFO_WRITE_DEPTH          (DATA_USER_IN/PAYLOAD_BITS*16),             //positive integer
      .FIFO_WRITE_DEPTH          (128),             //positive integer
      .WRITE_DATA_WIDTH          (PAYLOAD_BITS),               //positive integer
      .WR_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_FULL_THRESH          (10),               //positive integer
      .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
      .READ_MODE                 ("std"),            //string; "std" or "fwft";
      .FIFO_READ_LATENCY         (1),                //positive integer;
      .READ_DATA_WIDTH           (DATA_USER_IN),               //positive integer
      .RD_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_EMPTY_THRESH         (10),               //positive integer
      .DOUT_RESET_VALUE          ("0"),              //string
      .CDC_SYNC_STAGES           (2),                //positive integer
      .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;
    ) xpm_fifo_async2user (
      .rst              (reset),
      .wr_clk           (clk),
      .wr_en            (wr_en),
      .din              (fifo_in),
      .full             (full),
      .overflow         (), // not used
      .wr_rst_busy      (wr_rst_busy),
      .rd_clk           (clk_user),
      .rd_en            (rd_en),
      .dout             (fifo_out),
      .empty            (empty),
      .underflow        (), // not used
      .rd_rst_busy      (rd_rst_busy),
      .prog_full        (), // not used
      .wr_data_count    (), // not used
      .prog_empty       (), // not used
      .rd_data_count    (), // not used
      .sleep            (1'b0),
      .injectsbiterr    (1'b0),
      .injectdbiterr    (1'b0),
      .sbiterr          (),
      .dbiterr          ()
    );    
    
    // SynFIFO #(
    // .DSIZE(PAYLOAD_BITS),
    // .ASIZE(4)
    // )SynFIFO_inst (
	// .clk(clk),
	// .rst_n(!reset),
	// .rdata(fifo_out), 
	// .wfull(full), 
	// .rempty(empty), 
	// .wdata(fifo_in),
	// .winc(wr_en), 
	// .rinc(rd_en)
	// );
	
    assign dout_interface2user = fifo_out;
    
    //rd_en
    always@(*) begin
        if(empty) begin
            rd_en = 0;
        end else begin
            if(ack_user2interface) begin
                // rd_en = 1 && (!rd_rst_busy);
                rd_en = 1;
            end else begin
                // rd_en = ~vld_interface2user && (!rd_rst_busy);
                rd_en = ~vld_interface2user;
            end
        end
    end
        
    //vld_interface2user
    always@(posedge clk_user) begin // TODO: is this clk_user??
        if(reset_user) begin
            vld_interface2user <= 0;
        end else begin
            if(rd_en) begin
                vld_interface2user <= 1;
            end else begin
                if(vld_interface2user) begin
                    if(ack_user2interface) begin
                        vld_interface2user <= 0;
                    end else begin
                        vld_interface2user <= 1;
                    end
                end else begin
                    vld_interface2user <= 0;
                end
            end
        end
    end
endmodule
