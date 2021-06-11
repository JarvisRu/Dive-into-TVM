import tvm.relay.testing
from tvm import relay

mod, __ = tvm.relay.testing.mobilenet.get_workload()
print(mod)

class Manipulator(relay.ExprMutator):
    def visit_call(self, call):
        if call.op.name == "nn.conv2d":
            activation = call.args[0]
            weight = call.args[1]

            new_act = relay.multiply(activation, relay.const(10))
            new_weight = relay.divide(weight, relay.const(10))

            new_act = relay.cast(new_act, "int32")
            new_weight = relay.cast(new_weight, "int32")

            return relay.Call(self.visit(call.op), [new_act, new_weight], call.attrs)
        else:
            return super().visit_call(call)

    def __call__(self, func):
        return self.visit(func)


mod["main"] = Manipulator()(mod["main"])
print(mod)