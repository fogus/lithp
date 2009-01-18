# The Lithp interpreter is requires Python 3000 to function.  
# For more information:
#   http://www.slideshare.net/jza/python-3000
#   http://www.ibm.com/developerworks/linux/library/l-python3-1/
#   http://www.python.org/dev/peps/pep-3000/
#   http://www.python.org/dev/peps/

import getopt, sys
from lisp import Lisp
from env import Environment
from scanner import Scanner
from function import Function

NAME = "Lithp"
VERSION = "v0.0.1"
PROMPT = "lithp"

INVALID_OPS = 1

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
        
        self.scanner = Scanner()
        self.environment = Environment()
        
        self.init()

    def init(self):
        # Testing symbol defs
        self.environment.set("foo", Function(self.dummy))
        self.environment.set("bar", Function(self.dummy))
        self.environment.set("baz", Function(self.dummy))

    def usage(self):
        self.print_banner()
        print
        print(NAME.lower(), " <options> [lithpfiles]\n")

    def print_banner(self):
        print("The ", NAME, " programming shell ", VERSION)
        print("   by Fogus, http://fogus.me")
        
    def repl(self):
        print(self.environment)
        

if __name__ == '__main__':
    lithp = Lithp()
    
    try:
        opts, files = getopt.getopt(sys.argv[1:], "hd", ["help", "debug"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str( err)) # will print something like "option -a not recognized"
        lithp.usage()
        sys.exit(INVALID_OPS)
            
    for opt,arg in opts:
        if opt in ("--help", "-h"):
            lithp.usage()
            sys.exit( 0)
        elif opt in ("--debug", "-d"):
            lithp.verbose = True
        else:
            print("unknown option " + opt)

    lithp.print_banner()
    lithp.repl()
