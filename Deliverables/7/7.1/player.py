from helpers import *
from play_wrapper import PlayWrapper
from board_wrapper import BoardWrapper
from abc import abstractmethod
import copy
import json

PLAY_WRAP = PlayWrapper()
BOARD_WRAP = BoardWrapper()


class Player:

	# name = "no name"
	# color = EMPTY

	def __init__(self):
		self.name = "no name"
		self.color = EMPTY

	def set_name(self, name):
		self.name = name

	def get_name(self):
		return self.name

	def set_color(self, color):
		self.color = color

	def get_color(self):
		return self.color

	@abstractmethod
	def make_a_move(self, boards):
		pass


class Player1(Player):
	def __init__(self):
		super(Player1, self).__init__()

	def make_a_move(self, boards):
		history_is_good = PLAY_WRAP.check_history(boards, self.color)
		if history_is_good:
			for col in range(BOARD_SIZE):
				for row in range(BOARD_SIZE):
					if PLAY_WRAP.play(self.color, [row, col], copy.deepcopy(boards)):
						return [row, col]
			return "pass"

		return "This history makes no sense!"


class Player2(Player):

	def __init__(self):
		super(Player2, self).__init__()
		self.n = None
		with open('go-player.config') as config_file:
			n = json.load(config_file)
		self.n = n["depth"]

	def make_a_move(self, boards):
		history_is_good = PLAY_WRAP.check_history(boards, self.color)
		if not history_is_good:
			return "This history makes no sense!"

		if self.n == 1:
			point = self.find_capture_point(boards)
			if point:
				return point
			else:
				return self.normal_move(boards)

	def find_capture_point(self, boards):
		for col in range(BOARD_SIZE):
			for row in range(BOARD_SIZE):
				if PLAY_WRAP.play(self.color, [row, col], copy.deepcopy(boards)) and PLAY_WRAP.is_capture_move(self.color, [row, col], copy.deepcopy(boards[0])):
					return [row, col]
		return False

	def normal_move(self, boards):
		for col in range(BOARD_SIZE):
			for row in range(BOARD_SIZE):
				if PLAY_WRAP.play(self.color, [row, col], boards):
					return [row, col]
		return "pass"
