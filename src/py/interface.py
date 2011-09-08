# I guess my background as a Java programmer compels me to create pseudo-interfaces.  Is there no hope for the likes of me?

from error import UnimplementedFunctionError, EvaluationError

# Every form in Lithp is evalable
class Eval:
    def eval(self, environment, args=None):
        raise EvaluationError(environment, args, "Evaluation error")

# I read Henry Baker's paper *Equal Rights for Functional Objects or, The More Things Change, The More They Are the Same*
# and got a wild hair about `egal`.  However, it turns out that in McCarthy's Lisp the idea is trivial to the extreme.  Oh well...
# it's still a great paper.  [Clojure](http://clojure.org)'s creator Rich Hickey summarizes `egal` much more succinctly than I ever could:
#
# > ... the only things you can really compare for equality are immutable things, because if you compare two things for equality that
# > are mutable, and ever say true, and they're ever not the same thing, you are wrong.  Or you will become wrong at some point in the future.
#
# Pretty cool huh?
class Egal:
    def __eq__(self, rhs):
        raise UnimplementedFunctionError("Function not yet implemented", rhs)

