import inner_board as b

BOARD_SIZE = 19

class BoardWrapper:

	def __init__(self):
		pass
	'''
	OCCUPIED
	checks parameters, calls inner board
	'''
	def occupied(self,board,point):
		point = self.string_to_point(point)
		self.check_board(board)
		self.check_point(point)
		return b.occupied(board,point)

	'''
	OCCUPIES
	checks parameters, calles inner board
	'''
	def occupies(self,board,stone,point):
		point = self.string_to_point(point)
		self.check_board(board)
		self.check_stone(stone)
		self.check_point(point)
		return b.occupies(board,stone,point)

	'''
	PLACE
	checks parameters, calles inner board
	'''
	def place(self,board,stone,point):
		point = self.string_to_point(point)
		self.check_board(board)
		self.check_stone(stone)
		self.check_point(point)
		return b.place(board,stone,point)

	'''
	REACHABLE
	checks parameters, calles inner board
	'''
	def reachable(self,board,point,maybe_stone):
		point = self.string_to_point(point)
		self.check_board(board)
		self.check_point(point)
		self.check_stone(maybe_stone)
		return b.reachable(board,point,maybe_stone)

	'''
	REMOVE
	checks parameters, calles inner board
	'''
	def remove(self,board,stone,point):
		point = self.string_to_point(point)
		self.check_board(board)
		self.check_stone(stone)
		self.check_point(point)
		return b.remove(board,stone,point)

	'''
	GET_POINTS
	checks parameters, calles inner board
	'''
	def get_points(self,board,maybe_stone):
		self.check_board(board)
		self.check_stone(maybe_stone)
		return b.get_points(board,maybe_stone)

	'''
	STRING_TO_POINT
	converts input str "x-y" to int list [y, x] 
	'''
	def string_to_point(self,point):
		if isinstance(point,str) or isinstance(point,unicode):
			str_arr = point.split("-")
			int_arr = [int(coord) for coord in str_arr]
			return [int_arr[1]-1, int_arr[0]-1]
		return point

	'''
	CHECK_BOARD
	makes sure board is valid before wrapper calls the board 
	takes as input Board object - 19 rows, 19 cols
	returns True if valid, raises exception if not
	'''
	def check_board(self,board):
		#check number of rows
		if len(board) != BOARD_SIZE:
			raise Exception('Board must contain 19 rows.')

		#check length of all rows (because python is fake)
		#check board only has valid stones,maybestones
		for row in board:
			if len(row) != BOARD_SIZE:
				raise Exception('Board must be 19 columns wide.')
			for item in row:
				if item != " " and item != 'B' and item != 'W':
					raise Exception('Board contains invalid stones.')
		return True

	'''
	CHECK_POINT
	makes sure point is valid before passing to a method in board
	takes as input point (after converting to arr from str)
	returns True if valid, raises exception if not
	'''
	def check_point(self,point):
		#check length
		if len(point) != 2:
			raise Exception('Received invalid point.')

		#make sure both coords are ints
		if not isinstance(point[0],int) or not isinstance(point[1],int):
			raise Exception('Received invalid point.')

		#check coords in range
		if point[0] < 0 or point[0] > BOARD_SIZE-1 or point[1] < 0 or point[1] > BOARD_SIZE-1:
			raise Exception('Received invalid point.')

		return True

	'''
	CHECK_STONE
	makes sure stone is valid before passing to a method in board
	takes as input stone
	returns True if valid, raises exception if not
	'''
	def check_stone(self,stone):
		if stone != ' ' and stone != 'B' and stone != 'W':
			raise Exception('Received invalid Stone or MaybeStone.')

		return True







