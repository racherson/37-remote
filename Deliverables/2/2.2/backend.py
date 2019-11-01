import json

def sort(lst):
	lst = json.loads(lst)

	jsonList = []
	strList = []
	numList = []
	
	for item in lst:
		if isinstance(item, dict):
			jsonList.append(item)
		elif isinstance(item, str):
			strList.append(item)
		else:
			numList.append(item)

	numList.sort()
	strList.sort()
	jsonList = sorted(jsonList, key=mykey)

	return json.dumps(numList + strList + jsonList)

def mykey(x):
	depth = 0;
	while isinstance(x, dict):
		depth = depth + 1
		x = x["name"]
	return depth, int(isinstance(x, str)), x