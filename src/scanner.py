from atom import Symbol
from atom import String
from number import Number

class Scanner:
    def __init__(self, str=None):
       print("Initializing the scanner...")
       self.raw_source
       self.index = 0
       self.length = 0
       self.sexpr = []

       if str:
           self.sexpr = self.get_sexpr()

    def get_sexpr(self, source=None):
        if source:
            self.raw_source = source
            self.length = len(self.raw_source)
            self.index = 0

        

    def get_token(self):
        
