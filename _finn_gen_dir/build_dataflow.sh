##########################
## User directory setup ##
##########################

# use pre-build image
export FINN_DOCKER_TAG=maltanar/finn:dev_latest
export FINN_DOCKER_PREBUILT=1
export FINN_HOST_BUILD_DIR=/home/dopark/workspace/zcu102_tuning/prflow_DSE/_finn_gen_dir/build_dir
# rm previously generated build_dir
rm -rf $FINN_HOST_BUILD_DIR

export FINN_V21_DIR=/home/dopark/workspace/finn_v21.1

##########################################################################

# Generate new folding_config.json
python gen_folding_config.py

# Generate model.onnx (or use pre-trained) and generate HLS codes
cp folding_config.json ${FINN_V21_DIR}/_prflow_DSE
cp finn_cnn_gen.py $FINN_V21_DIR
cd $FINN_V21_DIR
bash ./run-docker.sh python finn_cnn_gen.py

# cd back to prflow dir
cd /home/dopark/workspace/zcu102_tuning/prflow_DSE/_finn_gen_dir

# Create wrapper, post process
python finn_hls_post_process.py 
