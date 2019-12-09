from helpers import *


'''
OCCUPIED
Expects board, point
returns true if board at point is occupied, false otherwise
'''
def occupied(board, point):
	# return board[point[0]][point[1]] != " "
	return board[point[0]][point[1]] != EMPTY


'''
OCCUPIES
Expects board, stone, point
returns true if board at point occupied by stone, false otherwise
'''
def occupies(board, stone, point):
	return board[point[0]][point[1]] == stone


'''
PLACE
expects board, stone, point
returns board if can place, "This seat is taken!" otherwise
'''
def place(board, stone, point):
	if board[point[0]][point[1]] == EMPTY:
		board[point[0]][point[1]] = stone
		return board
	return "This seat is taken!"


'''
REACHABLE
expects board, point, maybe_stone
returns true if maybe_stone reachable from point, false otherwise
'''
def reachable(board, point, maybe_stone):
	stone = board[point[0]][point[1]]
	visited = [[False]*BOARD_SIZE for x in range(BOARD_SIZE)]
	return dfs(board, point, stone, maybe_stone, visited)


'''
DFS
helper for reachable
expects board, point, stone, maybe_stone, visited array
returns true if maybe_stone reachable from point, false otherwise
'''
def dfs(board, point, stone, maybe_stone, visited):
	x = point[0]
	y = point[1]
	if x > BOARD_SIZE-1 or x < 0 or y > BOARD_SIZE-1 or y < 0:
		return False
	if visited[x][y]:
		return False
	else:
		visited[x][y] = True
	if board[x][y] != stone and board[x][y] != maybe_stone:
		return False
	if board[x][y] == maybe_stone:
		return True

	right = dfs(board, [x + 1, y], stone, maybe_stone, visited)
	left = dfs(board, [x - 1, y], stone, maybe_stone, visited)
	up = dfs(board, [x, y + 1], stone, maybe_stone, visited)
	down = dfs(board, [x, y - 1], stone, maybe_stone, visited)
	return up or down or left or right


'''
REMOVE
expects board, stone, point
returns board if can remove, "I am just a board! I cannot remove what is not there!" otherwise
'''
def remove(board, stone, point):
	if board[point[0]][point[1]] != stone:
		return "I am just a board! I cannot remove what is not there!"
	board[point[0]][point[1]] = EMPTY
	return board

'''
GET_POINTS
expects board, maybe_stone
'''
def get_points(board, maybe_stone):
	points = []
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if board[j][i] == maybe_stone:
				points.append([i, j])
	return points
