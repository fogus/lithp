from interface import Eval
from seq import List


class Atom(Eval):
    def __init__( self, d):
        self.data = d

    def __eq__(self, rhs):
        if isinstance(rhs, Atom):
            return (self.data == rhs.data)
        else:
            return False

class Symbol(Atom):
    def __init__(self, sym):
        super(Symbol, self).__init__(sym)

    def __repr__(self):
        return self.data

    def __hash__(self):
        return hash(self.data)

    def eval(self, env, args=None):
        return env.get(self.data)


class String(Atom):
    def __init__(self, str):
        super(String, self).__init__(str)

    def __repr__(self):
        return repr(self.string)

    def eval(self, env, args=None):
        return self.string

TRUE = Symbol("t")
FALSE = List()
