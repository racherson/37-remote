from player import Player1
from helpers import *


class DefaultPlayerWrapper:
	def __init__(self):
		# shadow states
		self.register_flag = False
		self.receive_flag = False
		self.player = Player1()

	def reset_for_new_game(self):
		self.register_flag = False
		self.receive_flag = False

	def register(self):
		print("register flag is", self.register_flag)
		if self.register_flag:
			return GONE_CRAZY
		self.register_flag = True
		print("registering default player")
		return self.player.get_name()

	def receive_stones(self, stone):
		if self.receive_flag or not self.register_flag:
			return GONE_CRAZY
		self.receive_flag = True
		print("receiving stones default player")
		self.player.set_color(stone)

	def set_name(self, name):
		self.player.set_name(name)

	def get_name(self):
		return self.player.get_name()

	def get_color(self):
		return self.player.get_color()

	def make_a_move(self, boards):
		if self.receive_flag and self.register_flag:
			if len(boards) > 3:
				return GONE_CRAZY
			print("make a move default player")
			return self.player.make_a_move(boards)
		return GONE_CRAZY

	def end_game(self):
		pass
