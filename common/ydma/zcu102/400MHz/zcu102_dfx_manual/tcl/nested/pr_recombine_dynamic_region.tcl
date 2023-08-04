# open the lastly routed design, this is our final routed design
open_checkpoint ./overlay_p23/sub_p20_p1/p20_p1_subdivide_route_design.dcp

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst

pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p0
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst/p1
pr_recombine -cell pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst

pr_recombine -cell pfm_top_i/dynamic_region

write_bitstream -force -cell pfm_top_i/dynamic_region ./overlay_p23/dynamic_region.bit
close_project
