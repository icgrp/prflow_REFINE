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
    #include "test_set_0.dat",
    #include "test_set_1.dat"    
};