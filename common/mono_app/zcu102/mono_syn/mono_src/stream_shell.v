`timescale 1ns / 1ps

// Async FIFO module between operators
// Counters (full_cnt_wr, empty_cnt_rd, read_cnt_rd) will be used to identify bottleneck operator
// _wr and _rd indicate clock domain
module stream_shell #(
    parameter WRITE_DATA_WIDTH = 32,
    parameter READ_DATA_WIDTH = 32,
    parameter NUM_BRAM_ADDR_BITS = 7,
    localparam FIFO_DEPTH = (2**NUM_BRAM_ADDR_BITS)
    )(
    input wr_clk,
    input wr_rst,
    input [WRITE_DATA_WIDTH-1:0] din,
    input val_in,
    output ready_upward,

    input rd_clk,
    input rd_rst,
    output reg [READ_DATA_WIDTH-1:0] dout,
    output reg val_out,
    input ready_downward,

    input reset_ap_start_wr, // to reset full_cnt
    input reset_ap_start_rd, // to reset empty_cnt, read_cnt
    input state_wr,
    input state_rd,
    output reg [31:0] full_cnt_wr,
    output reg [31:0] empty_cnt_rd,
    output reg [31:0] read_cnt_rd,

    output full,
    output empty
    );

    // wire empty;
    reg rd_en;
    // wire full;
    wire wr_en;

    wire [WRITE_DATA_WIDTH-1:0] fifo_in;
    wire [READ_DATA_WIDTH-1:0] fifo_out;

    assign ready_upward = ~full;
    assign wr_en = val_in;
    assign fifo_in = din;


    // Three counters per stream_shell

    // count the number of input queue's full, clk(_bft) domain
    always@(posedge wr_clk) begin
        if(reset_ap_start_wr) full_cnt_wr <= 0;
        else begin
            if(full && !state_wr) full_cnt_wr <= full_cnt_wr + 1;
            else full_cnt_wr <= full_cnt_wr;
        end
    end

    // count the number of rd's empty, rd_clk domain
    always@(posedge rd_clk) begin
        if(reset_ap_start_rd) empty_cnt_rd <= 0;
        else begin
            if(empty && !state_rd) empty_cnt_rd <= empty_cnt_rd + 1;
            else empty_cnt_rd <= empty_cnt_rd;
        end
    end

    // count the number of input read, rd_clk domain
    always@(posedge rd_clk) begin
        if(reset_ap_start_rd) read_cnt_rd <= 0;
        else begin
            if(val_out && ready_downward && !state_rd) read_cnt_rd <= read_cnt_rd + 1;
            else read_cnt_rd <= read_cnt_rd;
        end
    end


    xpm_fifo_async # (
    
      // .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
      .FIFO_MEMORY_TYPE          ("auto"),           //string; "auto", "block", or "distributed";
      .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
      .RELATED_CLOCKS            (0),                // 250MHz and 350MHz are related clock?
      .FIFO_WRITE_DEPTH          (FIFO_DEPTH),             //positive integer
      .WRITE_DATA_WIDTH          (WRITE_DATA_WIDTH),               //positive integer
      .WR_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_FULL_THRESH          (10),               //positive integer
      .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
      .READ_MODE                 ("std"),            //string; "std" or "fwft";
      .FIFO_READ_LATENCY         (1),                //positive integer;
      .READ_DATA_WIDTH           (READ_DATA_WIDTH),               //positive integer
      .RD_DATA_COUNT_WIDTH       (),               //positive integer
      .PROG_EMPTY_THRESH         (10),               //positive integer
      .DOUT_RESET_VALUE          ("0"),              //string
      .CDC_SYNC_STAGES           (2),                //positive integer
      .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;
    
    ) xpm_fifo_async2user (

      .rst              (wr_rst),
      .wr_clk           (wr_clk),
      .wr_en            (wr_en),
      .din              (fifo_in),
      .full             (full),
      .overflow         (), // not used
      .wr_rst_busy      (), // not used
      .rd_clk           (rd_clk),
      .rd_en            (rd_en),
      .dout             (fifo_out),
      .empty            (empty),
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
    
/*
xpm_fifo_sync # (

  .FIFO_MEMORY_TYPE          ("block"),           //string; "auto", "block", or "distributed";
  .ECC_MODE                  ("no_ecc"),         //string; "no_ecc" or "en_ecc";
  //.RELATED_CLOCKS            (0),                //positive integer; 0 or 1
  .FIFO_WRITE_DEPTH          (FIFO_DEPTH),             //positive integer
  .WRITE_DATA_WIDTH          (PAYLOAD_BITS),               //positive integer
  .WR_DATA_COUNT_WIDTH       (NUM_BRAM_ADDR_BITS),               //positive integer
  .PROG_FULL_THRESH          (10),               //positive integer
  .FULL_RESET_VALUE          (0),                //positive integer; 0 or 1
  .READ_MODE                 ("std"),            //string; "std" or "fwft";
  .FIFO_READ_LATENCY         (1),                //positive integer;
  .READ_DATA_WIDTH           (PAYLOAD_BITS),               //positive integer
  .RD_DATA_COUNT_WIDTH       (NUM_BRAM_ADDR_BITS),               //positive integer
  .PROG_EMPTY_THRESH         (10),               //positive integer
  .DOUT_RESET_VALUE          ("0"),              //string
  //.CDC_SYNC_STAGES           (2),                //positive integer
  .WAKEUP_TIME               (0)                 //positive integer; 0 or 2;

) xpm_fifo_sync_inst (

  .rst              (reset),
  .wr_clk           (clk),
  .wr_en            (wr_en),
  .din              (fifo_in),
  .full             (full),
  .overflow         (overflow),
  .wr_rst_busy      (wr_rst_busy),
  //.rd_clk           (clk),
  .rd_en            (rd_en),
  .dout             (fifo_out),
  .empty            (empty),
  .underflow        (underflow),
  .rd_rst_busy      (rd_rst_busy),
  .prog_full        (prog_full),
  .wr_data_count    (wr_data_count),
  .prog_empty       (prog_empty),
  .rd_data_count    (rd_data_count),
  .sleep            (1'b0),
  .injectsbiterr    (1'b0),
  .injectdbiterr    (1'b0),
  .sbiterr          (),
  .dbiterr          ()

);
*/

    localparam NODATA = 1'b0;
    localparam VALDATA  = 1'b1;

    reg state;
    reg next_state;

    always@(posedge rd_clk) begin
        if(rd_rst)
            state <= NODATA;
        else
            state <= next_state;
    end


    //assign dout = state ? (fifo_out) : (empty ? 0 : fifo_out);


    always@(*) begin
        case(state)
            NODATA: begin
                if(empty) begin
                    next_state = NODATA;
                    rd_en = 0;
                    dout = 0;
                end else begin
                    next_state = VALDATA;
                    rd_en = 1;
                    dout = fifo_out;
                end
            end
            
            VALDATA: begin
                if(!ready_downward) begin
                    next_state = VALDATA;
                    rd_en = 0;
                    dout = fifo_out;
                end else if (empty) begin
                    next_state = NODATA;
                    rd_en = 0;
                    dout = fifo_out;
                end else begin
                    next_state = VALDATA;
                    rd_en = 1;
                    dout = fifo_out;
                end
            end
        endcase
    end

    //val_out
    always@(posedge rd_clk) begin
        if(rd_rst) begin
            val_out <= 0;
        end else begin
            case(state)
                NODATA: begin
                    if(empty) begin
                        val_out <= 0;
                    end else begin
                        val_out <= 1;
                    end
                end
                
                VALDATA: begin
                    if(!ready_downward) begin
                        val_out <= 1;
                    end else if (ready_downward && empty) begin
                        val_out <= 0;
                    end else if (ready_downward && (!empty)) begin
                        val_out <= 1;
                    end
                end
            endcase
        end
    end

endmodule
