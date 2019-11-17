from referee import Referee


class Ref_Wrapper:
	def __init__(self):
		self.ref = Referee()

	def set_players(self, name1, name2):
		return self.ref.set_players(name1, name2)

	def make_action(self, action):
		return self.ref.make_action(action)
