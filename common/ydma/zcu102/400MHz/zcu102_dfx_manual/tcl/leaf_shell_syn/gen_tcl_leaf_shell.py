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

            filedata =  "set top_name leaf_i"  + str(num_input) + 'o' + str(num_output) + "\n"
            filedata += 'set dir "./src4level2/leaf_shell/leaf_interface_src/"\n'
            filedata += 'set contents [glob -nocomplain -directory $dir *]\n'
            filedata += 'foreach item $contents {\n'
            filedata += '  add_files -norecurse $item\n'
            filedata += '}\n'

            filedata += "add_files ./src4level2/leaf_shell/" + str(clk_user) + "MHz/$top_name.v\n"
            filedata += "set_param general.maxThreads 8\n"
            filedata += "set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]\n"
            filedata += "synth_design -top $top_name -part xczu9eg-ffvb1156-2-e -mode out_of_context\n"
            filedata += "write_checkpoint -force ./overlay_p23/leaf_shell/" + str(clk_user) + "MHz/$top_name.dcp\n"
            filedata += "report_utilization -hierarchical > ./overlay_p23/leaf_shell/" + str(clk_user) + "MHz/util_$top_name.rpt\n"

            filename = "./" + str(clk_user) + 'MHz/syn_leaf_i' + str(num_input) + 'o' + str(num_output) + '.tcl'
            with open(filename, "w") as outfile:
                outfile.write(filedata)