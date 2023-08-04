open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0
write_checkpoint -force ./overlay_p23/sub_p8_p0/p8_p0_subdivide_recombined.dcp
write_bitstream -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0 ./overlay_p23/p8_p0_subdivide.bit
write_abstract_shell -force -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0 ./overlay_p23/p8_p0
report_utilization -pblocks p8_p0 > ./overlay_p23/utilization_p8_p0.rpt
# report_utilization > ./overlay_p23/abs_analysis/p8_p0.rpt
close_project