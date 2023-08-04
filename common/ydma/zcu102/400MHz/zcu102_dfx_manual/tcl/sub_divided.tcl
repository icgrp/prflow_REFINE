
open_checkpoint ./checkpoint/hw_bb_locked.dcp             
pr_subdivide -cell pfm_top_i/dynamic_region -subcells {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page2_inst pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst pfm_top_i/dynamic_region/PR_pages_top_0/inst/page8_inst pfm_top_i/dynamic_region/PR_pages_top_0/inst/page12_inst pfm_top_i/dynamic_region/PR_pages_top_0/inst/page16_inst pfm_top_i/dynamic_region/PR_pages_top_0/inst/page20_inst} ./checkpoint/pfm_dynamic.dcp

write_checkpoint -force ./checkpoint/hw_bb_divided.dcp

