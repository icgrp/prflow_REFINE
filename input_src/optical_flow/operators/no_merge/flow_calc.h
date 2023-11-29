void flow_calc(
    hls::stream<ap_uint<128>> &Input_1,
    hls::stream<ap_uint<256>> &Output_1
    );
#pragma map_target = HW