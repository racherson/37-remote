# from referee import Referee
from helpers import *
from board_wrapper import BoardWrapper

BOARD_WRAP = BoardWrapper()


class Ref_Wrapper:

	def __init__(self, ref):
		self.ref = ref

	def play_game(self):
		return self.ref.play_game()

	def set_players(self):
		return self.ref.set_players()

	def make_action(self, action):
		if action != PASS:
			try:
				action = BOARD_WRAP.string_to_point(action)
				BOARD_WRAP.check_point(action)
			except:
				raise Exception("Received invalid move")

		return self.ref.make_action(action)

	def update_boards(self, new_board):
		BOARD_WRAP.check_board(new_board)
		self.ref.update_boards(new_board)

	def get_winner(self, illegal_move):
		if not isinstance(illegal_move, bool):
			raise Exception("Received invalid arg illegal_move")
		return self.ref.get_winner(illegal_move)
