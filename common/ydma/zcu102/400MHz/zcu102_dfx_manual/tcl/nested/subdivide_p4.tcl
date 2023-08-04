open_checkpoint ./overlay_p23/sub_p2/p2_subdivide_route_design.dcp        
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1} ./overlay_p23/subdivide/page_quad_subdivide_p4.dcp
exec mkdir -p ./overlay_p23/sub_p4/
write_checkpoint -force ./overlay_p23/sub_p4/static_p4.dcp
