import unittest
from referee import *
from helpers import *


class TestGetAndSetMethods(unittest.TestCase):
    def test_set_players(self):
        ref = Referee()
        name1 = "sarah"
        name2 = "rachel"
        ref.set_players(name1,name2)
        self.assertEqual(ref.current_turn.get_name(), "sarah")
        self.assertEqual(ref.get_opponent_player().get_name(), "rachel")

    def test_update_boards(self):
        ref = Referee()
        boards = [EMPTY_BOARD]
        new_board = EMPTY_BOARD
        new_board[0][0] = BLACK
        self.assertEqual(len(ref.boards), 1)
        ref.update_boards(new_board)
        self.assertEqual(len(ref.boards), 2)
        self.assertEqual(ref.boards, [new_board, EMPTY_BOARD])

    def test_get_winner(self):
        ref = Referee()
        ref.set_players("sarah", "rachel")
        ref.boards = [EMPTY_BOARD]
        self.assertEqual(ref.get_winner(True), ["rachel"])
        ref.boards = [EMPTY_BOARD, EMPTY_BOARD, EMPTY_BOARD]
        self.assertEqual(ref.get_winner(False), ["rachel","sarah"])
        ref.boards[0][0][0] = "W"
        self.assertEqual(ref.get_winner(False), ["rachel"])
        ref.boards[0][0][0] = EMPTY

    def test_make_action(self):
        ref = Referee()
        ref.set_players("sarah", "rachel")
        ref.boards = None
        ref.boards = [EMPTY_BOARD]
        self.assertEqual(ref.make_action("pass"), [EMPTY_BOARD, EMPTY_BOARD])
        self.assertEqual(ref.make_action("pass"), ["rachel", "sarah"])

        ref.boards[0][0][0] = "B"
        self.assertEqual(ref.make_action("1-1"), ["sarah"])
        ref.boards[0][0][0] = EMPTY

    def test_make_valid_move(self):
        ref = Referee()
        ref.set_players("sarah", "rachel")
        ref.boards = [EMPTY_BOARD]
        ref.num_passes = 0
        new_board = [[' ' for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        new_board[0][1] = "B"
        self.assertEqual(ref.make_action("2-1"), [new_board, EMPTY_BOARD])


if __name__ == '__main__':
    unittest.main()
