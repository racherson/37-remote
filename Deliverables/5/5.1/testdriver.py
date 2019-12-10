import sys
import json
from json import JSONDecoder, JSONDecodeError
import re
from player_wrapper import Player_Wrapper
import play_wrapper

play_wrap = play_wrapper.PlayWrapper()
p1 = Player_Wrapper("no name")
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
        except JSONDecodeError:
            raise Exception("Can't parse")
        yield obj

s = ""
for line in sys.stdin:
	s += line

ls = []


for line in decode_stacked(s):
    if len(line) == 1:
        if line[0] == "register":
            ls.append(p1.register())
            continue
    elif len(line) == 2:
        if line[0] == "receive-stones":
            p1.receive_stones(line[1])
        elif line[0] == "make-a-move":
            output = p1.make_a_move(line[1])
            if len(output) == 2:
                ls.append(point_to_string(output))
            else:
                ls.append(output)
    else:
        raise Exception("Invalid Input")


print(json.dumps(ls, separators=(',', ':')))
