class Program:
  def __init__(self):
    self.ICs = {}
    self.globals = {}
    self.tree = []

  def addGlobal(self, name, proto=None, line=None):
    if name in self.globals:
      return False
    else: 
      self.globals[name] = { "name": name, "type": proto, "defined": line }
      return True

  def addTreeExpr(self, _global, op, args=None):
    if _global[0].parent == None: self.addGlobal(_global[0].value, _global[1], _global[2])
    _global = _global[0]
    if op != None:
      newArgs = []
      for arg in args:
        if arg.type == "IDENT":
          newArgs.append({"name": arg.value, "parent": arg.parent, "type": "IDENT"})
        else:
          newArgs.append({"type": arg.type})
      self.tree.append({ "dest": {"name": _global.value, "parent": _global.parent}, "op": op, "arg": newArgs, "line": _global.pos[1] })

  def addIC(self, IC):
    self.ICs[IC.name] = IC

  def toDictionary(self):
    dictICs = {}
    for ick in self.ICs: 
      dictICs[ick] = self.ICs[ick].toDictionary()  
    return {"ICs": dictICs, "globals": self.globals, "tree": self.tree}

  def __repr__(self):
    return f"Program({{ICs: '{self.ICs}', globals: {self.globals}, tree: {self.tree}}})"