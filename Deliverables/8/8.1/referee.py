from helpers import *
from play_wrapper import PlayWrapper
from ref_wrapper import Ref_Wrapper
import socket

PLAY_WRAP = PlayWrapper()


class Referee:
	def __init__(self, remote_player, default_player):
		self.boards = [EMPTY_BOARD]
		self.current_turn = None
		self.num_passes = 0
		self.REF_WRAP = Ref_Wrapper(self)
		self.PLAYER1_WRAP = remote_player
		self.PLAYER2_WRAP = default_player

	def get_boards(self):
		return self.boards

	def get_action(self):
		if self.current_turn == self.PLAYER1_WRAP:
			try:
				move = self.current_turn.make_a_move(self.boards)
				return move
			except socket.error:
				return self.get_winner(True)
		move = self.current_turn.make_a_move(self.boards)
		return move

	def play_game(self, name1, name2):
		players = self.set_players(name1, name2)
		if len(players) != 2:  # crazy
			return players
		while True:
			action = self.get_action()
			if isinstance(action[0], str) and len(action) < 3:
				return action
			print(action)
			action_made = self.make_action(action)
			if isinstance(action_made, str) or isinstance(action_made[0], str):
				return action_made

	def set_players(self, name1, name2):
		self.current_turn = self.PLAYER1_WRAP
		# self.PLAYER1_WRAP.set_name(name1)
		if self.PLAYER1_WRAP.receive_stones(BLACK):
			return self.get_winner(True)
		self.PLAYER2_WRAP.set_name(name2)
		self.PLAYER2_WRAP.receive_stones(WHITE)
		return self.PLAYER1_WRAP.get_color(), self.PLAYER2_WRAP.get_color()

	def make_action(self, action):
		if action == PASS:
			self.num_passes += 1
			if self.num_passes == 2:
				illegal_move = False
				return self.REF_WRAP.get_winner(illegal_move)
			self.REF_WRAP.update_boards(self.boards[0])
			self.change_current_turn()
			return self.boards 

		self.num_passes = 0
		point = action
		if not PLAY_WRAP.action([self.get_current_stone(), [point, self.boards]]):
			illegal_move = True
			return self.REF_WRAP.get_winner(illegal_move)
		new_board = PLAY_WRAP.get_next_board(self.get_current_stone(), point, self.boards[0])
		self.REF_WRAP.update_boards(new_board)
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
			return sorted([self.PLAYER1_WRAP.get_name(), self.PLAYER2_WRAP.get_name()])

		winner = max(score, key=score.get)
		return [self.current_turn.get_name()] if self.current_turn.get_color() == winner else [self.get_opponent_player().get_name()]

	def get_current_stone(self):
		return self.current_turn.get_color()

	def get_opponent_player(self):
		return self.PLAYER2_WRAP if self.current_turn == self.PLAYER1_WRAP else self.PLAYER1_WRAP

	def change_current_turn(self):
		self.current_turn = self.get_opponent_player()

