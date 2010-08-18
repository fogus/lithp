# I one day plan to create a whole battery of errors so that the REPL provides a detailed report whenever
# something goes wrong.  That day is not now.

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnimplementedFunctionError(Error):
    def __init__(self, message, thing):
        self.thing = thing
        self.message = message

    def __str__(self):
        return self.message + repr(self.thing)

class EvaluationError(Error):
    def __init__(self, env, args, message):
        self.env = env
        self.args = args
        self.message = message

    def __str__(self):
        return self.message + ", " + repr(self.args) + " in environment " + self.env.level
