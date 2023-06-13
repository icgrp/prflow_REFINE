1) Make sure user directory in build_dataflow.sh is correct
2) source build_dataflow.sh 
   to generate HLS code in FINN_HOST_BUILD_DIR
   For now, it's generating HLS codes for pre-trained CNN-6 (VGG net based)
3) python finn_hls_post_process.py 
   to create wrapped HLS functions in ./src/operators/
4) cp ./src/operators/* ../input_src/test/operators/