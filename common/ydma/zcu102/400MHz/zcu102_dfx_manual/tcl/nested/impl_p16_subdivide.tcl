create_project -in_memory -part xczu9eg-ffvb1156-2-e
add_files ./overlay_p23/sub_p16/static_p16.dcp
add_files ./overlay_p23/page_double.dcp
set_property SCOPED_TO_CELLS { pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1} [get_files ./overlay_p23/page_double.dcp]
add_files ./xdc/nested/p16_subdivide.xdc
set_property USED_IN {implementation} [get_files ./xdc/nested/p16_subdivide.xdc]
set_property PROCESSING_ORDER LATE [get_files ./xdc/nested/p16_subdivide.xdc]
link_design -mode default -reconfig_partitions {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1} -part xczu9eg-ffvb1156-2-e -top pfm_top_wrapper
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_link_design.dcp
opt_design
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_opt_design.dcp
place_design
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_place_design.dcp
phys_opt_design
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_phy_opt_design.dcp
route_design
write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_route_design.dcp

# update_design -black_box -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0
# update_design -black_box -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1
# lock_design -level routing
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_static.dcp
# close_project

# open_checkpoint ./overlay_p23/sub_p16/p16_subdivide_route_design.dcp
# pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst
# write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_recombined.dcp
# write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst ./overlay_p23/p16_subdivide.bit
# close_project

# open_checkpoint ./overlay_p23/sub_p16/p16_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0 -black_box
# lock_design -level routing
# write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0 ./overlay_p23/p16_p0
# close_project

# open_checkpoint ./overlay_p23/sub_p16/p16_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1 -black_box
# lock_design -level routing
# write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1 ./overlay_p23/p16_p1
# close_project
