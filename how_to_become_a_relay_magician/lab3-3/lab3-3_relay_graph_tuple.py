from tvm import relay
import tvm

dummy_0 = relay.var("dummy_0", shape=(2, 2))
dummy_1 = relay.var("dummy_1", shape=(2, 2))
def gen_func():
    x0 = relay.var("x0", shape=(2, 2))
    y0 = relay.var("y0", shape=(2, 2))
    compute = relay.subtract(relay.add(x0, y0), relay.multiply(x0, y0))
    relu = relay.nn.relu(compute)
    return relay.Function([x0, y0], relu, relay.TensorType((2, 2), dtype="float32"))

# case 1
func_1 = gen_func()
func_2 = gen_func()
func_call_1 = relay.Call(func_1, [dummy_0, dummy_1])
func_call_2 = relay.Call(func_2, [dummy_0, func_call_1])
tuple_call = relay.Tuple([func_call_1, func_call_2])
ret_type = relay.TensorType((2, 2), dtype="float32")
main_func = relay.Function([dummy_0, dummy_1], tuple_call, relay.TupleType([ret_type, ret_type]))
mod = tvm.IRModule.from_expr(main_func)
print("case 1:\n", mod)

# case 2
dummy_tup = relay.Var("dummy_tup", type_annotation=relay.TupleType([relay.TensorType((2, 2), dtype="float32"), relay.TensorType((2, 2), dtype="float32")]))
tup_get_0 = relay.TupleGetItem(dummy_tup, 0)
tup_get_1 = relay.TupleGetItem(dummy_tup, 1)
func_call_1 = relay.Call(func_1, [tup_get_0, tup_get_1])
func_call_2 = relay.Call(func_2, [tup_get_0, func_call_1])
main_func = relay.Function([dummy_tup], func_call_2, relay.TensorType((2, 2), dtype="float32"))
mod2 = tvm.IRModule.from_expr(main_func)
print("case 2:\n", mod2)