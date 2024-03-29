create_project -in_memory -part xczu9eg-ffvb1156-2-e
set part xczu9eg-ffvb1156-2-e
set context_dcp "../../p4.dcp"
set user_logic_dcp_0 "../../page_quad.dcp"
add_files $context_dcp
add_files $user_logic_dcp_0
set_property SCOPED_TO_CELLS { pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst} [get_files $user_logic_dcp_0]
link_design -mode default -reconfig_partitions {pfm_top_i/dynamic_region/PR_pages_top_0/inst/page4_inst} -part $part -top pfm_top_wrapper

opt_design
place_design
route_design