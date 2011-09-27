from interface import Eval
from atom import FALSE

# Functions

# As you might have imagined, McCarthy's Lisp derives much of its power from the function.  The `Function`
# class is used exclusively for *builtin* functions (i.e. the magnificent seven).  Each core function is
# implemented as a regular Python method, each taking an `Environment` and its arguments.
class Function(Eval):
    def __init__(self, fn):
        self.fn = fn

    def __repr__( self):
        return "<built-in function %s>" % id(self.fn)

    # Evaluation just delegates out to the builtin.
    def eval(self, env, args):
        return self.fn(env, args)

# &lambda; &lambda; &lambda;

# The real power of McCarthy's Lisp srpings from Alonzo Chruch's &lambda;-calculus.
class Lambda(Eval):
    def __init__(self, n, b):
        # The names that occur in the arg list of the lambda are bound (or dummy) variables
        self.names = n
        # Unlike the builtin functions, lambdas have arbitrary bodies
        self.body =  b

    def __repr__(self):
        return "<lambda %s>" % id(self)

    # Every invocation of a lambda causes its bound variables to be pushed onto the
    # dynamic bindings stack.  McCarthy only touches briefly on the idea that combining functions
    # built from lambda is problemmatic.  In almost a throw-away sentence he states, "different bound
    # variables may be represented by the same symbol. This is called collision of bound variables."  If you
    # take the time to explore [core.lisp](core.html) then you will see what this means in practice.
    # The reason for these difficulties is a direct result of dynamic scoping.  McCarthy suggests that
    # a way to avoid these issues is to use point-free combinators to eliminate the need for variables
    # entirely.  This approach is a book unto itself -- which is likely the reason that McCarthy skips it.
    def push_bindings(self, containing_env, values):
        containing_env.push()

        self.set_bindings(containing_env, values)

    # The bindings are set one by one corresponding to the input values.
    def set_bindings(self, containing_env, values):
        for i in range(len(values)):
            containing_env.environment.binds[self.names[i].data] = values[i].eval(containing_env.environment)

    # The evaluation of a lambda is not much more complicated than a builtin function, except that it will
    # establish bindings in the root context.  Additionally, the root context will hold all bindings, so free
    # variables will also be in play.
    def eval(self, env, args):
        values = [a for a in args]

        if len(values) != len(self.names):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(len(self.names), len(args)))

        # Dynamic scope requires that names be bound on the global environment stack ...
        LITHP = env.get("__lithp__")

        # ... so I do just that.
        self.push_bindings(LITHP, values)

        # Now each form in the body is evaluated one by one, and the last determines the return value
        ret = FALSE
        for form in self.body:
            ret = form.eval(LITHP.environment)

        # Finally, the bindings established by the lambda are popped off of the dynamic stack
        LITHP.pop()
        return ret

# Closures

# McCarthy's Lisp does not define closures and in fact the precense of closures in the context of a pervasive dynamic
# scope is problemmatic.  However, this fact was academic to me and didn't really map conceptually to anything that I
# had experienced in the normal course of my programming life.  Therefore, I added closures to see what would happen.
# It turns out that if you thought that bound variables caused issues then your head will explode to find out what
# closures do.  Buyer beware.  However, closures are disabled by default.
class Closure(Lambda):
    def __init__(self, e, n, b):
        Lambda.__init__(self, n, b)
        self.env = e

    def __repr__(self):
        return "<lexical closure %s>" % id(self)

    # It's hard to imagine that this is the only difference between dynamic and lexical scope.  That is, whereas the
    # latter established bindings in the root context, the former does so only at the most immediate.  Of course, there
    # is no way to know this, so I had to make sure that the right context was passed within [lithp.py](index.html).
    def push_bindings(self, containing_env, values):
        containing_env.push(self.env.binds)

        self.set_bindings(containing_env, values)


import lithp
