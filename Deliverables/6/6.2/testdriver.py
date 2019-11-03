import sys
import json
from json import JSONDecoder
import re
from ref_wrapper import Ref_Wrapper
from helpers import *

REF_WRAP = Ref_Wrapper()
NOT_WHITESPACE = re.compile(r'[^\s]')

def point_to_string(point):
    return str(point[1]+1) + "-" + str(point[0]+1)

def decode_stacked(document, pos=0, decoder=JSONDecoder()):
    while True:
        match = NOT_WHITESPACE.search(document, pos)
        if not match:
            return
        pos = match.start()

        try:
            obj, pos = decoder.raw_decode(document, pos)
        except:
            raise Exception("Can't parse")
        yield obj

s = ""
for line in sys.stdin:
	s += line

ls = []
counter = 0
players = []
most_recent_boards = [EMPTY_BOARD]
for line in decode_stacked(s):
    if counter == 0:
        players.append(line)
    elif counter == 1:
        players.append(line)
        color1, color2 = REF_WRAP.set_players(players[0], players[1])
        ls.append(color1)
        ls.append(color2)
    else:
        ls.append(most_recent_boards)
        new_boards = REF_WRAP.make_action(line)
        most_recent_boards = new_boards
        if isinstance(new_boards[0], str):
            break
    counter += 1

print(json.dumps(ls, separators=(',', ':')))












