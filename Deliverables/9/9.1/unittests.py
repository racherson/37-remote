import unittest
from helpers import *
from board_wrapper import BoardWrapper
from player_wrapper import Player_Wrapper

b = BoardWrapper()
board = [
	[BLACK, WHITE, BLACK],
	[BLACK, WHITE, BLACK],
	[BLACK, WHITE, EMPTY]
]

boards = [
	board, board, board
]
class Test_Player(unittest.TestCase):
	def test_init(self):
		p = Player_Wrapper("sarah")
		self.assertEqual(p.register_flag, False)
		self.assertEqual(p.receive_flag, False)
		self.assertEqual(p.player.name, "sarah")

	def test_register(self):
		p = Player_Wrapper("sarah")
		self.assertEqual(p.register(), "sarah")
		self.assertEqual(p.register(), GONE_CRAZY)

	def test_receive_stones(self):
		p = Player_Wrapper("sarah")
		self.assertEqual(p.receive_stones(BLACK), GONE_CRAZY)
		p.register()
		p.receive_stones(BLACK)
		self.assertEqual(p.player.color, BLACK)
		self.assertEqual(p.receive_stones(BLACK), GONE_CRAZY)

	def test_make_move(self):
		p = Player_Wrapper("sarah")
		p.register()
		self.assertEqual(p.make_a_move(boards), GONE_CRAZY)
		p.receive_stones(WHITE)
		self.assertNotEqual(p.make_a_move(boards), GONE_CRAZY)

class Test_Board(unittest.TestCase):
	def test_occupied(self):
		self.assertEqual(b.occupied(board,[1,1]), True)
		self.assertEqual(b.occupied(board,"1-1"), True)
		self.assertEqual(b.occupied(board,[2,2]), False)
		self.assertEqual(b.occupied(board,"3-3"), False)
		self.assertRaises(Exception, b.occupied, board, "5-5")

	def test_occupies(self):
		self.assertEqual(b.occupies(board, BLACK, "1-1"), True)
		self.assertEqual(b.occupies(board, BLACK, [0,0]), True)
		self.assertRaises(Exception, b.occupies, board, BLACK, "5,5")
		self.assertRaises(Exception, b.occupies, [1], BLACK, "1-1")
		self.assertRaises(Exception, b.occupies, board, "black", "1-1")

	def test_place(self):
		self.assertEqual(b.place(board, BLACK, "1-1"), "This seat is taken!")
		self.assertEqual(b.place(board, BLACK, "3-3"), [
			[BLACK, WHITE, BLACK],
			[BLACK, WHITE, BLACK],
			[BLACK, WHITE, BLACK]
		])

	def test_remove(self):
		self.assertEqual(b.remove(board, BLACK, "3-3"), 
			[
			[BLACK, WHITE, BLACK],
			[BLACK, WHITE, BLACK],
			[BLACK, WHITE, EMPTY]
		])
		self.assertEqual(b.remove(board, BLACK, "2-1"), "I am just a board! I cannot remove what is not there!")
		self.assertEqual(b.remove(board, BLACK, "3-3"), "I am just a board! I cannot remove what is not there!")

	def test_reachable(self):
		self.assertEqual(b.reachable(board, "1-1", EMPTY), False)
		self.assertEqual(b.reachable(board, "1-1", BLACK), True)
		self.assertEqual(b.reachable(board, "1-1", WHITE), True)

	def test_get_points(self):
		self.assertEqual(b.get_points(board, EMPTY), ["3-3"])
		self.assertEqual(b.get_points(board, WHITE), ["2-1", "2-2", "2-3"])

if __name__ == '__main__':
    unittest.main()