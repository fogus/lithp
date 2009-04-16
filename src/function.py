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
    def __init__(self, n, b):
        self.names = n
        self.body =  b

    def __repr__(self):
        return "<lambda %s>" % id(self)

    def store_bindings(self, containing_env):
        containing_env.push()

    def eval(self, env, args):
        values = [a for a in args]

        if len(values) != len(self.names):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(len(self.names), len(args)))

        LITHP = env.get("__lithp__")

        store_bindings(LITHP)

        for i in range(len(values)):
            LITHP.environment.binds[self.names[i].data] = values[i].eval(LITHP.environment)

        ret = FALSE
        for form in self.body:
            ret = form.eval(LITHP.environment)

        LITHP.pop()
        return ret

class Closure(Lambda):
    def __init__(self, e, n, b):
        super(Lambda, self).__init__(n, b)
        self.env = e

    def __repr__(self):
        return "<lexical closure %s>" % id(self)

    def store_bindings(self, containing_env):
        containing_env.push(self.env.binds)


import lithp
