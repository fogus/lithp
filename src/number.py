from interface import Eval
import re


class Number(Eval):
    def __init__( self, v):
        self.value = v

    def __repr__( self):
        return repr(self.value)

    def eval( self, env, args=None):
        return self

class Integral(Number):
    REGEX = re.compile(r'^[+-]?\d+$')

    def __init__( self, v):
        super(Integral, self).__init__(v)

