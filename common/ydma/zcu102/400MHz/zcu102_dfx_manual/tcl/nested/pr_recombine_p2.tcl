open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst
write_checkpoint -force ./overlay_p23/sub_p2/p2_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst ./overlay_p23/p2_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst ./overlay_p23/p2
report_utilization -pblocks p2 > ./overlay_p23/utilization_p2.rpt
# report_utilization > ./overlay_p23/abs_analysis/p2.rpt
close_project
