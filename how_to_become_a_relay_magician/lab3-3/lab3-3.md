# Create Relay graph - Tuple usage

## Key idea
- `relay.Tuple` can be used to aggregate the result
  - The fields can containe `relay.Expr`
  - accompany with `relay.TupleType` as return type
    - with `relay.Type` in fields
- `relay.TupleGetItem` can be used to fetch the field in the tuple
  - e.q. %0 is a tuple with 3 fields
    - `%0.x` while **x** is the index of the field

## Things you should know
- The difference between `relay.var` & `relay.Var`
  - Both of them create a `relay.Var`
  - First one is to construct with `name(str)`, `shape`, `dtype(str)`
  - Second one is to construct with `name(str)`, `(type_annotation)relay.Type`

## Related references
None