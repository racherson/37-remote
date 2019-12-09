from helpers import *
from play_wrapper import PlayWrapper
from board_wrapper import BoardWrapper
from abc import abstractmethod
import copy
import json
import random

PLAY_WRAP = PlayWrapper()
BOARD_WRAP = BoardWrapper()


class Player:

	def __init__(self, name):
		self.name = name
		self.color = EMPTY

	def register(self):
		return self.name

	def receive_stones(self, stone):
		self.set_color(stone)
		return None

	def set_color(self, color):
		self.color = color

	def get_color(self):
		return self.color

	@abstractmethod
	def make_a_move(self, boards):
		pass


class Player1(Player):
	def __init__(self, name):
		super(Player1, self).__init__(name)

	def make_a_move(self, boards):
		history_is_good = PLAY_WRAP.check_history(boards, self.color)
		if history_is_good:
			for col in range(BOARD_SIZE):
				for row in range(BOARD_SIZE):
					if PLAY_WRAP.play(self.color, [row, col], copy.deepcopy(boards)):
						return BOARD_WRAP.point_to_string([row, col])
			return PASS
		return BAD_HISTORY


class Player2(Player):

	def __init__(self, name):
		super(Player2, self).__init__(name)
		self.n = None
		with open('go-player.config') as config_file:
			n = json.load(config_file)
		self.n = n["depth"]

	def make_a_move(self, boards):
		history_is_good = PLAY_WRAP.check_history(boards, self.color)
		if not history_is_good:
			return BAD_HISTORY

		if self.n == 1:
			point = self.find_capture_point(boards)
			if point:
				return BOARD_WRAP.point_to_string(point)
			else:
				return self.normal_move(boards)

	def find_capture_point(self, boards):
		for col in range(BOARD_SIZE):
			for row in range(BOARD_SIZE):
				if PLAY_WRAP.play(self.color, [row, col], copy.deepcopy(boards)) and PLAY_WRAP.is_capture_move(self.color, [row, col], copy.deepcopy(boards[0])):
					return BOARD_WRAP.point_to_string([row, col])
		return False

	def normal_move(self, boards):
		for col in range(BOARD_SIZE):
			for row in range(BOARD_SIZE):
				if PLAY_WRAP.play(self.color, [row, col], boards):
					return BOARD_WRAP.point_to_string([row, col])
		return PASS


class Player3(Player):

	def __init__(self, name):
		super(Player3, self).__init__(name)

	def make_a_move(self, boards):
		row = random.randint(0, BOARD_SIZE)
		if row == BOARD_SIZE:
			return PASS
		col = random.randint(0, BOARD_SIZE - 1)
		return BOARD_WRAP.point_to_string([row, col])
