open_checkpoint ./overlay_p23/sub_p16_p1/p16_p1_subdivide_route_design.dcp  
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p1} ./overlay_p23/subdivide/page_quad_subdivide_p20.dcp
exec mkdir -p ./overlay_p23/sub_p20/
write_checkpoint -force ./overlay_p23/sub_p20/static_p20.dcp
