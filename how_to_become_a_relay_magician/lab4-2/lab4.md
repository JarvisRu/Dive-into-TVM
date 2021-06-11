# Manipulate Relay Grpah - Fetching function in graph

## Key idea
- Use `relay.transform.MergeComposite()` to perfrom patter-based annotation
  - it will make the subgraph that matched with defined-pattern be grouped into a function
- Use `relay.ExprVisitor` to collect the information in the module
- Use `relay.ExprMutator` to modify the module

## Things you should know
- Afte wrapping the subgraph into the function, it'll generate a call node to call that function
  - the **args** of call node is the param/inputs of main graph
  - the **params** of the function of the call node is a dummy name created by TVM
- Since TVM using dict to save params, it uses its name as the key to map the param to variable
  - If we want to compile and run the fetched function directly, we should recover its param name from dummy name to its real name
- In `FunFetcher`, we use 
  - `real_var_name` to save the real name of a variable corresponding to a param
  - `var_in_func_name` to save the dummy name that presents in function 

## Related references
None