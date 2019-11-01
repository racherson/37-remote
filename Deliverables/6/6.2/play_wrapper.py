#wrapper class for Play
import play

class PlayWrapper:

	def __init__(self):
		pass

	def action(self, act):
		return play.action(act)

	def score(self, board):
		return play.score(board)

	def check_history(self,boards,stone):
		return play.check_history(boards,stone)

	def play(self,stone,point,boards):
		return play.play(stone,point,boards)

	def is_capture_move(self,stone,point,board):
		return play.is_capture_move(stone,point,board)

	def get_next_board(self,stone,point,board):
		return play.get_next_board(stone,point,board)