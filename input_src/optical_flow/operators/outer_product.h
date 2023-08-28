void outer_product(
    hls::stream<ap_uint<32>> &Input_1,
    hls::stream<ap_uint<32>> &Input_2,
    hls::stream<ap_uint<32>> &Input_3,
    hls::stream<ap_uint<96>> &Output_1,
    hls::stream<ap_uint<96>> &Output_2
    );
#pragma map_target = HW