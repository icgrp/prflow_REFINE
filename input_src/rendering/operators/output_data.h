void output_data (
    hls::stream<ap_uint<128>> & Input_1,
    hls::stream<ap_uint<128>> & Input_2,
    hls::stream<ap_uint<128>> & Input_3,
    hls::stream<ap_uint<128>> & Input_4,
    hls::stream<ap_uint<512>> & Output_1
    );
#pragma map_target = HW