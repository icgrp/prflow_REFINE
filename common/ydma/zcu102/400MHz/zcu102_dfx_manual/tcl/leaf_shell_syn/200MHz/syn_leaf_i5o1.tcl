set top_name leaf_i5o1
set dir "./src4level2/leaf_shell/leaf_interface_src/"
set contents [glob -nocomplain -directory $dir *]
foreach item $contents {
  add_files -norecurse $item
}
add_files ./src4level2/leaf_shell/200MHz/$top_name.v
set_param general.maxThreads 8
set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]
synth_design -top $top_name -part xczu9eg-ffvb1156-2-e -mode out_of_context
write_checkpoint -force ./overlay_p23/leaf_shell/200MHz/$top_name.dcp
report_utilization -hierarchical > ./overlay_p23/leaf_shell/200MHz/util_$top_name.rpt
