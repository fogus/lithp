from interface import Eval

class Seq(Eval):
    def car(self):
        pass

    def cdr(self):
        pass

    def cons(self):
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

        return form.eval(env, self.nodes[1:])
