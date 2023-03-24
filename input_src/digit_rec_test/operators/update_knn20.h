void update_knn20(hls::stream<ap_uint<32> > & Input_1, hls::stream<ap_uint<512> > & Output_1);
#pragma map_target = HW page_num = 21 inst_mem_size = 65536

#pragma HLS_PR=1 clb =2 ff = 1 bram =1.1 dsp =1.2
#pragma Output_1_depth = 8
