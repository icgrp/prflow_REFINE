set top_name page_double_subdivide_p16_p1
set output_name subdivide/page_double_subdivide_p16_p1

add_files "./src4level2/subdivide/p_d_s_p16_p1.v"

set_param general.maxThreads  8
set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]
# set logFileId [open ./runOOC.log "w"]
# set start_time [clock seconds]
set_param general.maxThreads  8 
synth_design -top $top_name -part xczu9eg-ffvb1156-2-e -mode out_of_context
write_checkpoint -force ./checkpoint/$output_name.dcp
# set end_time [clock seconds]
# set total_seconds [expr $end_time - $start_time]
# puts $logFileId "syn: $total_seconds seconds"
report_utilization -hierarchical > utilization.rpt

