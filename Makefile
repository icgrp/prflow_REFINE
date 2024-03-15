############################################################################################

# prj_name=digit_rec_BRAM
# prj_name=digit_rec_LUTRAM
# prj_name=optical_flow_DSP
# prj_name=rendering
# prj_name=spam_filter_BRAM
# prj_name=spam_filter_DSP
prj_name=spam_filter_LUTRAM

#############################################################################################

src=./common/verilog_src
ws=workspace
ws_overlay=$(ws)/F001_overlay
ws_hls=$(ws)/F002_hls_$(prj_name)
ws_syn=$(ws)/F003_syn_$(prj_name)
ws_impl=$(ws)/F004_impl_$(prj_name)
ws_bit=$(ws)/F005_bits_$(prj_name)
ws_mono=$(ws)/F007_mono_$(prj_name)
ws_mono_overlay=$(ws)/F007_overlay_mono

host_dir=./input_src/$(prj_name)/host
operators_dir=./input_src/$(prj_name)/operators
# operators_src=$(wildcard $(operators_dir)/*.cpp)

# operators=$(basename $(notdir $(operators_src)))
operators=$(shell python ./pr_flow/parse_op_list.py -prj $(prj_name))

operators_hls_targets=$(foreach n, $(operators), $(ws_hls)/run_log_$(n).log)
operators_syn_targets=$(foreach n, $(operators), $(ws_syn)/$(n)/page_netlist.dcp)

operators_pblocks=$(foreach n, $(operators), $(ws_syn)/$(n)/pblock.json)
# WIP: operators_impl is necessary only when there exists multiple operators in one PR 
operators_impl=$(shell python ./pr_flow/parse_op_list.py -prj $(prj_name))

# operators_bit_targets=$(foreach n, $(operators_impl), $(ws_bit)/$(n).bit)
operators_bit_targets=$(foreach n, $(operators_impl), $(ws_impl)/$(n)/page_routed.dcp)
operators_xclbin_targets=$(foreach n, $(operators_impl), $(ws_bit)/$(n).xclbin)
operators_runtime_target=$(ws_bit)/sd_card/app.exe

mono_target=$(ws_mono)/ydma.xclbin


# freq may need to be Makefile input
freq?=400
NPROC=32

all: $(operators_runtime_target)


mono: $(mono_target)
$(mono_target):./input_src/$(prj_name)/host/top.cpp ./pr_flow/monolithic.py $(operators_hls_targets)
	python pr_flow.py $(prj_name) -monolithic -op '$(operators)'
	cd $(ws_mono) && ./main.sh && python write_result.py --mono || python write_result.py --mono --fail
	@if [ -f $(ws_mono)/__success__ ]; then\
		echo "---------------------------------";\
		echo "## Monolithic bitstream is ready!";\
		echo "---------------------------------";\
	else\
		echo "------------------------------------";\
		echo "## Monolithic implementation failed ";\
		echo "------------------------------------";\
		python pr_flow.py $(prj_name) --record_time_mono;\
		./run_on_fpga_mono_failed.sh;\
	fi;\


runtime:$(operators_runtime_target) # NOTE: operators
$(operators_runtime_target):./input_src/$(prj_name)/host/host.cpp $(operators_xclbin_targets) ./pr_flow/runtime.py
	python pr_flow.py $(prj_name) -runtime -op '$(operators)'
	cp $(operators_xclbin_targets) $(ws_bit)/sd_card
	cd $(ws_bit)/$(prj_name)/host && ./gen_runtime.sh

	
xclbin: $(operators_xclbin_targets) # NOTE: operators_impl
$(operators_xclbin_targets): sync_impl
	python pr_flow.py $(prj_name) -xclbin -op $(basename $(notdir $@))
	cd $(ws_bit) && ./main_$(basename $(notdir $@)).sh $(operators_impl)

# Wait untill all implementation runs are finished
sync_impl: $(operators_bit_targets) 
	@if [ "$(shell python pr_flow.py $(prj_name) --check_impl_result -op '$(operators_impl)')" = "Success" ]; then\
		echo "------------------------------------";\
		echo "## All partial bitstreams are ready!";\
		echo "------------------------------------";\
	else\
		if [ "$(shell python pr_flow.py $(prj_name) --check_impl_result -op '$(operators_impl)')" = "Timing" ]; then\
			echo "------------------------------------";\
			echo "## Some runs have timing violations ";\
			echo "------------------------------------";\
			python pr_flow.py $(prj_name) --record_time;\
			./run_on_fpga_timing.sh;\
		else\
			echo "---------------------------------------";\
			echo "## Some runs failed in implementations ";\
			echo "---------------------------------------";\
			python pr_flow.py $(prj_name) --record_time;\
			# Try to increment pblock size for failed operators \
			python pr_flow.py $(prj_name) -pg -op "$(shell python pr_flow.py $(prj_name) --check_impl_result -op '$(operators_impl)')";\
			if [ ! -f $(ws_syn)/pblock_assignment.json ]; then\
        		touch './input_src/'$(prj_name)'/__NoC_done__';\
				# If new increased sized pblock NOT available, move to monolithic (using current failed parameters) \
				make incr_mono;\
			else\
				# If new increased sized pblock available, give it another try \
				make all --ignore-errors -j$(NPROC);\
				./run_on_fpga.sh;\
			fi;\
		fi;\
	fi;\
# 		make incr --no-print-directory && make bits -j$(NPROC) --no-print-directory && make sync_impl --no-print-directory;\


record_NoC_success:
	python pr_flow.py $(prj_name) --record_time --impl_success

record_mono_success:
	python pr_flow.py $(prj_name) --record_time_mono --impl_success


incr_NoC:./input_src/$(prj_name)/__NoC_done__
./input_src/$(prj_name)/__NoC_done__:
	python pr_flow.py $(prj_name) -incr
	make sync_pg_assign --ignore-errors -j$(NPROC)
	if [ ! -f ./input_src/$(prj_name)/__NoC_done__ ]; then\
		make all --ignore-errors -j$(NPROC);\
		./run_on_fpga.sh;\
	fi;\

incr_mono:./input_src/$(prj_name)/__mono_done__
./input_src/$(prj_name)/__mono_done__:
	touch ./input_src/$(prj_name)/__NoC_done__
	python pr_flow.py $(prj_name) -incr
	make mono --ignore-errors -j$(NPROC)
	./run_on_fpga_mono.sh

bits:$(operators_bit_targets) # NOTE: operators_impl
$(operators_bit_targets):$(ws_impl)/%/page_routed.dcp:$(ws_overlay)/__overlay_is_ready__ $(ws_syn)/%/pblock.json $(ws_syn)/%/page_netlist.dcp
	python pr_flow.py $(prj_name) -impl -op $(notdir $(subst /page_routed.dcp,,$@))
	# After Implementation, write success/fail results and based on the results
	cd $(ws_impl)/$(notdir $(subst /page_routed.dcp,,$@)) && ./main.sh $(operators_impl) &&\
	 python write_result.py || python write_result.py --fail

sync_pg_assign:$(operators_pblocks) 
$(operators_pblocks):$(ws_syn)/%/pblock.json: pg_assign

pg_assign:$(ws_syn)/pblock_assignment.json
$(ws_syn)/pblock_assignment.json:$(operators_syn_targets) $(operators_dir)/specs.json
	python pr_flow.py $(prj_name) -pg -op '$(operators_impl)'
	if [ ! -f $(ws_syn)/pblock_assignment.json ]; then\
		python pr_flow.py $(prj_name) --record_time;\
		touch './input_src/'$(prj_name)'/__NoC_done__';\
		# If no pblock maping available, move to monolithic (using current failed parameters) \
		make incr_mono;\
	fi;\

# Synthesis
syn:$(operators_syn_targets)
# Out-of-Context Synthesis from Verilog to post-synthesis DCP
$(operators_syn_targets):$(ws_syn)/%/page_netlist.dcp:$(ws_hls)/run_log_%.log $(ws_overlay)/__overlay_is_ready__
	python pr_flow.py $(prj_name) -syn -op $(subst run_log_,,$(basename $(notdir $<)))
	cd $(ws_syn)/$(subst run_log_,,$(basename $(notdir $<))) && ./main.sh $(operators)

# HLS
hls: $(operators_hls_targets)
# High-Level-Synthesis from C to Verilog
$(operators_hls_targets):$(ws_hls)/run_log_%.log:$(operators_dir)/%.cpp $(operators_dir)/%.h ./pr_flow/hls.py
	python pr_flow.py $(prj_name) -hls -op $(basename $(notdir $<))
	cd $(ws_hls) && ./main_$(basename $(notdir $<)).sh $(operators)


overlay: $(ws_overlay)/__overlay_is_ready__
$(ws_overlay)/__overlay_is_ready__:
	python pr_flow.py $(prj_name) -g 'psnoc' -op '$(basename $(notdir $(operators)))'
	cd ./workspace/F001_overlay && ./main.sh

overlay_mono: $(ws_mono_overlay)/__overlay_mono_is_ready__
$(ws_mono_overlay)/__overlay_mono_is_ready__:
	python pr_flow.py $(prj_name) -g 'mono' -op '$(basename $(notdir $(operators)))'
	cd $(ws_mono_overlay) && ./main_overlay_mono.sh



.PHONY: report 
report: 
	 python ./pr_flow.py $(prj_name) -op '$(notdir $(subst /page_routed.dcp,,$(operators_bit_targets))) ' -rpt

report_syn: 
	 python ./pr_flow.py $(prj_name) -op '$(notdir $(subst /page_netlist.dcp,,$(operators_syn_targets))) ' -rpt_s

report_mono: 
	 python ./pr_flow.py $(prj_name) -op '$(notdir $(subst /page_routed.dcp,,$(operators_bit_targets))) ' -rpt_m -freq=$(freq)


clear:
	rm -rf ./workspace/*$(prj_name)

clear_incr:
	rm -rf ./workspace/*$(prj_name)
	rm -rf run_on_*.sh
	rm -rf ./_bi_results/$(prj_name)/*
	rm -rf ./input_src/$(prj_name)/__NoC_done__
	rm -rf ./input_src/$(prj_name)/__mono_done__
	rm -rf ./input_src/$(prj_name)/params/ops_to_compile.json
	rm -rf ./input_src/$(prj_name)/params/prev_param.json
	rm -rf ./input_src/$(prj_name)/params/best.txt
	rm -rf ./input_src/$(prj_name)/params/visited/*
	rm -rf ./input_src/$(prj_name)/params/results/*
	rm -rf ./input_src/$(prj_name)/operators/*
	mkdir -p ./input_src/$(prj_name)/operators/no_merge
	if [ -f ./input_src/$(prj_name)/folding_config_init.json ]; then\
		cp ./input_src/$(prj_name)/folding_config_init.json ./input_src/$(prj_name)/folding_config.json;\
	fi;\
	cp ./input_src/$(prj_name)/params/init_param.json ./input_src/$(prj_name)/params/cur_param.json 
	cd ./input_src/$(prj_name)/ && python gen_next_param.py
	cp ./input_src/$(prj_name)/params/ops_init.json ./input_src/$(prj_name)/params/ops_to_compile.json 

# clean:
# # 	rm -rf ./workspace
# 	rm -rf ./pr_flow/*.pyc

clear_impl:
	rm -rf ./workspace/F004_impl_$(prj_name)
	rm -rf ./workspace/F005_bits_$(prj_name)
