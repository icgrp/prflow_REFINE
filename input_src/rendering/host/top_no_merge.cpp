prj_rast1(Input_1, prj_rast1_out_1);
rast2_i1(prj_rast1_out_1, rast2_i1_out_1);
zculling_i1(rast2_i1_out_1, zculling_i1_out);
coloringFB_i1(zculling_i1_out, coloringFB_i1_out);
output_data(coloringFB_i1_out, Output_1);