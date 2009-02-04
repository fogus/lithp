from interface import Eval

class Seq(Eval):
    def __init__( self):
        self.data = None

    def car(self):
        pass

    def cdr(self):
        pass

    def cons(self):
        pass

    # The following four functions needed for iterability
    def __iter__(self):
        pass

    def __len__(self):
        pass

    def __contains__(self, e):
        pass

    def __getitem__(self, e):
        pass


class List(Seq):
    def __init__(self, l=None):
        super(List, self).__init__()

        if l is None:
            self.data = []
        else:
            self.data = l

    def car(self):
        return self.data[0]

    def cdr(self):
        try:
            return List(self.data[1:])
        except:
            return List([])

    def cons(self, e):
        n = List(self.data[:])
        ndata.insert(0, e)
        return n

    def eval(self, env, args=None):
        form = self.car().eval(env)

        return form.eval(env, self.cdr())

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __contains__(self, e):
        return e in self.data

    def __getitem__(self, e):
        return self.data[e]

