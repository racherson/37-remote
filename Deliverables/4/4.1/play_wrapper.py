#wrapper class for Play
import play

class PlayWrapper:

	def __init__(self):
		pass

	def action(self, act):
		return play.action(act)

	def score(self, board):
		return play.score(board)