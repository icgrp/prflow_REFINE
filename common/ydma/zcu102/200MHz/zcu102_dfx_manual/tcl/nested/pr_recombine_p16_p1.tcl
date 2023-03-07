open_checkpoint ./checkpoint/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/ydma_1/page16_inst/p1
write_checkpoint -force ./checkpoint/sub_p16_p1/p16_p1_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/ydma_1/page16_inst/p1 ./checkpoint/p16_p1_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/ydma_1/page16_inst/p1 ./checkpoint/p16_p1
report_utilization -pblocks p16_p1 > ./checkpoint/utilization_p16_p1.rpt
# report_utilization > ./checkpoint/abs_analysis/p16_p1.rpt
close_project