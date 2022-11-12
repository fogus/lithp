from unittest import TestCase
from atom import TRUE, FALSE
from atom import Atom
from atom import Symbol
from seq import List
from env import Environment


class AtomTests(TestCase):
    def test_truthiness(self):
        self.assertEqual(TRUE, Symbol("t"))

    def test_falsiness(self):
        self.assertEqual(FALSE, List())

    def test_atomness(self):
        foo = Atom("foo")
        another_foo = Atom("foo")
        bar = Atom("bar")
        baz = Atom("baz")

        self.assertTrue(foo == foo)
        self.assertTrue(foo == another_foo)
        self.assertTrue(foo != bar)
        self.assertTrue(baz != bar)
        self.assertTrue(foo != bar != baz)

    def test_symbolness(self):
        foo = Symbol("foo")
        another_foo = Symbol("foo")
        bar = Symbol("bar")
        e = Environment(None, {"foo": foo})

        self.assertTrue(foo != bar)
        self.assertTrue(foo == another_foo)
        self.assertTrue(another_foo == foo)
        self.assertTrue(foo.__hash__() == another_foo.__hash__())
        self.assertTrue(foo.eval(e) == foo)
