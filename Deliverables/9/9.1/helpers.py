'''
CONSTANTS
'''

BOARD_SIZE = 9
WHITE = 'W'
BLACK = 'B'
EMPTY = ' '
EMPTY_BOARD = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
PASS = "pass"
GONE_CRAZY = "GO has gone crazy!"
LEAGUE = "--league"
CUP = "--cup"
recv_size = 4096

'''
EXCEPTIONS
'''
class InvalidPoint(Exception):
	pass

class InvalidBoard(Exception):
	pass

class InvalidStone(Exception):
	pass

class InvalidMaybeStone(Exception):
	pass

class InvalidMove(Exception):
	pass

class NoDataReceived(Exception):
	pass


'''
GET_OPPONENT
helper
expects stone, returns its opponent if valid input
'''
def get_opponent(stone):
	if stone == BLACK:
		return WHITE
	if stone == WHITE:
		return BLACK


'''
IS_BOARD_EMPTY
helper
expects board, returns True if empty, False otherwise
'''
def is_board_empty(board):
	for row in range(BOARD_SIZE):
		for col in range(BOARD_SIZE):
			if board[row][col] != EMPTY:
				return False
	return True


'''
IS_BOARD
helper
expects board, returns true if valid size, false otherwise
'''
def is_board(board):
	return len(board) == BOARD_SIZE and len(board[0]) == BOARD_SIZE
