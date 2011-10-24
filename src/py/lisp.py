# RIP John McCarthy 1927.09.04 - 2011.10.23

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
#    1.  `lambda` *(defined in [lithp.py](index.html))*
#    2.  `label`
#
# <http://www-formal.stanford.edu/jmc/recursive.html>
#

# The `Lisp` class defines the magnificent seven in terms of the runtime environment built
# thus far (i.e. dynamic scope, lambda, etc.).
#
class Lisp:
    SPECIAL = "()"
    
    # The magnificent seven are tainted by a pair of useful, but ugly functions, `dummy` and `println`
    # purely for practical matters.
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
    #           |           |        size goes toward zero                  
    #           |           |                  |                            
    #           |           |                  |                            
    #           |           |                  v                            
    #       |   |    |      |                                               
    #     4 |   |    |      |                                               
    #       |   V    |      |                                               
    #     3 | elem3  |      |                                               
    #       |        |      |                  ^                            
    #     2 | elem2  |      |                  |                                 
    #       |        |      |                  |                                 
    #     1 | elem1  |<-----+           stack grows up                          
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
    # The `car` function works as follows:
    #
    #     (car (quote (a b c)))
    #     ;=> a
    # 
    # The car of an empty list is an error (TODO: check if this is the case in McCarthy's Lisp)
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
    # Lisp from the beginning was built with the philosophy that lists should be a first-class citizen of the language; not only in 
    # the realm of execution, but also generation and manipulation.   If you look at my implementation of `List` in [seq.py](seq.html)
    # you'll notice that it's pretty standard fare.  That is, it, like most lisp implementations is backed by a boring sequential store
    # where one element conceptually points to the next and blah blah blah.  **Boring**.  Where the cons-cell shines is that it is a 
    # very general purpose ADT that can be used in a number of ways, but primary among them is the ability to represent the list.
    #
    # Lists in the early Lisp was precisely a chain of cons cells and the operators `car` and `cdr` pointed to very
    # specific implementation details that over time became generalized to mean "the first thing" and "the rest of the things"
    # respectively.  But the fact remains that the cons cell solves a problem that is often difficult to do properly.  That is,
    # how could Lisp represent a container that solved a number of requirements:
    #
    # * Represents a list
    # * Represents a pair
    # * Implementation efficiency
    # * Heterogeneous
    #
    # It would be interesting to learn the precise genesis of the idea behind the cons cell, but I imagine that it must have provoked
    # a eureka moment.  
    #
    # I've already discussed how the IBM 704 hardware was especially ammenable to solving this problem efficiently, but the other points
    # bear further consideration.  Lisp popularly stands for "LISt Processing language" but as I explained, the basic unit of data was
    # instead the cons cell structure.  The fact of the matter is that the cons cell serves as both the implementation detail for lists
    # **and** the abstraction of a pair, all named oddly as if the implementation mattered.  If Lisp had originally gone whole hog into the
    # abstraction game, then `car` and `cdr` would have been `first` and `rest` and would have spared the world decades of whining.
    # 
    # Modern Lisps like Common Lisp rarely implement lists as chains of cons cells.  Instead, it's preferred to create proper lists
    # with the `list` or `list*` functions and access them via `first` or `rest` (`cons` still persists thanks to its more general
    # meaning of "construct") and to only use `car` and `cdr` when dealing with cons cells.  You can probably tell a lot about the
    # level of knowledge for a Lisp programmer by the way that they construct and access lists.  For example, a programmer like
    # myself whose exposure to Common Lisp has been entirely academic, you will probably see a propensity toward the use of `car` and
    # `cdr` instead of leveraging the more expressive sequence abstractions.
    #
    # The `cdr` function works as follows:
    #
    #     (cdr (quote (a b c)))
    #     ;=> (b c)
    # 
    # The cdr of an empty list is an empty list (TODO: check if this is the case in McCarthy's Lisp)
    #
    def cdr(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        cell = args[0].eval(env)

        if not isinstance(cell, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return cell.cdr()

    #### cons

    # So if Common Lisp has a more general sequence abstraction, then why would we still want to keep the cons cell?  The reason is
    # that the cons cell is more flexible than a sequence and allows for a more intuitive way to build things like trees, pairs, and
    # to represent code structure.
    # 
    # This function simply delegates the matter of consing to the target object.
    #
    # The `cons` function works as follows:
    #
    #     (cons (quote a) nil)
    #     ;=> (a)
    #
    #     (cons (quote a) (quote (b c)))
    #     ;=> (a b c)
    #
    #     (cons (quote a) (quote b))
    #     ;=> Error
    # 
    # I've agonized long and hard over wheter or not to implement McCarthy Lisp as the language described in *Recursive functions...*
    # as the anecdotal version only partially described in the *LISP 1.5 Programmer's Manual* and in most cases the former was my
    # choice.  The creation of "dotted pairs" (I believe) was not an aspect of the original description and therefore is not represented
    # in Lithp.  Sadly, I think that in some cases these version are mixed because I originally went down the path of creating a version of 
    # Litho compatible with linear Lisp and Lisp 1.5, so this is a product of some pollution in the varying ideas.
    #
    def cons(self, env, args):
        if(len(args) > 2):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        first = args[0].eval(env)
        second = args[1].eval(env)

        return second.cons(first)

    #### atom

    # Checks if a function is an atom; returns truthy if so.  One thing to note is that the empty
    # list `()` is considered an atom because it cannot be deconstructed further.
    #
    # The `atom` function works as follows:
    #
    #     (atom (quote a))
    #     ;=> t
    #     
    #     (atom nil)
    #     ;=> t
    #     
    #     (atom (quote (a b c)))
    #     ;=> ()
    #
    # Recall that the empty list is falsity.
    #
    def atom(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        first = args[0].eval(env)

        if first == FALSE:
            return TRUE
        elif isinstance(first, Symbol):
            return TRUE

        return FALSE

    #### label

    # Defines a named binding in the dynamic environment.
    def label(self, env, args):
        if(len(args) != 2):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))
        
        # Notice that the first argument to `label` (a symbol) is **not** evaluated.  This is the key difference between
        # a Lisp function and a special form (and macro, but I will not talk about those here).  That is, in *all*
        # cases the arguments to a function are evaluated from left to right before being passed into the function.
        # Conversely, special forms have special semantics for evaluation that cannot be directly emulated or implemented 
        # using functions.
        env.set(args[0].data, args[1].eval(env))
        return env.get(args[0].data)
