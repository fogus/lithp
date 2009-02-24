class Eval:
    def eval(self, environment, args=None):
        raise Error ["Unimplemented"]

class Egal:
    def __eq__(self, rhs):
        raise Error ["Unimplemented"]

