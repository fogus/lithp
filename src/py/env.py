# The `Environment` class represents the dynamic environment of McCarthy's original Lisp.  The creation of 
# this class is actually an interesting story.  As many of you probably know, [Paul Graham wrote a paper and 
# code for McCarthy's original Lisp](http://www.paulgraham.com/rootsoflisp.html) and it was my first exposure to 
# the stark simplicity of the language.  The simplicity is breath-taking!
#
# However, while playing around with the code I found that in using the core functions (i.e. `null.`, `not.`, etc.) 
# I was not experiencing the full effect of the original.  That is, the original Lisp was dynamically scoped, but 
# the Common Lisp used to implement and run (CLisp in the latter case) Graham's code was lexically scoped.  Therefore, 
# by attempting to write high-level functions using only the magnificent 7 and Graham's core functions in the Common Lisp
# I was taking advantage of lexical scope; something not available to McCarthy and company.  Of course, the whole reason
# that Graham wrote `eval.` was to enforce dynamic scoping (he used a list of symbol-value pairs where the dynamic variables
# were added to its front when introduced).  However, that was extremely cumbersome to use:
# 
#     (eval. 'a '((a 1) (a 2)))
#     ;=> 1
#
# So I then implemented a simple REPL in Common Lisp that fed input into `eval.` and maintained the current environment list.
# That was fun, but I wasn't sure that I was learning anything at all.  Therefore, years later I came across the simple
# REPL and decided to try to implement my own core environment for the magnificent 7 to truly get a feel for what it took
# to build a simple language up from scratch.  I suppose if I were a real manly guy then I would have found an IBM 704, but 
# that would be totally insane. (email me if you have one that you'd like to sell for cheap)
#
# Anyway, the point of this is that I needed to start with creating an `Environment` that provided dynamic scoping, and the
# result is this.
class Environment:
    # The binding are stored in a simple dict and the stack discipline is emulated through the `parent` link
    def __init__(self, par=None, bnd=None):
        if bnd:
            self.binds = bnd
        else:
            self.binds = {}

        self.parent = par

        if par:
            self.level = self.parent.level + 1
        else:
            self.level = 0

    # Getting a binding potentially requires the traversal of the parent link
    def get(self, key):
        if key in self.binds:
            return self.binds[key]
        elif self.parent:
            return self.parent.get(key)
        else:
            raise ValueError("Invalid symbol " + key)

    # Setting a binding is symmetric to getting
    def set(self, key, value):
        if key in self.binds:
            self.binds[key] = value
        elif self.parent:
            self.parent.set(key,value)
        else:
            self.binds[key] = value

    def definedp(self, key):
        if key in self.binds.keys():
            return True

        return False
    
    # Push a new binding by creating a new Env
    #
    # Dynamic scope works like a stack.  Whenever a variable is created it's binding is pushed onto a
    # global stack.  In this case, the stack is simulated through a chain of parent links.  So if you were to
    # create the following:
    #
    #     (label a nil)
    #     (label frobnicate (lambda () (cons a nil)))
    #     
    #     ((lambda (a)
    #        (frobnicate))
    #      (quote x))
    #
    # Then the stack would look like the figure below within the body of `frobnicate`:
    #
    #     |         |
    #     |         |
    #     | a = 'x  |
    #     | ------- |
    #     | a = nil |
    #     +---------+
    # 
    # Meaning that when accessing `a`, `frobnicate`  will get the binding at the top of the stack, producing the result `(x)`.  This push/pop
    # can become difficult, so people have to do all kinds of tricks to avoid confusion (i.e. pseudo-namespace via variable naming schemes).
    #
    def push(self, bnd=None):
        return Environment(self, bnd)

    def pop(self):
        return self.parent

    def __repr__( self):
        ret = "\nEnvironment %s:\n" % self.level
        keys = [i for i in self.binds.keys() if not i[:2] == "__"]

        for key in keys:
            ret = ret + " %5s: %s\n" % (key, self.binds[key])

        return ret
