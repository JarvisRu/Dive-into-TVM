import tvm.relay.testing
from tvm import relay
from tvm.relay.dataflow_pattern import *

mod, __ = tvm.relay.testing.mobilenet.get_workload()
# print(mod)

class FuncFetcher(relay.ExprVisitor):
    """Fetch desired pattern(function) into a list with information
    With desired pattern is wrapped with a function, this visitor collect functions into list.
    Also, collect the arguments for each desired pattern, create a map to match the 
    argument name with parameter name.
    """
    def __init__(self):
        super().__init__()
        self.target_funcs = set()
        self.recover_map = {}

    def visit_function(self, f):
        self.visit(f.body)

    def visit_call(self, call):
        if isinstance(call.op, relay.Function):
            self.target_funcs.add(call.op)
            
            for idx, arg in enumerate(call.args):
                real_var_name = arg.name_hint if isinstance(arg, relay.Var) else "activation"
                var_in_func_name = call.op.params[idx].name_hint
                self.recover_map[var_in_func_name] = real_var_name
            
        self.visit(call.op)
        for a in call.args:
            self.visit(a)
    
    def __call__(self, fn): 
        self.visit(fn)
        return self.target_funcs, self.recover_map

class RecoverWorker(relay.ExprMutator):
    """With recover_map, replace parameters' name of fetched function with its arguments from main module
    To make fetched function as a individual module, the input is compatiable with original params now
    """
    def __init__(self, recover_map):
        super().__init__()
        self.recover_map = recover_map

    def visit_function(self, fn):
        new_body = self.visit(fn.body)
        new_params = list(relay.analysis.free_vars(new_body))

        return relay.Function(
            new_params,
            new_body,
            None,
            type_params=fn.type_params,
            attrs=None,
        )

    def visit_var(self, var):
        if var.name_hint in self.recover_map:
            recover_as = self.recover_map[var.name_hint]
            if isinstance(recover_as, str):
                new_name = recover_as
                new_var = relay.frontend.common.new_var(new_name,
                                                    shape=var.type_annotation.shape,
                                                    dtype=var.type_annotation.dtype)
                return new_var
            elif isinstance(recover_as, relay.Constant):
                return recover_as
        return var

    def __call__(self, fn): 
        return self.visit(fn)

# define the desired pattern
def conv2d_batch_pattern():
    pat = is_op("nn.conv2d")(wildcard(), wildcard())
    pat = is_op("nn.batch_norm")(pat, wildcard(), wildcard(), wildcard(), wildcard())
    return pat
patterns = [("test.conv2d_batch_pattern", conv2d_batch_pattern())]

mod = relay.transform.InferType()(mod)

# perform pattern-based annotation
annotated_mod = relay.transform.MergeComposite(patterns)(mod)

# collect fetched function into target_funcs, record map of parameter name -> argument name
target_funcs, recover_map = FuncFetcher()(annotated_mod["main"])

# create module individually
fetched_mods = list()
for func in target_funcs:
    fetched_mods.append(tvm.IRModule.from_expr(func))

# recover var name of created module as data name
for fetch_mod in fetched_mods:
    fetch_mod["main"] = RecoverWorker(recover_map)(fetch_mod["main"])
    print(fetch_mod)