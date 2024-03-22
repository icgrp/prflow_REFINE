void output_collect(
 hls::stream<ap_uint<64> > & Input_1,
 hls::stream<ap_uint<64> > & Input_2,
 hls::stream<ap_uint<64> > & Input_3,
 hls::stream<ap_uint<64> > & Input_4,
 hls::stream<ap_uint<256> > & Output_1
);
#pragma map_target = HW