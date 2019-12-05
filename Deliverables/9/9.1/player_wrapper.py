from player import Player1
from helpers import *


class Player_Wrapper:
	def __init__(self, name):
		# shadow states
		self.register_flag = False
		self.receive_flag = False
		self.player = Player1(name)

	def reset_for_new_game(self):
		print("resetting flags")
		self.register_flag = False
		self.receive_flag = False

	def register(self):
		if self.register_flag:
			print(self.register_flag)
			return GONE_CRAZY
		self.register_flag = True
		return self.player.register()

	def receive_stones(self, stone):
		if self.receive_flag or not self.register_flag:
			return GONE_CRAZY
		self.receive_flag = True
		self.player.set_color(stone)

	def get_color(self):
		return self.player.get_color()

	def make_a_move(self, boards):
		if self.receive_flag and self.register_flag:
			if len(boards) > 3:
				return GONE_CRAZY
			return self.player.make_a_move(boards)
		return GONE_CRAZY

	def end_game(self):
		pass
