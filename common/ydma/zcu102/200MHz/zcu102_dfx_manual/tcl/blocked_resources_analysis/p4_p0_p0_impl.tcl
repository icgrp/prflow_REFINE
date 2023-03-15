create_project -in_memory -part xczu9eg-ffvb1156-2-e
set part xczu9eg-ffvb1156-2-e
set context_dcp "../../p4_p0_p0.dcp"
set user_logic_dcp_0 "../../page.dcp"
add_files $context_dcp
add_files $user_logic_dcp_0
set_property SCOPED_TO_CELLS { pfm_top_i/dynamic_region/ydma_1/page4_inst/p0/p0} [get_files $user_logic_dcp_0]
link_design -mode default -reconfig_partitions {pfm_top_i/dynamic_region/ydma_1/page4_inst/p0/p0} -part $part -top pfm_top_wrapper

opt_design
place_design
route_design