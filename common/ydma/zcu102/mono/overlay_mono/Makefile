ifndef XILINX_VIVADO
  $(error Environment variable XILINX_VIVADO is required and should point to Vitis install area)
endif

vitis_impl_tcl_name=vitis_design_wrapper
kl_name=ydma
workspace=..
impl_dir=$(workspace)/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup


overlay_mono_syn:./checkpoint/overlay_mono_syn.dcp
./checkpoint/overlay_mono_syn.dcp: $(impl_dir)/gen_overlay_mono_syn.tcl
	./shell/run_gen_overlay_mono_syn.sh $(workspace) 
	cp $(impl_dir)/overlay_mono_syn.dcp ./checkpoint

modify:$(impl_dir)/gen_overlay_mono_syn.tcl
$(impl_dir)/gen_overlay_mono_syn.tcl:./python/mk_gen_overlay_mono_syn.py create_hier_bd
	./shell/run_python.sh ./python/mk_gen_overlay_mono_syn.py $(workspace) $(kl_name) $(vitis_impl_tcl_name)

# Adjust directory in create_hier_bd.tcl, cp it to impl dir, and run it
# vitis_design_wrapper.dcp is new synthesized netlist, which contains black box module for monolithic
create_hier_bd:./checkpoint/vitis_design_wrapper.dcp
./checkpoint/vitis_design_wrapper.dcp: ./python/mk_create_hier_bd_tcl.py checkpoint
	python ./python/mk_create_hier_bd_tcl.py
	./shell/run_gen_hier_bd.sh $(workspace)
	cp ${workspace}/_x/link/vivado/vpl/prj/prj.runs/synth_1/vitis_design_wrapper.dcp ./checkpoint

checkpoint:
	mkdir -p checkpoint
	mkdir -p $(impl_dir)
	cp -r $(workspace)/_x/link/vivado/vpl/prj/prj.runs/impl_1/* $(impl_dir)

clean:
	rm -rf *.log *.jou *.rpt .Xil hd_visual *.str *.txt checkpoint/* 
