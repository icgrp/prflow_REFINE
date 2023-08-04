open_checkpoint ./overlay_p23/sub_p8_p1/p8_p1_subdivide_route_design.dcp     
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p1} ./overlay_p23/subdivide/page_quad_subdivide_p12.dcp
exec mkdir -p ./overlay_p23/sub_p12/
write_checkpoint -force ./overlay_p23/sub_p12/static_p12.dcp
