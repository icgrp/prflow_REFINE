#include "typedefs.h"

// ydma.cpp for NoC-based overlay generation
extern "C" {
	void ydma(
			bit64 * input1,
			bit512 * input2,
			bit64 * output1,
			bit512 * output2,
			int config_size,
			int input_size,
			int output_size,
			int num_total_cnt // will be calculated in runtime.py and overwrite host.cpp
	)
	{
#pragma HLS INTERFACE m_axi port=input1 bundle=aximm1
#pragma HLS INTERFACE m_axi port=input2 bundle=aximm2
#pragma HLS INTERFACE m_axi port=output1 bundle=aximm1
#pragma HLS INTERFACE m_axi port=output2 bundle=aximm2


	    bit64 v1_buffer[512];   // Local memory to store vector1
		#pragma HLS STREAM variable=v1_buffer depth=512

	    bit512 v2_buffer[1024];   // Local memory to store vector2
		#pragma HLS STREAM variable=v2_buffer depth=1024


#pragma HLS DATAFLOW

	    	for(int i=0; i<config_size; i++){ v1_buffer[i] = input1[i]; }
	    	for(int i=0; i<num_total_cnt; i++){ output1[i] = v1_buffer[i]; }


	    	for(int i=0; i<input_size;  i++){ v2_buffer[i] = input2[i]; }
	    	for(int i=0; i<output_size; i++){ output2[i] = v2_buffer[i]; }

	}
}


void data32to512(
		hls::stream< bit32 > & Input_1,
		hls::stream< bit512 > & Output_1
		)
{
#pragma HLS INTERFACE axis register_mode=both register port=Input_1
#pragma HLS INTERFACE axis register_mode=both register port=Output_1

	bit512 out_tmp;
	for(int i=0; i<16; i++){
#pragma HLS PIPELINE II=1
		out_tmp(i*32+31, i*32) = Input_1.read();
	}
	Output_1.write(out_tmp);
}


// config_parser for bottleneck identification ver.
// Function below should be the input of HLS to generate config_parser* HDL files
// then copied to ./common/ydma/zcu102/400MHz/zcu102_dfx_manual/src4level2/ydma_bb/
void config_parser(
		hls::stream< bit64 > & input1,
		hls::stream< bit512 > & input2,
		hls::stream< bool > & input3,
		hls::stream< bit64 > & output1,
		hls::stream< bit32 > & output2,
		hls::stream< bit32 > & output3,
		hls::stream< ap_uint<16> > & output4
)
{
#pragma HLS INTERFACE axis register_mode=both register port=input1
#pragma HLS INTERFACE axis register_mode=both register port=input2
#pragma HLS INTERFACE axis register_mode=both register port=input3
#pragma HLS INTERFACE axis register_mode=both register port=output1
#pragma HLS INTERFACE axis register_mode=both register port=output2
#pragma HLS INTERFACE axis register_mode=both register port=output3
#pragma HLS INTERFACE axis register_mode=both register port=output4

	bit64 v1_buffer[256];
	unsigned int config_num;
	unsigned int data_num;
	unsigned int num_ops;
	unsigned int output_size;
	ap_uint<16> num_total_cnt;

	config_num = input1.read();
	data_num = input1.read();
	num_ops = input1.read();
	output_size = input1.read();
	num_total_cnt = input1.read();

	// 1) Read the configuration packets
	for(int i=0; i<config_num; i++){
#pragma HLS PIPELINE II=1
		v1_buffer[i] = input1.read();
	}

	// 2) Send the configuration packets to the BFT
	for(int i=0; i<config_num; i++){
#pragma HLS PIPELINE II=1
		output1.write(v1_buffer[i]);
	}

	// 3) Send output_size, num_cnt_read to leaf_interface_1(DMA operator's)
	output3.write(output_size);
	output4.write(num_total_cnt);

	// 4) Transfer the data to the kernel
	for(int i=0; i<data_num; i++){
		bit512 in_tmp;
		in_tmp = input2.read();
		for(int j=0; j<16; j++){
#pragma HLS PIPELINE II=1
			output2.write(in_tmp(32*j+31, 32*j));
		}
	}

	// 5) Read the configuration packets for is_done mode (per operator)
	for(int i=0; i<num_ops; i++){
#pragma HLS PIPELINE II=1
		v1_buffer[i] = input1.read();
	}

//	bool is_done_detected = edge2pulse(is_done);
	bool is_done = input3.read();
	if(is_done){
		// 6) Send the configuration packets for is_done mode (per operator)
		for(int i=0; i<num_ops; i++){
#pragma HLS PIPELINE II=1
			output1.write(v1_buffer[i]);
		}
	}
}

/*
void config_parser(
		hls::stream< bit64 > & input1,
		hls::stream< bit512 > & input2,
		hls::stream< bit64 > & output1,
		hls::stream< bit32 > & output2,
		hls::stream< bit64 > & output3

		)
{
#pragma HLS INTERFACE axis register_mode=both register port=input1
#pragma HLS INTERFACE axis register_mode=both register port=input2
#pragma HLS INTERFACE axis register_mode=both register port=output1
#pragma HLS INTERFACE axis register_mode=both register port=output2
#pragma HLS INTERFACE axis register_mode=both register port=output3

	bit64 v1_buffer;
	unsigned int config_num;
	unsigned int data_num;

	v1_buffer = input1.read();
	config_num = v1_buffer(31, 0);
	v1_buffer = input1.read();
	data_num = v1_buffer(31, 0);

	output3.write(config_num);
	output3.write(data_num);
	// send the configuration packets to the BFT
	for(int i=0; i<config_num; i++){
//#pragma HLS PIPELINE II=1
		v1_buffer = input1.read();
		output1.write(v1_buffer);
		output3.write(v1_buffer);
	}

	// transfer the data to the kernel
	for(int i=0; i<data_num; i++){
		bit512 in_tmp;
		in_tmp = input2.read();
		for(int j=0; j<16; j++){
#pragma HLS PIPELINE II=1
			output2.write(in_tmp(32*j+31, 32*j));
		}
	}

}

void config_parser_bk(
		hls::stream< bit64 > & input1,
		hls::stream< bit512 > & input2,
		hls::stream< bit64 > & output1,
		hls::stream< bit32 > & output2,
		hls::stream< bit64 > & output3

		)
{
#pragma HLS INTERFACE axis register_mode=both register port=input1
#pragma HLS INTERFACE axis register_mode=both register port=input2
#pragma HLS INTERFACE axis register_mode=both register port=output1
#pragma HLS INTERFACE axis register_mode=both register port=output2
#pragma HLS INTERFACE axis register_mode=both register port=output3

	bit64 v1_buffer[256];
	unsigned int config_num;
	unsigned int data_num;

	config_num = input1.read();
	data_num = input1.read();


	// read the configuration packets
	for(int i=0; i<config_num; i++){
#pragma HLS PIPELINE II=1
		v1_buffer[i] = input1.read();
	}

	// send the configuration packets to the BFT
	for(int i=0; i<config_num; i++){
#pragma HLS PIPELINE II=1
		output1.write(v1_buffer[i]);
	}

	// send the configuration packets back to the host
	output3.write(config_num);
	output3.write(data_num);
	for(int i=0; i<config_num; i++){
#pragma HLS PIPELINE II=1
		output3.write(v1_buffer[i]);
	}

	// transfer the data to the kernel
	for(int i=0; i<data_num; i++){
		bit512 in_tmp;
		in_tmp = input2.read();
		for(int j=0; j<16; j++){
#pragma HLS PIPELINE II=1
			output2.write(in_tmp(32*j+31, 32*j));
		}
	}
}

void config_collector(
		hls::stream< bit64 > & input1,
		hls::stream< bit64 > & input2,
		hls::stream< bit64 > & output1
		)
{
#pragma HLS INTERFACE axis register_mode=both register port=input1
#pragma HLS INTERFACE axis register_mode=both register port=input2
#pragma HLS INTERFACE axis register_mode=both register port=output1

	bit64 v1_buffer[256];

	for(int i=0; i<10; i++){
#pragma HLS PIPELINE II=1
		v1_buffer[i] = input1.read();
	}

	for(int i=0; i<12; i++){
#pragma HLS PIPELINE II=1
		bit64 tmp;
		tmp = v1_buffer[i] + input2.read();
		output1.write(tmp);
	}

}
*/