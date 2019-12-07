import sys
import json
from json import JSONDecoder, JSONDecodeError
import re
import play_wrapper

play_wrap = play_wrapper.PlayWrapper()
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
    if len(line) == 2:
        ls.append(play_wrap.action(line))
    else:
        ls.append(play_wrap.score(line))

print(json.dumps(ls, separators=(',', ':')))
