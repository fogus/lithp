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

class LongInt(Number):
    REGEX = re.compile(r'^[+-]?\d+[lL]$')

    def __init__( self, v):
        super(LongInt, self).__init__(v)

class Float(Number):
    REGEX = re.compile(r'^[+-]?(\d+\.\d*$|\d*\.\d+$)')

    def __init__( self, v):
        super(Float, self).__init__(v)

