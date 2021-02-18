def throwErr(file, pos, msg, code):
  print(f"{file}:{str(pos[1])}:{str(pos[0])} - {msg}")
  exit(code)

def readFile(filename):
  with open(filename, "r") as foo:
    return foo.read()

import json
def readInput(filename):
	with open(filename, "r") as file:
		return json.loads(bytearray(map(lambda x: int(x, 16), file.read(-1).split(" "))).decode("utf-8"))