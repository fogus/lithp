class Lisp:
    SPECIAL = "()'"

    """
    The original Lisp described by McCarthy in his 1960 paper describes the following function set:
    1.  `atom`
    2.  `car`
    3.  `cdr`
    4.  `cond`
    5.  `cons`
    6.  `eq`        (done for Number)
    7.  `quote`

    http://www-formal.stanford.edu/jmc/recursive.html
    """
    def dummy(self, env, args):
        print("I do nothing, but you gave me: ")
        self.println(env, args)

    def eq(self, env, args):
        if len(args) > 2:
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(2, len(args)))

        return (args[0] == args[1])

    def quote(self, env, args):
        if(len(args) > 1):
            raise ValueError("Wrong number of arguments, expected {0}, got {1}".format(1, len(args)))

        return args[0]

    def println(self, env, args):
        for a in args:
            result = a.eval(env)
            self.stdout.write( "%s " % str( result))

        self.stdout.write( "\n")
        return True
