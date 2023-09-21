#include "../host/typedefs.h"
#include "../operators/data_transfer.h"
#include "../operators/layer_0.h"
#include "../operators/layer_1.h"
#include "../operators/layer_2.h"
#include "../operators/layer_3.h"
#include "../operators/layer_4.h"
#include "../operators/layer_5.h"
#include "../operators/layer_last.h"
#include "../operators/out_data_collect.h"


void top(hls::stream<ap_uint<512> > & Input_1, hls::stream<ap_uint<512> > & Output_1)
{
#pragma HLS INTERFACE ap_hs port=Input_1
#pragma HLS INTERFACE ap_hs port=Output_1


    hls::stream<ap_uint<8>> data_transfer_OUT_1("data_transfer_OUT_1");
#pragma HLS STREAM variable=data_transfer_OUT_1 depth=32

    hls::stream<ap_uint<8>> layer_0_OUT_1("layer_0_OUT_1");
#pragma HLS STREAM variable=layer_0_OUT_1 depth=32


    std::cout << "Data transfer start" << std::endl;
    data_transfer(Input_1, Output_1);

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
