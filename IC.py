class IC:
  def __init__(self, name):
    self.name = name
    self.locals = {}
    self.tree = []

  def addLocal(self, name, proto=None, line=None):
    if name in self.locals:
      return False
    else:  
      self.locals[name] = { "name": name, "type": proto, "defined": line }
      return True

  def addTreeExpr(self, local, op , args=None):
    if local[0].parent == None: self.addLocal(local[0].value, local[1], local[2])
    local = local[0]
    if op != None:
      newArgs = []
      for arg in args:
        if arg.type == "IDENT":
          newArgs.append({"name": arg.value, "parent": arg.parent})
      self.tree.append({ "dest": {"name": local.value, "parent": local.parent}, "op": op, "arg": newArgs, "line": local.pos[1] })

  def toDictionary(self):
    return {"name": self.name, "locals": self.locals, "tree": self.tree}

  def __repr__(self):
    return f"IC({{name: '{self.name}', locals: {self.locals}, tree: {self.tree}}})"