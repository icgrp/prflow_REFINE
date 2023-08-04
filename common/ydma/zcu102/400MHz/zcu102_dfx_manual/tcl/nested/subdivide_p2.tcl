open_checkpoint ./overlay_p23/overlay.dcp             
pr_subdivide -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst/p0 pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst/p1} ./overlay_p23/subdivide/page_double_subdivide_p2.dcp
exec mkdir -p ./overlay_p23/sub_p2/
write_checkpoint -force ./overlay_p23/sub_p2/static_p2.dcp
