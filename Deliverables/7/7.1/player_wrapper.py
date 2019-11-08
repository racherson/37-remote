from player import Player
from helpers import *


class Player_Wrapper:
	def __init__(self):
		self.player = None

	def register(self):
		self.player = Player()
		return self.player.get_name()

	def receive_stones(self, stone):
		self.player.set_color(stone)

	def set_name(self, name):
		self.player.set_name(name)

	def get_name(self):
		return self.player.get_name()

	def get_color(self):
		return self.player.get_color()

	def make_a_move(self, boards):
		if self.player.get_color() == EMPTY:
			raise Exception("Player did not receive stones yet")
		return self.player.make_a_move(boards)
