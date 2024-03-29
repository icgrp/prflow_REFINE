open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p1
write_checkpoint -force ./overlay_p23/sub_p12_p1/p12_p1_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p1 ./overlay_p23/p12_p1_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p1 ./overlay_p23/p12_p1
report_utilization -pblocks p12_p1 > ./overlay_p23/utilization_p12_p1.rpt
# report_utilization > ./overlay_p23/abs_analysis/p12_p1.rpt
close_project