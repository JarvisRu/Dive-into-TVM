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
main_func = relay.Function([dummy_0, dummy_1], func_call_2, relay.TensorType((2, 2), dtype="float32"))
mod = tvm.IRModule.from_expr(main_func)
print("case 1:\n", mod)

# case 2
mod2 = tvm.IRModule({"func1" : func_1, "func2" : func_2})
gv1 = mod2.get_global_var("func1")
gv2 = mod2.get_global_var("func2")
# mod.ad
func_call_1 = relay.Call(gv1, [dummy_0, dummy_1])
func_call_2 = relay.Call(gv2, [dummy_0, func_call_1])
main_func = relay.Function([dummy_0, dummy_1], func_call_2, relay.TensorType((2, 2), dtype="float32"))
mod2["main"] = main_func
print("case 2:\n", mod2)