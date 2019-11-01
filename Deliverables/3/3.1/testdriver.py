import sys
import json
from json import JSONDecoder, JSONDecodeError
import re
import board_wrapper

board_wrap = board_wrapper.BoardWrapper()
NOT_WHITESPACE = re.compile(r'[^\s]')

def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(document, pos)
        except JSONDecodeError:
            print("ERROR")
        yield obj

s = ""
for line in sys.stdin:
	s += line

ls = []
for line in decode_stacked(s):
	if len(line) != 2:
		raise Exception("json object is invalid!")
	#CHECK LENGTHS OF STATEMENTS IN EACH IF STATEMENT
	board = line[0]
	statement = line[1]

	#queries
	if statement[0] == "occupied?":
		point = statement[1]
		ls.append(board_wrap.occupied(board,point))
	elif statement[0] == "occupies?":
		stone,point = statement[1:]
		ls.append(board_wrap.occupies(board,stone,point))
	elif statement[0] == "reachable?":
		point,maybe_stone = statement[1:]
		ls.append(board_wrap.reachable(board,point,maybe_stone))

	#commands
	elif statement[0] == "place":
		stone,point = statement[1:]
		ls.append(board_wrap.place(board,stone,point))
	elif statement[0] == "remove":
		stone,point = statement[1:]
		ls.append(board_wrap.remove(board,stone,point))
	elif statement[0] == "get-points":
		maybe_stone = statement[1]
		ls.append(board_wrap.get_points(board,maybe_stone))
	else:
		raise Exception("invalid statement")

print(json.dumps(ls, separators=(',', ':')))















