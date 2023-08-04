create_pblock p8_p0_p0
add_cells_to_pblock [get_pblocks p8_p0_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0/p0]]
resize_pblock [get_pblocks p8_p0_p0] -add {SLICE_X60Y180:SLICE_X76Y234}
resize_pblock [get_pblocks p8_p0_p0] -add {DSP48E2_X12Y72:DSP48E2_X15Y93}
resize_pblock [get_pblocks p8_p0_p0] -add {RAMB18_X8Y72:RAMB18_X9Y93 RAMB18_X7Y72:RAMB18_X7Y89}
resize_pblock [get_pblocks p8_p0_p0] -add {RAMB36_X8Y36:RAMB36_X9Y46 RAMB36_X7Y36:RAMB36_X7Y44}
set_property SNAPPING_MODE ON [get_pblocks p8_p0_p0]
set_property IS_SOFT FALSE [get_pblocks p8_p0_p0]

create_pblock p8_p0_p1
add_cells_to_pblock [get_pblocks p8_p0_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0/p1]]
resize_pblock [get_pblocks p8_p0_p1] -add {SLICE_X77Y180:SLICE_X95Y234}
resize_pblock [get_pblocks p8_p0_p1] -add {DSP48E2_X16Y72:DSP48E2_X17Y93}
resize_pblock [get_pblocks p8_p0_p1] -add {RAMB18_X10Y72:RAMB18_X12Y93}
resize_pblock [get_pblocks p8_p0_p1] -add {RAMB36_X10Y36:RAMB36_X12Y46}
set_property SNAPPING_MODE ON [get_pblocks p8_p0_p1]
set_property IS_SOFT FALSE [get_pblocks p8_p0_p1]