pblock_page_dict = {
            'p4': ['4','5','6','7'], 
            'p8': ['8','9','10','11'],
            'p12': ['12','13','14','15'],
            'p16': ['16','17','18','19'],
            'p20': ['20','21','22','23'],

            'p2': ['2','3'], 
            'p4_p0': ['4','5'], 'p4_p1': ['6','7'],
            'p8_p0': ['8','9'], 'p8_p1': ['10','11'], 
            'p12_p0': ['12','13'], 'p12_p1': ['14','15'], 
            'p16_p0': ['16','17'], 'p16_p1': ['18','19'],
            'p20_p0': ['20','21'], 'p20_p1': ['22','23'],

            'p2_p0': ['2'], 'p2_p1': ['3'],
            'p4_p0_p0': ['4'], 'p4_p0_p1': ['5'], 'p4_p1_p0': ['6'], 'p4_p1_p1': ['7'],
            'p8_p0_p0': ['8'], 'p8_p0_p1': ['9'], 'p8_p1_p0': ['10'], 'p8_p1_p1': ['11'],
            'p12_p0_p0': ['12'], 'p12_p0_p1': ['13'], 'p12_p1_p0': ['14'], 'p12_p1_p1': ['15'],
            'p16_p0_p0': ['16'], 'p16_p0_p1': ['17'], 'p16_p1_p0': ['18'], 'p16_p1_p1': ['19'],
            'p20_p0_p0': ['20'], 'p20_p0_p1': ['21'], 'p20_p1_p0': ['22'], 'p20_p1_p1': ['23']
}


pblock_xclbin_dict = {
            'p2': [],
            'p2_p0': ['p2_subdivide.xclbin'], 
            'p2_p1': ['p2_subdivide.xclbin'],

            'p4': [], 
            'p4_p0': ['p4_subdivide.xclbin'], 
            'p4_p1': ['p4_subdivide.xclbin'],
            'p4_p0_p0': ['p4_p0_subdivide.xclbin', 'p4_subdivide.xclbin'],
            'p4_p0_p1': ['p4_p0_subdivide.xclbin', 'p4_subdivide.xclbin'], 
            'p4_p1_p0': ['p4_p1_subdivide.xclbin', 'p4_subdivide.xclbin'], 
            'p4_p1_p1': ['p4_p1_subdivide.xclbin', 'p4_subdivide.xclbin'],

            'p8': [], 
            'p8_p0': ['p8_subdivide.xclbin'], 
            'p8_p1': ['p8_subdivide.xclbin'],
            'p8_p0_p0': ['p8_p0_subdivide.xclbin', 'p8_subdivide.xclbin'],
            'p8_p0_p1': ['p8_p0_subdivide.xclbin', 'p8_subdivide.xclbin'], 
            'p8_p1_p0': ['p8_p1_subdivide.xclbin', 'p8_subdivide.xclbin'], 
            'p8_p1_p1': ['p8_p1_subdivide.xclbin', 'p8_subdivide.xclbin'],

            'p12': [], 
            'p12_p0': ['p12_subdivide.xclbin'], 
            'p12_p1': ['p12_subdivide.xclbin'],
            'p12_p0_p0': ['p12_p0_subdivide.xclbin', 'p12_subdivide.xclbin'],
            'p12_p0_p1': ['p12_p0_subdivide.xclbin', 'p12_subdivide.xclbin'], 
            'p12_p1_p0': ['p12_p1_subdivide.xclbin', 'p12_subdivide.xclbin'], 
            'p12_p1_p1': ['p12_p1_subdivide.xclbin', 'p12_subdivide.xclbin'],

            'p16': [], 
            'p16_p0': ['p16_subdivide.xclbin'], 
            'p16_p1': ['p16_subdivide.xclbin'],
            'p16_p0_p0': ['p16_p0_subdivide.xclbin', 'p16_subdivide.xclbin'],
            'p16_p0_p1': ['p16_p0_subdivide.xclbin', 'p16_subdivide.xclbin'], 
            'p16_p1_p0': ['p16_p1_subdivide.xclbin', 'p16_subdivide.xclbin'], 
            'p16_p1_p1': ['p16_p1_subdivide.xclbin', 'p16_subdivide.xclbin'],

            'p20': [], 
            'p20_p0': ['p20_subdivide.xclbin'], 
            'p20_p1': ['p20_subdivide.xclbin'],
            'p20_p0_p0': ['p20_p0_subdivide.xclbin', 'p20_subdivide.xclbin'],
            'p20_p0_p1': ['p20_p0_subdivide.xclbin', 'p20_subdivide.xclbin'], 
            'p20_p1_p0': ['p20_p1_subdivide.xclbin', 'p20_subdivide.xclbin'], 
            'p20_p1_p1': ['p20_p1_subdivide.xclbin', 'p20_subdivide.xclbin']
}



##
## 400MHz overlay
##

BRAM_MARGIN_single_dict_400MHz = {
    'p2_p0': 0.10, 
    'p2_p1': 0.10, 
    'p4_p0_p0': 0.20, 
    'p4_p0_p1': 0.10, 
    'p4_p1_p0': 0.10, 
    'p4_p1_p1': 0.10, 
    'p8_p0_p0': 0.10, 
    'p8_p0_p1': 0.10, 
    'p8_p1_p0': 0.10, 
    'p8_p1_p1': 0.10, 
    'p12_p0_p0': 0.10, 
    'p12_p0_p1': 0.10, 
    'p12_p1_p0': 0.10, 
    'p12_p1_p1': 0.10, 
    'p16_p0_p0': 0.10, 
    'p16_p0_p1': 0.10, 
    'p16_p1_p0': 0.20, 
    'p16_p1_p1': 0.10, 
    'p20_p0_p0': 0.20, 
    'p20_p0_p1': 0.10, 
    'p20_p1_p0': 0.10, 
    'p20_p1_p1': 0.10}

BRAM_MARGIN_double_dict_400MHz = {
    'p2': 0.10, 
    'p4_p0': 0.20, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.20, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

BRAM_MARGIN_quad_dict_400MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}

LUT_MARGIN_single_dict_400MHz = {
    'p2_p0': 0.15, 
    'p2_p1': 0.15, 
    'p4_p0_p0': 0.15, 
    'p4_p0_p1': 0.15, 
    'p4_p1_p0': 0.15, 
    'p4_p1_p1': 0.15, 
    'p8_p0_p0': 0.15, 
    'p8_p0_p1': 0.15, 
    'p8_p1_p0': 0.15, 
    'p8_p1_p1': 0.15, 
    'p12_p0_p0': 0.15, 
    'p12_p0_p1': 0.15, 
    'p12_p1_p0': 0.15, 
    'p12_p1_p1': 0.15, 
    'p16_p0_p0': 0.15, 
    'p16_p0_p1': 0.15, 
    'p16_p1_p0': 0.15, 
    'p16_p1_p1': 0.15, 
    'p20_p0_p0': 0.15, 
    'p20_p0_p1': 0.15, 
    'p20_p1_p0': 0.15, 
    'p20_p1_p1': 0.15}

LUT_MARGIN_double_dict_400MHz = {
    'p2': 0.10, 
    'p4_p0': 0.10, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

LUT_MARGIN_quad_dict_400MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}


##
## 350MHz overlay
##

BRAM_MARGIN_single_dict_350MHz = {
    'p2_p0': 0.10, 
    'p2_p1': 0.10, 
    'p4_p0_p0': 0.20, 
    'p4_p0_p1': 0.20, 
    'p4_p1_p0': 0.10, 
    'p4_p1_p1': 0.10, 
    'p8_p0_p0': 0.10, 
    'p8_p0_p1': 0.10, 
    'p8_p1_p0': 0.10, 
    'p8_p1_p1': 0.10, 
    'p12_p0_p0': 0.10, 
    'p12_p0_p1': 0.10, 
    'p12_p1_p0': 0.10, 
    'p12_p1_p1': 0.10, 
    'p16_p0_p0': 0.20, 
    'p16_p0_p1': 0.10, 
    'p16_p1_p0': 0.20, 
    'p16_p1_p1': 0.10, 
    'p20_p0_p0': 0.20, 
    'p20_p0_p1': 0.10, 
    'p20_p1_p0': 0.20, 
    'p20_p1_p1': 0.10}

BRAM_MARGIN_double_dict_350MHz = {
    'p2': 0.10, 
    'p4_p0': 0.20, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.20, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

BRAM_MARGIN_quad_dict_350MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}

LUT_MARGIN_single_dict_350MHz = {
    'p2_p0': 0.15, 
    'p2_p1': 0.15, 
    'p4_p0_p0': 0.15, 
    'p4_p0_p1': 0.15, 
    'p4_p1_p0': 0.15, 
    'p4_p1_p1': 0.15, 
    'p8_p0_p0': 0.15, 
    'p8_p0_p1': 0.15, 
    'p8_p1_p0': 0.15, 
    'p8_p1_p1': 0.15, 
    'p12_p0_p0': 0.15, 
    'p12_p0_p1': 0.15, 
    'p12_p1_p0': 0.15, 
    'p12_p1_p1': 0.15, 
    'p16_p0_p0': 0.15, 
    'p16_p0_p1': 0.15, 
    'p16_p1_p0': 0.15, 
    'p16_p1_p1': 0.15, 
    'p20_p0_p0': 0.15, 
    'p20_p0_p1': 0.15, 
    'p20_p1_p0': 0.15, 
    'p20_p1_p1': 0.15}

LUT_MARGIN_double_dict_350MHz = {
    'p2': 0.10, 
    'p4_p0': 0.10, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

LUT_MARGIN_quad_dict_350MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}


##
## 300MHz overlay
##

BRAM_MARGIN_single_dict_300MHz = {
    'p2_p0': 0.10, 
    'p2_p1': 0.10, 
    'p4_p0_p0': 0.20, 
    'p4_p0_p1': 0.10, 
    'p4_p1_p0': 0.10, 
    'p4_p1_p1': 0.10, 
    'p8_p0_p0': 0.10, 
    'p8_p0_p1': 0.10, 
    'p8_p1_p0': 0.10, 
    'p8_p1_p1': 0.10, 
    'p12_p0_p0': 0.10, 
    'p12_p0_p1': 0.10, 
    'p12_p1_p0': 0.10, 
    'p12_p1_p1': 0.10, 
    'p16_p0_p0': 0.10, 
    'p16_p0_p1': 0.10, 
    'p16_p1_p0': 0.20, 
    'p16_p1_p1': 0.10, 
    'p20_p0_p0': 0.20, 
    'p20_p0_p1': 0.10, 
    'p20_p1_p0': 0.10, 
    'p20_p1_p1': 0.10}

BRAM_MARGIN_double_dict_300MHz = {
    'p2': 0.10, 
    'p4_p0': 0.20, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.20, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

BRAM_MARGIN_quad_dict_300MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}

LUT_MARGIN_single_dict_300MHz = {
    'p2_p0': 0.15, 
    'p2_p1': 0.15, 
    'p4_p0_p0': 0.15, 
    'p4_p0_p1': 0.15, 
    'p4_p1_p0': 0.15, 
    'p4_p1_p1': 0.15, 
    'p8_p0_p0': 0.15, 
    'p8_p0_p1': 0.15, 
    'p8_p1_p0': 0.15, 
    'p8_p1_p1': 0.15, 
    'p12_p0_p0': 0.15, 
    'p12_p0_p1': 0.15, 
    'p12_p1_p0': 0.15, 
    'p12_p1_p1': 0.15, 
    'p16_p0_p0': 0.15, 
    'p16_p0_p1': 0.15, 
    'p16_p1_p0': 0.15, 
    'p16_p1_p1': 0.15, 
    'p20_p0_p0': 0.15, 
    'p20_p0_p1': 0.15, 
    'p20_p1_p0': 0.15, 
    'p20_p1_p1': 0.15}

LUT_MARGIN_double_dict_300MHz = {
    'p2': 0.10, 
    'p4_p0': 0.10, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

LUT_MARGIN_quad_dict_300MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}


##
## 250MHz overlay
##

BRAM_MARGIN_single_dict_250MHz = {
    'p2_p0': 0.10, 
    'p2_p1': 0.10, 
    'p4_p0_p0': 0.20, 
    'p4_p0_p1': 0.10, 
    'p4_p1_p0': 0.10, 
    'p4_p1_p1': 0.10, 
    'p8_p0_p0': 0.10, 
    'p8_p0_p1': 0.10, 
    'p8_p1_p0': 0.10, 
    'p8_p1_p1': 0.10, 
    'p12_p0_p0': 0.10, 
    'p12_p0_p1': 0.10, 
    'p12_p1_p0': 0.10, 
    'p12_p1_p1': 0.10, 
    'p16_p0_p0': 0.10, 
    'p16_p0_p1': 0.10, 
    'p16_p1_p0': 0.20, 
    'p16_p1_p1': 0.10, 
    'p20_p0_p0': 0.20, 
    'p20_p0_p1': 0.10, 
    'p20_p1_p0': 0.20, 
    'p20_p1_p1': 0.10}

BRAM_MARGIN_double_dict_250MHz = {
    'p2': 0.10, 
    'p4_p0': 0.20, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.20, 
    'p20_p1': 0.10}

BRAM_MARGIN_quad_dict_250MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}

LUT_MARGIN_single_dict_250MHz = {
    'p2_p0': 0.15, 
    'p2_p1': 0.15, 
    'p4_p0_p0': 0.15, 
    'p4_p0_p1': 0.15, 
    'p4_p1_p0': 0.15, 
    'p4_p1_p1': 0.15, 
    'p8_p0_p0': 0.15, 
    'p8_p0_p1': 0.15, 
    'p8_p1_p0': 0.15, 
    'p8_p1_p1': 0.15, 
    'p12_p0_p0': 0.15, 
    'p12_p0_p1': 0.15, 
    'p12_p1_p0': 0.15, 
    'p12_p1_p1': 0.15, 
    'p16_p0_p0': 0.15, 
    'p16_p0_p1': 0.15, 
    'p16_p1_p0': 0.15, 
    'p16_p1_p1': 0.15, 
    'p20_p0_p0': 0.15, 
    'p20_p0_p1': 0.15, 
    'p20_p1_p0': 0.15, 
    'p20_p1_p1': 0.15}

LUT_MARGIN_double_dict_250MHz = {
    'p2': 0.10, 
    'p4_p0': 0.10, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

LUT_MARGIN_quad_dict_250MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}


##
## 200MHz overlay
##

BRAM_MARGIN_single_dict_200MHz = {
    'p2_p0': 0.10, 
    'p2_p1': 0.10, 
    'p4_p0_p0': 0.20, 
    'p4_p0_p1': 0.10, 
    'p4_p1_p0': 0.10, 
    'p4_p1_p1': 0.10, 
    'p8_p0_p0': 0.10, 
    'p8_p0_p1': 0.10, 
    'p8_p1_p0': 0.10, 
    'p8_p1_p1': 0.10, 
    'p12_p0_p0': 0.10, 
    'p12_p0_p1': 0.10, 
    'p12_p1_p0': 0.10, 
    'p12_p1_p1': 0.10, 
    'p16_p0_p0': 0.10, 
    'p16_p0_p1': 0.10, 
    'p16_p1_p0': 0.20, 
    'p16_p1_p1': 0.10, 
    'p20_p0_p0': 0.20, 
    'p20_p0_p1': 0.10, 
    'p20_p1_p0': 0.20, 
    'p20_p1_p1': 0.10}

BRAM_MARGIN_double_dict_200MHz = {
    'p2': 0.10, 
    'p4_p0': 0.20, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.20, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

BRAM_MARGIN_quad_dict_200MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}

LUT_MARGIN_single_dict_200MHz = {
    'p2_p0': 0.15, 
    'p2_p1': 0.15, 
    'p4_p0_p0': 0.15, 
    'p4_p0_p1': 0.15, 
    'p4_p1_p0': 0.15, 
    'p4_p1_p1': 0.15, 
    'p8_p0_p0': 0.15, 
    'p8_p0_p1': 0.15, 
    'p8_p1_p0': 0.15, 
    'p8_p1_p1': 0.15, 
    'p12_p0_p0': 0.15, 
    'p12_p0_p1': 0.15, 
    'p12_p1_p0': 0.15, 
    'p12_p1_p1': 0.15, 
    'p16_p0_p0': 0.15, 
    'p16_p0_p1': 0.15, 
    'p16_p1_p0': 0.15, 
    'p16_p1_p1': 0.15, 
    'p20_p0_p0': 0.15, 
    'p20_p0_p1': 0.15, 
    'p20_p1_p0': 0.15, 
    'p20_p1_p1': 0.15}

LUT_MARGIN_double_dict_200MHz = {
    'p2': 0.10, 
    'p4_p0': 0.10, 
    'p4_p1': 0.10, 
    'p8_p0': 0.10, 
    'p8_p1': 0.10, 
    'p12_p0': 0.10, 
    'p12_p1': 0.10, 
    'p16_p0': 0.10, 
    'p16_p1': 0.10, 
    'p20_p0': 0.10, 
    'p20_p1': 0.10}

LUT_MARGIN_quad_dict_200MHz = {
    'p4': 0.10, 
    'p8': 0.10, 
    'p12': 0.10, 
    'p16': 0.10, 
    'p20': 0.10}




# TODO: fix these hard numbers
BRAM_MARGIN_single_dict = {"400": BRAM_MARGIN_single_dict_400MHz,
                           "350": BRAM_MARGIN_single_dict_350MHz,
                           "300": BRAM_MARGIN_single_dict_300MHz,
                           "250": BRAM_MARGIN_single_dict_250MHz,
                           "200": BRAM_MARGIN_single_dict_200MHz}

BRAM_MARGIN_double_dict = {"400": BRAM_MARGIN_double_dict_400MHz,
                           "350": BRAM_MARGIN_double_dict_350MHz,
                           "300": BRAM_MARGIN_double_dict_300MHz,
                           "250": BRAM_MARGIN_double_dict_250MHz,
                           "200": BRAM_MARGIN_double_dict_200MHz}

BRAM_MARGIN_quad_dict = {"400": BRAM_MARGIN_quad_dict_400MHz,
                         "350": BRAM_MARGIN_quad_dict_350MHz,
                         "300": BRAM_MARGIN_quad_dict_300MHz,
                         "250": BRAM_MARGIN_quad_dict_250MHz,
                         "200": BRAM_MARGIN_quad_dict_200MHz}

LUT_MARGIN_single_dict = {"400": LUT_MARGIN_single_dict_400MHz,
                          "350": LUT_MARGIN_single_dict_350MHz,
                          "300": LUT_MARGIN_single_dict_300MHz,
                          "250": LUT_MARGIN_single_dict_250MHz,
                          "200": LUT_MARGIN_single_dict_200MHz}

LUT_MARGIN_double_dict = {"400": LUT_MARGIN_double_dict_400MHz,
                          "350": LUT_MARGIN_double_dict_350MHz,
                          "300": LUT_MARGIN_double_dict_300MHz,
                          "250": LUT_MARGIN_double_dict_250MHz,
                          "200": LUT_MARGIN_double_dict_200MHz}

LUT_MARGIN_quad_dict = {"400": LUT_MARGIN_quad_dict_400MHz,
                        "350": LUT_MARGIN_quad_dict_350MHz,
                        "300": LUT_MARGIN_quad_dict_300MHz,
                        "250": LUT_MARGIN_quad_dict_250MHz,
                        "200": LUT_MARGIN_quad_dict_200MHz}
