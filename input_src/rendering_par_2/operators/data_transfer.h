void data_transfer (
		hls::stream<ap_uint<512> > & Input_1,
		hls::stream<ap_uint<128> > & Output_1
		);
#pragma map_target = HW