from error import UnimplementedFunctionError, EvaluationError

class Eval:
    def eval(self, environment, args=None):
        raise EvaluationError(environment, args, "Evaluation error")

class Egal:
    def __eq__(self, rhs):
        raise UnimplementedFunctionError(rhs, "Function not yet implemented")

