open_checkpoint ./overlay_p23/sub_p4_p1/p4_p1_subdivide_route_design.dcp       
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p1} ./overlay_p23/subdivide/page_quad_subdivide_p8.dcp
exec mkdir -p ./overlay_p23/sub_p8/
write_checkpoint -force ./overlay_p23/sub_p8/static_p8.dcp
