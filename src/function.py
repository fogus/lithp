from interface import Eval

class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def __repr__( self):
        return "<built-in function %s>" % id( self.fn)

    def eval(self, env, args):
        return self.fn(env, args)
