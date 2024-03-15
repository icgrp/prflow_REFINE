This branch is just to create some different benchmarks that would fit in single, double or quad pages.
Similar benchmarks are used in https://github.com/dj-park/isFit too.

#### Setup
If you install Vitis on **/tools/Xilinx**, you should set **Xilinx_dir** 
in [./common/configure/configure.xml](./common/configure/configure.xml) as below.
```xml
  <spec name = "Xilinx_dir"         value = "/tools/Xilinx/Vitis/2022.1/settings64.sh" />
```

#### Run
   ```
   make syn -j$(nproc)
   ```

#### Parameterize
You can tweak some param values in typedefs.h file to generate a range of different sizes of operators.
For example, in [./input_src/digit_rec_BRAM/host/typedefs.h](./input_src/digit_rec_BRAM/host/typedefs.h),
try different values of `K_CONST`, `IMAGE_SIZE`, or `IMAGE_WIDTH`.
