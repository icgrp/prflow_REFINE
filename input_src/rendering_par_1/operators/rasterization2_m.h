void rasterization2_m (
		hls::stream<ap_uint<32> > & Input_1,
		hls::stream<ap_uint<32> > & Output_1
		);
#pragma map_target = HW inst_mem_size = 65536
#pragma HLS_PR=1 clb =4 ff = 1 bram =2.4 dsp =1.2
  //#pragma HLS_PR=1 clb =8 bram =8.4 dsp =8.2




