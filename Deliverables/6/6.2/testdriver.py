import sys
import json
from json import JSONDecoder
import re
import play_wrapper
from player_wrapper import Player_Wrapper
from ref_wrapper import Ref_Wrapper
from helpers import *
import itertools

play_wrap = play_wrapper.PlayWrapper()
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

ls = ["B","W"]

REF_WRAP = Ref_Wrapper()
lines = decode_stacked(s)
#lines = list(lines)

# REF_WRAP.set_players(lines[0],lines[1])
# ls.append([EMPTY_BOARD])
# for i in range(2,len(lines)):
#     new_boards = REF_WRAP.make_action(lines[i])
#     ls.append(new_boards)
#     if isinstance(new_boards[0], str):
#         break

counter = 0
players = []
for line in lines:
    if counter == 0:
        players.append(line)
    elif counter == 1:
        players.append(line)
        REF_WRAP.set_players(players[0], players[1])
    else:
        new_boards = REF_WRAP.make_action(line)
        ls.append(new_boards)
        if isinstance(new_boards[0], str):
            break
    counter += 1

print(json.dumps(ls, separators=(',', ':')))












