create_project finn_vivado_stitch_proj /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/vivado_stitch_proj_vlj7ajte -part xczu9eg-ffvb1156-2-e
set_property ip_repo_paths [list $::env(FINN_ROOT)/finn-rtllib/memstream                                                                     ] [current_project]
update_ip_catalog
create_bd_design "finn_design"
create_bd_cell -type ip -vlnv  StreamingFIFO_0
create_bd_cell -type ip -vlnv  Thresholding_Batch_0
create_bd_cell -type ip -vlnv  StreamingFIFO_1
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_0
create_bd_cell -type ip -vlnv  StreamingFIFO_2
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_0
create_bd_cell -type ip -vlnv  StreamingFIFO_3
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_1
create_bd_cell -type ip -vlnv  StreamingFIFO_4
create_bd_cell -type ip -vlnv  MatrixVectorActivation_0
create_bd_cell -type ip -vlnv  StreamingFIFO_5
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_2
create_bd_cell -type ip -vlnv  StreamingFIFO_6
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_1
create_bd_cell -type ip -vlnv  StreamingFIFO_7
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_3
create_bd_cell -type ip -vlnv  StreamingFIFO_8
create_bd_cell -type ip -vlnv  MatrixVectorActivation_1
create_bd_cell -type ip -vlnv  StreamingFIFO_9
create_bd_cell -type ip -vlnv  StreamingMaxPool_Batch_0
create_bd_cell -type ip -vlnv  StreamingFIFO_10
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_4
create_bd_cell -type ip -vlnv  StreamingFIFO_11
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_2
create_bd_cell -type ip -vlnv  StreamingFIFO_12
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_5
create_bd_cell -type ip -vlnv  StreamingFIFO_13
create_bd_cell -type ip -vlnv  MatrixVectorActivation_2
create_bd_cell -type ip -vlnv  StreamingFIFO_14
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_6
create_bd_cell -type ip -vlnv  StreamingFIFO_15
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_3
create_bd_cell -type ip -vlnv  StreamingFIFO_16
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_7
create_bd_cell -type ip -vlnv  StreamingFIFO_17
create_bd_cell -type ip -vlnv  MatrixVectorActivation_3
create_bd_cell -type ip -vlnv  StreamingFIFO_18
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_8
create_bd_cell -type ip -vlnv  StreamingFIFO_19
create_bd_cell -type ip -vlnv  StreamingMaxPool_Batch_1
create_bd_cell -type ip -vlnv  StreamingFIFO_20
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_9
create_bd_cell -type ip -vlnv  StreamingFIFO_21
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_4
create_bd_cell -type ip -vlnv  StreamingFIFO_22
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_10
create_bd_cell -type ip -vlnv  StreamingFIFO_23
create_bd_cell -type ip -vlnv  MatrixVectorActivation_4
create_bd_cell -type ip -vlnv  StreamingFIFO_24
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_11
create_bd_cell -type ip -vlnv  StreamingFIFO_25
create_bd_cell -type ip -vlnv  ConvolutionInputGenerator_5
create_bd_cell -type ip -vlnv  StreamingFIFO_26
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_12
create_bd_cell -type ip -vlnv  StreamingFIFO_27
create_bd_cell -type ip -vlnv  MatrixVectorActivation_5
create_bd_cell -type ip -vlnv  StreamingFIFO_28
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_13
create_bd_cell -type ip -vlnv  StreamingFIFO_29
create_bd_cell -type ip -vlnv  MatrixVectorActivation_6
create_bd_cell -type ip -vlnv  StreamingFIFO_30
create_bd_cell -type ip -vlnv  StreamingDataWidthConverter_Batch_14
create_bd_cell -type ip -vlnv  StreamingFIFO_31
create_bd_cell -type ip -vlnv  MatrixVectorActivation_7
create_bd_cell -type ip -vlnv  StreamingFIFO_32
create_bd_cell -type ip -vlnv  MatrixVectorActivation_8
create_bd_cell -type ip -vlnv  StreamingFIFO_33
create_bd_cell -type ip -vlnv  LabelSelect_Batch_0
create_bd_cell -type ip -vlnv  StreamingFIFO_34
make_bd_pins_external [get_bd_pins StreamingFIFO_0/ap_clk]
set_property name ap_clk [get_bd_ports ap_clk_0]
make_bd_pins_external [get_bd_pins StreamingFIFO_0/ap_rst_n]
set_property name ap_rst_n [get_bd_ports ap_rst_n_0]
make_bd_pins_external [get_bd_pins StreamingFIFO_0/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins Thresholding_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins Thresholding_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_0/out_V] [get_bd_intf_pins Thresholding_Batch_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_1/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_1/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins Thresholding_Batch_0/out_V] [get_bd_intf_pins StreamingFIFO_1/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_1/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_2/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_2/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_0/out_V] [get_bd_intf_pins StreamingFIFO_2/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_2/out_V] [get_bd_intf_pins ConvolutionInputGenerator_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_3/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_3/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_0/out_V] [get_bd_intf_pins StreamingFIFO_3/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_3/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_1/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_4/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_4/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_4/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_1/out_V] [get_bd_intf_pins StreamingFIFO_4/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_4/out_V] [get_bd_intf_pins MatrixVectorActivation_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_5/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_5/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_5/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_0/out_V] [get_bd_intf_pins StreamingFIFO_5/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_5/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_2/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_6/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_6/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_6/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_2/out_V] [get_bd_intf_pins StreamingFIFO_6/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_6/out_V] [get_bd_intf_pins ConvolutionInputGenerator_1/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_7/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_7/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_7/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_1/out_V] [get_bd_intf_pins StreamingFIFO_7/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_7/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_3/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_8/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_8/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_8/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_3/out_V] [get_bd_intf_pins StreamingFIFO_8/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_8/out_V] [get_bd_intf_pins MatrixVectorActivation_1/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_9/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_9/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_9/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_1/out_V] [get_bd_intf_pins StreamingFIFO_9/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingMaxPool_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingMaxPool_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_9/out_V] [get_bd_intf_pins StreamingMaxPool_Batch_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_10/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_10/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_10/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingMaxPool_Batch_0/out_V] [get_bd_intf_pins StreamingFIFO_10/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_4/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_4/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_10/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_4/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_11/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_11/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_11/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_4/out_V] [get_bd_intf_pins StreamingFIFO_11/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_11/out_V] [get_bd_intf_pins ConvolutionInputGenerator_2/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_12/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_12/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_12/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_2/out_V] [get_bd_intf_pins StreamingFIFO_12/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_5/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_5/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_12/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_5/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_13/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_13/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_13/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_5/out_V] [get_bd_intf_pins StreamingFIFO_13/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_2/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_2/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_13/out_V] [get_bd_intf_pins MatrixVectorActivation_2/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_14/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_14/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_14/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_2/out_V] [get_bd_intf_pins StreamingFIFO_14/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_6/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_6/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_14/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_6/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_15/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_15/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_15/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_6/out_V] [get_bd_intf_pins StreamingFIFO_15/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_15/out_V] [get_bd_intf_pins ConvolutionInputGenerator_3/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_16/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_16/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_16/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_3/out_V] [get_bd_intf_pins StreamingFIFO_16/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_7/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_7/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_16/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_7/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_17/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_17/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_17/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_7/out_V] [get_bd_intf_pins StreamingFIFO_17/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_3/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_3/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_17/out_V] [get_bd_intf_pins MatrixVectorActivation_3/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_18/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_18/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_18/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_3/out_V] [get_bd_intf_pins StreamingFIFO_18/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_8/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_8/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_18/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_8/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_19/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_19/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_19/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_8/out_V] [get_bd_intf_pins StreamingFIFO_19/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingMaxPool_Batch_1/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingMaxPool_Batch_1/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_19/out_V] [get_bd_intf_pins StreamingMaxPool_Batch_1/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_20/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_20/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_20/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingMaxPool_Batch_1/out_V] [get_bd_intf_pins StreamingFIFO_20/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_9/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_9/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_20/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_9/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_21/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_21/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_21/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_9/out_V] [get_bd_intf_pins StreamingFIFO_21/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_4/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_4/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_21/out_V] [get_bd_intf_pins ConvolutionInputGenerator_4/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_22/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_22/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_22/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_4/out_V] [get_bd_intf_pins StreamingFIFO_22/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_10/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_10/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_22/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_10/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_23/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_23/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_23/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_10/out_V] [get_bd_intf_pins StreamingFIFO_23/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_4/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_4/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_23/out_V] [get_bd_intf_pins MatrixVectorActivation_4/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_24/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_24/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_24/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_4/out_V] [get_bd_intf_pins StreamingFIFO_24/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_11/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_11/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_24/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_11/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_25/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_25/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_25/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_11/out_V] [get_bd_intf_pins StreamingFIFO_25/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins ConvolutionInputGenerator_5/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins ConvolutionInputGenerator_5/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_25/out_V] [get_bd_intf_pins ConvolutionInputGenerator_5/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_26/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_26/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_26/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins ConvolutionInputGenerator_5/out_V] [get_bd_intf_pins StreamingFIFO_26/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_12/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_12/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_26/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_12/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_27/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_27/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_27/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_12/out_V] [get_bd_intf_pins StreamingFIFO_27/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_5/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_5/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_27/out_V] [get_bd_intf_pins MatrixVectorActivation_5/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_28/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_28/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_28/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_5/out_V] [get_bd_intf_pins StreamingFIFO_28/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_13/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_13/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_28/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_13/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_29/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_29/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_29/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_13/out_V] [get_bd_intf_pins StreamingFIFO_29/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_6/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_6/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_29/out_V] [get_bd_intf_pins MatrixVectorActivation_6/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_30/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_30/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_30/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_6/out_V] [get_bd_intf_pins StreamingFIFO_30/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingDataWidthConverter_Batch_14/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingDataWidthConverter_Batch_14/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_30/out_V] [get_bd_intf_pins StreamingDataWidthConverter_Batch_14/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_31/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_31/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_31/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins StreamingDataWidthConverter_Batch_14/out_V] [get_bd_intf_pins StreamingFIFO_31/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_7/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_7/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_31/out_V] [get_bd_intf_pins MatrixVectorActivation_7/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_32/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_32/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_32/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_7/out_V] [get_bd_intf_pins StreamingFIFO_32/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins MatrixVectorActivation_8/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins MatrixVectorActivation_8/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_32/out_V] [get_bd_intf_pins MatrixVectorActivation_8/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_33/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_33/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_33/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins MatrixVectorActivation_8/out_V] [get_bd_intf_pins StreamingFIFO_33/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins LabelSelect_Batch_0/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins LabelSelect_Batch_0/ap_clk]
connect_bd_intf_net [get_bd_intf_pins StreamingFIFO_33/out_V] [get_bd_intf_pins LabelSelect_Batch_0/in0_V]
connect_bd_net [get_bd_ports ap_rst_n] [get_bd_pins StreamingFIFO_34/ap_rst_n]
connect_bd_net [get_bd_ports ap_clk] [get_bd_pins StreamingFIFO_34/ap_clk]
make_bd_pins_external [get_bd_pins StreamingFIFO_34/maxcount]
set_property name maxcount [get_bd_ports maxcount_0]
connect_bd_intf_net [get_bd_intf_pins LabelSelect_Batch_0/out_V] [get_bd_intf_pins StreamingFIFO_34/in0_V]
make_bd_intf_pins_external [get_bd_intf_pins StreamingFIFO_0/in0_V]
set_property name s_axis_0 [get_bd_intf_ports in0_V_0]
make_bd_intf_pins_external [get_bd_intf_pins StreamingFIFO_34/out_V]
set_property name m_axis_0 [get_bd_intf_ports out_V_0]
set_property CONFIG.FREQ_HZ 100000000.000000 [get_bd_ports /ap_clk]
regenerate_bd_layout
validate_bd_design
save_bd_design
make_wrapper -files [get_files /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/vivado_stitch_proj_vlj7ajte/finn_vivado_stitch_proj.srcs/sources_1/bd/finn_design/finn_design.bd] -top
add_files -norecurse /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/vivado_stitch_proj_vlj7ajte/finn_vivado_stitch_proj.srcs/sources_1/bd/finn_design/hdl/finn_design_wrapper.v
set_property top finn_design_wrapper [current_fileset]
ipx::package_project -root_dir /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/vivado_stitch_proj_vlj7ajte/ip -vendor xilinx_finn -library finn -taxonomy /UserIP -module finn_design -import_files
ipx::remove_segment -quiet m_axi_gmem0:APERTURE_0 [ipx::get_address_spaces m_axi_gmem0 -of_objects [ipx::current_core]]
set_property core_revision 2 [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
ipx::create_xgui_files [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
set_property value_resolve_type user [ipx::get_bus_parameters -of [ipx::get_bus_interfaces -of [ipx::current_core ]]]
file copy -force data ip/
ipx::add_file_group -type software_driver {} [ipx::current_core]
set_property type mdd [ipx::add_file data/finn_design.mdd [ipx::get_file_groups xilinx_softwaredriver -of_objects [ipx::current_core]]]
set_property type tclSource [ipx::add_file data/finn_design.tcl [ipx::get_file_groups xilinx_softwaredriver -of_objects [ipx::current_core]]]
ipx::update_checksums [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
ipx::save_core [ipx::find_open_core xilinx_finn:finn:finn_design:1.0]
set all_v_files [get_files -filter {USED_IN_SYNTHESIS == 1 && (FILE_TYPE == Verilog || FILE_TYPE == SystemVerilog || FILE_TYPE =="Verilog Header")}]
set fp [open /home/dopark/workspace/zcu102_tuning/prflow_DSE/input_src/finn_cnn_cifar10/_finn_gen_dir/build_dir/vivado_stitch_proj_vlj7ajte/all_verilog_srcs.txt w]
foreach vf $all_v_files {puts $fp $vf}
close $fp
