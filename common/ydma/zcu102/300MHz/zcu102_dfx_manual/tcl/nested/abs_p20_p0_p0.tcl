open_checkpoint ./checkpoint/sub_p20_p1/p20_p1_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/ydma_1/page20_inst/p0/p0 -black_box
# lock_design -level routing
write_abstract_shell -force -cell pfm_top_i/dynamic_region/ydma_1/page20_inst/p0/p0 ./checkpoint/p20_p0_p0
report_utilization -pblocks p20_p0_p0 > ./checkpoint/utilization_p20_p0_p0.rpt
# report_utilization > ./checkpoint/abs_analysis/p20_p0_p0.rpt
close_project