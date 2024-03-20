void data_2_1(
	hls::stream<ap_uint<32> > & Input_1,
	hls::stream<ap_uint<32> > & Input_2,
	hls::stream<ap_uint<256> > & Output_1
	);
#pragma map_target = HW