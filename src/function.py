from interface import Eval

class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def eval(self, env, args):
#        return self.fn(env, args)
        return Integral(138)
