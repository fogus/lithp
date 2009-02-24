class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnimplementedFunctionError(Error):
    def __init__(self, args, message):
        self.args = args
        self.message = message

    def __str__(self):
        return self.message + ", " + repr(self.args)

class EvaluationError(Error):
    def __init__(self, env, args, message):
        self.env = env
        self.args = args
        self.message = message

    def __str__(self):
        return self.message + ", " + repr(self.args) + " in environment " + self.env.level
