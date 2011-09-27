from interface import Eval, Egal
from seq import Seq, List
from error import UnimplementedFunctionError

#### Atoms

# McCarthy's Lisp defined two fundamental types: lists and atoms.  The class `Atom`
# represents that latter type.  Originally an atom was defined as simply something
# immutable and unique.
#
# There is currently a disparity in the implementation of Lithp in that atoms are created
# and stored within the contextual environment and therefore their uniqueness cannot
# be guaranteed.  This is an artifact of implementation and not a problem in emulating
# McCarthy's Lisp.
#
# One point of note is that in the original there were **no numbers**.  Instead, numbers
# had to be represented as lists of atoms, proving to be quite slow. (McCarthy 1979)  Numbers
# were not implemented until after Lisp 1.5 (**TODO** what version?)
class Atom(Eval, Egal):
    def __init__(self, d):
        self.data = d

    def __eq__(self, rhs):
        if isinstance(rhs, Atom):
            return (self.data == rhs.data)
        else:
            return False

#### Symbols

# The symbol was the basic atom in Lisp 1 and served as the basic unit of data.  In his early
# papers McCarthy freely mixes the terms atom and symbol.
class Symbol(Atom):
    def __init__(self, sym):
        Atom.__init__(self, sym)

    def __repr__(self):
        return self.data

    def __hash__(self):
        return hash(self.data)

    def eval(self, env, args=None):
        return env.get(self.data)

#### Truth

# The first symbol created is `t`, corresponding to logical true.  It's a little unclear to me
# how this operated in the original Lisp.  That is, was the symbol `t` meant as logical truth or
# were symbols true by default?  I suppose I will have to dig deeper for an answer.
TRUE = Symbol("t")

# Logical false is easy -- the empty list
FALSE = List()

#### Strings

# In McCarthy's original paper (McCarthy 1960) he uses the term *string* to mean symbols, but later on
# he mentions them in a different context reagrding their role in something called *linear Lisp*.  I started
# down the path of implementing linear Lisp also, but got sidetracked.  Perhaps I will find time to complete it
# sometime in the future.  In the meantime strings are provided, but are not compliant with the Lisp 1
# formalization.
#
# The first point of note is that the `String` class implements the `Seq` abstraction.  This is needed by the
# definition of linear Lisp that defines three functions of strings: `first`, `rest`, and `combine`.  If you play
# around with strings in the Lithp REPL you'll see that they conform to the linear Lisp formalism.
#
# This class will likely change in the future.
class String(Atom, Seq):
    def __init__(self, str):
        Atom.__init__(self, str)

    def __repr__(self):
        return repr(self.data)

    def eval(self, env, args=None):
        return self

    # The `cons` behavior is (roughly) the same as the `combine` behavior defined in linear Lisp
    # Instead of returning a list however, the string `cons` returns another string.
    # I originally added the ability to `combine` strings and symbols, but I might pull that back.
    def cons(self, e):
        if e.__class__ != self.__class__ and e.__class__ != Symbol.__class__:
            raise UnimplementedFunctionError("Cannot cons a string and a ", e.__class__.__name__)

        return String(e.data + self.data)

    # `car` is roughly the same as `first` in linear Lisp
    def car(self):
        return Symbol(self.data[0])

    # `cdr` is roughly the same as `rest` in linear Lisp
    def cdr(self):
        return String(self.data[1:])
