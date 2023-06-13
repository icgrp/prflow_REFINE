import json, random
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b',         '--bottleneck', required = True)
    args = parser.parse_args()
    bottleneck = args.bottleneck

    print(bottleneck)

    # Based on bottleneck operator, read cur_param.json and 
    # and select better param from params.json, and then
    # write a new cur_param.json






# CNV_OUT_CH_POOL = [(64, False), (64, True), (128, False), (128, True), (256, False), (256, False)]
# INTERMEDIATE_FC_FEATURES = [(256, 512), (512, 512)]
# LAST_FC_IN_FEATURES = 512
# LAST_FC_PER_OUT_CH_SCALING = False
# POOL_SIZE = 2
# KERNEL_SIZE = 3

# def get_divisors(n):
#     divisor_list = []
#     for i in range(1, int(n / 2) + 1):
#         if n % i == 0:
#             divisor_list.append(i)
#     divisor_list.append(n)
#     return divisor_list


# with open('./folding_config_copy.json', 'r') as infile:
#     folding_dict = json.load(infile)

# NUM_LAYERS = 6
# for i in range(NUM_LAYERS):
#     conv_SIMD = -1
#     mva_SIMD = -1
#     mva_PE = -1

#     if i == 0:
#         conv_SIMD = 3 # fixed
#         in_ch = 3
#     else:
#         in_ch = CNV_OUT_CH_POOL[i-1][0]
#     out_ch, is_pool_enabled = CNV_OUT_CH_POOL[i]

#     possible_conv_SIMD_list = get_divisors(in_ch)

#     possible_mva_SIMD_list = get_divisors(KERNEL_SIZE**2 * in_ch)
#     possible_mva_PE_list = get_divisors(out_ch)

#     key = "ConvolutionInputGenerator_" + str(i)
#     if conv_SIMD == -1:
#         conv_SIMD = random.choice(possible_conv_SIMD_list)
#     folding_dict[key]["SIMD"] = conv_SIMD

#     key = "MatrixVectorActivation_" + str(i)
#     mva_SIMD = random.choice(possible_mva_SIMD_list)
#     mva_PE = random.choice(possible_mva_PE_list)

#     folding_dict[key]["SIMD"] = mva_SIMD
#     folding_dict[key]["PE"] = mva_PE

#     # print("layer: " + str(i))
#     # print("ConvolutionInputGenerator_" + str(i))
#     # print("possible_conv_SIMD_list: ")
#     # print(possible_conv_SIMD_list)
#     # print()
#     # print("MatrixVectorActivation_" + str(i))
#     # print("possible_mva_SIMD_list: ")
#     # print(possible_mva_SIMD_list)
#     # print("possible_mva_PE_list: ")
#     # print(possible_mva_PE_list)
#     # print()

# for i in range(3):
#     mva_SIMD = -1
#     mva_PE = -1

#     if i == 2:
#         mva_PE = 1

#         in_features = INTERMEDIATE_FC_FEATURES[-1][1]
#         out_features = 10
#     else:
#         in_features, out_features = INTERMEDIATE_FC_FEATURES[i]

#     possible_mva_SIMD_list = get_divisors(in_features)
#     possible_mva_PE_list = get_divisors(out_features)

#     key = "MatrixVectorActivation_" + str(i + NUM_LAYERS)
#     mva_SIMD = random.choice(possible_mva_SIMD_list)
#     if mva_PE == -1:
#         mva_PE = random.choice(possible_mva_PE_list)

#     folding_dict[key]["SIMD"] = mva_SIMD
#     folding_dict[key]["PE"] = mva_PE

#     # print("MatrixVectorActivation_" + str(i + NUM_LAYERS))
#     # print("possible_mva_SIMD_list: ")
#     # print(possible_mva_SIMD_list)
#     # print("possible_mva_PE_list: ")
#     # print(possible_mva_PE_list)
#     # print()


# # folding_dict = json.dumps(folding_dict, indent=4)
# # print(folding_dict)

# with open('./folding_config.json', 'w') as outfile:
#     json.dump(folding_dict, outfile)


# # C: Input channel
# # C': Output channel
# {
#   "Defaults": {},

#   # Layer_0

#   "Thresholding_Batch_0": {
#     "PE": 1,   ## fixed to 1
#     "ram_style": "distributed",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "ConvolutionInputGenerator_0": {
#     "SIMD": 3, ## fixed to 3, divisors of 3 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_0": {
#     "PE": 8,  # divisors of 64 (C')
#     "SIMD": 27, # divisors of 27 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },


#   # Layer_1

#   "ConvolutionInputGenerator_1": {
#     "SIMD": 64, # divisors of 64 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_1": {
#     "PE": 64,  # divisors of 64 (C')
#     "SIMD": 72, # divisors of 576 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "StreamingMaxPool_Batch_0": {
#     "PE": 1 # fixed, only supported for 1D max pool
#   },


#   # Layer_2

#   "ConvolutionInputGenerator_2": {
#     "SIMD": 16, # divisors of 64 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_2": {
#     "PE": 32, # divisors of 128 (C')
#     "SIMD": 72, # divisors of 576 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },


#   # Layer_3

#   "ConvolutionInputGenerator_3": {
#     "SIMD": 16, # divisors of 128 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_3": {
#     "PE": 32, # divisors of 128 (C')
#     "SIMD": 72, # divisors of 1152 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "StreamingMaxPool_Batch_1": {
#     "PE": 1 # fixed, only supported for 1D max pool
#   },


#   # Layer_4

#   "ConvolutionInputGenerator_4": {
#     "SIMD": 2, # divisors of 128 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_4": {
#     "PE": 8, # divisors of 256 (C')
#     "SIMD": 72, # divisors of 1152 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },


#   # Layer_5

#   "ConvolutionInputGenerator_5": {
#     "SIMD": 1, # divisors of 256 (C)
#     "ram_style": "distributed"
#   },
#   "MatrixVectorActivation_5": {
#     "PE": 1, # divisors of 256 (C')
#     "SIMD": 72, # divisors of 2304 (K^2 * C)
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },


#   # Layer_last

#   "MatrixVectorActivation_6": {
#     "PE": 1, # divisors of 512
#     "SIMD": 16, # divisors of 256
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "MatrixVectorActivation_7": {
#     "PE": 1, # divisors of 512
#     "SIMD": 32, # divisors of 512
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "MatrixVectorActivation_8": {
#     "PE": 1, # fixed to 1, divisors of 10
#     "SIMD": 1, # divisors of 512
#     "ram_style": "auto",
#     "resType": "lut",
#     "mem_mode": "const",
#     "runtime_writeable_weights": 0
#   },
#   "LabelSelect_Batch_0": {
#     "PE": 1  ## fixed to 1
#   }
# }