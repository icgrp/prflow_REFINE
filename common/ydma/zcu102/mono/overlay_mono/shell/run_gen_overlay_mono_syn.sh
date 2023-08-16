#!/bin/bash -e
workspace=$1


cd ${workspace}/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup/
vivado -mode batch -source  gen_overlay_mono_syn.tcl
cd -