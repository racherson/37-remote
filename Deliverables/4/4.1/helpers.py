BOARD_SIZE = 19
WHITE = 'W'
BLACK = 'B'
EMPTY = ' '

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
expects board, returns true if is a board (instead of string)
'''
def is_board(board):
	return len(board) == BOARD_SIZE and len(board[0]) == BOARD_SIZE