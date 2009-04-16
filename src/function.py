from interface import Eval
from atom import FALSE

class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def __repr__( self):
        return "<built-in function %s>" % id(self.fn)

    def eval(self, env, args):
        return self.fn(env, args)

# ((lambda (x) x) 42)
# ((lambda (x y) (eq x y)) 42 138)
# ((lambda (f x y) (f x y)) (lambda (a b) (eq a b)) 1 2)
# ((lambda (f x y) (f x y)) eq 1 2)
#
# TODO:
# There is still a major issue with bindings.  Run consecutively:
# (label x (pair (quote (a)) (quote (1))))
# (label x (pair (quote (a)) (quote (1))))
class Lambda(Eval):
    def __init__(self, e, n, b):
        self.env =   e
        self.names = n
        self.body =  b

    def __repr__( self):
        return "<lambda %s>" % id(self)

    def eval(self, env, args):
        values = [a for a in args]

        if len(values) != len(self.names):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(len(self.names), len(args)))

        LITHP = env.get("__lithp__")

        if self.env:
            LITHP.push(self.env.binds)
        else:
            LITHP.push()

        for i in range(len(values)):
            LITHP.environment.binds[self.names[i].data] = values[i].eval(LITHP.environment)

        ret = FALSE
        for form in self.body:
            ret = form.eval(LITHP.environment)

        LITHP.pop()
        return ret

import lithp
