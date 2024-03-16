`timescale 1ns / 1ps 

module expand_queue_fifo #(
    parameter PAYLOAD_BITS = 32,
    parameter IN_WIDTH = 512,
    parameter OUT_WIDTH = 32,
    parameter INPUT_PORT = 0
    )(
    clk,
    reset,
    d_a,
    vld_a,
    rdy_a,
    d_b,
    vld_b,
    rdy_b,

    is_done_mode_user,
    full_cnt,
    empty_cnt,
    read_cnt,
    stall_condition);
input                      clk;
input                      reset;
input [IN_WIDTH-1:0]       d_a;
input                      vld_a;
output                     rdy_a;
output  [OUT_WIDTH-1:0] d_b;
output                  vld_b;
input                      rdy_b;

input is_done_mode_user;
output reg [PAYLOAD_BITS-1:0] full_cnt;
output reg [PAYLOAD_BITS-1:0] empty_cnt;
output reg [PAYLOAD_BITS-1:0] read_cnt;
output stall_condition;

    // SynFIFO
    wire full, empty;
    wire [IN_WIDTH-1:0] fifo_in, fifo_out;
    wire wr_en;
    reg rd_en;

    // expand_queue
    wire [IN_WIDTH-1:0] din;
    reg vld_in; 
    wire rdy_upward;

    expand_queue#(
      .IN_WIDTH(IN_WIDTH),
      .OUT_WIDTH(OUT_WIDTH)
    )e_q(
      .clk(clk),
      .reset(reset),
      .din(din),
      .vld_in(vld_in),
      .rdy_upward(rdy_upward),

      .dout(d_b),
      .vld_out(vld_b),
      .rdy_downward(rdy_b)
    );

    assign din = fifo_out;

    //rd_en
    always@(*) begin
        if(empty) begin
            rd_en = 0;
        end else begin
            if(rdy_upward) begin
                rd_en = 1;
            end else begin
                rd_en = ~vld_in;
            end
        end
    end

    //vld_in
    always@(posedge clk) begin
        if(reset) begin
            vld_in <= 0;
        end else begin
            if(rd_en) begin
                vld_in <= 1;
            end else begin
                if(vld_in) begin
                    if(rdy_upward) begin
                        vld_in <= 0;
                    end else begin
                        vld_in <= 1;
                    end
                end else begin
                    vld_in <= 0;
                end
            end
        end
    end

    SynFIFO #(
        .DSIZE(IN_WIDTH),
        .ASIZE(5),
        .RAM_TYPE("distributed")
    )SynFIFO_inst (
        .clk(clk),
        .rst_n(!reset),
        .rdata(fifo_out), 
        .wfull(full), 
        .rempty(empty), 
        .wdata(fifo_in),
        .winc(wr_en), 
        .rinc(rd_en)
    );

    assign wr_en = (~full) && vld_a;
    assign rdy_a = ~full;
    assign fifo_in = d_a;

    /////////////////////////
    // counter logic below //
    /////////////////////////

    // Stall condition generator
    generate
        case(INPUT_PORT)
            1: assign stall_condition = (!is_done_mode_user) && rdy_b && empty; // if this is input port fifo
            // 1: assign stall_condition = 0; // if this is input port fifo
            0: assign stall_condition = (!is_done_mode_user) && vld_a && full; // if this is output port fifo
        endcase
    endgenerate

    // full_cnt
    always@(posedge clk) begin
        if(reset) full_cnt <= 0;
        else begin
            if(full && !is_done_mode_user) full_cnt <= full_cnt + 1;
            else full_cnt <= full_cnt;
        end
    end

    // empty_cnt
    always@(posedge clk) begin
        if(reset) empty_cnt <= 0;
        else begin
            if(empty && !is_done_mode_user) empty_cnt <= empty_cnt + 1;
            else empty_cnt <= empty_cnt;
        end
    end

    // read_cnt
    always@(posedge clk) begin
        if(reset) read_cnt <= 0;
        else begin
            if(vld_b && rdy_b && !is_done_mode_user) read_cnt <= read_cnt + 1;
            else read_cnt <= read_cnt;
        end
    end

endmodule
