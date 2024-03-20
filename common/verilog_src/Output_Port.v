`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05/11/2018 11:49:24 PM
// Design Name: 
// Module Name: Output_Port
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


module Output_Port#(
    parameter PACKET_BITS = 97,
    parameter NUM_LEAF_BITS = 6,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter PAYLOAD_BITS = 64, 
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter FREESPACE_UPDATE_SIZE = 64,
    parameter DATA_USER_OUT = 32,
    parameter OUTPUT_0 = 0,
    localparam FIFO_DEPTH = (2**NUM_BRAM_ADDR_BITS)
    )(
    input clk,
    input clk_user,
    input reset,
    input reset_user,    

    input [NUM_LEAF_BITS-1:0] dst_leaf, // clk(_bft) domain
    input [NUM_PORT_BITS-1:0] dst_port, // clk(_bft) domain
    input [NUM_ADDR_BITS-1:0] fifo_addr, // clk(_bft) domain
    input [NUM_ADDR_BITS-1:0] freespace, // clk(_bft) domain
    input update_freespace_en, // clk(_bft) domain
    input update_fifo_addr_en, // clk(_bft) domain
    input add_freespace_en, // clk(_bft) domain
    output [PACKET_BITS-1:0] internal_out,
    output empty,
    input rd_en_sel,

    //user interface
    output ack_b_out2user,
    input [DATA_USER_OUT-1:0] din_leaf_user2interface,
    input vld_user2b_out,
    
    input is_done_mode, // clk(_bft) domain
    input is_done_mode_user, // clk_user domain
    output reg [PAYLOAD_BITS-1:0] output_port_full_cnt,
    output reg [PAYLOAD_BITS-1:0] output_port_empty_cnt,
    input is_sending_full_cnt_reg,
    input [NUM_LEAF_BITS-1:0] self_leaf_reg,
    input [NUM_PORT_BITS-1:0] self_port_reg,
    input [1:0] cnt_type_reg,

    input vld_cnt,
    input [PAYLOAD_BITS-1:0] cnt_val,

    output output_port_stall_condition
    );

    reg valid;

    wire [DATA_USER_OUT-1:0] din;
    wire [PAYLOAD_BITS-1:0] dout;  
    wire wr_en;
    wire rd_en;
    reg [NUM_ADDR_BITS-1:0] FreeCnt;
    reg [NUM_ADDR_BITS-1:0] fifo_addr_reg;

    wire full;

    wire [NUM_LEAF_BITS-1:0] self_leaf;
    wire [NUM_PORT_BITS-1:0] self_port;
    wire [1:0] cnt_type;
    wire is_sending_full_cnt;
    wire full_small, empty_small;

    wire wr_en_small;
    wire [PAYLOAD_BITS-1:0] cnt_val_in, cnt_val_out;
    wire wr_rst_busy,rd_rst_busy;
    wire rd_en_small;
    reg valid_small;

    
    generate
        wire [PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_LEAF_BITS-NUM_PORT_BITS-2-1:0] cnt_dout;
        if(PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_LEAF_BITS-NUM_PORT_BITS-2 > PAYLOAD_BITS) begin
            wire [PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_LEAF_BITS-NUM_PORT_BITS-2-PAYLOAD_BITS-1:0] remaining_bits;
            assign remaining_bits = 0;
            assign cnt_dout = {remaining_bits, cnt_val_out[PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_LEAF_BITS-NUM_PORT_BITS-2-1:0]};
        end
        else begin
            assign cnt_dout = cnt_val_out[PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_LEAF_BITS-NUM_PORT_BITS-2-1:0];
        end

        if(PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_ADDR_BITS-PAYLOAD_BITS-1>=0) begin
            wire [PACKET_BITS-1-NUM_LEAF_BITS-NUM_PORT_BITS-NUM_ADDR_BITS-PAYLOAD_BITS-1:0] reserved_bits;
            assign reserved_bits = 0;
            // assign internal_out = valid ? {1'b1, dst_leaf, dst_port, reserved_bits, fifo_addr_reg, dout} : 0;

            assign internal_out = is_sending_full_cnt ? (valid_small ? {1'b1, dst_leaf, dst_port, self_leaf, self_port, cnt_type, cnt_dout} : 0) : 
                                                        ((valid && !(is_done_mode)) ? {1'b1, dst_leaf, dst_port, reserved_bits, fifo_addr_reg, dout} : 0);
        end else begin
            // assign internal_out = valid ? {1'b1, dst_leaf, dst_port, fifo_addr_reg, dout} : 0;
            assign internal_out = is_sending_full_cnt ? (valid_small ? {1'b1, dst_leaf, dst_port, self_leaf, self_port, cnt_type, cnt_dout} : 0) : 
                                                        ((valid && !(is_done_mode)) ?  {1'b1, dst_leaf, dst_port, fifo_addr_reg, dout} : 0);
        end
    endgenerate
        
    
    // assign ack_b_out2user = wr_en;
    assign ack_b_out2user = ~full;
    // write bram_out, it manipulates write port of b_out_9
                   
    always@(posedge clk) begin
         if(reset) begin
             FreeCnt = 2**NUM_ADDR_BITS-1;
         end else begin
             if(update_freespace_en)
                 FreeCnt <= freespace;
             else if(rd_en && add_freespace_en)
             //else if(add_freespace_en)
                 FreeCnt <= FreeCnt + FREESPACE_UPDATE_SIZE - 1;
             else if(!rd_en && add_freespace_en)
                 FreeCnt <= FreeCnt + FREESPACE_UPDATE_SIZE;
             else if(rd_en && (!add_freespace_en) && (FreeCnt > 0))
                 FreeCnt <= FreeCnt - 1;
             else
                 FreeCnt <= FreeCnt;
         end
     end


    always@(posedge clk) begin
        if(reset) begin
            fifo_addr_reg = 0;
        end else begin
            if(update_fifo_addr_en)
                fifo_addr_reg <= fifo_addr;
            else if(valid)
                fifo_addr_reg <= fifo_addr_reg + 1;
            else
                fifo_addr_reg <= fifo_addr_reg;
        end
    end
    
    
    // assign rd_en = ((FreeCnt > 0) && (!empty)) ? rd_en_sel : 1'b0;
    // assign rd_en = ((FreeCnt > 0) && (!empty || !empty_small) && !rd_rst_busy) ? rd_en_sel : 1'b0;


    assign rd_en = ((FreeCnt > 0) && (!empty)) ? rd_en_sel : 1'b0;
    assign rd_en_small = ((FreeCnt > 0) && (!empty_small)) ? rd_en_sel : 1'b0;
    
    always@(posedge clk) begin
        if(reset) begin
            valid = 0;
        end else begin
            valid <= rd_en;
        end
    end    
    
    always@(posedge clk) begin
        if(reset) begin
            valid_small = 0;
        end else begin
            valid_small <= rd_en_small;
        end
    end    
    
                  
    
    // xpm_fifo_async # (

    //   .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
    //   .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
    //   .RELATED_CLOCKS            (0),                // 250MHz and 350MHz are related clock?
    //   .FIFO_WRITE_DEPTH          (FIFO_DEPTH),             //positive integer
    //   // .FIFO_WRITE_DEPTH          (512),             //positive integer
    //   .WRITE_DATA_WIDTH          (1 + NUM_LEAF_BITS + NUM_PORT_BITS + 2 + PAYLOAD_BITS),               //positive integer
    //   .WR_DATA_COUNT_WIDTH       (NUM_BRAM_ADDR_BITS),               //positive integer
    //   .PROG_FULL_THRESH          (10),               //positive integer
    //   .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
    //   .READ_MODE                 ("std"),            //string; "std" or "fwft";
    //   .FIFO_READ_LATENCY         (1),                //positive integer;
    //   .READ_DATA_WIDTH           (1 + NUM_LEAF_BITS + NUM_PORT_BITS + 2  + PAYLOAD_BITS),               //positive integer
    //   .RD_DATA_COUNT_WIDTH       (NUM_BRAM_ADDR_BITS),               //positive integer
    //   .PROG_EMPTY_THRESH         (10),               //positive integer
    //   .DOUT_RESET_VALUE          ("0"),              //string
    //   .CDC_SYNC_STAGES           (2),                //positive integer
    //   .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;

    // ) xpm_fifo_async_inst (

    //   .rst              (reset_user),
    //   .wr_clk           (clk_user),
    //   .wr_en            (wr_en),
    //   .din              ({is_sending_full_cnt_reg,self_leaf_reg,self_port_reg,cnt_type_reg,din}),
    //   .full             (full),
    //   .overflow         (), // not used
    //   .wr_rst_busy      (), // not used
    //   .rd_clk           (clk),
    //   .rd_en            (rd_en),
    //   .dout             ({is_sending_full_cnt,self_leaf,self_port,cnt_type,dout}),
    //   .empty            (empty),
    //   .underflow        (), // not used
    //   .rd_rst_busy      (), // not used
    //   .prog_full        (), // not used
    //   .wr_data_count    (), // not used
    //   .prog_empty       (), // not used
    //   .rd_data_count    (), // not used
    //   .sleep            (1'b0),
    //   .injectsbiterr    (1'b0),
    //   .injectdbiterr    (1'b0),
    //   .sbiterr          (),
    //   .dbiterr          ()

    // );

    // write_b_out is wr_en generator (combinational)
    write_b_out #(
        .PAYLOAD_BITS(DATA_USER_OUT)
        )wbo(
        .vld_user2b_out(vld_user2b_out), 
        .din_leaf_user2interface(din_leaf_user2interface), 
        .full(full),
        .wr_en(wr_en), 
        .din(din));

    xpm_fifo_async # (
      .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
      .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
      .RELATED_CLOCKS            (0),                // 250MHz and 350MHz are related clock?
      .FIFO_WRITE_DEPTH          (FIFO_DEPTH),             //positive integer
      .WRITE_DATA_WIDTH          (DATA_USER_OUT),               //positive integer
      .WR_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_FULL_THRESH          (10),               //positive integer
      .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
      .READ_MODE                 ("std"),            //string; "std" or "fwft";
      .FIFO_READ_LATENCY         (1),                //positive integer;
      .READ_DATA_WIDTH           (PAYLOAD_BITS),               //positive integer
      .RD_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_EMPTY_THRESH         (10),               //positive integer
      .DOUT_RESET_VALUE          ("0"),              //string
      .CDC_SYNC_STAGES           (2),                //positive integer
      .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;
    ) xpm_fifo_async_inst (
      .rst              (reset_user),
      .wr_clk           (clk_user),
      .wr_en            (wr_en),
      .din              (din),
      .full             (full),
      .overflow         (), // not used
      .wr_rst_busy      (wr_rst_busy),
      .rd_clk           (clk),
      .rd_en            (rd_en),
      .dout             (dout),
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


    write_b_out #(
        .PAYLOAD_BITS(PAYLOAD_BITS)
        )wbo_small(
        .vld_user2b_out(vld_cnt), 
        .din_leaf_user2interface(cnt_val), 
        .full(full_small),
        .wr_en(wr_en_small), 
        .din(cnt_val_in));

    generate
        if (OUTPUT_0 != 0) begin
            xpm_fifo_async # (
              .FIFO_MEMORY_TYPE          ("auto"),           //string; "auto", "block", or "distributed";
              .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
              .RELATED_CLOCKS            (0),                // 250MHz and 350MHz are related clock?
              .FIFO_WRITE_DEPTH          (OUTPUT_0),       // This number is determined by the number of IO ports, 16 or 32   // positive integer
              .WRITE_DATA_WIDTH          (1 + NUM_LEAF_BITS + NUM_PORT_BITS + 2 + PAYLOAD_BITS),               //positive integer
              .WR_DATA_COUNT_WIDTH       (),               //positive integer
              .PROG_FULL_THRESH          (10),               //positive integer
              .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
              .READ_MODE                 ("std"),            //string; "std" or "fwft";
              .FIFO_READ_LATENCY         (1),                //positive integer;
              .READ_DATA_WIDTH           (1 + NUM_LEAF_BITS + NUM_PORT_BITS + 2 + PAYLOAD_BITS),               //positive integer
              .RD_DATA_COUNT_WIDTH       (),               //positive integer
              .PROG_EMPTY_THRESH         (10),               //positive integer
              .DOUT_RESET_VALUE          ("0"),              //string
              .CDC_SYNC_STAGES           (2),                //positive integer
              .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;
            ) xpm_fifo_async_small_inst (
              .rst              (reset_user),
              .wr_clk           (clk_user),
              .wr_en            (wr_en_small),
              .din              ({is_sending_full_cnt_reg, self_leaf_reg, self_port_reg, cnt_type_reg, cnt_val_in}),
              .full             (full_small),
              .overflow         (), // not used
              .wr_rst_busy      (), // not used
              .rd_clk           (clk),
              .rd_en            (rd_en_small),
              .dout             ({is_sending_full_cnt, self_leaf, self_port, cnt_type, cnt_val_out}),
              .empty            (empty_small),
              .underflow        (), // not used
              .rd_rst_busy      (), // not used
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
        end
        else begin
            assign is_sending_full_cnt = 0;
            assign self_leaf = 0;
            assign self_port = 0;
            assign cnt_type = 0;
            assign cnt_val_out = 0;
            assign full_small = 1;
            assign empty_small = 1;
        end
    endgenerate


    // fifo for self_leaf_reg, self_port_reg, cnt_type_reg. Used only after is_done
    // SynFIFO_distributed #(
    // .DSIZE(1 + NUM_LEAF_BITS + NUM_PORT_BITS + 2),
    // .ASIZE(4)
    // )SynFIFO_distributed_inst (
    //     .clk(clk),
    //     .rst_n(!reset),
    //     .rdata({is_sending_full_cnt,self_leaf,self_port,cnt_type}), 
    //     .wfull(), 
    //     .rempty(), 
    //     .wdata({is_sending_full_cnt_reg,self_leaf_reg,self_port_reg,cnt_type_reg}),
    //     .winc(wr_en), 
    //     .rinc(rd_en)
    //     );



    // SynFIFO SynFIFO_inst (
    // 	.clk(clk),
    // 	.rst_n(!reset),
    // 	.rdata(dout), 
    // 	.wfull(full), 
    // 	.rempty(empty), 
    // 	.wdata(din),
    // 	.winc(wr_en), 
    // 	.rinc(rd_en)
    // 	);


    /////////////////////////
    // counter logic below //
    /////////////////////////
    // User is ready to output data but output queue is full
    assign output_port_stall_condition = (!is_done_mode_user) && vld_user2b_out && full;

    // count the number of output queue's full, clk_user domain
    always@(posedge clk_user) begin
        if(reset_user) output_port_full_cnt <= 0;
        else begin
            if(full && !is_done_mode_user) output_port_full_cnt <= output_port_full_cnt + 1;
            else output_port_full_cnt <= output_port_full_cnt;
        end
    end

    // count the number of output queue's empty, clk(_bft) domain
    always@(posedge clk) begin
        if(reset) output_port_empty_cnt <= 0;
        else begin
            if(empty && !is_done_mode) output_port_empty_cnt <= output_port_empty_cnt + 1;
            else output_port_empty_cnt <= output_port_empty_cnt;
        end
    end

    // count the number of output queue's write
    // DJP: This shuold match with Input's read cnt, so redundant 
    // always@(posedge clk_user) begin
    //     if(reset_user) output_port_write_cnt <= 0;
    //     else begin
    //         if(vld_user2b_out && ack_b_out2user && !is_done_mode) output_port_write_cnt <= output_port_write_cnt + 1;
    //         else output_port_write_cnt <= output_port_write_cnt;
    //     end
    // end

endmodule


// small synchronous FIFO, synthesized to distributed RAM
/*
module SynFIFO_distributed (
    clk,
    rst_n,
    rdata, 
    wfull, 
    rempty, 
    wdata,
    winc, 
    rinc
    );
    
parameter DSIZE = 32;
parameter ASIZE = 4;
parameter MEMDEPTH = 1<<ASIZE;
parameter RAM_TYPE = "distributed";     // Type of RAM: string; "auto", "block", or "distributed";

    output reg [DSIZE-1:0] rdata;
    output wfull;
    output rempty;

    input [DSIZE-1:0] wdata;
    input winc, rinc, clk, rst_n;

    reg [ASIZE:0] wptr;
    reg [ASIZE:0] rptr;
    (* ram_style = RAM_TYPE *) reg [DSIZE-1:0] ex_mem [0:MEMDEPTH-1];
    wire [DSIZE-1:0] rdata_tmp;

    wire wfull_r;
    wire [ASIZE:0] wptr_1;

    always @(posedge clk)
        if (!rst_n) wptr <= 0;
        else if (winc && !wfull) begin
            ex_mem[wptr[ASIZE-1:0]] <= wdata;
            wptr <= wptr+1;
        end


    always @(posedge clk)
        if (!rst_n) rptr <= 0;
        else if (rinc && !rempty) rptr <= rptr+1;

    assign wptr_1 = wptr + 1;   
    assign rdata_tmp = ex_mem[rptr[ASIZE-1:0]];
    assign rempty = (rptr == wptr);
    assign wfull = ((wptr_1[ASIZE-1:0] == rptr[ASIZE-1:0]) && (wptr_1[ASIZE] != rptr[ASIZE])) || wfull_r;
    assign wfull_r = (wptr[ASIZE-1:0] == rptr[ASIZE-1:0]) && (wptr[ASIZE] != rptr[ASIZE]);

    always @(posedge clk) begin
        if(!rst_n) begin
            rdata <= 0;
        end else if(rinc) begin
            rdata <= rdata_tmp;
        end else begin
            rdata <= rdata;
        end
    end

endmodule
*/