/**********
Copyright (c) 2018, Xilinx, Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.  3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software
without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
**********/

#define CL_HPP_CL_1_2_DEFAULT_BUILD
#define CL_HPP_TARGET_OPENCL_VERSION 120
#define CL_HPP_MINIMUM_OPENCL_VERSION 120
#define CL_HPP_ENABLE_PROGRAM_CONSTRUCTION_FROM_ARRAY_COMPATIBILITY 1
#define CL_USE_DEPRECATED_OPENCL_1_2_APIS



#include <vector>
#include <unistd.h>
#include <iostream>
#include <fstream>
#include <CL/cl2.hpp>
#include "typedefs.h"
#include "test_data.h"
#include <sys/time.h>
#include <numeric>


using namespace std;

#define CONFIG_SIZE 16
#define NUM_TESTS 9600
#define BATCH_SIZE 640
#define NUM_BATCHES NUM_TESTS/BATCH_SIZE

// 64 uint8 data in 512bit, so divide it by 64, 
#define INPUT_SIZE BATCH_SIZE*32*32*3/64
// 64 uint8 output in 512bit, so divide it by 64
#define OUTPUT_SIZE 10

// Forward declaration of utility functions included at the end of this file
std::vector<cl::Device> get_xilinx_devices();
char *read_binary_file(const std::string &xclbin_file_name, unsigned &nb);

// ------------------------------------------------------------------------------------
// Main program
// ------------------------------------------------------------------------------------
int main(int argc, char **argv)
{
    //TARGET_DEVICE macro needs to be passed from gcc command line
    if (argc < 2)
    {
        std::cout << "Usage: " << argv[0] << " <xclbin>" << std::endl;
        return EXIT_FAILURE;
    }

    // Variables for time measurement
    struct timeval start, end;

    std::vector<cl::Device> devices;
    cl::Device device;
    std::vector<cl::Platform> platforms;
    bool found_device = false;

    //traversing all Platforms To find Xilinx Platform and targeted
    //Device in Xilinx Platform
    cl::Platform::get(&platforms);
    for (size_t i = 0; (i < platforms.size()) & (found_device == false); i++)
    {
        cl::Platform platform = platforms[i];
        std::string platformName = platform.getInfo<CL_PLATFORM_NAME>();
        if (platformName == "Xilinx")
        {
            devices.clear();
            platform.getDevices(CL_DEVICE_TYPE_ACCELERATOR, &devices);
            if (devices.size())
            {
                device = devices[0];
                found_device = true;
                break;
            }
        }
    }
    if (found_device == false)
    {
        std::cout << "Error: Unable to find Target Device "
                  << device.getInfo<CL_DEVICE_NAME>() << std::endl;
        return EXIT_FAILURE;
    }

    // Creating Context and Command Queue for selected device
    cl::Context context(device);

    // Load xclbin
    for (int i = 1; i < argc; i++)
    {
        char *xclbinFilename = argv[i];
        std::cout << "Loading: '" << xclbinFilename << "'\n";
        std::ifstream bin_file(xclbinFilename, std::ifstream::binary);
        bin_file.seekg(0, bin_file.end);
        unsigned nb = bin_file.tellg();
        bin_file.seekg(0, bin_file.beg);
        char *buf = new char[nb];
        bin_file.read(buf, nb);

        // Creating Program from Binary File
        cl::Program::Binaries bins;
        bins.push_back({buf, nb});
        devices.resize(1);
        cl::Program program(context, devices, bins);
    }
    std::cout << "Done!" << std::endl;

    // ------------------------------------------------------------------------------------
    // Step 1: Initialize the OpenCL environment
    // ------------------------------------------------------------------------------------
    cl_int err;
    std::string binaryFile = (argc == 1) ? "ydma.xclbin" : argv[argc-1];
    unsigned fileBufSize;
    devices.resize(1);
    //cl::Context context(device, NULL, NULL, NULL, &err);
    char *fileBuf = read_binary_file(binaryFile, fileBufSize);
    cl::Program::Binaries bins{{fileBuf, fileBufSize}};
    cl::Program program(context, devices, bins, NULL, &err);
    cl::CommandQueue q(context, device, CL_QUEUE_PROFILING_ENABLE, &err);
    cl::Kernel krnl_ydma(program, "ydma", &err);

    // ------------------------------------------------------------------------------------
    // Step 2: Create buffers and initialize test values
    // ------------------------------------------------------------------------------------
    // Create the buffers and allocate memory
    cl::Buffer in1_buf(context, CL_MEM_READ_ONLY, sizeof(bit64) * CONFIG_SIZE, NULL, &err);

    cl::Buffer in2_buf[NUM_BATCHES];
    for (int i = 0; i < NUM_BATCHES; i++){
        in2_buf[i] = cl::Buffer(context, CL_MEM_READ_ONLY, sizeof(bit512) * INPUT_SIZE, NULL, &err);
    }

    cl::Buffer out1_buf(context, CL_MEM_WRITE_ONLY, sizeof(bit64) * CONFIG_SIZE, NULL, &err);

    cl::Buffer out2_buf[NUM_BATCHES];
    for (int i = 0; i < NUM_BATCHES; i++){
        out2_buf[i] = cl::Buffer(context, CL_MEM_WRITE_ONLY, sizeof(bit512) * OUTPUT_SIZE, NULL, &err);
    }


    // Map host-side buffer memory to user-space pointers
    bit64 *in1 = (bit64 *)q.enqueueMapBuffer(in1_buf, CL_TRUE, CL_MAP_WRITE, 0, sizeof(bit64) * CONFIG_SIZE);
    // bit512 *in2 = (bit512 *)q.enqueueMapBuffer(in2_buf, CL_TRUE, CL_MAP_WRITE, 0, sizeof(bit512) * INPUT_SIZE);

    bit512 *in2[NUM_BATCHES];
    for (int i = 0; i < NUM_BATCHES; i++){
        in2[i] = (bit512 *)q.enqueueMapBuffer(in2_buf[i], CL_TRUE, CL_MAP_WRITE, 0, sizeof(bit512) * INPUT_SIZE);
    }

    bit64 *out1 = (bit64 *)q.enqueueMapBuffer(out1_buf, CL_TRUE, CL_MAP_WRITE | CL_MAP_READ, 0, sizeof(bit64) * CONFIG_SIZE);
    // bit512 *out2 = (bit512 *)q.enqueueMapBuffer(out2_buf, CL_TRUE, CL_MAP_WRITE | CL_MAP_READ, 0, sizeof(bit512) * OUTPUT_SIZE);

    bit512 *out2[NUM_BATCHES];
    for (int i = 0; i < NUM_BATCHES; i++){
        out2[i] = (bit512 *)q.enqueueMapBuffer(out2_buf[i], CL_TRUE, CL_MAP_WRITE | CL_MAP_READ, 0, sizeof(bit512) * OUTPUT_SIZE);
    }



    // Initialize the vectors used in the test
    // pack input data for better performance

    in1[0].range(63, 32) = 0x00000000;
    in1[0].range(31,  0) = 0x00000000;

    in1[1].range(63, 32) = 0x00000000;
    in1[1].range(31,  0) = INPUT_SIZE;

    // configure packets



    std::cout << "Init input data " << std::endl;
    // Prepare input data for this batch
    for (int i = 0; i < NUM_BATCHES; i++){
        std::cout << "Init input data - Batch idx: " << i << std::endl;
        for (int j = 0; j < INPUT_SIZE; j++){
            for (int k = 0; k < 64; k++){
                in2[i][j](8*k+7, 8*k+0) = test_data[INPUT_SIZE*64*i + 64*j + k]; // The first data is the lowest bits
            }
        }
    }


    int mismatch = 0;

    std::cout << "Start Processing" << std::endl;
    std::vector<long long> elapsed_vector;

    for (int i = 0; i < NUM_BATCHES; i++){
        gettimeofday(&start, NULL);
        // ------------------------------------------------------------------------------------
        // Step 3: Run the kernel
        // ------------------------------------------------------------------------------------
        // Set kernel arguments

        krnl_ydma.setArg(0, in1_buf);
        krnl_ydma.setArg(1, in2_buf[i]);
        krnl_ydma.setArg(2, out1_buf);
        krnl_ydma.setArg(3, out2_buf[i]);
        krnl_ydma.setArg(4, CONFIG_SIZE);
        krnl_ydma.setArg(5, INPUT_SIZE);
        krnl_ydma.setArg(6, OUTPUT_SIZE);

        // Schedule transfer of inputs to device memory, execution of kernel, and transfer of outputs back to host memory
        if(i == 0){
            q.enqueueMigrateMemObjects({in1_buf, in2_buf[i]}, 0 /* 0 means from host*/);
        }
        else{
            q.enqueueMigrateMemObjects({in2_buf[i]}, 0 /* 0 means from host*/);            
        }
        q.enqueueTask(krnl_ydma);

        if(i == 0){
            q.enqueueMigrateMemObjects({out1_buf, out2_buf[i]}, CL_MIGRATE_MEM_OBJECT_HOST);
        }
        else{
            q.enqueueMigrateMemObjects({out2_buf[i]}, CL_MIGRATE_MEM_OBJECT_HOST);
        }

        // Wait for all scheduled operations to finish
        q.finish();

        gettimeofday(&end, NULL);
        // ------------------------------------------------------------------------------------
        // Step 4: Check Results and Release Allocated Resources
        // ------------------------------------------------------------------------------------
        long long elapsed = (end.tv_sec - start.tv_sec) * 1000000LL + end.tv_usec - start.tv_usec;   
        printf("elapsed time: %lld us\n", elapsed);
        elapsed_vector.push_back(elapsed);

        for (int j = 0; j < OUTPUT_SIZE; j++){
            for (int k = 0; k < 64; k++){
                uint8_t result_8bit = out2[i][j](8*k+7, 8*k);
                uint8_t expected_8bit = expected_labels[BATCH_SIZE*i + 64*j + k];
                // std::cout << "expected_8bit: " << expected_8bit << std::endl;

                if((int)result_8bit != (int)expected_8bit){
                    // std::cout << "expected_8bit: " << (int)expected_8bit << std::endl;
                    // std::cout << "result_8bit: " << (int)result_8bit << std::endl;
                    mismatch++;
                }
            }
        }
        std::cout << "mismatch so far: " << mismatch << std::endl;
    }

    std::cout << "num of mismatch: " << mismatch << std::endl;
    std::cout << "Accuracy = " << float(NUM_TESTS - mismatch) / NUM_TESTS << std::endl;
    long long elapsed_sum = std::accumulate(elapsed_vector.begin(), elapsed_vector.end(), 0.0);
    printf("avg elapsed time: %lld us\n", elapsed_sum/elapsed_vector.size());

    std::ofstream outfile;
    outfile.open("result-finn_cnn_ciar10.txt", std::ios_base::app);
    outfile << "avg elapsed time: " << elapsed_sum/elapsed_vector.size() << "us\n";
    outfile << "accuracy: " << float(NUM_TESTS - mismatch) / NUM_TESTS << "\n";

    return EXIT_SUCCESS;
}

// ------------------------------------------------------------------------------------
// Utility functions
// ------------------------------------------------------------------------------------
std::vector<cl::Device> get_xilinx_devices()
{
    size_t i;
    cl_int err;
    std::vector<cl::Platform> platforms;
    err = cl::Platform::get(&platforms);
    cl::Platform platform;
    for (i = 0; i < platforms.size(); i++)
    {
        platform = platforms[i];
        std::string platformName = platform.getInfo<CL_PLATFORM_NAME>(&err);
        if (platformName == "Xilinx")
        {
            std::cout << "INFO: Found Xilinx Platform" << std::endl;
            break;
        }
    }
    if (i == platforms.size())
    {
        std::cout << "ERROR: Failed to find Xilinx platform" << std::endl;
        exit(EXIT_FAILURE);
    }

    //Getting ACCELERATOR Devices and selecting 1st such device
    std::vector<cl::Device> devices;
    err = platform.getDevices(CL_DEVICE_TYPE_ACCELERATOR, &devices);
    return devices;
}

char *read_binary_file(const std::string &xclbin_file_name, unsigned &nb)
{
    if (access(xclbin_file_name.c_str(), R_OK) != 0)
    {
        printf("ERROR: %s xclbin not available please build\n", xclbin_file_name.c_str());
        exit(EXIT_FAILURE);
    }
    //Loading XCL Bin into char buffer
    std::cout << "INFO: Loading '" << xclbin_file_name << "'\n";
    std::ifstream bin_file(xclbin_file_name.c_str(), std::ifstream::binary);
    bin_file.seekg(0, bin_file.end);
    nb = bin_file.tellg();
    bin_file.seekg(0, bin_file.beg);
    char *buf = new char[nb];
    bin_file.read(buf, nb);
    return buf;
}