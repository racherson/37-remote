#play
from board_wrapper import BoardWrapper
import copy
from helpers import *
BOARD_WRAP = BoardWrapper()

'''
ACTION
expects act = [Stone,Move]
returns true if valid move and false if not
'''
def action(act):
	stone,move = act

	if move == "pass":
		return True

	else: #move is play
		point,boards = move
		if check_history(boards, stone):
			return play(stone,point,boards)
		return False

'''
PLAY
expects stone, point, boards
plays, returns true if valid, false otherwise
'''
def play(stone, point, boards):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(stone)
	BOARD_WRAP.check_point(point)
	for board in boards:
		BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	board = boards[0]
	new_board = BOARD_WRAP.place(board,stone,point)

	if not is_board(new_board):
		return False

	opponent = get_opponent(stone)
	new_board = capture_opponent(new_board, opponent)

	if not is_board(new_board):
		return False

	#case when board returns to state after stone's previous turn
	new_board = capture_opponent(new_board, opponent)
	if len(boards) >= 2 and new_board == boards[1]:
		return False

	#suicide case
	if is_suicide(new_board,stone):
		return False

	return True

'''
CHECK_HISTORY
expects array of 1-3 boards, stone
returns true if history is valid, false otherwise
'''
def check_history(boards, stone):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(stone)
	for board in boards:
		BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	if len(boards) == 1:
		return is_board_empty(boards[0]) and stone == BLACK

	if not check_alternating(stone, boards):
		return False

	if len(boards) == 2:
		if stone == BLACK:
			return False
		if not is_board_empty(boards[1]):
			return False

		return len(BOARD_WRAP.get_points(boards[0],WHITE)) == 0 and len(BOARD_WRAP.get_points(boards[0],BLACK)) <= 1

	if len(boards) == 3:
		if not check_valid_board(boards[2]):
			return False
		
		if boards[0] == boards[1] == boards[2] or boards[0] == boards[2]:
			return False

		if is_board_empty(boards[1]) and is_board_empty(boards[2]) and len(BOARD_WRAP.get_points(boards[0], BLACK)) > len(BOARD_WRAP.get_points(boards[0], WHITE)):
			return False

		if not check_turn(stone, boards[2], boards[1]) or not check_turn(get_opponent(stone), boards[1], boards[0]):
			return False

	return True

'''
CHECK_ALTERNATING
expects array of 1-3 boards, current turn's stone
returns true if the players alternated, false otherwise
'''
def check_alternating(stone, boards):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(stone)
	for board in boards:
		BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	num_boards = len(boards)

	if num_boards == 2 or num_boards == 3:
		opp_diff = len(BOARD_WRAP.get_points(boards[0], get_opponent(stone))) - len(BOARD_WRAP.get_points(boards[1], get_opponent(stone)))
		stone_diff = len(BOARD_WRAP.get_points(boards[0], stone)) - len(BOARD_WRAP.get_points(boards[1], stone))
		if (opp_diff != 1 and opp_diff != 0) or stone_diff > 0:
			return False

		if num_boards == 3:
			opp_diff = len(BOARD_WRAP.get_points(boards[1], get_opponent(stone))) - len(BOARD_WRAP.get_points(boards[2], get_opponent(stone)))
			stone_diff = len(BOARD_WRAP.get_points(boards[1], stone)) - len(BOARD_WRAP.get_points(boards[2], stone))
			if (stone_diff != 1 and stone_diff != 0) or opp_diff > 0:
				return False
	return True

'''
CHECK_TURN
expects stone and two boards in sequential order
returns true if the turn taken was valid, false otherwise
'''
def check_turn(stone, old_board, new_board):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(stone)
	BOARD_WRAP.check_board(old_board)
	BOARD_WRAP.check_board(new_board)

	'''
	CODE
	'''
	if old_board == new_board:
		return True

	points_old = BOARD_WRAP.get_points(old_board, stone)
	points_new = BOARD_WRAP.get_points(new_board, stone)

	if len(points_old) == len(points_new) - 1:
		new_point = list(set(points_new)-set(points_old))[0]
		cpy = copy.deepcopy(old_board)
		moved_board = BOARD_WRAP.place(cpy, stone, new_point)

		moved_board = capture_opponent(moved_board, get_opponent(stone))

		if is_suicide(moved_board, stone):
			return False

		return moved_board == new_board
	return False

'''
CHECK_VALID_BOARD
expects board and returns true if board is possible (no stones that should have been captured),
false otherwise
'''
def check_valid_board(board):
	b = BOARD_WRAP.get_points(board,BLACK)
	w = BOARD_WRAP.get_points(board,WHITE)
	points = b + w

	for point in points:
		if has_no_liberties(board,point):
			return False

	return True


'''
CAPTURE_OPPONENT
takes in board and opponent's stone
captures opponent's stones and returns new board or "I am just a board! I cannot remove what is not 
there!" if fails to capture 
'''
def capture_opponent(board, opponent):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(opponent)
	BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	new_board = board
	captured = get_captured(board)
	for point in captured:
		if board[point[0]][point[1]] == opponent:
			new_board = BOARD_WRAP.remove(board, opponent, point)
	return new_board

'''
IS_SUICIDE
expects board and stone
returns true if suicide (invalid), false otherwise
'''
def is_suicide(board, stone):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_stone(stone)
	BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	captured = get_captured(board)
	for point in captured:
		if board[point[0]][point[1]] == stone:
			return True
	return False

'''
GET_CAPTURED
takes in board
returns a list of points where stones have no liberties
'''
def get_captured(board):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	captured = []
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if has_no_liberties(board,[row,col]):
				captured.append([row,col])
	return captured

'''
HAS_NO_LIBERTIES
expeects board and point
returns true if stone at that point has no liberties, false otherwise
'''
def has_no_liberties(board, point):
	'''
	INTERFACE
	'''
	BOARD_WRAP.check_point(point)
	BOARD_WRAP.check_board(board)

	'''
	CODE
	'''
	return not BOARD_WRAP.reachable(board, point, EMPTY)

'''
SCORE
expects board
returns a dictionary of form {"B":val,"W":val} with the score
'''
def score(board):
	white = 0
	black = 0

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if board[i][j] == BLACK:
				black += 1
			elif board[i][j] == WHITE:
				white += 1
			else:
				point = [i,j]
				if BOARD_WRAP.reachable(board, point, BLACK) and not BOARD_WRAP.reachable(board, point, WHITE):
					black += 1
				if not BOARD_WRAP.reachable(board, point, BLACK) and BOARD_WRAP.reachable(board, point, WHITE):
					white += 1

	score = {BLACK:black,WHITE:white}

	return score
