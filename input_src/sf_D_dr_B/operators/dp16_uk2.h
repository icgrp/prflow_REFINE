void dp16_uk2(
	hls::stream<ap_uint<64> > & Input_1,
	hls::stream<ap_uint<32> > & Input_2,
	hls::stream<ap_uint<32> > & Input_3,
	hls::stream<ap_uint<32> > & Output_1,
	hls::stream<ap_uint<32> > & Output_2,
	hls::stream<ap_uint<32> > & Output_3
	)
#pragma map_target = HW
