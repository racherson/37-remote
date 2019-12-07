from helpers import *
from play_wrapper import PlayWrapper
from ref_wrapper import Ref_Wrapper
import socket

PLAY_WRAP = PlayWrapper()


# change this from a class to just a function?
class Referee:
	def __init__(self, remote_player, default_player, player1_name, player2_name):
		self.boards = [EMPTY_BOARD]
		self.current_turn = None
		self.num_passes = 0
		self.REF_WRAP = Ref_Wrapper(self)
		self.PLAYER1_WRAP = remote_player
		self.PLAYER2_WRAP = default_player
		self.player1_name = player1_name
		self.player2_name = player2_name

	def play_game(self):
		players = self.set_players()
		if len(players) != 2:  # crazy
			return players
		while True:
			action, illegal = self.get_action()
			if isinstance(action[0], str) and len(action) < 3:
				return action, illegal
			action_made, illegal = self.make_action(action)
			if isinstance(action_made, str) or isinstance(action_made[0], str):
				return action_made, illegal

	def get_action(self):
		# try:
		move = self.current_turn.make_a_move(self.boards)
		return move, False
		# except:
		# 	return self.get_winner(True)

	def set_players(self):
		self.current_turn = self.PLAYER1_WRAP
		try:
			received = self.PLAYER1_WRAP.receive_stones(BLACK)
		except socket.error:
			return self.get_winner(True)
		if received:
			return self.get_winner(True)

		try:
			received = self.PLAYER2_WRAP.receive_stones(WHITE)
		except socket.error:
			self.current_turn = self.PLAYER2_WRAP
			return self.get_winner(True)
		if received:
			self.current_turn = self.PLAYER2_WRAP
			return self.get_winner(True)
		return self.PLAYER1_WRAP.get_color(), self.PLAYER2_WRAP.get_color()

	def make_action(self, action):
		if action == PASS:
			self.num_passes += 1
			if self.num_passes == 2:
				illegal_move = False
				return self.REF_WRAP.get_winner(illegal_move)
			self.REF_WRAP.update_boards(self.boards[0])
			self.change_current_turn()
			return self.boards, False

		self.num_passes = 0
		point = action
		if not PLAY_WRAP.action([self.get_current_stone(), [point, self.boards]]):
			illegal_move = True
			return self.REF_WRAP.get_winner(illegal_move)
		new_board = PLAY_WRAP.get_next_board(self.get_current_stone(), point, self.boards[0])
		self.REF_WRAP.update_boards(new_board)
		self.change_current_turn()
		return self.boards, False

	def update_boards(self, new_board):
		boards = self.boards
		boards = [new_board] + boards
		if len(boards) > 3:
			boards.remove(boards[-1])
		self.boards = boards

	def get_winner(self, illegal_move):
		if illegal_move:
			winner_name = self.player_name(self.get_opponent_player())
			self.notify_players_end_game()
			return [winner_name], illegal_move
		score = PLAY_WRAP.score(self.boards[0])
		if score[BLACK] == score[WHITE]:
			self.notify_players_end_game()
			return sorted([self.player1_name, self.player2_name]), illegal_move

		winner = max(score, key=score.get)
		self.notify_players_end_game()
		return [self.player_name(self.current_turn)] if self.current_turn.get_color() == winner else\
					[self.player_name(self.get_opponent_player())], illegal_move

	def get_current_stone(self):
		return self.current_turn.get_color()

	def get_opponent_player(self):
		return self.PLAYER2_WRAP if self.current_turn == self.PLAYER1_WRAP else self.PLAYER1_WRAP

	def change_current_turn(self):
		self.current_turn = self.get_opponent_player()

	def player_name(self, player_wrap):
		if player_wrap == self.PLAYER1_WRAP:
			return self.player1_name
		return self.player2_name

	def notify_players_end_game(self):
		self.PLAYER1_WRAP.end_game()
		self.PLAYER2_WRAP.end_game()

