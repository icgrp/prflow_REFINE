import os
# clk_user = 200
# num_input = 4
# num_output = 1
clk_user_list = [200,250,300,350,400]
num_input_list = [1,2,3,4,5,6,7]
num_output_list = [1,2,3,4,5,6,7]


for clk_user in clk_user_list:
    os.system("mkdir -p " + str(clk_user) + "MHz")
    for num_input in num_input_list:
        for num_output in num_output_list:

            filedata =  "`timescale 1ns / 1ps\n"
            filedata += "module leaf_i"  + str(num_input) + 'o' + str(num_output) + "(\n"
            filedata += "    input wire clk_200,\n"
            filedata += "    input wire clk_250,\n"
            filedata += "    input wire clk_300,\n"
            filedata += "    input wire clk_350,\n"
            filedata += "    input wire clk_400,\n"
            filedata += "    input wire [49-1 : 0] din_leaf_bft2interface,\n"
            filedata += "    output wire [49-1 : 0] dout_leaf_interface2bft,\n"
            filedata += "    input wire resend,\n"
            filedata += "    input wire reset_400,\n"
            filedata += "    input wire ap_start\n"
            filedata += "    );\n"
            filedata += "\n"
            filedata += "    wire ap_start_user;\n"
            filedata += "    wire [32-1 :0] "
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "dout_leaf_interface2user_" + str(i) + ";\n"
                else: 
                    filedata += "dout_leaf_interface2user_" + str(i) + ", "

            filedata += "    wire "
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "vld_interface2user_" + str(i) + ";\n"
                else: 
                    filedata += "vld_interface2user_" + str(i) + ", "

            filedata += "    wire "
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "ack_user2interface_" + str(i) + ";\n"
                else: 
                    filedata += "ack_user2interface_" + str(i) + ", "
            filedata += "\n"


            filedata += "    wire [32-1 :0] "
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "din_leaf_user2interface_" + str(i) + ";\n"
                else: 
                    filedata += "din_leaf_user2interface_" + str(i) + ", "

            filedata += "    wire "
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "vld_user2interface_" + str(i) + ";\n"
                else: 
                    filedata += "vld_user2interface_" + str(i) + ", "

            filedata += "    wire "
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "ack_interface2user_" + str(i) + ";\n"
                else: 
                    filedata += "ack_interface2user_" + str(i) + ", "
            filedata += "\n"


            filedata += "    wire clk_user;\n"
            filedata += "    assign clk_user = clk_" + str(clk_user) + ";\n"
            filedata += "    wire reset_ap_start_user;\n"
            filedata += "\n"

            filedata += "    wire [48:0] dout_leaf_interface2bft_tmp;\n"
            filedata += "    assign dout_leaf_interface2bft = resend ? 0 : dout_leaf_interface2bft_tmp;\n"
            filedata += "\n"

            filedata += "    leaf_interface #(\n"
            filedata += "        .PACKET_BITS(49),\n"
            filedata += "        .PAYLOAD_BITS(32),\n"
            filedata += "        .NUM_LEAF_BITS(5),\n"
            filedata += "        .NUM_PORT_BITS(4),\n"
            filedata += "        .NUM_ADDR_BITS(7),\n"

            filedata += "        .NUM_IN_PORTS(" + str(num_input) + "),\n"
            filedata += "        .NUM_OUT_PORTS(" + str(num_output) + "),\n"

            filedata += "        .NUM_BRAM_ADDR_BITS(7),\n"
            filedata += "        .FREESPACE_UPDATE_SIZE(64)\n"
            filedata += "    )leaf_interface_inst(\n"
            filedata += "        .clk(clk_400),\n"
            filedata += "        .clk_user(clk_user),\n"
            filedata += "        .reset(reset_400),\n"
            filedata += "        .din_leaf_bft2interface(din_leaf_bft2interface),\n"
            filedata += "        .dout_leaf_interface2bft(dout_leaf_interface2bft_tmp),\n"
            filedata += "        .ap_start_user(ap_start_user), // not used\n"
            filedata += "        .resend(resend),\n"
            filedata += "\n"

            filedata += "        .dout_leaf_interface2user({"
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "dout_leaf_interface2user_" + str(i) + "}),\n"
                else: 
                    filedata += "dout_leaf_interface2user_" + str(i) + ","

            filedata += "        .vld_interface2user({"
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "vld_interface2user_" + str(i) + "}),\n"
                else: 
                    filedata += "vld_interface2user_" + str(i) + ","

            filedata += "        .ack_user2interface({"
            for i in range(num_input,0,-1):
                if i == 1:
                    filedata += "ack_user2interface_" + str(i) + "}),\n"
                else: 
                    filedata += "ack_user2interface_" + str(i) + ","



            filedata += "        .ack_interface2user({"
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "ack_interface2user_" + str(i) + "}),\n"
                else: 
                    filedata += "ack_interface2user_" + str(i) + ","

            filedata += "        .vld_user2interface({"
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "vld_user2interface_" + str(i) + "}),\n"
                else: 
                    filedata += "vld_user2interface_" + str(i) + ","

            filedata += "        .din_leaf_user2interface({"
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "din_leaf_user2interface_" + str(i) + "}),\n"
                else: 
                    filedata += "din_leaf_user2interface_" + str(i) + ","

            filedata += "\n"
            filedata += "        .ap_start(ap_start),\n"
            filedata += "        .reset_ap_start_user(reset_ap_start_user)\n"
            filedata += "    );\n"
            filedata += "\n"


            filedata += "    user_kernel_bb user_kernel_inst( \n"
            filedata += "        .clk_user(clk_" + str(clk_user) + "),\n"
            filedata += "        .reset(reset_ap_start_user),\n"

            for i in range(num_input,0,-1):
                filedata += "        .dout_leaf_interface2user_" + str(i) + "(dout_leaf_interface2user_" + str(i) + "),\n"
            for i in range(num_input,0,-1):
                filedata += "        .vld_interface2user_" + str(i) + "(vld_interface2user_" + str(i) + "),\n"
            for i in range(num_input,0,-1):
                filedata += "        .ack_user2interface_" + str(i) + "(ack_user2interface_" + str(i) + "),\n"

            filedata += "\n"
            for i in range(num_output,0,-1):
                filedata += "        .din_leaf_user2interface_" + str(i) + "(din_leaf_user2interface_" + str(i) + "),\n"
            for i in range(num_output,0,-1):
                filedata += "        .vld_user2interface_" + str(i) + "(vld_user2interface_" + str(i) + "),\n"
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "        .ack_interface2user_" + str(i) + "(ack_interface2user_" + str(i) + ")\n"
                else:
                    filedata += "        .ack_interface2user_" + str(i) + "(ack_interface2user_" + str(i) + "),\n"
            filedata += "        );\n"
            filedata += "\n"
            filedata += "endmodule\n"

            filedata += "\n"
            filedata += "module user_kernel_bb(\n"
            filedata += "    input wire clk_user,\n"
            filedata += "    input wire reset,\n"
            for i in range(num_input,0,-1):
                filedata += "    input wire [32-1:0] dout_leaf_interface2user_" + str(i) + ",\n"
            for i in range(num_input,0,-1):
                filedata += "    input wire vld_interface2user_" + str(i) +  ",\n"
            for i in range(num_input,0,-1):
                filedata += "    output wire ack_user2interface_" + str(i) +  ",\n"
            filedata += "\n"

            for i in range(num_output,0,-1):
                filedata += "    output wire [32-1:0] din_leaf_user2interface_" + str(i) + ",\n"
            for i in range(num_output,0,-1):
                filedata += "    output wire vld_user2interface_" + str(i) +  ",\n"
            for i in range(num_output,0,-1):
                if i == 1:
                    filedata += "    input wire ack_interface2user_" + str(i) +  "\n"
                else:
                    filedata += "    input wire ack_interface2user_" + str(i) +  ",\n"
            filedata += "    );\n"
            filedata += "\n"
            filedata += "endmodule\n"


            filename = "./" + str(clk_user) + 'MHz/leaf_i' + str(num_input) + 'o' + str(num_output) + '.v'
            with open(filename, "w") as outfile:
                outfile.write(filedata)