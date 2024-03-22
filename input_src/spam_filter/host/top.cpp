data_in_redir(Input_1, Output_1_redir, Output_2_redir, Output_3_redir, Output_4_redir);
dotProduct_i1(Output_1_redir, Output_1_sigmoid, Output_1_dot_1, Output_2_dot_1);
dotProduct_i3(Output_2_redir, Output_2_sigmoid, Output_1_dot_3, Output_2_dot_3);
dotProduct_i5(Output_3_redir, Output_3_sigmoid, Output_1_dot_5, Output_2_dot_5);
dotProduct_i7(Output_4_redir, Output_4_sigmoid, Output_1_dot_7, Output_2_dot_7);
sigmoid(Output_1_dot_1, Output_1_dot_3, Output_1_dot_5, Output_1_dot_7, Output_1_sigmoid, Output_2_sigmoid, Output_3_sigmoid, Output_4_sigmoid);
output_collect(Output_2_dot_1, Output_2_dot_3, Output_2_dot_5, Output_2_dot_7, Output_1);