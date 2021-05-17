# Load a model from frontend API

## Key idea
- Various model format can be imported into TVM with frontend API
- Relay module can be print beautifully by 

## Things you need to know
- The model in TVM is basically constructed by two objects
  - relay module (tvm.IRModule)
  - params (a dict of param name to tvm.NDArray)
- If you have onnx file in your filesystem, please open it by [netron](https://lutzroeder.github.io/netron/)
  - to check the arch with model formated in Relay
- IRModule has the map that maps
  - global_var to function
  - The default global_var is `main`

## Related references
- Where tvm.IRModule is defined in
  - Python : `python/tvm/ir/module.py`
    - it call cpp function by **_ffi_** 
  - Cpp : `include/tvm/ir/module.h`
    - where it implement the function
