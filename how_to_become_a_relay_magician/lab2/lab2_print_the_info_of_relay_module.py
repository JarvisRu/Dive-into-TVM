import onnx
from tvm import relay

onnx_model = onnx.load("../../materials/simple_mnist.onnx")
mod, params = relay.frontend.from_onnx(onnx_model)
print("mod : ", mod)

class MyVisitor(relay.ExprVisitor):

    def __init__(self):
        super().__init__()

    def visit_function(self, fn):
        print("fn params : ", fn.params)
        print("fn ret_type : ", fn.ret_type)
        # traverse entire grpah by visit body
        self.visit(fn.body)

    def visit_call(self, call):
        print("Visit call")
        self.visit(call.op)
        print("call's args : ", call.args)
        for a in call.args:
            self.visit(a)

    def visit_var(self, var):
        print("var name ", var.name_hint)
        print("var type_annotation ", var.type_annotation)

    def visit_op(self, op):
        print("Visit op name : ", op.name)

    def __call__(self, fn):
        self.visit(fn)

MyVisitor()(mod["main"])