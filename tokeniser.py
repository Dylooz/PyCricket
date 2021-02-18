from utils import readFile

tokenTypes = {
  "": False,
  "$": "CLASS_SYMBOL",
  ":": "CONNECTION",
  "#": "INSTANCE_OF",
  "*": "DEFINITION",
  "[": "OPEN_BRACE",
  "]": "CLOSE_BRACE",
  ";": "SEMICOLON",
  "hi": "HIGH_CONSTANT",
  "lo": "LOW_CONSTANT",
  "im": "IMPEDANCE_CONSTANT",
  "plu": "PULL_UP_RESISTOR",
  "pld": "PULL_DOWN_RESISTOR",
  "tri": "TRI_STATE_GATE",
  "not": "NOT_GATE",
  "and": "AND_GATE",
  "or": "OR_GATE",
  "xor": "XOR_GATE",
  "nand": "NAND_GATE",
  "nor": "NOR_GATE",
  "xnor": "XNOR_GATE"
}

class Token:
  def __init__(self, val, tkType, pos):
    self.value = val
    self.type = tkType
    self.pos = pos
    self.parent = None

    if self.type == "IDENT" and len(self.value.split(".")) > 1:
      self.parent = self.value.split(".")[:-1]
      self.value = self.value.split(".")[-1]

  def __repr__(self):
    return f"Token({{value: '{self.value}', type: '{self.type}', pos: {self.pos}}}"

class TokenStream:
  def __init__(self, tokens):
    self.index = 0
    self.tokens = tokens

  def next(self):
    item = self.tokens[self.index]
    self.index += 1
    return item

  def peek(self):
    return self.tokens[self.index]

def identifyToken(token):
  tk = token.lower()
  try:
    return tokenTypes[tk]
  except KeyError:
    return "IDENT"

def tokenise(source):
  program = readFile(source)
  token = ""
  tokens = []
  posInSrc = [0, 1] # 0th char of 1st line
  for char in program:
    posInSrc[0] += 1
    if char == "\n": 
      posInSrc[1] += 1 # increment line by one
      posInSrc[0] = 1
    if char.strip() == "" or char in list(tokenTypes.keys()):
      tkType = identifyToken(token)
      if tkType != False: tokens.append(Token(token, tkType, posInSrc.copy()))
      token = ""
      tkType = identifyToken(char.strip())
      if tkType != False: tokens.append(Token(char, tkType, posInSrc.copy()))
    else: token += char
  return tokens

def nextToken(tokenStream):
  try:
    return tokenStream.next()
  except IndexError:
    with open(SOURCE_FILE, "r") as src:
      lines = src.readlines()
    throwErr(SOURCE_FILE, [len(lines[-1]), len(lines)], "Unexpected EOF", 2)