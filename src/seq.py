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
