import unittest
from helpers import *
from board_wrapper import BoardWrapper
from player_wrapper import Player_Wrapper
from tournament_admin import *

b = BoardWrapper()
board = [
	[BLACK, WHITE, BLACK],
	[BLACK, WHITE, BLACK],
	[BLACK, WHITE, EMPTY]
]

boards = [
	board, board, board
]

r = "rachel"
s = "sarah"


class Test_Player(unittest.TestCase):
	def test_init(self):
		p = Player_Wrapper(s)
		self.assertEqual(p.register_flag, False)
		self.assertEqual(p.receive_flag, False)
		self.assertEqual(p.player.name, s)

	def test_register(self):
		p = Player_Wrapper(s)
		self.assertEqual(p.register(), s)
		self.assertEqual(p.register(), GONE_CRAZY)

	def test_receive_stones(self):
		p = Player_Wrapper(s)
		self.assertEqual(p.receive_stones(BLACK), GONE_CRAZY)
		p.register()
		p.receive_stones(BLACK)
		self.assertEqual(p.player.color, BLACK)
		self.assertEqual(p.receive_stones(BLACK), GONE_CRAZY)

	def test_make_move(self):
		p = Player_Wrapper(s)
		p.register()
		self.assertEqual(p.make_a_move(boards), GONE_CRAZY)
		p.receive_stones(WHITE)
		self.assertNotEqual(p.make_a_move(boards), GONE_CRAZY)


class Test_Board(unittest.TestCase):
	def test_occupied(self):
		self.assertEqual(b.occupied(board, [1, 1]), True)
		self.assertEqual(b.occupied(board, "1-1"), True)
		self.assertEqual(b.occupied(board, [2, 2]), False)
		self.assertEqual(b.occupied(board, "3-3"), False)
		self.assertRaises(InvalidPoint, b.occupied, board, "5-5")

	def test_occupies(self):
		self.assertEqual(b.occupies(board, BLACK, "1-1"), True)
		self.assertEqual(b.occupies(board, BLACK, [0,0]), True)
		self.assertRaises(InvalidPoint, b.occupies, board, BLACK, "5,5")
		self.assertRaises(InvalidBoard, b.occupies, [1], BLACK, "1-1")
		self.assertRaises(InvalidStone, b.occupies, board, "black", "1-1")

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


class Test_Tournament(unittest.TestCase):
	def test_add_player_to_tournament(self):
		name = r
		p = Player_Wrapper(name)
		add_player_to_tournament(p, name, False)
		self.assertEqual(players[name], p)
		self.assertEqual(rankings[name], 0)
		self.assertEqual(beaten[name], [])
		self.assertTrue(name in player_list)

	def test_add_default_players(self):
		p = Player_Wrapper(s)
		add_player_to_tournament(p, s, False)
		sock, DefaultPlayer = setup_from_config()
		add_default_players(1, DefaultPlayer)
		self.assertEqual(len(players), 2)
		self.assertEqual(len(rankings), 2)
		self.assertEqual(len(beaten), 2)
		self.assertEqual(len(player_list), 2)
		sock.close()

	def test_flip_coin(self):
		self.assertTrue(flip_coin(r, s) in [[r], [s]])
		self.assertFalse(flip_coin(r, s) in [r, s])

	def test_get_loser(self):
		self.assertEqual(get_loser(r, s, r), s)
		self.assertEqual(get_loser("player1", "player2", "player2"), "player1")
		self.assertRaises(InvalidPlayer, get_loser, r, s, "mark")

	def test_create_default_player(self):
		sock, DefaultPlayer = setup_from_config()
		player, name = create_default_player(DefaultPlayer, cheater=False)
		self.assertEqual(name, "default-player-1")
		self.assertTrue(player.register_flag)
		player2, name2 = create_default_player(DefaultPlayer, cheater=True)
		self.assertEqual(name2, "replacement-default-player-2")
		self.assertTrue(player2.register_flag)
		sock.close()

	def test_play_game(self):
		name1 = r
		p1 = Player_Wrapper(name1)
		name2 = s
		p2 = Player_Wrapper(name2)
		winner, loser, illegal = play_game(p1, p2, name1, name2)
		self.assertEqual(winner, [s])
		self.assertEqual(loser, r)
		self.assertTrue(illegal)

	def test_update_league(self):
		sock, DefaultPlayer = setup_from_config()
		curr_rachel_rankings = rankings[r]
		curr_sarah_rankings = rankings[s]
		update_league([r], s, False, DefaultPlayer)
		self.assertEqual(beaten[r], [s])
		self.assertEqual(rankings[r], curr_rachel_rankings + 1)
		update_league([s], r, True, DefaultPlayer)
		self.assertEqual(rankings[r], 0)
		self.assertFalse(r in player_list)
		self.assertEqual(beaten[s], [])
		self.assertEqual(rankings[s], curr_sarah_rankings + 2)
		sock.close()

	def test_update_cup(self):
		curr_rachel_rankings = rankings[r]
		update_cup([r], s, False)
		self.assertEqual(rankings[r], curr_rachel_rankings + 1)
		update_cup([s], r, True)
		self.assertEqual(rankings[s], 1)
		self.assertEqual(rankings[r], 0)


if __name__ == '__main__':
	unittest.main()
