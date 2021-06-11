# Manipulate Relay Grpah

## Key idea
- You can use `relay.ExprMutator` to modify graph's structure
- Args of `relay.Call` can be chained with other Ops
  - embedding handcrafted Ops

## Things you should know
- Except for handling with customize behavior, we can use `super().visit()` to do what super class does.

## Related references
None