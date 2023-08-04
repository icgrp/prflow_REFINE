create_project -in_memory -part xczu9eg-ffvb1156-2-e
add_files ./overlay_p23/sub_p16_p0/static_p16_p0.dcp
add_files ./overlay_p23/page.dcp
set_property SCOPED_TO_CELLS { pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1} [get_files ./overlay_p23/page.dcp]
add_files ./xdc/nested/p16_p0_subdivide.xdc
set_property USED_IN {implementation} [get_files ./xdc/nested/p16_p0_subdivide.xdc]
set_property PROCESSING_ORDER LATE [get_files ./xdc/nested/p16_p0_subdivide.xdc]
link_design -mode default -reconfig_partitions {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1} -part xczu9eg-ffvb1156-2-e -top pfm_top_wrapper
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_link_design.dcp
opt_design
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_opt_design.dcp
place_design
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_place_design.dcp
phys_opt_design
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_phy_opt_design.dcp
route_design
write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_route_design.dcp

# update_design -black_box -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0
# update_design -black_box -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1
# lock_design -level routing
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_static.dcp
# close_project

# open_checkpoint ./overlay_p23/sub_p16_p0/p16_p0_subdivide_route_design.dcp
# pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0
# write_checkpoint -force ./overlay_p23/sub_p16_p0/p16_p0_subdivide_recombined.dcp
# write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0 ./overlay_p23/p16_p0_subdivide.bit
# close_project

# open_checkpoint ./overlay_p23/sub_p16_p0/p16_p0_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0 -black_box
# lock_design -level routing
# write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p0 ./overlay_p23/p16_p0_p0
# close_project

# open_checkpoint ./overlay_p23/sub_p16_p0/p16_p0_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1 -black_box
# lock_design -level routing
# write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0/p1 ./overlay_p23/p16_p0_p1
# close_project