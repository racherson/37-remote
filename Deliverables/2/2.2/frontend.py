import sys
import json
import backend
from json import JSONDecoder, JSONDecodeError
import re

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

sortedList = []
tempList = []
count = 0
for line in decode_stacked(s):
	tempList.append(line)
	count = count + 1
	if count == 10:
		count = 0
		sortedList.append(json.loads(backend.sort(json.dumps(tempList))))
		tempList = []


print(json.dumps(sortedList))
