`timescale 1ns / 1ps

// Increments tall counter per operator
module stall_cnt(
    input clk, // clk the operator runs
    input reset,

    input state, // 0: running, 1: done
    input input_stall_condition,
    input output_stall_condition,
    output reg [31:0] stall_cnt
    );

    wire stall_condition;
    assign stall_condition = input_stall_condition || output_stall_condition;
    always@(posedge clk) begin
        if(reset) stall_cnt <= 0;
        else begin
            if(!state && stall_condition) stall_cnt <= stall_cnt + 1;
            else stall_cnt <= stall_cnt;
        end
    end

endmodule
