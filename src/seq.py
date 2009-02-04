from interface import Eval

class Seq(Eval):
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
        if l is None:
            self.nodes = []
        else:
            self.nodes = l

    def car(self):
        return self.nodes[0]

    def cdr(self):
        try:
            return List(self.nodes[1:])
        except:
            return List([])

    def cons(self, e):
        n = List(self.nodes[:])
        n.nodes.insert(0, e)
        return n

    def eval(self, env, args=None):
        form = self.car().eval(env)

        return form.eval(env, self.cdr())

    def __iter__(self):
        return self.nodes.__iter__()

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, e):
        return e in self.nodes

    def __getitem__(self, e):
        return self.nodes[e]