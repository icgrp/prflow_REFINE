create_pblock p2_p0
add_cells_to_pblock [get_pblocks p2_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst/p0]]
resize_pblock [get_pblocks p2_p0] -add {SLICE_X61Y0:SLICE_X76Y54 SLICE_X60Y0:SLICE_X60Y49}
resize_pblock [get_pblocks p2_p0] -add {DSP48E2_X12Y0:DSP48E2_X15Y21}
resize_pblock [get_pblocks p2_p0] -add {RAMB18_X8Y0:RAMB18_X9Y21 RAMB18_X7Y0:RAMB18_X7Y19}
resize_pblock [get_pblocks p2_p0] -add {RAMB36_X8Y0:RAMB36_X9Y10 RAMB36_X7Y0:RAMB36_X7Y9}
set_property SNAPPING_MODE ON [get_pblocks p2_p0]
set_property IS_SOFT FALSE [get_pblocks p2_p0]


create_pblock p2_p1
add_cells_to_pblock [get_pblocks p2_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst/p1]]
resize_pblock [get_pblocks p2_p1] -add {SLICE_X77Y0:SLICE_X95Y54}
resize_pblock [get_pblocks p2_p1] -add {DSP48E2_X16Y0:DSP48E2_X17Y21}
resize_pblock [get_pblocks p2_p1] -add {RAMB18_X10Y0:RAMB18_X12Y21}
resize_pblock [get_pblocks p2_p1] -add {RAMB36_X10Y0:RAMB36_X12Y10}
set_property SNAPPING_MODE ON [get_pblocks p2_p1]
set_property IS_SOFT FALSE [get_pblocks p2_p1]
