##########################
## User directory setup ##
##########################

# use pre-build image
export PRJ_DIR=/home/dopark/workspace/zcu102_tuning/prflow_DSE_bi_22.1
export FINN_DOCKER_TAG=maltanar/finn:dev_latest
export FINN_DOCKER_PREBUILT=1
export FINN_HOST_BUILD_DIR=${PRJ_DIR}/input_src/finn_cnn1/_finn_gen_dir/build_dir
# rm previously generated build_dir
rm -rf $FINN_HOST_BUILD_DIR
rm -rf ./_finn_gen_dir/src/*.cpp
rm -rf ./_finn_gen_dir/src/*.h

export FINN_V22_DIR=/home/dopark/workspace/finn_v22.1

##########################################################################

# Generate folding_config.json based on cur_param.json
# Nothing much.. just change params like 'PE13' TO 'PE'
# python gen_folding_config.py

# Generate model.onnx (or use pre-trained) and generate HLS codes
cp folding_config.json ${FINN_V22_DIR}/_prflow_DSE/folding_config.json
cp ./_finn_gen_dir/finn_cnn_gen.py $FINN_V22_DIR
cd $FINN_V22_DIR
bash ./run-docker.sh python finn_cnn_gen.py

# cd back to prflow dir
cd ${PRJ_DIR}/input_src/finn_cnn1
