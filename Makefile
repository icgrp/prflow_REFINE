############################################################################################

# prj_name=digit_rec_test
#prj_name=digit_reg_par_40
# prj_name?=digit_reg_par_80

# prj_name=optical_flow_64_single
# prj_name=optical_flow_64_final
# prj_name=optical_flow_96_single
# prj_name=optical_flow_96_final
#prj_name=optical_flow_incr

# prj_name=rendering_par_1
# prj_name=rendering_par_2

#prj_name=spam_filter_par_32
# prj_name=spam_filter_par_32_dot_merged
#prj_name=spam_filter_par_64

#############################################################################################

src=./common/verilog_src
ws=workspace
ws_overlay=$(ws)/F001_overlay
ws_hls=$(ws)/F002_hls_$(prj_name)
ws_syn=$(ws)/F003_syn_$(prj_name)
ws_impl=$(ws)/F004_impl_$(prj_name)
ws_bit=$(ws)/F005_bits_$(prj_name)

host_dir=./input_src/$(prj_name)/host
operators_dir=./input_src/$(prj_name)/operators
operators_src=$(wildcard $(operators_dir)/*.cpp)

operators=$(basename $(notdir $(operators_src)))
operators_hls_targets=$(foreach n, $(operators), $(ws_hls)/runLog$(n).log)
operators_syn_targets=$(foreach n, $(operators), $(ws_syn)/$(n)/page_netlist.dcp)

operators_pblocks=$(foreach n, $(operators), $(ws_syn)/$(n)/pblock.json)
# WIP: operators_impl is necessary only when there exists multiple operators in one PR 
operators_impl=$(shell python ./pr_flow/parse_op_list.py -prj $(prj_name))

# operators_bit_targets=$(foreach n, $(operators_impl), $(ws_bit)/$(n).bit)
operators_bit_targets=$(foreach n, $(operators_impl), $(ws_impl)/$(n)/_impl_result.txt)
operators_xclbin_targets=$(foreach n, $(operators_impl), $(ws_bit)/$(n).xclbin)
operators_runtime_target=$(ws_bit)/sd_card/app.exe



# freq may need to be Makefile input
freq?=400

all: $(operators_runtime_target)

runtime:$(operators_runtime_target) # NOTE: operators
$(operators_runtime_target):./input_src/$(prj_name)/host/host.cpp $(operators_xclbin_targets) ./pr_flow/runtime.py
	python pr_flow.py $(prj_name) -runtime -op '$(operators)' -freq=$(freq)
	cp $(operators_xclbin_targets) $(ws_bit)/sd_card
	cd $(ws_bit)/$(prj_name)/host && ./gen_runtime.sh

	
xclbin: $(operators_xclbin_targets) # NOTE: operators_impl
$(operators_xclbin_targets): sync_impl
	python pr_flow.py $(prj_name) -xclbin -op $(basename $(notdir $@)) -freq=$(freq)
	cd $(ws_bit) && ./main_$(basename $(notdir $@)).sh $(operators_impl)

# Wait untill all implementation runs are finished, TODO: may need to remove impl_result.txt?
sync_impl: $(operators_bit_targets) 
	@if [ "$(shell python pr_flow.py $(prj_name) -c -op '$(operators_impl)')" = "Success" ]; then\
		echo "------------------------------------";\
		echo "## All partial bitstreams are ready!";\
		echo "------------------------------------";\
	else\
		echo "------------------------------------";\
		echo "## Some runs failed ;-(";\
		echo "------------------------------------";\
# 		make incr --no-print-directory && make bits -j$(nproc) --no-print-directory && make sync_impl --no-print-directory;\
	fi

incr:
	echo "nothing for now"

bits:$(operators_bit_targets) # NOTE: operators_impl
$(operators_bit_targets):$(ws_impl)/%/_impl_result.txt:$(ws_overlay)/__overlay_is_ready__ $(ws_syn)/%/pblock.json $(ws_syn)/%/page_netlist.dcp
	python pr_flow.py $(prj_name) -impl -op $(notdir $(subst /_impl_result.txt,,$@)) -freq=$(freq)
	# After Implementation, write success/fail results and based on the results
	cd $(ws_impl)/$(notdir $(subst /_impl_result.txt,,$@)) && ./main.sh $(operators_impl) &&\
	 python write_result.py || python write_result.py --fail

sync_pg_assign:$(operators_pblocks) 
$(operators_pblocks):$(ws_syn)/%/pblock.json: pg_assign

pg_assign:$(ws_syn)/pblock_assignment.json
$(ws_syn)/pblock_assignment.json:$(operators_syn_targets) $(operators_dir)/pblock_operators_list.json
	if [ ! -f $(ws_syn)/pblock_assignment.json ]; then python pr_flow.py $(prj_name) -pg -op '$(operators_impl)' -freq=$(freq); fi

# Synthesis
syn:$(operators_syn_targets)
# Out-of-Context Synthesis from Verilog to post-synthesis DCP
$(operators_syn_targets):$(ws_syn)/%/page_netlist.dcp:$(ws_hls)/runLog%.log $(ws_overlay)/__overlay_is_ready__ ./pr_flow/syn.py
	python pr_flow.py $(prj_name) -syn -op $(subst runLog,,$(basename $(notdir $<)))
	cd $(ws_syn)/$(subst runLog,,$(basename $(notdir $<))) && ./main.sh $(operators)

# HLS
hls: $(operators_hls_targets)
# High-Level-Synthesis from C to Verilog
$(operators_hls_targets):$(ws_hls)/runLog%.log:$(operators_dir)/%.cpp $(operators_dir)/%.h $(host_dir)/typedefs.h ./pr_flow/hls.py
	python pr_flow.py $(prj_name) -hls -op $(basename $(notdir $<)) -freq=$(freq)
	cd $(ws_hls) && ./main_$(basename $(notdir $<)).sh $(operators)

bft_n=23
overlay: $(ws_overlay)/__overlay_is_ready__
$(ws_overlay)/__overlay_is_ready__:
	python pr_flow.py $(prj_name) -g -op '$(basename $(notdir $(operators)))' -bft_n=$(bft_n) -freq=$(freq)
	cd ./workspace/F001_overlay && ./main.sh

.PHONY: report 
report: 
	 python ./pr_flow.py $(prj_name) -op '$(notdir $(subst /_impl_result.txt,,$(operators_bit_targets))) ' -rpt



# When pre-stocking overlays,
# if bft_n==23: p2~p23 
# if bft_n==10, p2~p10
# if bft_n==12, p2~p12
overlay_only:
	python pr_flow.py $(prj_name) -g -op '$(basename $(notdir $(operators)))' -bft_n=$(bft_n) -freq=$(freq)
	cd ./workspace/F001_overlay && ./main.sh



clear:
	rm -rf ./workspace/*$(prj_name)

clean:
	rm -rf ./workspace
	rm -rf ./pr_flow/*.pyc

clear_impl:
	rm -rf ./workspace/F004_impl_$(prj_name)
	rm -rf ./workspace/F005_bits_$(prj_name)


# Incremental compile
# prj_name=optical_flow_incr
# incr:
# 	python pr_flow.py $(prj_name) -incr -op '$(operators)'
# run_on_fpga:
# 	if [ ! -f ./input_src/$(prj_name)/operators/__test_done__ ]; then cd $(ws_bit) && ./run_on_fpga.sh; fi

# test_dir=$(wildcard ./input_src/$(prj_name)/operators/test_*)
# done_signals=$(foreach d, $(test_dir), $(d)/__done__)
# revert_to_init:
# 	rm -rf $(done_signals)
# 	rm -rf ./input_src/$(prj_name)/operators/__test_done__
# 	rm -rf ./input_src/$(prj_name)/operators/_best/
# 	rm -f ./input_src/$(prj_name)/operators/best_result.txt
# 	rm -rf ./input_src/$(prj_name)/operators/*.cpp ./input_src/$(prj_name)/operators/*.h ./input_src/$(prj_name)/operators/*.json
# 	cp ./input_src/$(prj_name)/operators/_original/* ./input_src/$(prj_name)/operators/
# 	mv ./input_src/$(prj_name)/operators/top.cpp ./input_src/$(prj_name)/host/top.cpp
