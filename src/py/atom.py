from interface import Eval, Egal
from seq import Seq, List
from error import UnimplementedFunctionError

class Atom(Eval, Egal):
    def __init__(self, d):
        self.data = d

    def __eq__(self, rhs):
        if isinstance(rhs, Atom):
            return (self.data == rhs.data)
        else:
            return False

class Symbol(Atom):
    def __init__(self, sym):
        Atom.__init__(self, sym)

    def __repr__(self):
        return self.data

    def __hash__(self):
        return hash(self.data)

    def eval(self, env, args=None):
        return env.get(self.data)

TRUE = Symbol("t")
FALSE = List()

class String(Atom, Seq):
    def __init__(self, str):
        super(String, self).__init__(str)

    def __repr__(self):
        return repr(self.data)

    def eval(self, env, args=None):
        return self

    def cons(self, e):
        if e.__class__ != self.__class__ and e.__class__ != Symbol.__class__:
            raise UnimplementedFunctionError("Cannot cons a string and a ", e.__class__.__name__)

        return String(e.data + self.data)

    def car(self):
        return Symbol(self.data[0])

    def cdr(self):
        return String(self.data[1:])
