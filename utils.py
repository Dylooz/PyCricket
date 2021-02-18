def throwErr(file, pos, msg, code):
  print(f"{file}:{str(pos[1])}:{str(pos[0])} - {msg}")
  exit(code)

def readFile(filename):
  with open(filename, "r") as foo:
    return foo.read()