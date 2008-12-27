from interface import Evalable


class Function(Evalable):
    def __init__(self, fn):
        self.fn = fn

    def eval(self, env, args):
        return self.fn(env, args)
