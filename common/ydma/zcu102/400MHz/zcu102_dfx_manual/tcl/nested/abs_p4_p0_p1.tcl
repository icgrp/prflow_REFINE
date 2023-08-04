open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0/p1 -black_box
# lock_design -level routing
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0/p1 ./overlay_p23/p4_p0_p1
report_utilization -pblocks p4_p0_p1 > ./overlay_p23/utilization_p4_p0_p1.rpt
# report_utilization > ./overlay_p23/abs_analysis/p4_p0_p1.rpt
close_project