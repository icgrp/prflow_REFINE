gradient_xyz_calc(Input_1, gradient_x, gradient_y, gradient_z);
gradient_weight_y(gradient_x, gradient_y, gradient_z, y_filtered_x, y_filtered_y, y_filtered_z);
gradient_weight_x(y_filtered_x, y_filtered_y, y_filtered_z, filtered_gradient_x, filtered_gradient_y, filtered_gradient_z);
outer_product(filtered_gradient_x, filtered_gradient_y, filtered_gradient_z, outer_product_out_1);
tensor_weight_y_i1(outer_product_out_1, tensor_weight_y_out_1);
tensor_weight_x_i1(tensor_weight_y_out_1, tensor_weight_x_out_1);
flow_calc(tensor_weight_x_out_1,  Output_1);