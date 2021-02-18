from tokeniser import *
from utils import *
from IC import IC
from program import Program

rhsExprs = {
  "HIGH_CONSTANT": 0,
  "LOW_CONSTANT": 0,
  "IMPEDANCE_CONSTANT": 0,
  "PULL_UP_RESISTOR": 1,
  "PULL_DOWN_RESISTOR": 1,
  "TRI_STATE_GATE": 2,
  "NOT_GATE": 1,
  "AND_GATE": 2,
  "OR_GATE": 2,
  "XOR_GATE": 2,
  "NAND_GATE": 2,
  "NOR_GATE": 2,
  "XNOR_GATE": 2,
  "IDENT": 0
}


def parseLHS(tkGen):
  nextTk = nextToken(tkGen)
  if nextTk.type == "IDENT":
    var = nextTk
    
    nextTk = nextToken(tkGen)
    if nextTk.type == "CONNECTION":
      return ((var, None, None), False)

    elif nextTk.type == "INSTANCE_OF":

      proto = nextToken(tkGen)
      if proto.type != "IDENT": throwErr(SOURCE_FILE, proto.pos, "Expected IC name", 2) 

      nextTk = nextToken(tkGen)
      if nextTk.type != "DEFINITION": throwErr(SOURCE_FILE, proto.pos, "Expected '*'", 2)

      smi = nextToken(tkGen)
      if smi.type != "SEMICOLON": throwErr(SOURCE_FILE, nextTk.pos, "Missing semicolon", 2)

      return ((var, proto.value, proto.pos[1]), True)

    elif nextTk.type == "DEFINITION":

      smi = nextToken(tkGen)
      if smi.type != "SEMICOLON": throwErr(SOURCE_FILE, nextTk.pos, "Missing semicolon", 2)

      return ((var, None, None), True)

  else:
    throwErr(SOURCE_FILE, nextTk.pos, "Expected identifier as left-hand side of assignment or defintion", 2)

def parseRHS(tkGen):
  op = nextToken(tkGen)
  if not (op.type in rhsExprs): throwErr(SOURCE_FILE, op.pos, f"Unexpected '{op.value}' in right-hand side of assignment", 2)

  if rhsExprs[op.type] == 0:
    nextTk = nextToken(tkGen)
    if nextTk.type != "SEMICOLON": throwErr(SOURCE_FILE, nextTk.pos, "Missing semicolon", 2) 

    return (op.type, [op])

  else:
    args = []
    for i in range(rhsExprs[op.type]):
      arg = nextToken(tkGen)
      if not (arg.type in ["HIGH_CONSTANT", "LOW_CONSTANT", "IMPEDANCE_CONSTANT", "IDENT"]): throwErr(SOURCE_FILE, arg.pos, f"Unexpected '{nextTk.value}' in right-hand side of assignment", 2)
      args.append(arg)

    nextTk = nextToken(tkGen)
    if nextTk.type != "SEMICOLON": throwErr(SOURCE_FILE, nextTk.pos, "Missing semicolon", 2)

    return (op.type, args)

def parseExpr(tokens):
  variable, terminated = parseLHS(tokens)
  if not terminated:
    op, arg = parseRHS(tokens)
    return (variable, op, arg)

  return (variable, None, [])

def parse(tokens):
  tkGen = TokenStream(tokens)
  program = Program()

  while tkGen.index < len(tokens):
    token = tkGen.peek()
    if token.type == "CLASS_SYMBOL":
      nextToken(tkGen)

      nextTk = nextToken(tkGen)
      if nextTk.type != "IDENT": throwErr(SOURCE_FILE, nextTk.pos, "Expected IC name", 2)
      
      curIC = IC(nextTk.value)
      
      nextTk = nextToken(tkGen)
      if nextTk.type != "OPEN_BRACE": throwErr(SOURCE_FILE, nextTk.pos, "Expected IC defintion", 2)

      while tkGen.peek().type != "CLOSE_BRACE":
        local, op, arg = parseExpr(tkGen)
        curIC.addTreeExpr(local, op, arg)

      nextToken(tkGen)
      program.addIC(curIC)

    else:
      _global, op, arg = parseExpr(tkGen)

      program.addTreeExpr(_global, op, arg)

  return program