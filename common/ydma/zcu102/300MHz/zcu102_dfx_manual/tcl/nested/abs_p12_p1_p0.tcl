open_checkpoint ./checkpoint/sub_p20_p1/p20_p1_subdivide_route_design.dcp
# update_design -cell pfm_top_i/dynamic_region/ydma_1/page12_inst/p1/p0 -black_box
# lock_design -level routing
write_abstract_shell -force -cell pfm_top_i/dynamic_region/ydma_1/page12_inst/p1/p0 ./checkpoint/p12_p1_p0
report_utilization -pblocks p12_p1_p0 > ./checkpoint/utilization_p12_p1_p0.rpt
# report_utilization > ./checkpoint/abs_analysis/p12_p1_p0.rpt
close_project