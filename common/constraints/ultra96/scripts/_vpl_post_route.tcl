# This file was automatically generated by Vpl
if { ![info exists _is_init_cmds] } {
  source ./scripts/vpl_init.tcl
  source ./scripts/ocl_util.tcl
  source ./scripts/platform.tcl
  source ./scripts/debug_profile_hooks.tcl
  namespace import ocl_util::*

  set _is_init_cmds true
}



# generate cookie file for messaging
write_cookie_file_impl "ydma"

# utilization reports
report_utilization_impl true "ydma" "routed" "pfm_top_i/dynamic_region" $input_dir $vivado_output_dir

# kernel service update
update_kernel_info $steps_log $vpl_output_dir "pfm_top_i/dynamic_region"

# update noc node information
update_profile_metadata_postroute $vpl_output_dir
