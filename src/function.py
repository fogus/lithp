from interface import Eval
from atom import FALSE


class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def __repr__( self):
        return "<built-in function %s>" % id( self.fn)

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
    def __init__(self, e, bnd, b):
        self.env =   e
        self.binds = bnd
        self.body =  b

    def __repr__( self):
        return "<lambda %s>" % id(self)

    def eval(self, env, args):
        values = [a for a in args]

        if len(values) != len(self.binds):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(len(self.binds), len(args)))

        ME = env.get("lithp")

        if self.env:
            ME.push(self.env.binds)
        else:
            ME.push()

        for i in range(len(values)):
            ME.environment.binds[self.binds[i].data] = values[i].eval(env)

        ret = FALSE
        for form in self.body:
            ret = form.eval(ME.environment)

        ME.pop()
        return ret

import lithp
