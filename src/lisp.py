class Lisp:
    """
    The original Lisp described by McCarthy in his 1960 paper describes the following function set:
    1.  `atom`
    2.  `car`
    3.  `cdr`
    4.  `cond`
    5.  `cons`
    6.  `eq`
    7.  `quote`

    http://www-formal.stanford.edu/jmc/recursive.html
    """
    def dummy(self, env, args):
        print "I do nothing"
