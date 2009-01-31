from interface import Eval


class Number(Eval):
    def __init__( self, v):
        self.value = v

    def __repr__( self):
        return repr(self.value)

    def eval( self, env, args=None):
        return self
