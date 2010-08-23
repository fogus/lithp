from atom import TRUE
from atom import FALSE
from atom import Symbol
from seq import Seq
from fun import Lambda

# The original Lisp described by McCarthy in his 1960 paper describes the following function set:
#
#    1.  `atom`
#    2.  `car`
#    3.  `cdr`
#    4.  `cond`
#    5.  `cons`
#    6.  `eq`
#    7.  `quote`
#
# Plus two special forms:
#
#    1.  `lambda`
#    2.  `label`
#
# <http://www-formal.stanford.edu/jmc/recursive.html>
#

# The `Lisp` class defines the magnificent seven in terms of the runtime environment built
# thus far (i.e. dynamic scope, lambda, etc.)
class Lisp:
    SPECIAL = "()"
    
    # The magnificent seven are tainted by a pair of useful, but ugly functions
    def dummy(self, env, args):
        print("I do nothing, but you gave me: ")
        self.println(env, args)

    def println(self, env, args):
        for a in args:
            result = a.eval(env)
            self.stdout.write( "%s " % str( result))

        self.stdout.write( "\n")
        return TRUE

    #### `cond`

    # Did you know that McCarthy discovered conditionals?  This is only partially true.  That is,
    # Stephen Kleene defined the notion of a *primitive recursive function* and McCarthy built on
    # that by defining the conditional as a way to simplify the definition of recursive functions.
    # How would you define a recursive function without the use of a conditional in the terminating condition?
    # It turns out that you *can* define recursive functions this way (see fixed point combinators), but the 
    # use of the conditional vastly simplifies the matter.
    #
    # We take conditionals for granted these days so it's difficult to imagine writing programs that
    # were not able to use them, or used a subset of their functionality.
    #
    # The `cond` form is used as follows:
    #
    #     (cond ((atom (quote (a b))) (quote foo)) 
    #           ((atom (quote a))     (quote bar)) 
    #           (t (quote baz)))
    #     
    #     ;=> bar
    #
    def cond(self, env, args):
        for test in args:
            result = test.car().eval(env)

            if result == TRUE:
                return test.data[1].eval(env)

        return FALSE

    #### `eq`

    # Equality is delegated out to the objects being tested, so I will not discuss the mechanics here.  
    # However, examples of usage are as follows:
    #
    #     (eq nil (quote ()))
    #     ;=> t
    #
    #     (eq (quote (a b)) (quote (a b)))
    #     ;=> t
    #
    #     (eq (quote a) (quote b))
    #     ;=> ()
    #
    def eq(self, env, args):
        if len(args) > 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        if args[0].eval(env) == args[1].eval(env):
            return TRUE

        return FALSE

    #### `quote`

    # The `quote` builtin does one thing -- it returns exactly what was given to it without evaluation:
    #
    #     (quote a)
    #     ;=> a
    #     
    #     (quote (car (quote (a b c))))
    #     ;=> (car (quote (a b c)))
    #
    # Of course, you can evaluate the thing that `quote` returns:
    #
    #     (eval (quote (car (quote (a b c)))) (quote ()))
    #     ;=> a
    #
    def quote(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        return args[0]

    #### `car`

    # The original Lisp implementation was written for the IBM 704 by Steve Russell (a genius of the highest
    # order -- also the creator/discoverer of [Spacewar!](http://pdp-1.computerhistory.org/pdp-1/?f=theme&s=4&ss=3) 
    # and continuations).  The somewhat obtuse name for a function that returns the first element of an s-expression
    # derives from the idiosyncracies of the IBM 704 on which Lisp was first implemented.  The `car` function was
    # thus a shortening of the term "Contents of the Address part of Register number" that in itself has a very interesting
    # explanation.  That is, `car` was used to refer to the first half of the wordsize addressed by the IBM 704.  In this
    # particular machine (and many others at that time and since) the wordsize could address more than twice of the
    # actual physical memory.  Taking this particular nuance of the IBM 704 into account, programmers were able to 
    # efficiently create stacks by using the address of the stack's top in one half-word and the negative of the 
    # allocated size in the other (the "Contents of Decrement part of Register number"), like so:
    #
    #      +----------+----------+
    #      |   top    |   -size  |
    #      +----------+----------+
    #           |           |
    #           |           |
    #           |           |
    #           |           |
    #       |   |    |      |
    #     4 |   |    |      |
    #       |   V    |      |
    #     3 | elem3  |      |
    #       |        |      |      
    #     2 | elem2  |      |
    #       |        |      |
    #     1 | elem1  |<-----+
    #       |        |
    #     0 | elem0  |
    #       +--------+
    #     
    # Whenever something was pushed onto the stack the number `1` was added to both half-words.  If the decrement
    # part of the word became zero then that signalled a stack-overflow, that was checked on each push or pop
    # instruction.  However, the use of the car/cdr half-words was used quite differently (McCarthy 1962).  That is,
    # The contents part contained a pointer to the memory location of the actual cons cell (see the documentation for 
    # the next function `cdr` for more information) element, and the decrement part contained a pointer to the
    # next cell:
    #
    #      +----------+----------+    +----------+----------+
    #      |   car    |   cdr    |--->|   car    |   cdr    | ...
    #      +----------+----------+    +----------+----------+
    #
    # The Lisp garbage collector used this structure to facilitate garbage collection by marking referenced chains of
    # cells as negative (sign bit), thus causing them to be ignored when performing memory reclamation.
    #
    def car(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))
        
        # Of course, I do not use pointer arithmetic to implement cons cells...
        cell = args[0].eval(env)
        
        # ... instead I define it in terms of a sequence abstraction.  This is a side-effect of originally
        # hoping to go further with this implementation (e.g. into linear Lisp), but as of now it's a bit heavy-weight
        # for what is actually needed.  But I wouldn't be a programmer if I didn't needlessly abstract.
        if not isinstance(cell, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return cell.car()

    #### `cdr`

    # In the previous function definition (`car`) I used the term cons-cell to describe the primitive structure underlying a 
    # Lisp list.  If you allow me, let me spend a few moments describing this elegant structure, and why it's such an important 
    # abstract data type (ADT).
    #
    # 
    def cdr(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        cell = args[0].eval(env)

        if not isinstance(cell, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return cell.cdr()

    # (cons (quote a) (cons (quote b) (cons (quote c) (quote ()))))
    def cons(self, env, args):
        if(len(args) > 2):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        first = args[0].eval(env)
        second = args[1].eval(env)

        return second.cons(first)

    def atom(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        first = args[0].eval(env)

        if first == FALSE:
            return TRUE
        elif isinstance(first, Symbol):
            return TRUE

        return FALSE

    # (def x (pair (quote (a)) (quote (1))))
    def label(self, env, args):
        if(len(args) != 2):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        env.set(args[0].data, args[1].eval(env))
        return env.get(args[0].data)
