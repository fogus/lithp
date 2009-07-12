from interface import Eval
import re
import types


class Number(Eval):
    def __init__( self, v):
        self.data = v

    def __repr__( self):
        return repr(self.data)

    def eval( self, env, args=None):
        return self

    def __eq__(self, rhs):
        if isinstance(rhs, Number):
            return (self.data == rhs.data)
        else:
            return False

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

