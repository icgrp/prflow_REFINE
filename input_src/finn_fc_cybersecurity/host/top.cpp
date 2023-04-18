#include "../host/typedefs.h"
#include "../operators/data_transfer.h"
#include "../operators/mva_0.h"
#include "../operators/mva_1.h"
#include "../operators/mva_2.h"
#include "../operators/mva_3.h"
#include "../operators/str_dwc_0.h"
#include "../operators/str_dwc_1.h"
#include "../operators/out_data_collect.h"


void top(hls::stream<ap_uint<512> > & Input_1, hls::stream<ap_uint<512> > & Output_1)
{
#pragma HLS INTERFACE ap_hs port=Input_1
#pragma HLS INTERFACE ap_hs port=Output_1


    hls::stream<ap_uint<32> > data_transfer_OUT_1("data_transfer_OUT_1");
#pragma HLS STREAM variable=data_transfer_OUT_1 depth=32
    hls::stream<ap_uint<32> > mva_0_OUT_1("mva_0_OUT_1");
#pragma HLS STREAM variable=mva_0_OUT_1 depth=32
    hls::stream<ap_uint<128> > str_dwc_0_OUT_1("str_dwc_0_OUT_1");
#pragma HLS STREAM variable=str_dwc_0_OUT_1 depth=32
    hls::stream<ap_uint<2> > mva_1_OUT_1("mva_1_OUT_1");
#pragma HLS STREAM variable=mva_1_OUT_1 depth=32
    hls::stream<ap_uint<128> > str_dwc_1_OUT_1("str_dwc_1_OUT_1");
#pragma HLS STREAM variable=str_dwc_1_OUT_1 depth=32
    hls::stream<ap_uint<2> > mva_2_OUT_1("mva_2_OUT_1");
#pragma HLS STREAM variable=mva_2_OUT_1 depth=32
    hls::stream<ap_uint<1> > mva_3_OUT_1("mva_3_OUT_1");
#pragma HLS STREAM variable=mva_3_OUT_1 depth=32


    std::cout << "Data transfer start" << std::endl;
    data_transfer(Input_1, data_transfer_OUT_1);

    for (int i = 0; i<1000; i++){
        std::cout << "Layer 0 start" << std::endl;
        mva_0(data_transfer_OUT_1, mva_0_OUT_1);
        str_dwc_0(mva_0_OUT_1, str_dwc_0_OUT_1);

        std::cout << "Layer 1 start" << std::endl;
        mva_1(str_dwc_0_OUT_1, mva_1_OUT_1);
        str_dwc_1(mva_1_OUT_1, str_dwc_1_OUT_1);

        std::cout << "Layer 2 start" << std::endl;
        mva_2(str_dwc_1_OUT_1, mva_2_OUT_1);

        std::cout << "Layer 3 start" << std::endl;
        mva_3(mva_2_OUT_1, mva_3_OUT_1);        
    }

    std::cout << "Output collect start" << std::endl;
    out_data_collect(mva_3_OUT_1, Output_1);

}

extern "C" {
    void ydma (
            bit64 * input1,
            bit512 * input2,
            bit64 * output1,
            bit512 * output2,
            int config_size,
            int input_size,
            int output_size
            )
    {
#pragma HLS INTERFACE m_axi port=input1 bundle=aximm1
#pragma HLS INTERFACE m_axi port=input2 bundle=aximm2
#pragma HLS INTERFACE m_axi port=output1 bundle=aximm1
#pragma HLS INTERFACE m_axi port=output2 bundle=aximm2

#pragma HLS DATAFLOW

        bit64 v1_buffer[256];   // Local memory to store vector1
        //hls::stream< unsigned int > v1_buffer;
        #pragma HLS STREAM variable=v1_buffer depth=256

        hls::stream<ap_uint<512> > Input_1("Input_1_str");
        hls::stream<ap_uint<512> > Output_1("Output_str");

        for(int i=0; i<config_size; i++){ 
            v1_buffer[i] = input1[i]; 
            //printf("input1[%d]\n", i);
        }

        for(int i=0; i<config_size; i++){ output1[i] = v1_buffer[i]; }

        for(int i=0; i<input_size;  i++){
            bit512 in_tmp = input2[i];
            Input_1.write(in_tmp);
        }
      
        top(Input_1, Output_1);

        for(int i=0; i<output_size; i++){
            bit512 out_tmp;
            out_tmp = Output_1.read();
            output2[i] = out_tmp;
        }    
    }
}



// void top_top (
//         bit512 * input2,
//         bit512 * output2
//         )
// {
// #pragma HLS DATAFLOW

//       hls::stream<ap_uint<512> > Input_1("Input_1_str");
//       hls::stream<ap_uint<512> > Output_1("Output_str");

//   for(int i=0; i<INPUT_SIZE;  i++){
//             bit512 in_tmp = input2[i];
//             Input_1.write(in_tmp);
//       }
  
//       top(Input_1, Output_1);
 
//       for(int i=0; i<32; i++){
//           bit512 out_tmp;
//       out_tmp = Output_1.read();
//       output2[i] = out_tmp;
//       }
// }


