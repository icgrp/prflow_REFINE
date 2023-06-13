import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',         '--build_dir', default='./_prflow_DSE')
    args = parser.parse_args()
    build_dir = args.build_dir

    from finn.util.basic import make_build_dir
    from finn.util.visualization import showInNetron
    import os
        
    # build_dir = os.environ["FINN_BUILD_DIR"]
    # build_dir = "./"

    import onnx
    from finn.util.test import get_test_model_trained
    import brevitas.onnx as bo
    from qonnx.core.modelwrapper import ModelWrapper
    from qonnx.transformation.infer_shapes import InferShapes
    from qonnx.transformation.fold_constants import FoldConstants
    from qonnx.transformation.general import GiveReadableTensorNames, GiveUniqueNodeNames, RemoveStaticGraphInputs

    cnv = get_test_model_trained("CNV", 1, 1)
    bo.export_finn_onnx(cnv, (1, 3, 32, 32), build_dir + "/end2end_cnv_w1a1_export.onnx")
    model = ModelWrapper(build_dir + "/end2end_cnv_w1a1_export.onnx")
    model = model.transform(InferShapes())
    model = model.transform(FoldConstants())
    model = model.transform(GiveUniqueNodeNames())
    model = model.transform(GiveReadableTensorNames())
    model = model.transform(RemoveStaticGraphInputs())
    model.save(build_dir + "/end2end_cnv_w1a1_tidy.onnx")

    from finn.util.pytorch import ToTensor
    from qonnx.transformation.merge_onnx_models import MergeONNXModels
    from qonnx.core.datatype import DataType

    model = ModelWrapper(build_dir+"/end2end_cnv_w1a1_tidy.onnx")
    global_inp_name = model.graph.input[0].name
    ishape = model.get_tensor_shape(global_inp_name)
    # preprocessing: torchvision's ToTensor divides uint8 inputs by 255
    totensor_pyt = ToTensor()
    chkpt_preproc_name = build_dir+"/end2end_cnv_w1a1_preproc.onnx"
    bo.export_finn_onnx(totensor_pyt, ishape, chkpt_preproc_name)

    # join preprocessing and core model
    pre_model = ModelWrapper(chkpt_preproc_name)
    model = model.transform(MergeONNXModels(pre_model))
    # add input quantization annotation: UINT8 for all BNN-PYNQ models
    global_inp_name = model.graph.input[0].name
    model.set_tensor_datatype(global_inp_name, DataType["UINT8"])

    from qonnx.transformation.insert_topk import InsertTopK
    from qonnx.transformation.infer_datatypes import InferDataTypes

    # postprocessing: insert Top-1 node at the end
    model = model.transform(InsertTopK(k=1))
    # chkpt_name = build_dir+"/end2end_cnv_w1a1_pre_post.onnx"
    chkpt_name = build_dir+"/model.onnx" # final model
    # tidy-up again
    model = model.transform(InferShapes())
    model = model.transform(FoldConstants())
    model = model.transform(GiveUniqueNodeNames())
    model = model.transform(GiveReadableTensorNames())
    model = model.transform(InferDataTypes())
    model = model.transform(RemoveStaticGraphInputs())
    model.save(chkpt_name)


    # Generate HLS source codes
    import onnx
    import torch
    import finn.builder.build_dataflow as build
    import finn.builder.build_dataflow_config as build_cfg

    import finn.builder.build_dataflow as build
    import finn.builder.build_dataflow_config as build_cfg
    import os
    import shutil

    model_file = build_dir + "/model.onnx"
    folding_config_file = build_dir + "/folding_config.json"

    rtlsim_output_dir = "output_ipstitch_ooc_rtlsim"

    #Delete previous run results if exist
    if os.path.exists(rtlsim_output_dir):
        shutil.rmtree(rtlsim_output_dir)
        print("Previous run results deleted!")

    cfg_stitched_ip = build.DataflowBuildConfig(
        output_dir          = rtlsim_output_dir,
        folding_config_file = folding_config_file,
        mvau_wwidth_max     = 80,
        target_fps          = 1000000,
        synth_clk_period_ns = 10.0,
        fpga_part           = "xczu9eg-ffvb1156-2-e",
        generate_outputs=[
    #         build_cfg.DataflowOutputType.STITCHED_IP,
    #         build_cfg.DataflowOutputType.RTLSIM_PERFORMANCE,
            build_cfg.DataflowOutputType.OOC_SYNTH,
        ],
        default_mem_mode = build_cfg.ComputeEngineMemMode.CONST
    )

    build.build_dataflow_cfg(model_file, cfg_stitched_ip)
