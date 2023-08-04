open_checkpoint ./overlay_p23/sub_p16_p0/p16_p0_subdivide_route_design.dcp
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1 -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1/p1} ./overlay_p23/subdivide/page_double_subdivide_p16_p1.dcp
exec mkdir -p ./overlay_p23/sub_p16_p1/
write_checkpoint -force ./overlay_p23/sub_p16_p1/static_p16_p1.dcp
