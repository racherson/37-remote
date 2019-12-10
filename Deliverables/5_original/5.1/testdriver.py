import sys
import json
from json import JSONDecoder, JSONDecodeError
import re
import play_wrapper
from game import Game

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
        except JSONDecodeError:
            raise Exception("Can't parse")
        yield obj

s = ""
for line in sys.stdin:
	s += line

ls = []

gameplay = Game()

for line in decode_stacked(s):
    if len(line) == 1:
        if line[0] == "register":
            ls.append(gameplay.register())
            continue
    elif len(line) == 2:
        if line[0] == "receive-stones":
            gameplay.receive_stones(line[1])
        elif line[0] == "make-a-move":
            output = gameplay.make_a_move(line[1])
            if len(output) == 2:
                ls.append(point_to_string(output))
            else:
                ls.append(output)
    else:
        raise Exception("Invalid Input")


print(json.dumps(ls, separators=(',', ':')))
