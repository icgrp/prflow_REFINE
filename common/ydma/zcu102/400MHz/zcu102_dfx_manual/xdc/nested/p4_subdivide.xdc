create_pblock p4_p0
add_cells_to_pblock [get_pblocks p4_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0]]
resize_pblock [get_pblocks p4_p0] -add {SLICE_X87Y60:SLICE_X95Y114 SLICE_X60Y60:SLICE_X84Y114}
resize_pblock [get_pblocks p4_p0] -add {DSP48E2_X12Y24:DSP48E2_X17Y45}
resize_pblock [get_pblocks p4_p0] -add {RAMB18_X8Y24:RAMB18_X12Y45 RAMB18_X7Y24:RAMB18_X7Y43}
resize_pblock [get_pblocks p4_p0] -add {RAMB36_X8Y12:RAMB36_X12Y22 RAMB36_X7Y12:RAMB36_X7Y21}
set_property SNAPPING_MODE ON [get_pblocks p4_p0]
set_property IS_SOFT FALSE [get_pblocks p4_p0]

create_pblock p4_p1
add_cells_to_pblock [get_pblocks p4_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1]]
resize_pblock [get_pblocks p4_p1] -add {SLICE_X60Y125:SLICE_X95Y179}
resize_pblock [get_pblocks p4_p1] -add {DSP48E2_X12Y50:DSP48E2_X17Y71}
resize_pblock [get_pblocks p4_p1] -add {RAMB18_X7Y50:RAMB18_X12Y71}
resize_pblock [get_pblocks p4_p1] -add {RAMB36_X7Y25:RAMB36_X12Y35}
set_property SNAPPING_MODE ON [get_pblocks p4_p1]
set_property IS_SOFT FALSE [get_pblocks p4_p1]