# we can simply load model from frontend API
# we dont show it since it has showed in TVM docs

# Load model from the benchmark saving in the testing
import tvm.relay.testing

def print_with_type(obj):
    print(f"Type : {type(obj)} / {obj}")

mod, params = tvm.relay.testing.mobilenet.get_workload()

# mod is tvm.IRModule which represent the arch of model
print_with_type(mod)

print("--")

# params is the dict of name to tvm.NDArray which saves the weight that model need
print_with_type(params)