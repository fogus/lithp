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
DEPTH_MARK = "."

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
        self.print_banner()

        self.scanner = Scanner()
        self.environment = Environment()
        
        self.init()

    def init(self):
        # Define core functions
        self.environment.set( "print", Function( self.println))
        self.environment.set("foo", Function(self.dummy))

    def usage(self):
        self.print_banner()
        print
        print(NAME.lower(), " <options> [lithp files]\n")

    def print_banner(self):
        print("The ", NAME, " programming shell ", VERSION)
        print("   by Fogus, http://fogus.me")
        
    def repl(self):
        print(self.environment)

        while True:
            source = self.get_complete_command()

            if source in ["(quit)"]:
                break
 
            print(source)

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

            line = line  + self.read_line(prompt)
            oparens = 0
            cparens = 0
            for c in line:
                if c == "(":
                    oparens = oparens + 1
                elif c == ")":
                    cparens = cparens + 1
            if oparens > cparens:
                return self.get_complete_command( line, depth+1)
            else:
                return line

    def read_line( self, prompt) :
        """raw_input with pseudo I/O streams."""
        if prompt :
            self.stdout.write("%s" % prompt)
            self.stdout.flush()
        line = self.stdin.readline()    
        if line[-1] == "\n":
            line = line[:-1]

        return line  
        

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

    lithp.repl()
