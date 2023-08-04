create_pblock p16_p0
add_cells_to_pblock [get_pblocks p16_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0]]
resize_pblock [get_pblocks p16_p0] -add {SLICE_X0Y365:SLICE_X36Y419}
resize_pblock [get_pblocks p16_p0] -add {DSP48E2_X0Y146:DSP48E2_X6Y167}
resize_pblock [get_pblocks p16_p0] -add {RAMB18_X0Y146:RAMB18_X4Y167}
resize_pblock [get_pblocks p16_p0] -add {RAMB36_X0Y73:RAMB36_X4Y83}
set_property SNAPPING_MODE ON [get_pblocks p16_p0]
set_property IS_SOFT FALSE [get_pblocks p16_p0]

create_pblock p16_p1
add_cells_to_pblock [get_pblocks p16_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1]]
resize_pblock [get_pblocks p16_p1] -add {SLICE_X36Y300:SLICE_X36Y349 SLICE_X0Y300:SLICE_X35Y354}
resize_pblock [get_pblocks p16_p1] -add {DSP48E2_X0Y120:DSP48E2_X6Y141}
resize_pblock [get_pblocks p16_p1] -add {RAMB18_X0Y120:RAMB18_X4Y141}
resize_pblock [get_pblocks p16_p1] -add {RAMB36_X0Y60:RAMB36_X4Y70}
set_property SNAPPING_MODE ON [get_pblocks p16_p1]
set_property IS_SOFT FALSE [get_pblocks p16_p1]



