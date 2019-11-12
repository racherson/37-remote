from helpers import *
from play_wrapper import PlayWrapper
from player_wrapper import Player_Wrapper

PLAY_WRAP = PlayWrapper()
PLAYER1_WRAP = Player_Wrapper()
PLAYER2_WRAP = Player_Wrapper()

class Referee:
	def __init__(self):
		self.boards = [EMPTY_BOARD]
		self.current_turn = None
		self.num_passes = 0


	# def get_boards(self):
	# 	return self.boards

	def set_players(self,name1,name2):
		self.current_turn = PLAYER1_WRAP
		PLAYER1_WRAP.register()
		PLAYER2_WRAP.register()
		PLAYER1_WRAP.set_name(name1)
		PLAYER1_WRAP.receive_stones(BLACK)
		PLAYER2_WRAP.set_name(name2)
		PLAYER2_WRAP.receive_stones(WHITE)
		return PLAYER1_WRAP.get_color(), PLAYER2_WRAP.get_color()

	def reset_passes(self):
		self.num_passes = 0

	def make_action(self, action):
		if action == PASS:
			self.num_passes += 1
			if self.num_passes == 2:
				illegal_move = False
				return self.get_winner(illegal_move)
			self.update_boards(self.boards[0])
			self.change_current_turn()
			return self.boards 

		self.reset_passes()
		point = action
		if not PLAY_WRAP.action([self.get_current_stone(), [point, self.boards]]):
			illegal_move = True
			return self.get_winner(illegal_move)
		new_board = PLAY_WRAP.get_next_board(self.get_current_stone(), point, self.boards[0])
		self.update_boards(new_board)
		self.change_current_turn()
		return self.boards


	def update_boards(self, new_board):
		boards = self.boards
		boards = [new_board] + boards
		if len(boards) > 3:
			boards.remove(boards[-1])
		self.boards = boards

	def get_winner(self, illegal_move):
		if illegal_move:
			winner = self.get_opponent_player()
			name = winner.get_name()
			return [name]

		score = PLAY_WRAP.score(self.boards[0])
		if score[BLACK] == score[WHITE]:
			return sorted([PLAYER1_WRAP.get_name(), PLAYER2_WRAP.get_name()])

		winner = max(score,key=score.get)
		return [self.current_turn.get_name()] if self.current_turn.get_color() == winner else [self.get_opponent_player().get_name()]

	def get_current_stone(self):
		return self.current_turn.get_color()

	def get_opponent_player(self):
		return PLAYER2_WRAP if self.current_turn == PLAYER1_WRAP else PLAYER1_WRAP

	def change_current_turn(self):
		self.current_turn = self.get_opponent_player()

