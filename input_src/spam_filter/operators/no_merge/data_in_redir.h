void data_in_redir(
	hls::stream<ap_uint<256> > & Input_1,
	hls::stream<ap_uint<64> > & Output_1,
	hls::stream<ap_uint<64> > & Output_2
	);

#pragma map_target = HW