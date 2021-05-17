from tvm import relay
import tvm

x0 = relay.var("x0", shape=(2, 2))
y0 = relay.var("y0", shape=(2, 2))
compute = relay.subtract(relay.add(x0, y0), relay.multiply(x0, y0))
relu = relay.nn.relu(compute)
func = relay.Function([x0, y0], relu, relay.TensorType((2, 2), dtype="float32"))
mod = tvm.IRModule.from_expr(func)
print(mod)
