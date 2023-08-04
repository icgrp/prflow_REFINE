create_pblock p4_p1_p0
add_cells_to_pblock [get_pblocks p4_p1_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1/p0]]
resize_pblock [get_pblocks p4_p1_p0] -add {SLICE_X60Y125:SLICE_X76Y179}
resize_pblock [get_pblocks p4_p1_p0] -add {DSP48E2_X12Y50:DSP48E2_X15Y71}
resize_pblock [get_pblocks p4_p1_p0] -add {RAMB18_X8Y50:RAMB18_X9Y71 RAMB18_X7Y52:RAMB18_X7Y71}
resize_pblock [get_pblocks p4_p1_p0] -add {RAMB36_X8Y25:RAMB36_X9Y35 RAMB36_X7Y26:RAMB36_X7Y35}
set_property SNAPPING_MODE ON [get_pblocks p4_p1_p0]
set_property IS_SOFT FALSE [get_pblocks p4_p1_p0]

create_pblock p4_p1_p1
add_cells_to_pblock [get_pblocks p4_p1_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1/p1]]
resize_pblock [get_pblocks p4_p1_p1] -add {SLICE_X77Y125:SLICE_X95Y179}
resize_pblock [get_pblocks p4_p1_p1] -add {DSP48E2_X16Y50:DSP48E2_X17Y71}
resize_pblock [get_pblocks p4_p1_p1] -add {RAMB18_X10Y50:RAMB18_X12Y71}
resize_pblock [get_pblocks p4_p1_p1] -add {RAMB36_X10Y25:RAMB36_X12Y35}
set_property SNAPPING_MODE ON [get_pblocks p4_p1_p1]
set_property IS_SOFT FALSE [get_pblocks p4_p1_p1]