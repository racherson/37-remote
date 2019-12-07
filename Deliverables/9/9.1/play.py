# play
from board_wrapper import BoardWrapper
import copy
from helpers import *
BOARD_WRAP = BoardWrapper()

'''
ACTION
expects act = [Stone,Move]
'''
def action(act):
	stone,move = act

	if move == "pass":
		return True

	else: # move is play
		point, boards = move
		if check_history(boards, stone):
			return play(stone, point, boards)
		return False


'''
PLAY
expects stone, point, boards
plays, returns true if valid, false otherwise
'''
def play(stone, point, boards):
	board = boards[0]
	new_board = BOARD_WRAP.place(copy.deepcopy(board), stone, point)

	if not is_board(new_board):
		return False

	new_board = capture_opponent(new_board, get_opponent(stone))

	if not is_board(new_board):
		return False

	# case when board returns to state after stone's previous turn
	opponent = BLACK if stone == WHITE else WHITE
	new_board = capture_opponent(new_board, opponent)
	if len(boards) >= 2 and new_board == boards[1]:
		return False

	# suicide case
	if is_suicide(new_board, stone):
		return False

	return True


'''
CHECK_HISTORY
expects array of 1-3 boards, stone
returns true if history is valid, false otherwise
'''
def check_history(boards, stone):
	if len(boards) == 1:
		return is_board_empty(boards[0]) and stone == BLACK

	if not check_alternating(stone, boards[0], boards[1]):
		return False

	if len(boards) == 2:
		if stone == BLACK:
			return False
		if not is_board_empty(boards[1]):
			return False

		return len(BOARD_WRAP.get_points(boards[0], WHITE)) == 0 and len(BOARD_WRAP.get_points(boards[0], BLACK)) <= 1

	if len(boards) == 3:

		if not check_valid_board(boards[2]):
			return False

		if not check_alternating(stone, boards[2], boards[1]):
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
def check_alternating(stone, board1, board2):
	opp_diff = len(BOARD_WRAP.get_points(board1, get_opponent(stone))) - len(BOARD_WRAP.get_points(board2, get_opponent(stone)))
	stone_diff = len(BOARD_WRAP.get_points(board1, stone)) - len(BOARD_WRAP.get_points(board2, stone))
	if (opp_diff != 1 and opp_diff != 0) or stone_diff > 0:
		return False

	return True



'''
CHECK_TURN
expects stone and two boards in sequential order
returns true if the turn taken was valid, false otherwise
'''
def check_turn(stone, old_board, new_board):

	if old_board == new_board:
		return True

	points_old = BOARD_WRAP.get_points(old_board, stone)
	points_new = BOARD_WRAP.get_points(new_board, stone)

	opponent_old = BOARD_WRAP.get_points(old_board,get_opponent(stone))
	intersection = [el for el in points_new if el in opponent_old]
	if len(intersection) != 0:
		return False

	if len(points_old) == len(points_new) - 1:
		new_point = list(set(points_new)-set(points_old))[0]
		cpy = copy.deepcopy(old_board)
		moved_board = BOARD_WRAP.place(cpy, stone, new_point)
		if isinstance(moved_board, str):
			return False

		moved_board = capture_opponent(moved_board, get_opponent(stone))

		if is_suicide(moved_board, stone):
			return False

		return moved_board == new_board
	return False


'''
CAPTURE_OPPONENT
takes in board and opponent's stone
captures opponent's stones and returns new board
'''
def capture_opponent(board, opponent):
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
	captured = get_captured(board)
	for point in captured:
		if board[point[0]][point[1]] == stone:
			return True
	return False


def check_valid_board(board):
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if board[row][col] == BLACK or board[row][col] == WHITE:
				if has_no_liberties(board, [row, col]):
					return False
	return True


'''
GET_CAPTURED
takes in board
returns a list of points where stones have no liberties
'''
def get_captured(board):
	captured = []
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if has_no_liberties(board, [row, col]):
				captured.append([row, col])
	return captured


'''
HAS_NO_LIBERTIES
expeects board and point
returns true if stone at that point has no liberties, false otherwise
'''
def has_no_liberties(board, point):
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

	score = {}
	score[BLACK] = black
	score[WHITE] = white

	return score


def is_capture_move(stone, point, board):
	board = BOARD_WRAP.place(board, stone, point)
	new_board = capture_opponent(copy.deepcopy(board), get_opponent(stone))
	return new_board != board


def get_next_board(stone, point, board):
	new_board = BOARD_WRAP.place(copy.deepcopy(board), stone, point)
	new_board = capture_opponent(copy.deepcopy(new_board), get_opponent(stone))
	return new_board
