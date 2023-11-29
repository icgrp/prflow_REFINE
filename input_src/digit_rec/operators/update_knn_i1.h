void update_knn_i1(
    hls::stream<ap_uint<256>> & Input_1,
    hls::stream<ap_uint<32>> & Output_1
    );
#pragma map_target = HW