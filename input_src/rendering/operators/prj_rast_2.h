void prj_rast_2 (
    hls::stream<ap_uint<256>> & Input_1,
    hls::stream<ap_uint<32>> & Output_1,
    hls::stream<ap_uint<32>> & Output_2
    );
#pragma map_target = HW