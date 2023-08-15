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

modify:$(impl_dir)/gen_overlay_mono_syn.tcl
$(impl_dir)/gen_overlay_mono_syn.tcl:$(impl_dir)/$(vitis_impl_tcl_name).tcl ./python/mk_gen_overlay_mono_syn.py checkpoint
	./shell/run_python.sh ./python/mk_gen_overlay_mono_syn.py $(workspace) $(kl_name) $(vitis_impl_tcl_name)

# Adjust directory in create_hier_bd.tcl, cp it to impl dir, and run it
create_hier_bd:$(impl_dir)/create_hier_bd.tcl
$(impl_dir)/create_hier_bd.tcl: ./python/mk_create_hier_bd_tcl.py
	python ./python/mk_create_hier_bd_tcl.py
	./shell/run_gen_hier_bd.sh $(workspace)

checkpoint:
	mkdir -p checkpoint
	mkdir -p $(workspace)/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup
	cp -r $(workspace)/_x/link/vivado/vpl/prj/prj.runs/impl_1/* $(workspace)/_x/link/vivado/vpl/prj/prj.runs/impl_1_backup

clean:
	rm -rf *.log *.jou *.rpt .Xil hd_visual *.str *.txt checkpoint/* 
