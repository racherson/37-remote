import sys
import json
import backend

lst = []
count = 0
for line in sys.stdin:
	l = json.loads(line.strip())
	lst.append(l)
	count = count + 1
	if count == 10:
		break

print(backend.sort(json.dumps(lst)))