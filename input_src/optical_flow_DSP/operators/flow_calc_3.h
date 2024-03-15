void flow_calc_3(
    hls::stream< ap_uint<32> > &Input_1,
    hls::stream< ap_uint<32> > &Input_2,
    hls::stream< ap_uint<32> > &Input_3,
    hls::stream< ap_uint<256> > &Output_1);
#pragma map_target = HW
