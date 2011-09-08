import string
import re

from atom import Symbol, String
from number import Number, Integral, LongInt, Float
from lisp import Lisp
from seq import List

DELIM = string.whitespace + Lisp.SPECIAL

class Reader:
    def __init__(self, str=None):
       self.raw_source = str
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

        token = self.get_token()
        expr = None

        if token == ')':
            raise ValueError("Unexpected right paren")
        elif token == '(':
            expr = []
            token = self.get_token()

            while token != ')':
                if token == '(':
                    # Start parsing again.
                    self.prev()
                    expr.append(self.get_sexpr())
                elif token == None:
                    raise ValueError("Invalid end of expression: ", self.raw_source)
                else:
                    expr.append(token)

                token = self.get_token()

            return List(expr)
        else:
            return token


    def get_token(self):
        if self.index >= self.length:
            return None

        # Kill whitespace
        while self.index < self.length and self.current() in string.whitespace:
            self.next()

        # Check if we had a string of whitespace
        if self.index == self.length:
            return None

        if self.current() in Lisp.SPECIAL:
            self.next()

            return self.previous()
        # As mentioned in [atom.py](atom.html), I started down the path of implementing linear Lisp.
        # However, that work was never completed, but the reading of strings (surrounded by `"`) still remains
        # This may change in the future.
        elif self.current() == '"':
            # Parse a string.
            str = ""
            self.next()

            while self.current() != '"' and self.index < self.length:
                str = str + self.current()
                self.next()

            self.next()
            return String(str)
        else:
            token_str = ""

            # Build the token string
            while self.index < self.length - 1:
                if self.current() in DELIM:
                    break
                else:
                    token_str = token_str + self.current()
                    self.next()

            if not self.current() in DELIM:
                token_str = token_str + self.current()
                self.next()

            if Integral.REGEX.match(token_str):
                return Integral(int(token_str))
            elif Float.REGEX.match(token_str):
                return Float(float(token_str))
            elif LongInt.REGEX.match(token_str):
                return LongInt(int(token_str))
            else:
                return Symbol(token_str)

        return None

    def next(self):
        self.index = self.index + 1

    def prev(self):
        self.index = self.index - 1

    def current(self):
        return self.raw_source[self.index]

    def previous(self):
        return self.raw_source[self.index - 1]
