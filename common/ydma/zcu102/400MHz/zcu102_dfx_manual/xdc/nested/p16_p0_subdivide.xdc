create_pblock p16_p0_p0
add_cells_to_pblock [get_pblocks p16_p0_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0]]
resize_pblock [get_pblocks p16_p0_p0] -add {SLICE_X36Y370:SLICE_X36Y419 SLICE_X19Y365:SLICE_X35Y419}
resize_pblock [get_pblocks p16_p0_p0] -add {DSP48E2_X3Y146:DSP48E2_X6Y167}
resize_pblock [get_pblocks p16_p0_p0] -add {RAMB18_X3Y146:RAMB18_X4Y167}
resize_pblock [get_pblocks p16_p0_p0] -add {RAMB36_X3Y73:RAMB36_X4Y83}
set_property SNAPPING_MODE ON [get_pblocks p16_p0_p0]
set_property IS_SOFT FALSE [get_pblocks p16_p0_p0]

create_pblock p16_p0_p1
add_cells_to_pblock [get_pblocks p16_p0_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1]]
resize_pblock [get_pblocks p16_p0_p1] -add {SLICE_X0Y365:SLICE_X18Y419}
resize_pblock [get_pblocks p16_p0_p1] -add {DSP48E2_X0Y146:DSP48E2_X2Y167}
resize_pblock [get_pblocks p16_p0_p1] -add {RAMB18_X0Y146:RAMB18_X2Y167}
resize_pblock [get_pblocks p16_p0_p1] -add {RAMB36_X0Y73:RAMB36_X2Y83}
set_property SNAPPING_MODE ON [get_pblocks p16_p0_p1]
set_property IS_SOFT FALSE [get_pblocks p16_p0_p1]


