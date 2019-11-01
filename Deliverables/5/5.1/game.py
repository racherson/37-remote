from player import Player1, Player2
from helpers import *


class Game:
	def __init__(self):
		player1 = None

	def register(self):
		self.player1 = Player1()
		return self.player1.get_name()

	def receive_stones(self,stone):
		self.player1.set_color(stone)

	def make_a_move(self, boards):
		if self.player1.get_color() == EMPTY:
			raise Exception("Player did not receive stones yet")
		return self.player1.make_a_move(boards)
