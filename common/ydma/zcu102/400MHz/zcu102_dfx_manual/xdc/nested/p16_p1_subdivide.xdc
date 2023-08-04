create_pblock p16_p1_p0
add_cells_to_pblock [get_pblocks p16_p1_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1/p0]]
resize_pblock [get_pblocks p16_p1_p0] -add {SLICE_X36Y300:SLICE_X36Y344 SLICE_X19Y300:SLICE_X35Y354}
resize_pblock [get_pblocks p16_p1_p0] -add {DSP48E2_X3Y120:DSP48E2_X6Y141}
resize_pblock [get_pblocks p16_p1_p0] -add {RAMB18_X3Y120:RAMB18_X4Y141}
resize_pblock [get_pblocks p16_p1_p0] -add {RAMB36_X3Y60:RAMB36_X4Y70}
set_property SNAPPING_MODE ON [get_pblocks p16_p1_p0]
set_property IS_SOFT FALSE [get_pblocks p16_p1_p0]


create_pblock p16_p1_p1
add_cells_to_pblock [get_pblocks p16_p1_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1/p1]]
resize_pblock [get_pblocks p16_p1_p1] -add {SLICE_X0Y300:SLICE_X18Y354}
resize_pblock [get_pblocks p16_p1_p1] -add {DSP48E2_X0Y120:DSP48E2_X2Y141}
resize_pblock [get_pblocks p16_p1_p1] -add {RAMB18_X0Y120:RAMB18_X2Y141}
resize_pblock [get_pblocks p16_p1_p1] -add {RAMB36_X0Y60:RAMB36_X2Y70}
set_property SNAPPING_MODE ON [get_pblocks p16_p1_p1]
set_property IS_SOFT FALSE [get_pblocks p16_p1_p1]


