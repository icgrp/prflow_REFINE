open_checkpoint ./checkpoint/sub_p20_p1/p20_p1_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/ydma_1/page16_inst/p0/p1 -black_box
# lock_design -level routing
write_abstract_shell -force -cell pfm_top_i/dynamic_region/ydma_1/page16_inst/p0/p1 ./checkpoint/p16_p0_p1
report_utilization -pblocks p16_p0_p1 > ./checkpoint/utilization_p16_p0_p1.rpt
# report_utilization > ./checkpoint/abs_analysis/p16_p0_p1.rpt
close_project