# Print the info of relay module

## Key idea 
- ExprVisitor: traverse Relay IR without modifying it
- We can simply inherit it to override the visit function
- You can use `isinstance(a, type)` to check type

## Things you should know
- While traversing, it will start from the root of the relay tree
  - the root is the output of Relay IR (The end node)
- The following fields are super important
    - Function
        - `fn.body`: details (graph structure) are saved in body
        - `fn.params`: to define the used variable
        - `fn.ret_type`
    - Call: The basic call node
        - `call.op`: The operation to be called 
            - `if isinstance(call.op, relay.op)`
                - print `call.op.name`
        - `call.args`
    - Var
        - As local variable within the function, it need to be defined in `fn.params`, or
            - it becomes a `free_vars`
        - `var.name_hint`: Name of var
        - `var.type_annotation`
            - can get shape, dtype by `.dtype` `.shape`
    - Constants
        - `const.data`
    - Global_var
        - `gv.name_hint`: Name of gv


## Related references
- None