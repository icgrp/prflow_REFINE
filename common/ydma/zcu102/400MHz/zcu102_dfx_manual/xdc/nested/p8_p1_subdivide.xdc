create_pblock p8_p1_p0
add_cells_to_pblock [get_pblocks p8_p1_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p1/p0]]
resize_pblock [get_pblocks p8_p1_p0] -add {SLICE_X60Y245:SLICE_X76Y299}
resize_pblock [get_pblocks p8_p1_p0] -add {DSP48E2_X12Y98:DSP48E2_X15Y119}
resize_pblock [get_pblocks p8_p1_p0] -add {RAMB18_X8Y98:RAMB18_X9Y119 RAMB18_X7Y100:RAMB18_X7Y119}
resize_pblock [get_pblocks p8_p1_p0] -add {RAMB36_X8Y49:RAMB36_X9Y59 RAMB36_X7Y50:RAMB36_X7Y59}
set_property SNAPPING_MODE ON [get_pblocks p8_p1_p0]
set_property IS_SOFT FALSE [get_pblocks p8_p1_p0]

create_pblock p8_p1_p1
add_cells_to_pblock [get_pblocks p8_p1_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p1/p1]]
resize_pblock [get_pblocks p8_p1_p1] -add {SLICE_X77Y245:SLICE_X95Y299}
resize_pblock [get_pblocks p8_p1_p1] -add {DSP48E2_X16Y98:DSP48E2_X17Y119}
resize_pblock [get_pblocks p8_p1_p1] -add {RAMB18_X10Y98:RAMB18_X12Y119}
resize_pblock [get_pblocks p8_p1_p1] -add {RAMB36_X10Y49:RAMB36_X12Y59}
set_property SNAPPING_MODE ON [get_pblocks p8_p1_p1]
set_property IS_SOFT FALSE [get_pblocks p8_p1_p1]
