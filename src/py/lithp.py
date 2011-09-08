# Lithp - A interpreter for John McCarthy's original Lisp.
#
# The heavily documented code for [Lithp can be found on Github](http://github.com/fogus/lithp).
#
# It wasn't enough to write the Lisp interpreter -- I also wanted to share what I learned with *you*.  Reading
# this source code provides a snapshot into the mind of John McCarthy, Steve Russell, Timothy P. Hart, and Mike Levin and
# as an added bonus, myself.  The following source files are available for your reading:
# 
# - [atom.py](atom.html)
# - [env.py](env.html)
# - [error.py](error.html)
# - [fun.py](fun.html)
# - [interface.py](interface.html)
# - [lisp.py](lisp.html)
# - [lithp.py](index.html) *(this file)*
# - [number.py](number.html)
# - [reader.py](reader.html)
# - [seq.py](seq.html)
# - [core.lisp](core.html)
# 
# The Lithp interpreter requires Python 2.6.1+ to function.
#   please add comments, report errors, annecdotes, etc. to the [Lithp Github project page](http://github.com/fogus/lithp)
# 
import pdb
import getopt, sys, io
from env import Environment
from fun import Function
from atom import TRUE
from atom import FALSE
from lisp import Lisp
from reader import Reader
from error import Error
from fun import Lambda
from fun import Closure

NAME = "Lithp"
VERSION = "v1.1"
WWW = "http://fogus.me/fun/lithp/"
PROMPT = "lithp"
DEPTH_MARK = "."

class Lithp(Lisp):
    """ The Lithper class is the interpreter driver.  It does the following:
            1. Initialize the global environment
            2. Parse the cl arguments and act on them as appropriate
            3. Initialize the base Lisp functions
            4. Read input
            5. Evaluate
            6. Print
            7. Loop back to #4
    """
    def __init__( self):
        iostreams=(sys.stdin, sys.stdout, sys.stderr)
        (self.stdin, self.stdout, self.stderr) = iostreams

        self.debug = False
        self.verbose = True
        self.core = True
        self.closures = True

        self.rdr = Reader()
        self.environment = Environment()

        self.init()

    def init(self):
        # Define core functions
        self.environment.set("eq",     Function(self.eq))
        self.environment.set("quote",  Function(self.quote))
        self.environment.set("car",    Function(self.car))
        self.environment.set("cdr",    Function(self.cdr))
        self.environment.set("cons",   Function(self.cons))
        self.environment.set("atom",   Function(self.atom))
        self.environment.set("cond",   Function(self.cond))
        
        # Define utility function
        self.environment.set("print",  Function( self.println))

        # Special forms
        self.environment.set("lambda", Function(self.lambda_))
        self.environment.set("label",  Function(self.label))

        # Define core symbols
        self.environment.set("t", TRUE)

        # There is one empty list, and it's named `nil`
        self.environment.set("nil", FALSE)

        # Define meta-elements
        self.environment.set("__lithp__",  self)
        self.environment.set("__global__", self.environment)

    def usage(self):
        self.print_banner()
        print
        print NAME.lower(), " <options> [lithp files]\n"

    def print_banner(self):
        print "The", NAME, "programming shell", VERSION
        print "   by Fogus,", WWW
        print "   Type :help for more information"
        print

    def print_help(self):
        print "Help for Lithp v", VERSION
        print "  Type :help for more information"
        print "  Type :env to see the bindings in the current environment"
        print "  Type :load followed by one or more filenames to load source files"
        print "  Type :quit to exit the interpreter"

    def push(self, env=None):
        if env:
            self.environment = self.environment.push(env)
        else:
            self.environment = self.environment.push()

    def pop(self):
        self.environment = self.environment.pop()

    def repl(self):
        while True:
            # Stealing the s-expression parsing approach from [CLIPS](http://clipsrules.sourceforge.net/)
            source = self.get_complete_command() 

            # Check for any REPL directives
            if source in [":quit"]:
                break
            elif source in [":help"]:
                self.print_help()
            elif source.startswith(":load"):
                files = source.split(" ")[1:]
                self.process_files(files)
            elif source in [":env"]:
                print(self.environment)
            else:
                self.process(source)

    # Source is processed one s-expression at a time.
    def process(self, source):
        sexpr = self.rdr.get_sexpr(source)

        while sexpr:
            result = None

            try:
                result = self.eval(sexpr)
            except Error as err:
                print(err)

            if self.verbose:
                self.stdout.write("    %s\n" % result)

            sexpr = self.rdr.get_sexpr()

    # In the process of living my life I had always heard that closures and dynamic scope
    # cannot co-exist.  As a thought-experiment I can visualize why this is the case.  That is,
    # while a closure captures the contextual binding of a variable, lookups in dynamic scoping
    # occur on the dynamic stack.  This means that you may be able to close over a variable as 
    # long as it's unique, but the moment someone else defines a variable of the same name 
    # and attempt to look up the closed variable will resolve to the top-most binding on the 
    # dynamic stack.  This assumes the the lookup occurs before the variable of the same name
    # is popped.  While this is conceptually easy to grasp, I still wanted to see what would
    # happen in practice -- and it wasn't pretty.
    def lambda_(self, env, args):
        if self.environment != env.get("__global__") and self.closures:
            return Closure(env, args[0], args[1:])
        else:
            return Lambda(args[0], args[1:])

    # Delegate evaluation to the form.
    def eval(self, sexpr):
        try:
            return sexpr.eval(self.environment)
        except ValueError as err:
            print(err)
            return FALSE

    # A complete command is defined as a complete s-expression.  Simply put, this would be any
    # atom or any list with a balanced set of parentheses.
    def get_complete_command(self, line="", depth=0):
        if line != "":
            line = line + " "

        if self.environment.level != 0:
            prompt = PROMPT + " %i%s " % (self.environment.level, DEPTH_MARK * (depth+1))
        else:
            if depth == 0:
                prompt = PROMPT + "> "
            else:
                prompt = PROMPT + "%s " % (DEPTH_MARK * (depth+1))

            line = line + self.read_line(prompt)
            
            # Used to balance the parens
            balance = 0
            for ch in line:
                if ch == "(":
                    # This is not perfect, but will do for now
                    balance = balance + 1
                elif ch == ")":
                    # Too many right parens is a problem
                    balance = balance - 1
            if balance > 0:
                # Balanced parens gives zero
                return self.get_complete_command( line, depth+1)
            elif balance < 0:
                raise ValueError("Invalid paren pattern")
            else:
                return line

    def read_line( self, prompt) :
        if prompt and self.verbose:
            self.stdout.write("%s" % prompt)
            self.stdout.flush()

        line = self.stdin.readline()

        if(len(line) == 0):
            return "EOF"

        if line[-1] == "\n":
            line = line[:-1]

        return line

    # Lithp also processes files using the reader plumbing.
    def process_files(self, files):
        self.verbose = False

        for filename in files:
            infile = open( filename, 'r')
            self.stdin = infile

            source = self.get_complete_command()
            while(source not in ["EOF"]):
                self.process(source)

                source = self.get_complete_command()

            infile.close()
        self.stdin = sys.stdin

        self.verbose = True

if __name__ == '__main__':
    lithp = Lithp()

    try:
        opts, files = getopt.getopt(sys.argv[1:], "hd", ["help", "debug", "no-core", "no-closures"])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(str( err)) # will print something like "option -a not recognized"
        lithp.usage()
        sys.exit(1)

    for opt,arg in opts:
        if opt in ("--help", "-h"):
            lithp.usage()
            sys.exit(0)
        elif opt in ("--debug", "-d"):
            lithp.verbose = True
        elif opt in ("--no-core"):
            lithp.core = False
        elif opt in ("--no-closures"):
            lithp.closures = False
        else:
            print("unknown option " + opt)

    # Process the core lisp functions, if applicable
    if lithp.core:
        lithp.process_files(["../core.lisp"])

    if len(files) > 0:
        lithp.process_files(files)

    lithp.print_banner()
    lithp.repl()


#### References

# - (McCarthy 1979) *History of Lisp* by John MaCarthy
# - (McCarthy 1960) *Recursive functions of symbolic expressions and their computation by machine, part I* by John McCarthy
# - (Church 1941) *The Calculi of Lambda-Conversion* by Alonzo Church
# - (Baker 1993) *Equal Rights for Functional Objects or, The More Things Change, The More They Are the Same* by Henry Baker
# - (Kleene 1952) *Introduction of Meta-Mathematics* by Stephen Kleene
# - (McCarthy 1962) *LISP 1.5 Programmer's Manual* by John McCarthy, Daniel Edwards, Timothy Hart, and Michael Levin
# - (IBM 1955) *IBM 704 Manual of Operation* [here](http://www.cs.virginia.edu/brochure/images/manuals/IBM_704/IBM_704.html)
# - (Hart 1963) *AIM-57: MACRO Definitions for LISP* by Timothy P. Hart
