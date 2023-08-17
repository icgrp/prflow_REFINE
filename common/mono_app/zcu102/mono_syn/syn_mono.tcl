set top_name mono

add_files ./mono_src/mono.v
add_files ./mono_src/stream_shell.v
add_files ./mono_src/rise_detect.v
add_files ./mono_src/stall_cnt.v

set dir "./app_src/"
set contents [glob -nocomplain -directory $dir *]
foreach item $contents {
  if { [regexp {.*\.tcl} $item] } {
    source $item
  } else {
    add_files -norecurse $item
  }
}

set_param general.maxThreads  8
set_property XPM_LIBRARIES {XPM_CDC XPM_MEMORY XPM_FIFO} [current_project]
set logFileId [open ./run_mono_syn.log "w"]
set start_time [clock seconds]
synth_design -top $top_name -part xczu9eg-ffvb1156-2-e -mode out_of_context
write_checkpoint -force ./$top_name.dcp
set end_time [clock seconds]
set total_seconds [expr $end_time - $start_time]
puts $logFileId "syn: $total_seconds seconds"