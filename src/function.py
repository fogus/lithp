from interface import Eval
from atom import FALSE


class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def __repr__( self):
        return "<built-in function %s>" % id( self.fn)

    def eval(self, env, args):
        return self.fn(env, args)


class Lambda(Eval):
    def __init__(self, e, a, b):
        self.env =  e
        self.args = a
        self.body = b

    def __repr__( self):
        return "<lambda %s>" % id(self)

    def eval(self, env, args):
        print("foo")

        return FALSE
