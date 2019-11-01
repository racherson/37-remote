import sys
import json
from json import JSONDecoder
import re
import play_wrapper
from player_wrapper import Player_Wrapper
from ref_wrapper import Ref_Wrapper
from helpers import *

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
lines = list(lines)

REF_WRAP.set_players(lines[0],lines[1])
ls.append([EMPTY_BOARD])
for i in range(2,len(lines)):
    new_boards = REF_WRAP.make_action(lines[i])
    ls.append(new_boards)
    if isinstance(new_boards[0], str):
        break
    

    # if len(line) == 1:
    #     if line[0] == "register":
    #         ls.append(PLAYER_WRAP.register())
    #         continue
    # elif len(line) == 2:
    #     if line[0] == "receive-stones":
    #         PLAYER_WRAP.receive_stones(line[1])
    #     elif line[0] == "make-a-move":
    #         output = PLAYER_WRAP.make_a_move(line[1])
    #         if len(output) == 2:
    #             ls.append(point_to_string(output))
    #         else:
    #             ls.append(output)
    # else:
    #     raise Exception("Invalid Input")


print(json.dumps(ls, separators=(',', ':')))
