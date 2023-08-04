open_checkpoint ./overlay_p23/sub_p12/p12_subdivide_route_design.dcp
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0 -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0/p1} ./overlay_p23/subdivide/page_double_subdivide_p12_p0.dcp
exec mkdir -p ./overlay_p23/sub_p12_p0/
write_checkpoint -force ./overlay_p23/sub_p12_p0/static_p12_p0.dcp
