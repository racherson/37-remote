import unittest
from play import get_opponent
from play import get_captured

class TestHelperMethods(unittest.TestCase):
	def test_get_opponent(self):
		self.assertEqual(get_opponent("B"),"W")
		self.assertEqual(get_opponent("W"),"B")
		self.assertEqual(get_opponent("i"), None)
		self.assertEqual(get_opponent(1), None)

	def test_get_captured(self):
		board = [
		["B", "B", "B"],
		["B", "W", "B"],
		["B", "B", "B"]
		]
		self.assertEqual(get_captured(board), [1,1])

if __name__ == '__main__':
	unittest.main()