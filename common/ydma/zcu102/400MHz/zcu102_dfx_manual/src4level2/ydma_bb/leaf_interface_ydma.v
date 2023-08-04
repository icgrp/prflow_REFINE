`timescale 1ns / 1ps

// NUM_LEAF_BITS + NUM_PORT_BITS + NUM_ADDR_BITS == ADDR_TOTAL
// NUM_BRAM_ADDR_BITS =< NUM_ADDR_BITS
// NUM_BRAM_ADDR_BITS = NUM_BRAM_ADDR_BITS + NUM_ADDR_REMAINDER_BITS
// port values == 0,1 reserved for initialization packets
// in thise case, port values == 2,3,4,5,6,7,8 are BRAM_IN
// port values == 9,10,11,12,13,14,15 are BRAM_OUT

// leaf_interface for leaf_1
// It uses one clock, clk(_bft)
module leaf_interface_ydma #(
    
    parameter PACKET_BITS = 49,
    parameter PAYLOAD_BITS = 32, 
    parameter NUM_LEAF_BITS = 3,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter NUM_IN_PORTS = 1, 
    parameter NUM_OUT_PORTS = 1,
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter FREESPACE_UPDATE_SIZE = 64,
    localparam OUT_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS+NUM_ADDR_BITS+NUM_BRAM_ADDR_BITS+3,
    localparam IN_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS,
    localparam REG_CONTROL_BITS = OUT_PORTS_REG_BITS*NUM_OUT_PORTS+IN_PORTS_REG_BITS*NUM_IN_PORTS
    )(
    input clk,
    input reset,
    
    //data from BFT
    input [PACKET_BITS-1:0] din_leaf_bft2interface,
    
    //data to BFT
    output [PACKET_BITS-1:0] dout_leaf_interface2bft,
    input resend,

    //data to USER
    output [PAYLOAD_BITS*NUM_IN_PORTS-1:0] dout_leaf_interface2user,
    output [NUM_IN_PORTS-1:0] vld_interface2user,
    input [NUM_IN_PORTS-1:0] ack_user2interface,
    
    //data from USER
    output [NUM_OUT_PORTS-1:0] ack_interface2user,
    input [NUM_OUT_PORTS-1:0] vld_user2interface,
    input [PAYLOAD_BITS*NUM_OUT_PORTS-1:0] din_leaf_user2interface,
    
    // added for counter data
    output     [63:0] cnt,
    output reg        cnt_vld,
    input             cnt_ack,    
    input [31:0]      output_size,
    input             output_size_valid,
    input [15:0]      num_cnt_read,
    input             num_cnt_read_valid,
    output reg [7:0]  is_done_output_size,
    output reg        is_done_output_size_valid,
    
    input ap_start
    );

    wire [PACKET_BITS-1:0] stream_ExCtrl2sfc;
    wire [PACKET_BITS-1:0] stream_sfc2ExCtrl;
    wire [PACKET_BITS-1:0] configure_ExCtrl2ConCtrl;
    wire [REG_CONTROL_BITS-1:0] control_reg;
    wire resend_ExCtrl2sfc; 
    wire instr_wr_en_in;
    wire [31:0] instr_packet;
    wire is_done;
    wire [NUM_LEAF_BITS-1:0] self_leaf_reg;

    wire ap_start_asserted;
    rise_detect #(
        .data_width(1)
    )rise_detect_u(
        .data_out(ap_start_asserted),
        .data_in(ap_start),
        .clk(clk),
        .reset(reset)
    );
    // new_reset is used to reset addr, counter, mem vals when calling a new kernel    
    wire reset_ap_start;
    assign reset_ap_start = reset || ap_start_asserted;


    // cnt collected from operators are sent to host
    reg is_done_mode;
    wire [PACKET_BITS-1:0] din_leaf_bft2interface_normal_mode, din_leaf_bft2interface_is_done_mode;
    assign din_leaf_bft2interface_normal_mode = is_done_mode ? 0 : din_leaf_bft2interface; // normal data
    assign din_leaf_bft2interface_is_done_mode = is_done_mode ? din_leaf_bft2interface : 0;

    reg [15:0] num_cnt_read_reg;
    always@(posedge clk) begin 
        if(reset) num_cnt_read_reg <= 0;
        else begin
            if(num_cnt_read_valid) num_cnt_read_reg <= num_cnt_read;
            else num_cnt_read_reg <= num_cnt_read_reg;
        end
    end

    reg [63:0] cnt_din;
    reg cnt_din_vld;
    reg [15:0] num_cnt_sent_counter;
    always@(posedge clk) begin 
        if(reset) begin
            cnt_din <= 0;
            cnt_din_vld <= 0;
            num_cnt_sent_counter <= 0;
            is_done_mode <= 0;
        end
        else begin
            if(is_done_output_size) begin
                cnt_din <= 0;
                cnt_din_vld <= 0;
                num_cnt_sent_counter <= 0;
                is_done_mode <= 1; // toggle is_done_mode
            end
            else begin
                if(is_done_mode) begin
                    if(num_cnt_sent_counter < num_cnt_read_reg && 
                       din_leaf_bft2interface_is_done_mode[48] == 1) begin
                        cnt_din <= {15'd0, din_leaf_bft2interface_is_done_mode};
                        cnt_din_vld <= 1;
                        num_cnt_sent_counter <= num_cnt_sent_counter + 1;
                        is_done_mode <= is_done_mode;
                    end
                    else if(num_cnt_sent_counter == num_cnt_read_reg) begin
                        cnt_din <= 0;
                        cnt_din_vld <= 0;
                        num_cnt_sent_counter <= 0; // reset
                        is_done_mode <= 0; // untoggle is_done_mode
                    end
                    else begin
                        cnt_din <= 0;
                        cnt_din_vld <= 0;
                        num_cnt_sent_counter <= num_cnt_sent_counter;
                        is_done_mode <= is_done_mode;
                    end
                end
                else begin
                    cnt_din <= 0;
                    cnt_din_vld <= 0;
                    num_cnt_sent_counter <= 0;
                    is_done_mode <= 0;
                end
            end
        end
    end

    // code below copied from Input_port.v
    wire cnt_empty;
    wire [63:0] cnt_dout;
    reg cnt_rd_en;

    SynFIFO #(
        .DSIZE(64)
        )SynFIFO_cnt_inst (
        .clk(clk),
        .rst_n(!reset),
        .rdata(cnt_dout), 
        .wfull(), // 32*14 < 512, so should be enough for BFT-32 
        .rempty(cnt_empty), 
        .wdata(cnt_din),
        .winc(cnt_din_vld), 
        .rinc(cnt_rd_en)
    );
    assign cnt = cnt_dout;
    
    //rd_en
    always@(*) begin
        if(cnt_empty) begin
            cnt_rd_en = 0;
        end else begin
            if(cnt_ack) begin
                cnt_rd_en = 1;
            end else begin
                cnt_rd_en = ~cnt_vld;
            end
        end
    end
        
    //cnt_vld
    always@(posedge clk) begin
        if(reset) begin
            cnt_vld <= 0;
        end else begin
            if(cnt_rd_en) begin
                cnt_vld <= 1;
            end else begin
                if(cnt_vld) begin
                    if(cnt_ack) begin
                        cnt_vld <= 0;
                    end else begin
                        cnt_vld <= 1;
                    end
                end else begin
                    cnt_vld <= 0;
                end
            end
        end
    end


    // is_done generate logic
    reg [31:0] output_size_reg;
    reg [31:0] rd_en_counter;
    wire rd_en_input_1;
    always@(posedge clk) begin 
        if(reset) begin
            output_size_reg <= 0;
            rd_en_counter <= 0;

            is_done_output_size <= 0;
            is_done_output_size_valid <= 0;
        end 
        else begin
            if(output_size_valid) begin // when the kernel starts
                output_size_reg <= output_size * 16; // 16=512/32
                rd_en_counter <= 0; // reset
                is_done_output_size <= 0;
                is_done_output_size_valid <= 0;
            end
            else begin
                output_size_reg <= output_size_reg;
                if(rd_en_counter == output_size_reg && rd_en_counter != 0) begin
                    is_done_output_size <= 1; // asserted for 1 cycle
                    is_done_output_size_valid <= 1; // asserted for 1 cycle
                    rd_en_counter <= 0; // reset but will increment because cnt data
                end
                else begin
                    if(rd_en_input_1) begin
                        rd_en_counter <= rd_en_counter + 1;
                    end
                    else begin                    
                        rd_en_counter <= rd_en_counter; 
                    end
                    is_done_output_size <= 0;
                    is_done_output_size_valid <= 0;
                end
            end
        end
    end
    
    Extract_Control # (
        .PACKET_BITS(PACKET_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS)
    )ExCtrl(
        .clk(clk),
        .reset(reset),
        .din_leaf_bft2interface(din_leaf_bft2interface),
        .dout_leaf_interface2bft(dout_leaf_interface2bft),
        .resend(resend),
        .resend_out(resend_ExCtrl2sfc),
        .stream_in(stream_sfc2ExCtrl),
        .stream_out(stream_ExCtrl2sfc),
        .configure_out(configure_ExCtrl2ConCtrl),
        .instr_wr_en(instr_wr_en_in),
        .instr_packet(instr_packet),
        .ap_start_user() // this ap_start_user is artifact of PLD paper
    );

    Config_Controls_ydma # (
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS)
    )ConCtrl_ydma(
        .control_reg(control_reg),
        .clk(clk),
        .reset(reset),
        .configure_in(configure_ExCtrl2ConCtrl)
    );
    
    Stream_Flow_Control_ydma #(
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),
        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE)
    )sfc_ydma(
        .resend(resend_ExCtrl2sfc),
        .clk(clk),
        .reset(reset_ap_start),
        .stream_in(stream_ExCtrl2sfc),
        .stream_out(stream_sfc2ExCtrl),
        .control_reg(control_reg),
        .dout_leaf_interface2user(dout_leaf_interface2user),
        .vld_interface2user(vld_interface2user),
        .ack_user2interface(ack_user2interface),
        .ack_interface2user(ack_interface2user),
        .vld_user2interface(vld_user2interface),
        .din_leaf_user2interface(din_leaf_user2interface),
        .rd_en_input_1(rd_en_input_1) // difference from old sfc!
    );    
        
endmodule