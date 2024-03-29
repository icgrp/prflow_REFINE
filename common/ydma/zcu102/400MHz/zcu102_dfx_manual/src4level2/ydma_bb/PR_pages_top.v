module PR_pages_top(
        input wire clk_200,
        input wire clk_250,
        input wire clk_300,
        input wire clk_350,
        input wire clk_400,

        input wire ap_rst_n_inv_400_p2,
        input wire ap_rst_n_inv_400_p3,
        input wire ap_rst_n_inv_400_p4,
        input wire ap_rst_n_inv_400_p5,
        input wire ap_rst_n_inv_400_p6,
        input wire ap_rst_n_inv_400_p7,
        input wire ap_rst_n_inv_400_p8,
        input wire ap_rst_n_inv_400_p9,
        input wire ap_rst_n_inv_400_p10,
        input wire ap_rst_n_inv_400_p11,
        input wire ap_rst_n_inv_400_p12,
        input wire ap_rst_n_inv_400_p13,
        input wire ap_rst_n_inv_400_p14,
        input wire ap_rst_n_inv_400_p15,
        input wire ap_rst_n_inv_400_p16,
        input wire ap_rst_n_inv_400_p17,
        input wire ap_rst_n_inv_400_p18,
        input wire ap_rst_n_inv_400_p19,
        input wire ap_rst_n_inv_400_p20,
        input wire ap_rst_n_inv_400_p21,
        input wire ap_rst_n_inv_400_p22,
        input wire ap_rst_n_inv_400_p23,

        input wire ap_start_400_p2,
        input wire ap_start_400_p3,
        input wire ap_start_400_p4,
        input wire ap_start_400_p5,
        input wire ap_start_400_p6,
        input wire ap_start_400_p7,
        input wire ap_start_400_p8,
        input wire ap_start_400_p9,
        input wire ap_start_400_p10,
        input wire ap_start_400_p11,
        input wire ap_start_400_p12,
        input wire ap_start_400_p13,
        input wire ap_start_400_p14,
        input wire ap_start_400_p15,
        input wire ap_start_400_p16,
        input wire ap_start_400_p17,
        input wire ap_start_400_p18,
        input wire ap_start_400_p19,
        input wire ap_start_400_p20,
        input wire ap_start_400_p21,
        input wire ap_start_400_p22,
        input wire ap_start_400_p23,

        input wire resend_2,
        input wire resend_3,
        input wire resend_4,
        input wire resend_5,
        input wire resend_6,
        input wire resend_7,
        input wire resend_8,
        input wire resend_9,
        input wire resend_10,
        input wire resend_11,
        input wire resend_12,
        input wire resend_13,
        input wire resend_14,
        input wire resend_15,
        input wire resend_16,
        input wire resend_17,
        input wire resend_18,
        input wire resend_19,
        input wire resend_20,
        input wire resend_21,
        input wire resend_22,
        input wire resend_23,
        input wire [48:0] din_leaf_2,
        input wire [48:0] din_leaf_3,
        input wire [48:0] din_leaf_4,
        input wire [48:0] din_leaf_5,
        input wire [48:0] din_leaf_6,
        input wire [48:0] din_leaf_7,
        input wire [48:0] din_leaf_8,
        input wire [48:0] din_leaf_9,
        input wire [48:0] din_leaf_10,
        input wire [48:0] din_leaf_11,
        input wire [48:0] din_leaf_12,
        input wire [48:0] din_leaf_13,
        input wire [48:0] din_leaf_14,
        input wire [48:0] din_leaf_15,
        input wire [48:0] din_leaf_16,
        input wire [48:0] din_leaf_17,
        input wire [48:0] din_leaf_18,
        input wire [48:0] din_leaf_19,
        input wire [48:0] din_leaf_20,
        input wire [48:0] din_leaf_21,
        input wire [48:0] din_leaf_22,
        input wire [48:0] din_leaf_23,
        output wire [48:0] dout_leaf_2,
        output wire [48:0] dout_leaf_3,
        output wire [48:0] dout_leaf_4,
        output wire [48:0] dout_leaf_5,
        output wire [48:0] dout_leaf_6,
        output wire [48:0] dout_leaf_7,
        output wire [48:0] dout_leaf_8,
        output wire [48:0] dout_leaf_9,
        output wire [48:0] dout_leaf_10,
        output wire [48:0] dout_leaf_11,
        output wire [48:0] dout_leaf_12,
        output wire [48:0] dout_leaf_13,
        output wire [48:0] dout_leaf_14,
        output wire [48:0] dout_leaf_15,
        output wire [48:0] dout_leaf_16,
        output wire [48:0] dout_leaf_17,
        output wire [48:0] dout_leaf_18,
        output wire [48:0] dout_leaf_19,
        output wire [48:0] dout_leaf_20,
        output wire [48:0] dout_leaf_21,
        output wire [48:0] dout_leaf_22,
        output wire [48:0] dout_leaf_23);

        // UPDATE: page inst
        page_double_bb page2_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_2),
            .dout_leaf_interface2bft_0(dout_leaf_2),
            .resend_0(resend_2),
            .reset_400_0(ap_rst_n_inv_400_p2),
            .ap_start_0(ap_start_400_p2),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_3),
            .dout_leaf_interface2bft_1(dout_leaf_3),
            .resend_1(resend_3),
            .reset_400_1(ap_rst_n_inv_400_p3),
            .ap_start_1(ap_start_400_p3)
            );

        page_quad_bb page4_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_4),
            .dout_leaf_interface2bft_0(dout_leaf_4),
            .resend_0(resend_4),
            .reset_400_0(ap_rst_n_inv_400_p4),
            .ap_start_0(ap_start_400_p4),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_5),
            .dout_leaf_interface2bft_1(dout_leaf_5),
            .resend_1(resend_5),
            .reset_400_1(ap_rst_n_inv_400_p5),
            .ap_start_1(ap_start_400_p5),

            .clk_200_2(clk_200),
            .clk_250_2(clk_250),
            .clk_300_2(clk_300),
            .clk_350_2(clk_350),
            .clk_400_2(clk_400),
            .din_leaf_bft2interface_2(din_leaf_6),
            .dout_leaf_interface2bft_2(dout_leaf_6),
            .resend_2(resend_6),
            .reset_400_2(ap_rst_n_inv_400_p6),
            .ap_start_2(ap_start_400_p6),

            .clk_200_3(clk_200),
            .clk_250_3(clk_250),
            .clk_300_3(clk_300),
            .clk_350_3(clk_350),
            .clk_400_3(clk_400),
            .din_leaf_bft2interface_3(din_leaf_7),
            .dout_leaf_interface2bft_3(dout_leaf_7),
            .resend_3(resend_7),
            .reset_400_3(ap_rst_n_inv_400_p7),
            .ap_start_3(ap_start_400_p7)
            );    
            
        page_quad_bb page8_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_8),
            .dout_leaf_interface2bft_0(dout_leaf_8),
            .resend_0(resend_8),
            .reset_400_0(ap_rst_n_inv_400_p8),
            .ap_start_0(ap_start_400_p8),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_9),
            .dout_leaf_interface2bft_1(dout_leaf_9),
            .resend_1(resend_9),
            .reset_400_1(ap_rst_n_inv_400_p9),
            .ap_start_1(ap_start_400_p9),

            .clk_200_2(clk_200),
            .clk_250_2(clk_250),
            .clk_300_2(clk_300),
            .clk_350_2(clk_350),
            .clk_400_2(clk_400),
            .din_leaf_bft2interface_2(din_leaf_10),
            .dout_leaf_interface2bft_2(dout_leaf_10),
            .resend_2(resend_10),
            .reset_400_2(ap_rst_n_inv_400_p10),
            .ap_start_2(ap_start_400_p10),

            .clk_200_3(clk_200),
            .clk_250_3(clk_250),
            .clk_300_3(clk_300),
            .clk_350_3(clk_350),
            .clk_400_3(clk_400),
            .din_leaf_bft2interface_3(din_leaf_11),
            .dout_leaf_interface2bft_3(dout_leaf_11),
            .resend_3(resend_11),
            .reset_400_3(ap_rst_n_inv_400_p11),
            .ap_start_3(ap_start_400_p11)
            );


        page_quad_bb page12_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_12),
            .dout_leaf_interface2bft_0(dout_leaf_12),
            .resend_0(resend_12),
            .reset_400_0(ap_rst_n_inv_400_p12),
            .ap_start_0(ap_start_400_p12),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_13),
            .dout_leaf_interface2bft_1(dout_leaf_13),
            .resend_1(resend_13),
            .reset_400_1(ap_rst_n_inv_400_p13),
            .ap_start_1(ap_start_400_p13),

            .clk_200_2(clk_200),
            .clk_250_2(clk_250),
            .clk_300_2(clk_300),
            .clk_350_2(clk_350),
            .clk_400_2(clk_400),
            .din_leaf_bft2interface_2(din_leaf_14),
            .dout_leaf_interface2bft_2(dout_leaf_14),
            .resend_2(resend_14),
            .reset_400_2(ap_rst_n_inv_400_p14),
            .ap_start_2(ap_start_400_p14),

            .clk_200_3(clk_200),
            .clk_250_3(clk_250),
            .clk_300_3(clk_300),
            .clk_350_3(clk_350),
            .clk_400_3(clk_400),
            .din_leaf_bft2interface_3(din_leaf_15),
            .dout_leaf_interface2bft_3(dout_leaf_15),
            .resend_3(resend_15),
            .reset_400_3(ap_rst_n_inv_400_p15),
            .ap_start_3(ap_start_400_p15)
            );

            
        page_quad_bb page16_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_16),
            .dout_leaf_interface2bft_0(dout_leaf_16),
            .resend_0(resend_16),
            .reset_400_0(ap_rst_n_inv_400_p16),
            .ap_start_0(ap_start_400_p16),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_17),
            .dout_leaf_interface2bft_1(dout_leaf_17),
            .resend_1(resend_17),
            .reset_400_1(ap_rst_n_inv_400_p17),
            .ap_start_1(ap_start_400_p17),

            .clk_200_2(clk_200),
            .clk_250_2(clk_250),
            .clk_300_2(clk_300),
            .clk_350_2(clk_350),
            .clk_400_2(clk_400),
            .din_leaf_bft2interface_2(din_leaf_18),
            .dout_leaf_interface2bft_2(dout_leaf_18),
            .resend_2(resend_18),
            .reset_400_2(ap_rst_n_inv_400_p18),
            .ap_start_2(ap_start_400_p18),

            .clk_200_3(clk_200),
            .clk_250_3(clk_250),
            .clk_300_3(clk_300),
            .clk_350_3(clk_350),
            .clk_400_3(clk_400),
            .din_leaf_bft2interface_3(din_leaf_19),
            .dout_leaf_interface2bft_3(dout_leaf_19),
            .resend_3(resend_19),
            .reset_400_3(ap_rst_n_inv_400_p19),
            .ap_start_3(ap_start_400_p19)
            );

        page_quad_bb page20_inst(
            .clk_200_0(clk_200),
            .clk_250_0(clk_250),
            .clk_300_0(clk_300),
            .clk_350_0(clk_350),
            .clk_400_0(clk_400),
            .din_leaf_bft2interface_0(din_leaf_20),
            .dout_leaf_interface2bft_0(dout_leaf_20),
            .resend_0(resend_20),
            .reset_400_0(ap_rst_n_inv_400_p20),
            .ap_start_0(ap_start_400_p20),

            .clk_200_1(clk_200),
            .clk_250_1(clk_250),
            .clk_300_1(clk_300),
            .clk_350_1(clk_350),
            .clk_400_1(clk_400),
            .din_leaf_bft2interface_1(din_leaf_21),
            .dout_leaf_interface2bft_1(dout_leaf_21),
            .resend_1(resend_21),
            .reset_400_1(ap_rst_n_inv_400_p21),
            .ap_start_1(ap_start_400_p21),

            .clk_200_2(clk_200),
            .clk_250_2(clk_250),
            .clk_300_2(clk_300),
            .clk_350_2(clk_350),
            .clk_400_2(clk_400),
            .din_leaf_bft2interface_2(din_leaf_22),
            .dout_leaf_interface2bft_2(dout_leaf_22),
            .resend_2(resend_22),
            .reset_400_2(ap_rst_n_inv_400_p22),
            .ap_start_2(ap_start_400_p22),

            .clk_200_3(clk_200),
            .clk_250_3(clk_250),
            .clk_300_3(clk_300),
            .clk_350_3(clk_350),
            .clk_400_3(clk_400),
            .din_leaf_bft2interface_3(din_leaf_23),
            .dout_leaf_interface2bft_3(dout_leaf_23),
            .resend_3(resend_23),
            .reset_400_3(ap_rst_n_inv_400_p23),
            .ap_start_3(ap_start_400_p23)

            );

endmodule