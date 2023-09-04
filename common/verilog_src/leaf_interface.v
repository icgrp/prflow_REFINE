`timescale 1ns / 1ps

// NUM_LEAF_BITS + NUM_PORT_BITS + NUM_ADDR_BITS == ADDR_TOTAL
// NUM_BRAM_ADDR_BITS =< NUM_ADDR_BITS
// NUM_BRAM_ADDR_BITS = NUM_BRAM_ADDR_BITS + NUM_ADDR_REMAINDER_BITS
// port values == 0,1 reserved for initialization packets
// in thise case, port values == 2,3,4,5,6,7,8 are BRAM_IN
// port values == 9,10,11,12,13,14,15 are BRAM_OUT
// STALL_CNT is set to 1 for only one leaf interface per user operator
module leaf_interface #(
    
    parameter PACKET_BITS = 49,
    parameter PAYLOAD_BITS = 32, 
    parameter NUM_LEAF_BITS = 3,
    parameter NUM_PORT_BITS = 4,
    parameter NUM_ADDR_BITS = 7,
    parameter NUM_IN_PORTS = 1, 
    parameter NUM_OUT_PORTS = 1,
    parameter NUM_BRAM_ADDR_BITS = 7,
    parameter FREESPACE_UPDATE_SIZE = 64,
    parameter STALL_CNT = 0,
    localparam OUT_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS+NUM_ADDR_BITS+NUM_BRAM_ADDR_BITS+3,
    localparam IN_PORTS_REG_BITS = NUM_LEAF_BITS+NUM_PORT_BITS,
    localparam REG_CONTROL_BITS = OUT_PORTS_REG_BITS*NUM_OUT_PORTS+IN_PORTS_REG_BITS*NUM_IN_PORTS
    )(
    input clk,
    input clk_user,
    input reset,
    // input reset_user,
    
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
    
    // interface to configure the instruction mem for riscv
    // output [23:0] riscv_addr,
    // output [7:0] riscv_dout,
    // output instr_wr_en_out,
    
    // ap_start control the kernel logic
    output ap_start_user,
    // ap_start for leaf_interface
    input ap_start,
    output reset_ap_start_user,

    // When operator uses multiple leaf interfaces, 
    // stall conditions need to be sent to one leaf interface which
    // counts the num of stalls
    input input_port_cluster_stall_condition_others, 
    input output_port_cluster_stall_condition_others,
    output input_port_cluster_stall_condition_self,
    output output_port_cluster_stall_condition_self
    );
   
    wire [PACKET_BITS-1:0] stream_ExCtrl2sfc;
    wire [PACKET_BITS-1:0] stream_sfc2ExCtrl;
    wire [PACKET_BITS-1:0] configure_ExCtrl2ConCtrl;
    wire [REG_CONTROL_BITS-1:0] control_reg;
    wire resend_ExCtrl2sfc; 
    wire instr_wr_en_in;
    wire [31:0] instr_packet;

    wire [NUM_LEAF_BITS-1:0] self_leaf_reg_0;
    wire self_leaf_reg_0_src_send, self_leaf_reg_0_src_rcv;
    reg self_leaf_reg_0_dest_ack;
    wire self_leaf_reg_0_dest_req;
    wire [NUM_LEAF_BITS-1:0] self_leaf_reg_user_0;
    reg [NUM_LEAF_BITS-1:0] self_leaf_reg_user;

    wire reset_user;
    reg reset_1, reset_2, reset_3, reset_4, reset_5; 

    wire ap_start_asserted;
    wire reset_ap_start; 

    reg ap_start_1, ap_start_2; // in order to stretch ap_start for two more cycles
    wire ap_start_user_0;
    wire ap_start_user_0_asserted;

    wire is_done_0;
    reg is_done_1, is_done_2; // in order to stretch is_done_0 for two more cycles
    wire is_done_user;


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
        .ap_start_user(ap_start_user) // this ap_start_user is artifact of PLD paper
    );
    

    Config_Controls # (
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS)
    )ConCtrl(
        .control_reg(control_reg),
        .clk(clk),
        .reset(reset),
        .configure_in(configure_ExCtrl2ConCtrl),
        .is_done(is_done_0),

        .self_leaf_reg(self_leaf_reg_0),
        .self_leaf_reg_src_send(self_leaf_reg_0_src_send),
        .self_leaf_reg_src_rcv(self_leaf_reg_0_src_rcv)
    );


    // CDC for active high reset_user; reset_user is generated from reset(_bft)
    xpm_cdc_async_rst #(
       .DEST_SYNC_FF(4),    // DECIMAL; range: 2-10
       .INIT_SYNC_FF(0),    // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
       .RST_ACTIVE_HIGH(1)  // DECIMAL; 0=active low reset, 1=active high reset
    )
    xpm_cdc_async_reset_user_inst (
       .dest_arst(reset_user), // 1-bit output: src_arst asynchronous reset signal synchronized to destination
                              // clock domain. This output is registered. NOTE: Signal asserts asynchronously
                              // but deasserts synchronously to dest_clk. Width of the reset signal is at least
                              // (DEST_SYNC_FF*dest_clk) period.
       .dest_clk(clk_user),   // 1-bit input: Destination clock.
       .src_arst(reset)    // 1-bit input: Source asynchronous reset signal.
    );


    // DJP: ap_start_reset is asserted when reset is on OR ap_start is on.
    //      We need this to launch kernel multiple times because if we don't
    //      reset with the new kernel launch, freespace info in read_b_in  is
    //      not consistent with freespace info in NoC configuration pakcets, which is set to 127.
    //      IO queue counters are also reset with ap_start.
    rise_detect #(
        .data_width(1)
    )rise_detect_ap_start_u(
        .data_out(ap_start_asserted),
        .data_in(ap_start),
        .clk(clk),
        .reset(reset)
    );
    assign reset_ap_start = reset || ap_start_asserted;
    

    // CDC for ap_start, can also be done with xpm_cdc_pulse
    always @ (posedge clk) begin
        ap_start_1 <= ap_start;
        ap_start_2 <= ap_start_1;
    end
    xpm_cdc_single #(
       .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10
       .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
       .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
       .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input
    )
    xpm_cdc_single_ap_start_inst (
       .dest_out(ap_start_user_0), // 1-bit output: src_in synchronized to the destination clock domain. This output is
                                   // registered.
       .dest_clk(clk_user),        // 1-bit input: Clock signal for the destination clock domain.
       .src_clk(clk),              // 1-bit input: optional; required when SRC_INPUT_REG = 1
       .src_in(ap_start | ap_start_1 | ap_start_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.
    );
    rise_detect #(
        .data_width(1)
    )rise_detect_ap_start_user_u(
        .data_out(ap_start_user_0_asserted),
        .data_in(ap_start_user_0),
        .clk(clk_user),
        .reset(reset_user)
    );
    assign reset_ap_start_user = reset_user || ap_start_user_0_asserted;
    // xpm_cdc_pulse #(
    //    .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10
    //    .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
    //    .REG_OUTPUT(0),     // DECIMAL; 0=disable registered output, 1=enable registered output
    //    .RST_USED(0),       // DECIMAL; 0=no reset, 1=implement reset
    //    .SIM_ASSERT_CHK(0)  // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
    // )
    // xpm_cdc_pulse_ap_start_inst (
    //    .dest_pulse(ap_start_user_0), // 1-bit output: Outputs a pulse the size of one dest_clk period when a pulse
    //                             // transfer is correctly initiated on src_pulse input. This output is
    //                             // combinatorial unless REG_OUTPUT is set to 1.

    //    .dest_clk(clk_user),     // 1-bit input: Destination clock.
    //    .dest_rst(),     // 1-bit input: optional; required when RST_USED = 1
    //    .src_clk(clk),       // 1-bit input: Source clock.
    //    .src_pulse(ap_start | ap_start_1 | ap_start_2),   // 1-bit input: Rising edge of this signal initiates a pulse transfer to the
    //                             // destination clock domain. The minimum gap between each pulse transfer must be
    //                             // at the minimum 2*(larger(src_clk period, dest_clk period)). This is measured
    //                             // between the falling edge of a src_pulse to the rising edge of the next
    //                             // src_pulse. This minimum gap will guarantee that each rising edge of src_pulse
    //                             // will generate a pulse the size of one dest_clk period in the destination
    //                             // clock domain. When RST_USED = 1, pulse transfers will not be guaranteed while
    //                             // src_rst and/or dest_rst are asserted.

    //    .src_rst()        // 1-bit input: optional; required when RST_USED = 1
    // );



    // CDC for is_done_0, can also be done with xpm_cdc_pulse
    // Having is_done_3 could be dangerous because it could collide with is_sending_full_cnt_reg in sfc
    always @ (posedge clk) begin
        is_done_1 <= is_done_0;
        is_done_2 <= is_done_1;
    end
    xpm_cdc_single #(
       .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10
       .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
       .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
       .SRC_INPUT_REG(1)   // DECIMAL; 0=do not register input, 1=register input
    )
    xpm_cdc_single_is_done_inst (
       .dest_out(is_done_user), // 1-bit output: src_in synchronized to the destination clock domain. This output is
                                // registered.
       .dest_clk(clk_user),     // 1-bit input: Clock signal for the destination clock domain.
       .src_clk(clk),           // 1-bit input: optional; required when SRC_INPUT_REG = 1
       .src_in(is_done_0 | is_done_1 | is_done_2)      // 1-bit input: Input signal to be synchronized to dest_clk domain.
    );
    // xpm_cdc_pulse #(
    //    .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10
    //    .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
    //    .REG_OUTPUT(0),     // DECIMAL; 0=disable registered output, 1=enable registered output
    //    .RST_USED(0),       // DECIMAL; 0=no reset, 1=implement reset
    //    .SIM_ASSERT_CHK(0)  // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
    // )
    // xpm_cdc_pulse_is_done_inst (
    //    .dest_pulse(is_done_user), // 1-bit output: Outputs a pulse the size of one dest_clk period when a pulse
    //                             // transfer is correctly initiated on src_pulse input. This output is
    //                             // combinatorial unless REG_OUTPUT is set to 1.

    //    .dest_clk(clk_user),     // 1-bit input: Destination clock.
    //    .dest_rst(),     // 1-bit input: optional; required when RST_USED = 1
    //    .src_clk(clk),       // 1-bit input: Source clock.
    //    .src_pulse(is_done_0 | is_done_1 | is_done_2),   // 1-bit input: Rising edge of this signal initiates a pulse transfer to the
    //                             // destination clock domain. The minimum gap between each pulse transfer must be
    //                             // at the minimum 2*(larger(src_clk period, dest_clk period)). This is measured
    //                             // between the falling edge of a src_pulse to the rising edge of the next
    //                             // src_pulse. This minimum gap will guarantee that each rising edge of src_pulse
    //                             // will generate a pulse the size of one dest_clk period in the destination
    //                             // clock domain. When RST_USED = 1, pulse transfers will not be guaranteed while
    //                             // src_rst and/or dest_rst are asserted.

    //    .src_rst()        // 1-bit input: optional; required when RST_USED = 1
    // );



    // CDC for self_leaf_reg
    // DJP: I think, because self_leaf_reg_0 is reigstered once and stays static, CDC circuits may not be necessary..
    xpm_cdc_handshake #(
       .DEST_EXT_HSK(1),   // DECIMAL; 0=internal handshake, 1=external handshake
       .DEST_SYNC_FF(4),   // DECIMAL; range: 2-10
       .INIT_SYNC_FF(0),   // DECIMAL; 0=disable simulation init values, 1=enable simulation init values
       .SIM_ASSERT_CHK(0), // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
       .SRC_SYNC_FF(4),    // DECIMAL; range: 2-10
       .WIDTH(NUM_LEAF_BITS)           // DECIMAL; range: 1-1024
    )
    xpm_cdc_handshake_self_leaf_reg_inst (
       .dest_out(self_leaf_reg_user_0), // WIDTH-bit output: Input bus (src_in) synchronized to destination clock domain.
                            // This output is registered.

       .dest_req(self_leaf_reg_0_dest_req), // 1-bit output: Assertion of this signal indicates that new dest_out data has been
                            // received and is ready to be used or captured by the destination logic. When
                            // DEST_EXT_HSK = 1, this signal will deassert once the source handshake
                            // acknowledges that the destination clock domain has received the transferred data.
                            // When DEST_EXT_HSK = 0, this signal asserts for one clock period when dest_out bus
                            // is valid. This output is registered.

       .src_rcv(self_leaf_reg_0_src_rcv),   // 1-bit output: Acknowledgement from destination logic that src_in has been
                            // received. This signal will be deasserted once destination handshake has fully
                            // completed, thus completing a full data transfer. This output is registered.

       .dest_ack(self_leaf_reg_0_dest_ack), // 1-bit input: optional; required when DEST_EXT_HSK = 1
       .dest_clk(clk_user), // 1-bit input: Destination clock.
       .src_clk(clk),   // 1-bit input: Source clock.
       .src_in(self_leaf_reg_0),     // WIDTH-bit input: Input bus that will be synchronized to the destination clock
                            // domain.

       .src_send(self_leaf_reg_0_src_send)  // 1-bit input: Assertion of this signal allows the src_in bus to be synchronized to
                            // the destination clock domain. This signal should only be asserted when src_rcv is
                            // deasserted, indicating that the previous data transfer is complete. This signal
                            // should only be deasserted once src_rcv is asserted, acknowledging that the src_in
                            // has been received by the destination logic.
    );
    always @ (posedge clk_user) begin
        if(reset_ap_start_user) begin
            self_leaf_reg_user <= 0;
            self_leaf_reg_0_dest_ack <= 0;
        end
        else begin
            if(self_leaf_reg_0_dest_req) begin
                self_leaf_reg_user <= self_leaf_reg_user_0;
                self_leaf_reg_0_dest_ack <= 1;
            end
            else begin
                self_leaf_reg_user <= self_leaf_reg_user;
                self_leaf_reg_0_dest_ack <= 0;                
            end
        end
    end


    Stream_Flow_Control#(
        .PACKET_BITS(PACKET_BITS),
        .NUM_LEAF_BITS(NUM_LEAF_BITS),
        .NUM_PORT_BITS(NUM_PORT_BITS),
        .NUM_ADDR_BITS(NUM_ADDR_BITS),
        .PAYLOAD_BITS(PAYLOAD_BITS),
        .NUM_IN_PORTS(NUM_IN_PORTS),
        .NUM_OUT_PORTS(NUM_OUT_PORTS),
        .NUM_BRAM_ADDR_BITS(NUM_BRAM_ADDR_BITS),
        .FREESPACE_UPDATE_SIZE(FREESPACE_UPDATE_SIZE),
        .STALL_CNT(STALL_CNT)
    )sfc(
        .resend(resend_ExCtrl2sfc),
        .clk(clk),
        .clk_user(clk_user),
        .reset(reset_ap_start),
        .reset_user(reset_ap_start_user),
        .stream_in(stream_ExCtrl2sfc),
        .stream_out(stream_sfc2ExCtrl),
        .control_reg(control_reg),
        .dout_leaf_interface2user(dout_leaf_interface2user),
        .vld_interface2user(vld_interface2user),
        .ack_user2interface(ack_user2interface),
        .ack_interface2user(ack_interface2user),
        .vld_user2interface(vld_user2interface),
        .din_leaf_user2interface(din_leaf_user2interface),

        .is_done(is_done_0), // clk(_bft) domain
        .is_done_user(is_done_user), // clk_user domain
        .self_leaf(self_leaf_reg_user), // clk_user domain, as self_leaf_reg_0 is static, no problem in CDC

        .input_port_cluster_stall_condition_others(input_port_cluster_stall_condition_others),
        .output_port_cluster_stall_condition_others(output_port_cluster_stall_condition_others),
        .input_port_cluster_stall_condition_self(input_port_cluster_stall_condition_self),
        .output_port_cluster_stall_condition_self(output_port_cluster_stall_condition_self)
    );
        
    // instr_config riscv_config(
    //     .clk(clk),
    //     .instr_wr_en_in(instr_wr_en_in),
    //     .instr_packet(instr_packet),
    //     .addr(riscv_addr),
    //     .dout(riscv_dout),
    //     .instr_wr_en_out(instr_wr_en_out),
    //     .reset(reset)
    //   );


endmodule