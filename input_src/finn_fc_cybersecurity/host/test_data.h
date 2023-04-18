/*===============================================================*/
/*                                                               */
/*                          test.h                               */
/*                                                               */
/*                     Test data for BNN                         */
/*                                                               */
/*===============================================================*/
#include "typedefs.h"


const unsigned expected_labels[2 * 16] = {
    #include "expected.dat"
};

const unsigned test_data[2000 * 16] = {
    #include "test_set.dat"
};