/*===============================================================*/
/*                                                               */
/*                          test.h                               */
/*                                                               */
/*                     Test data for BNN                         */
/*                                                               */
/*===============================================================*/
#include "typedefs.h"


const uint8_t expected_labels[9600] = {
    #include "expected.dat"
};

const uint8_t test_data[9600 * 32 * 32 * 3] = {
    #include "test_data_0.dat"
    #include "test_data_1.dat"
    #include "test_data_2.dat"
    #include "test_data_3.dat"
    #include "test_data_4.dat"
    #include "test_data_5.dat"
    #include "test_data_6.dat"
    #include "test_data_7.dat"
    #include "test_data_8.dat"
    #include "test_data_9.dat"
    #include "test_data_10.dat"
    #include "test_data_11.dat"
    #include "test_data_12.dat"
    #include "test_data_13.dat"
    #include "test_data_14.dat"
};