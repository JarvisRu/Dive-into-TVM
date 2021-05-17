# Create Relay graph - Function usage

## Key idea
- `relay.Call` can call a functiono or a global_function (by GlobalVar)
- function params and arguments can't use the same variable
  - we use 
    - x0 & y0 as parameters
    - dummy_0 & dummy_1 as arguments
- You can update a existing module with new function using
  - item assignment (e.q. `mod2["main"] = main_func`)

## Things you should know
- `tvm.IRModule` can be created
  - by dict (please refer to `python/tvm/ir/module.py`)
  - by `from_expr()`
- Once module is created, you can get its GlobalVar by
  - using name to query : `get_global_var`
  - get the list of GlobalVar contained in the module : `get_global_vars`
- GlobalVar is callable
  - as it has defined its `__call__`

## Related references
None