This branch is just to create some different benchmarks that would fit in single, double or quad pages.
Similar benchmarks are used in https://github.com/dj-park/isFit too.

#### Setup
If you install Vitis on **/tools/Xilinx**, you should set **Xilinx_dir** 
in [./common/configure/configure.xml](./common/configure/configure.xml) as below.
```xml
  <spec name = "Xilinx_dir"         value = "/tools/Xilinx/Vitis/2022.1/settings64.sh" />
```

#### Run
Select the benchmark in the first line of the `Makefile`. Then,
   ```
   make syn -j$(nproc)
   ```
This will run HLS and synthesis for each operator in parallel.

#### Report
   ```
   make report_syn
   ```
This will print out post-synthesis resource estimates or design analysis estimates for each operator.

#### Parameterize
You can tweak some param values in `typedefs.h` file to generate a range of different sizes of operators.
For example, in [./input_src/digit_rec_BRAM/host/typedefs.h](./input_src/digit_rec_BRAM/host/typedefs.h),
try different values of `K_CONST`, `IMAGE_SIZE`, or `IMAGE_WIDTH`.
Also, you can easily add new operator by yourself. 
For examlpe, there are currently only 5 operators for digit_rec_BRAM benchmark ([./input_src/digit_rec_BRAM/operators/](./input_src/digit_rec_BRAM/operators/)).
But you can you can add a new operator like `update_knn_15.cpp` that has `#define PAR_FACTOR 150`.
Make sure that you add the new operator to [./input_src/digit_rec_BRAM/operators/specs.json](./input_src/digit_rec_BRAM/operators/specs.json) file as well.
