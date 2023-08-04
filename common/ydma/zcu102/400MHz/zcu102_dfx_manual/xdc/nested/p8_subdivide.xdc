create_pblock p8_p0
add_cells_to_pblock [get_pblocks p8_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0]]
resize_pblock [get_pblocks p8_p0] -add {SLICE_X61Y180:SLICE_X95Y234 SLICE_X60Y180:SLICE_X60Y229}
resize_pblock [get_pblocks p8_p0] -add {DSP48E2_X12Y72:DSP48E2_X17Y93}
resize_pblock [get_pblocks p8_p0] -add {RAMB18_X8Y72:RAMB18_X12Y93 RAMB18_X7Y72:RAMB18_X7Y91}
resize_pblock [get_pblocks p8_p0] -add {RAMB36_X8Y36:RAMB36_X12Y46 RAMB36_X7Y36:RAMB36_X7Y45}
set_property SNAPPING_MODE ON [get_pblocks p8_p0]
set_property IS_SOFT FALSE [get_pblocks p8_p0]

create_pblock p8_p1
add_cells_to_pblock [get_pblocks p8_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p1]]
resize_pblock [get_pblocks p8_p1] -add {SLICE_X60Y245:SLICE_X95Y299}
resize_pblock [get_pblocks p8_p1] -add {DSP48E2_X12Y98:DSP48E2_X17Y119}
resize_pblock [get_pblocks p8_p1] -add {RAMB18_X7Y98:RAMB18_X12Y119}
resize_pblock [get_pblocks p8_p1] -add {RAMB36_X7Y49:RAMB36_X12Y59}
set_property SNAPPING_MODE ON [get_pblocks p8_p1]
set_property IS_SOFT FALSE [get_pblocks p8_p1]