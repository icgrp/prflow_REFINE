// Logic for sending full_cnt values for input queues and output queues

// input_port_full_cnt from Input_Port_Cluster
// output_port_empty_cnt from Output_Port_Cluster are in clk(_bft) domain,
// but they are guaranteed to be static by the time they are sampled in clk_user
`define INPUT_PORT_MAX_NUM 8
`define OUTPUT_PORT_MIN_NUM 9

module send_IO_queue_cnt #(
    parameter NUM_LEAF_BITS = 6,
    parameter NUM_PORT_BITS = 4,
    parameter PAYLOAD_BITS = 32, 
    parameter NUM_IN_PORTS = 7, 
    parameter NUM_OUT_PORTS = 7,
    parameter STALL_CNT = 0
)(
    input clk_user,
    input reset_user,
    input is_done_user,
    input is_done_mode_user,
    input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_full_cnt,
    input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_empty_cnt,
    input [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_read_cnt,
    input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_full_cnt,
    input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_empty_cnt,
    input input_port_cluster_stall_condition,
    input output_port_cluster_stall_condition,
    input [NUM_LEAF_BITS-1:0] self_leaf, // clk_user domain

    output reg is_sending_full_cnt_reg,
    output reg [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] cnt_val,
    output reg [NUM_LEAF_BITS-1:0] self_leaf_reg,
    output reg [NUM_PORT_BITS-1:0] self_port_reg,
    output reg [1:0] cnt_type_reg // 3: full counter, 2: empty counter, 1: read coutner, 0: stall counter
);
    reg [PAYLOAD_BITS*NUM_IN_PORTS-1:0] input_port_cnt_tmp;
    reg [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] output_port_cnt_tmp;

    reg [NUM_PORT_BITS+1:0] num_in_ports_remain; // three(2bit) counters will be sent from input queue
    reg [NUM_PORT_BITS:0] num_out_ports_remain; // one(1bit) counter will be sent from output queue 
    reg num_others_remain;


    // count the number of stall for this user operator
    reg [PAYLOAD_BITS-1:0] stall_cnt;
    wire stall_condition;
    assign stall_condition = input_port_cluster_stall_condition || output_port_cluster_stall_condition;
    always@(posedge clk_user) begin
        if(reset_user) stall_cnt <= 0;
        else begin
            if(!is_done_mode_user && stall_condition) stall_cnt <= stall_cnt + 1;
            else stall_cnt <= stall_cnt;
        end
    end


    always@(posedge clk_user) begin
        if(reset_user) begin
            is_sending_full_cnt_reg <= 0;
            num_in_ports_remain <= NUM_IN_PORTS*3; // 3 is for full,empty,read cnt
            num_out_ports_remain <= NUM_OUT_PORTS*2; // 2 is for full,empty // write cnt is redundant with input's read
            num_others_remain <= STALL_CNT; // only stall counter for now...
            cnt_val <= 0;
            input_port_cnt_tmp <= 0;
            output_port_cnt_tmp <= 0;
            self_leaf_reg <= 0;
            self_port_reg <= 0;
            cnt_type_reg <= 0;
        end
        else begin
            self_leaf_reg <= self_leaf; // stays static

            if(is_done_user) begin // doesn't matter whether it's asserted for 1 cycle or 3 cycles
                is_sending_full_cnt_reg <= 1;
            end
            else if (num_in_ports_remain + num_out_ports_remain + num_others_remain == 0) begin
                is_sending_full_cnt_reg <= 0;
            end
            else begin
                is_sending_full_cnt_reg <= is_sending_full_cnt_reg;
            end

            if(is_done_user || is_sending_full_cnt_reg == 1) begin
                if (num_in_ports_remain > NUM_IN_PORTS*2) begin
                    num_in_ports_remain <= num_in_ports_remain - 1;
                    // only output_port_0 is active
                    cnt_val[PAYLOAD_BITS-1:0] <= input_port_cnt_tmp[PAYLOAD_BITS-1:0];
                    self_port_reg <= 2 + (NUM_IN_PORTS - (num_in_ports_remain - NUM_IN_PORTS*2));
                    cnt_type_reg <= 1; // input queue read cnt
                    if (num_in_ports_remain > NUM_IN_PORTS*2 + 1) input_port_cnt_tmp <= input_port_cnt_tmp >> PAYLOAD_BITS;
                    else input_port_cnt_tmp <= input_port_empty_cnt;
                end
                else if (num_in_ports_remain > NUM_IN_PORTS*1) begin
                    num_in_ports_remain <= num_in_ports_remain - 1;
                    cnt_val[PAYLOAD_BITS-1:0] <= input_port_cnt_tmp[PAYLOAD_BITS-1:0];
                    self_port_reg <= 2 + (NUM_IN_PORTS - (num_in_ports_remain - NUM_IN_PORTS*1));
                    cnt_type_reg <= 2; // input queue empty cnt
                    if (num_in_ports_remain > NUM_IN_PORTS*1 + 1) input_port_cnt_tmp <= input_port_cnt_tmp >> PAYLOAD_BITS;
                    else input_port_cnt_tmp <= input_port_full_cnt;
                end
                else if (num_in_ports_remain > NUM_IN_PORTS*0) begin
                    num_in_ports_remain <= num_in_ports_remain - 1;
                    cnt_val[PAYLOAD_BITS-1:0] <= input_port_cnt_tmp[PAYLOAD_BITS-1:0];
                    self_port_reg <= 2 + (NUM_IN_PORTS - (num_in_ports_remain - NUM_IN_PORTS*0));
                    cnt_type_reg <= 3; // input queue full cnt
                    if (num_in_ports_remain > NUM_IN_PORTS*0 + 1) input_port_cnt_tmp <= input_port_cnt_tmp >> PAYLOAD_BITS;
                    else input_port_cnt_tmp <= input_port_cnt_tmp; // must be 0
                end

                else if (num_out_ports_remain > NUM_OUT_PORTS*1) begin
                    num_out_ports_remain <= num_out_ports_remain - 1;
                    cnt_val[PAYLOAD_BITS-1:0] <= output_port_cnt_tmp[PAYLOAD_BITS-1:0];
                    self_port_reg <= `OUTPUT_PORT_MIN_NUM + (NUM_OUT_PORTS - (num_out_ports_remain - NUM_OUT_PORTS*1));
                    cnt_type_reg <= 3; // output queue full cnt
                    if (num_out_ports_remain > NUM_OUT_PORTS*1 + 1) output_port_cnt_tmp <= output_port_cnt_tmp >> PAYLOAD_BITS;
                    else output_port_cnt_tmp <= output_port_empty_cnt;
                end
                else if (num_out_ports_remain > NUM_OUT_PORTS*0) begin
                    num_out_ports_remain <= num_out_ports_remain - 1;
                    cnt_val[PAYLOAD_BITS-1:0] <= output_port_cnt_tmp[PAYLOAD_BITS-1:0];
                    self_port_reg <= `OUTPUT_PORT_MIN_NUM + (NUM_OUT_PORTS - (num_out_ports_remain - NUM_OUT_PORTS*0));
                    cnt_type_reg <= 2; // output queue empty cnt
                    if (num_out_ports_remain > NUM_OUT_PORTS*0 + 1) output_port_cnt_tmp <= output_port_cnt_tmp >> PAYLOAD_BITS;
                    else output_port_cnt_tmp <= output_port_cnt_tmp; // must be 0
                end
                else if (num_others_remain > 0) begin
                    num_others_remain <= num_others_remain - 1;
                    cnt_val[PAYLOAD_BITS-1:0] <= stall_cnt;
                    self_port_reg <= 0; // don't care
                    cnt_type_reg <= 0;
                end
            end
            else begin
                num_in_ports_remain <= num_in_ports_remain;
                num_out_ports_remain <= num_out_ports_remain;
                cnt_val <= cnt_val;
                self_port_reg <= self_port_reg;
                cnt_type_reg <= cnt_type_reg;
                // input_port_cnt_tmp <= input_port_full_cnt;
                input_port_cnt_tmp <= input_port_read_cnt;
                output_port_cnt_tmp <= output_port_full_cnt;
            end
        end
    end

endmodule



