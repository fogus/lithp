from atom import TRUE
from atom import FALSE
from atom import Symbol
from seq import Seq

class Lisp:
    SPECIAL = "()"

    """
    The original Lisp described by McCarthy in his 1960 paper describes the following function set:
    1.  `atom`    (/) done
    2.  `car`     (/) done
    3.  `cdr`     (/) done
    4.  `cond`
    5.  `cons`    (/) done
    6.  `eq`      (/) done
    7.  `quote`   (/) done

    http://www-formal.stanford.edu/jmc/recursive.html
    """
    def dummy(self, env, args):
        print("I do nothing, but you gave me: ")
        self.println(env, args)

    # (cond ((atom (quote (1 3))) (quote foo)) ((atom (quote a)) (quote bar)) (t (quote baz)))
    def cond(self, env, args):
        for test in args:
            result = test.car().eval(env)

            if result == TRUE:
                return test.data[1].eval(env)

        return FALSE

    def eq(self, env, args):
        if len(args) > 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        if args[0].eval(env) == args[1].eval(env):
            return TRUE

        return FALSE

    def quote(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        return args[0]

    def car(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        first_elem = args[0].eval(env)

        if not isinstance(first_elem, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return first_elem.car()

    def cdr(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        first_elem = args[0].eval(env)

        if not isinstance(first_elem, Seq):
            raise ValueError("Function not valid on non-sequence type.")

        return first_elem.cdr()

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

    def println(self, env, args):
        for a in args:
            result = a.eval(env)
            self.stdout.write( "%s " % str( result))

        self.stdout.write( "\n")
        return TRUE
