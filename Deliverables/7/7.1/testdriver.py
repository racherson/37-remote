import sys
import json
from json import JSONDecoder, JSONDecodeError
import re
import remote_player_wrapper

player_wrap = remote_player_wrapper.RemotePlayerWrapper()
NOT_WHITESPACE = re.compile(r'[^\s]')
GONE_CRAZY = "GO has gone crazy!"

def point_to_string(point):
    return str(point[1]+1) + "-" + str(point[0]+1)


def check_for_crazy(response):
    if response == "GO has gone crazy!":
        return True
    return False

def end_if_crazy(ls):
    ls.append(GONE_CRAZY)
    raise Exception("Invalid Input")


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
            response = player_wrap.register()
            ls.append(response)
            if check_for_crazy(response):
                break
            continue
        else:
            end_if_crazy(ls)
    elif len(line) == 2:
        if line[0] == "receive-stones":
            response = player_wrap.receive_stones(line[1])
            if check_for_crazy(response):
                ls.append(response)
                break
        elif line[0] == "make-a-move":
            output = player_wrap.make_a_move(line[1])
            if len(output) == 2:
                ls.append(point_to_string(output))
            else:
                ls.append(output)
                if check_for_crazy(output):
                    break
        else:
            end_if_crazy(ls)
    else:
        end_if_crazy(ls)

player_wrap.close()
player_wrap.sock.close()
print(json.dumps(ls, separators=(',', ':')))
