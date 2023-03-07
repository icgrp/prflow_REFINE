open_checkpoint ./checkpoint/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/ydma_1/page4_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/ydma_1/page4_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/ydma_1/page4_inst
write_checkpoint -force ./checkpoint/sub_p4/p4_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/ydma_1/page4_inst ./checkpoint/p4_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/ydma_1/page4_inst ./checkpoint/p4
report_utilization -pblocks p4 > ./checkpoint/utilization_p4.rpt
# report_utilization > ./checkpoint/abs_analysis/p4.rpt
close_project
