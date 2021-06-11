from tvm import relay
import tvm
import tvm.relay.testing

mod, _ = tvm.relay.testing.mobilenet.get_workload()
print("mod : ", mod)

num_of_conv2d = [0]

def _count_num_of_conv2d(expr):
    if isinstance(expr, relay.Call):
        if isinstance(expr.op, tvm.ir.Op):
            if expr.op.name == "nn.conv2d":
                num_of_conv2d[0] += 1

relay.analysis.post_order_visit(mod["main"], _count_num_of_conv2d)
print("num_of_conv2d : ", num_of_conv2d)

