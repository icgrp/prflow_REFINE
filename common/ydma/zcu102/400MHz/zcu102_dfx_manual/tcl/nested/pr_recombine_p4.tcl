open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst
write_checkpoint -force ./overlay_p23/sub_p4/p4_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst ./overlay_p23/p4_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst ./overlay_p23/p4
report_utilization -pblocks p4 > ./overlay_p23/utilization_p4.rpt
# report_utilization > ./overlay_p23/abs_analysis/p4.rpt
close_project
