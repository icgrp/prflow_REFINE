create_pblock p20_p0
add_cells_to_pblock [get_pblocks p20_p0] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p0]]
resize_pblock [get_pblocks p20_p0] -add {SLICE_X0Y245:SLICE_X36Y299}
resize_pblock [get_pblocks p20_p0] -add {DSP48E2_X0Y98:DSP48E2_X6Y119}
resize_pblock [get_pblocks p20_p0] -add {RAMB18_X0Y98:RAMB18_X4Y119}
resize_pblock [get_pblocks p20_p0] -add {RAMB36_X0Y49:RAMB36_X4Y59}
set_property SNAPPING_MODE ON [get_pblocks p20_p0]
set_property IS_SOFT FALSE [get_pblocks p20_p0]

create_pblock p20_p1
add_cells_to_pblock [get_pblocks p20_p1] [get_cells -quiet [list pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p1]]
resize_pblock [get_pblocks p20_p1] -add {SLICE_X36Y180:SLICE_X36Y229 SLICE_X0Y180:SLICE_X35Y234}
resize_pblock [get_pblocks p20_p1] -add {DSP48E2_X0Y72:DSP48E2_X6Y93}
resize_pblock [get_pblocks p20_p1] -add {RAMB18_X0Y72:RAMB18_X4Y93}
resize_pblock [get_pblocks p20_p1] -add {RAMB36_X0Y36:RAMB36_X4Y46}
set_property SNAPPING_MODE ON [get_pblocks p20_p1]
set_property IS_SOFT FALSE [get_pblocks p20_p1]