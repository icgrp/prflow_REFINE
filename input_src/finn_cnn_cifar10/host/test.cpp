#include <iostream>

const uint8_t expected_labels[64] = {
    #include "expected.dat"
};

int main(){

    for (int j = 0; j < 64; j++){

        // uint8_t result_8bit = out2[i](8*j+7, 8*j);
        uint8_t expected_8bit = expected_labels[j];
        std::cout << "expected_8bit: " << (int)expected_8bit << std::endl;

        // if(result_8bit != expected_8bit){
        //     // std::cout << "expected_bit: " << expected_bit << std::endl;
        //     // std::cout << "result_bit: " << result_bit << std::endl;
        //     mismatch++;
        // }
    }


    // unsigned results[2] = {0b00000000000000100010010100001111,0b11011111111111111111000011111111};
    // unsigned expected_label[2] = {0b00000000000000000000000000000000,0b00000000000000000000000000000000};
    // int mask;
    // int mismatch = 0;
    // std::cout << expected_label[0] << std::endl;
    // std::cout << expected_label[1] << std::endl;


    // for (int i = 0; i < 2; i++){
    //     mask = 0b01;
    //     for (int j = 0; j < 32; j++){
    //         int expected = expected_label[i] & mask;
    //         int result = results[i] & mask;
    //         // std::cout << "expected: " << expected << std::endl;
    //         // std::cout << "result: " << result << std::endl;
    //         mask = mask << 1;

    //         if(expected != result){
    //             mismatch++;
    //             // break;
    //         }
    //     }
    // }
    // std::cout << (2*32 - mismatch) << std::endl;
    // std::cout << "Accuracy = " << float(2*32 - mismatch) / (2*32)  << std::endl;
    return 42;
}
