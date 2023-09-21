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

const uint8_t test_data[9600 * 28 * 28 * 1] = {
    #include "test_data_0.dat"
};