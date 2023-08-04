open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst
write_checkpoint -force ./overlay_p23/sub_p16/p16_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst ./overlay_p23/p16_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst ./overlay_p23/p16
report_utilization -pblocks p16 > ./overlay_p23/utilization_p16.rpt
# report_utilization > ./overlay_p23/abs_analysis/p16.rpt
close_project
