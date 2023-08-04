create_pblock p12_p0_p0
add_cells_to_pblock [get_pblocks p12_p0_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0/p0]]
resize_pblock [get_pblocks p12_p0_p0] -add {SLICE_X60Y300:SLICE_X76Y354}
resize_pblock [get_pblocks p12_p0_p0] -add {DSP48E2_X12Y120:DSP48E2_X15Y141}
resize_pblock [get_pblocks p12_p0_p0] -add {RAMB18_X8Y120:RAMB18_X9Y141 RAMB18_X7Y120:RAMB18_X7Y137}
resize_pblock [get_pblocks p12_p0_p0] -add {RAMB36_X8Y60:RAMB36_X9Y70 RAMB36_X7Y60:RAMB36_X7Y68}
set_property SNAPPING_MODE ON [get_pblocks p12_p0_p0]
set_property IS_SOFT FALSE [get_pblocks p12_p0_p0]

create_pblock p12_p0_p1
add_cells_to_pblock [get_pblocks p12_p0_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0/p1]]
resize_pblock [get_pblocks p12_p0_p1] -add {SLICE_X77Y300:SLICE_X95Y354}
resize_pblock [get_pblocks p12_p0_p1] -add {DSP48E2_X16Y120:DSP48E2_X17Y141}
resize_pblock [get_pblocks p12_p0_p1] -add {RAMB18_X10Y120:RAMB18_X12Y141}
resize_pblock [get_pblocks p12_p0_p1] -add {RAMB36_X10Y60:RAMB36_X12Y70}
set_property SNAPPING_MODE ON [get_pblocks p12_p0_p1]
set_property IS_SOFT FALSE [get_pblocks p12_p0_p1]
