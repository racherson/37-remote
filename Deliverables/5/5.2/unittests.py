import unittest
from player import *
from helpers import *

class TestGetAndSetMethods(unittest.TestCase):
    def test_name(self):
        p = Player()
        self.assertEqual(p.get_name(), "no name")
        p.set_name("sarah")
        self.assertEqual(p.get_name(), "sarah")

    def test_color(self):
        p = Player()
        self.assertEqual(p.get_color(), EMPTY)
        p.set_color(BLACK)
        self.assertEqual(p.get_color(), BLACK)
        p.set_color(WHITE)
        self.assertEqual(p.get_color(), WHITE)

class TestPlayer1Methods(unittest.TestCase):
    def test_make_move(self):
        pass


if __name__ == '__main__':
    unittest.main()