from interface import Eval, Egal
from error import UnimplementedFunctionError

class Seq(Eval, Egal):
    def __init__( self):
        self.data = None

    def car(self):
        return self.data[0]

    def cdr(self):
        raise UnimplementedFunctionError("Function not yet implemented for ", self.__class__.__name__)

    def cons(self, e):
        raise UnimplementedFunctionError("Function not yet implemented for ", self.__class__.__name__)

    # The following four functions needed for iterability
    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __contains__(self, e):
        return e in self.data

    def __getitem__(self, e):
        return self.data[e]

    def __eq__(self, rhs):
        if not isinstance(rhs, Seq):
            return False

        if len(self) != len(rhs):
            return False

        for i in range(len(self.data)):
            if not self.data[i] == rhs.data[i]:
                return False

        return True


class List(Seq):
    def __init__(self, l=None):
        Seq.__init__(self)

        if l is None:
            self.data = []
        else:
            self.data = l

    def cdr(self):
        try:
            return List(self.data[1:])
        except:
            return List([])

    def cons(self, e):
        ret = List(self.data[:]) # bugfix 1234977437
        ret.data.insert(0, e)
        return ret

    def eval(self, env, args=None):
        form = self.car().eval(env)

        return form.eval(env, self.cdr())

    def __repr__(self):
        if self.data == []:
            return "()"

        ret = "(%s" % self.data[0]
        for e in self.data[1:]:
            ret = ret + " %s" % e

        return ret + ")"
