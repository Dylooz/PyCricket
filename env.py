from state import State

class Env:
	def __init__(self, obj, src):
		self.globals = obj["globals"]
		self.source_file = src
		self.ICs = obj["ICs"]
		self.loadedICs = {}
		self.opl = obj["tree"]
		self.instances = {}
		self.defaultState = "z"

		self.states = {
			"HIGH_CONSTANT": "h",
			"LOW_CONSTANT": "l",
			"IMPEDANCE_CONSTANT": "z"
		}

		self.logicFunctions = {
			"IDENT": (lambda args, line: self.resolveVar(args[0]["name"], args[0]["parent"], line)["state"]),
			"HIGH_CONSTANT": (lambda args, line: State("h")),
			"LOW_CONSTANT": (lambda args, line: State("l")),
			"IMPEDANCE_CONSTANT": (lambda args, line: State("z")),
			"PULL_UP_RESISTOR": (lambda args, line: self.pullUp(args, line)),
			"PULL_DOWN_RESISTOR": (lambda args, line: self.pullDown(args, line)),
			"TRI_STATE_GATE": (lambda args, line: self.triState(args, line)),
			"NOT_GATE": (lambda args, line: self.notGate(args, line)),
			"AND_GATE": (lambda args, line: self.andGate(args, line)),
			"OR_GATE": (lambda args, line: self.orGate(args, line)),
			"XOR_GATE": (lambda args, line: self.xorGate(args, line)),
			"NAND_GATE": (lambda args, line: self.nandGate(args, line)),
	  	"NOR_GATE": (lambda args, line: self.norGate(args, line)),
	  	"XNOR_GATE": (lambda args, line: self.xnorGate(args, line))
		}

		self.execRules = {
			"doErrorOnHighZInput": False,
		}

	def pullUp(self, args, line):
		return self.resolveVar(args[0]["name"], args[0]["parent"], line).pullUp()

	def pullDown(self, args, line):
		return self.resolveVar(args[0]["name"], args[0]["parent"], line).pullDown()

	def triState(self, args, line):
		if self.resolveVar(args[1]["name"], args[1]["parent"], line).state == "h":
			return self.resolveVar(args[0]["name"], args[0]["parent"], line)
		else:
			return State("z")

	def notGate(self, args, line):
		if args[0]["type"] == "IDENT":
			currentState = self.resolveVar(args[0]["name"], args[0]["parent"], line).state
		else:
			currentState = self.states(args[0]["type"])
		if currentState == "h":
			return State("l")
		elif currentState == "l":
			return State("h")
		else:
			return State("z")

	def andGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] == "h" and currentStates[1] == "h":
			return State("h")
		else:
			return State("l")

	def orGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] == "h" or currentStates[1] == "h":
			return State("h")
		else:
			return State("l")

	def xorGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] != currentStates[1]:
			return State("h")
		else:
			return State("l")

	def nandGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] == "h" and currentStates[1] == "h":
			return State("l")
		else:
			return State("h")

	def norGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] == "h" or currentStates[1] == "h":
			return State("l")
		else:
			return State("h")

	def xnorGate(self, args, line):
		currentStates = []
		
		if args[0]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[0]["name"], args[0]["parent"], line).state)
		else:
			currentStates.append(self.states(args[0]["type"]))
		if args[1]["type"] == "IDENT":
			currentStates.append(self.resolveVar(args[1]["name"], args[1]["parent"], line).state)
		else:
			currentStates.append(self.states(args[1]["type"]))

		if currentStates[0] == "z" or currentStates[1] == "z":
			return State("z")
		elif currentStates[0] != currentStates[1]:
			return State("l")
		else:
			return State("h")

	def init(self):

		for varname in self.globals:
			var = self.globals[varname]
			if var["type"] != None:
				self.newInstance(var["name"], var["type"], var["defined"])
			else:
				self.globals[varname]["state"] = State(self.defaultState)

	def newInstance(self, name, ictype, line):
		self.instances[name] = self.buildInstance(name, ictype, line)

	def buildInstance(self, name, ictype, line):
		instance = {
			"name": name,
			"type": ictype,
			"locals": {},
			"instances": {}
		}
		if ictype in self.ICs:
			for localkey in self.ICs[ictype]["locals"]:
				local = self.ICs[ictype]["locals"][localkey]
				if local["type"] == None:
					instance["locals"][local["name"]] = {"state": State(self.defaultState)}
				else:
					instance["instances"][local["name"]] = self.buildInstance(name, ictype)
		elif ictype in self.loadedICs:
			for localkey in self.loadedICs[ictype]["locals"]:
				local = self.ICs[ictype]["locals"][localkey]
				if local["type"] == None:
					instance["locals"][local["name"]] = {"state": State(self.defaultState)}
				else:
					instance["instances"][local["name"]] = self.buildInstance(name, ictype)
		else: 
			self.err(self.source_file, line, 3, f"DefinitionError: IC template'{ictype}' not defined or included")

		return instance

	def pulse(self):
		for expr in self.opl:
			if self.isIC(expr["dest"]["name"], expr["dest"]["parent"], expr["line"]): self.err(self.source_file, expr.line, 1, "AssignmentError: ICs cannot be the target of an assignment")
			self.resolveVar(expr["dest"]["name"], expr["dest"]["parent"], expr["line"])["state"].state = self.logicFunction(expr["op"], expr["arg"], expr["line"]).state
			if expr["dest"]["parent"] != None and expr["dest"]["parent"] != []:
				p = expr["dest"]["parent"].copy()
				first = p.pop(0)
				if not (first in self.instances): self.err(self.source_file, expr["line"], 3, f"DefinitionError: IC '{first}' isn't defined in the global scope")
				curInstance = self.instances[first]
				hier = [curInstance]
				for parent in p:
					try:
						curInstance = curInstance["instances"][parent]
						hier.append(curInstance)
					except KeyError:
							self.err(self.source_file, line, 3, f"DefinitionError: IC '{curInstance['name']}' has no child IC '{parent}'")

				for inst in hier:
					self.updateIC(inst)

	def updateIC(self, inst):
		pass

	def logicFunction(self, ftype, args, line):
		return self.logicFunctions[ftype](args, line)

	def resolveVar(self, name, parents, line):
		if parents == None or parents == []:
			try:
				return self.globals[name]
			except KeyError:
				self.err(self.source_file, line, 3, f"DefinitionError: Variable '{name}' isn't defined in the global scope")

		else:
			p = parents.copy()
			first = p.pop(0)
			if not (first in self.instances): self.err(self.source_file, line, 3, f"DefinitionError: IC '{first}' isn't defined in the global scope")
			curInstance = self.instances[first]
			for parent in p:
				try:
					curInstance = curInstance["instances"][parent]
				except KeyError:
						self.err(self.source_file, line, 3, f"DefinitionError: IC '{curInstance['name']}' has no child IC '{parent}'")

			try:
				return curInstance["locals"][name]
			except KeyError:
				self.err(self.source_file, line, 3, f"DefinitionError: IC '{curInstance['name']}' has no child '{name}'")

	def isIC(self, name, parents, line):
		if parents == None or parents == []:
			try:
				self.instances[name]
				return True
			except KeyError:
				try:
					self.globals[name]
					return False
				except KeyError:
					self.err(self.source_file, line, 3, f"DefinitionError: Variable '{name}' isn't defined in the global scope")

		else:
			p = parents.copy()
			first = p.pop(0)
			if not (first in self.instances): self.err(self.source_file, line, 3, f"DefinitionError: IC '{first}' isn't defined in the global scope")
			curInstance = self.instances[first]
			for parent in p:
				try:
					curInstance = curInstance["instances"][parent]
				except KeyError:
						self.err(self.source_file, line, 3, f"DefinitionError: IC '{curInstance['name']}' has no child IC '{parent}'")

			try:
				curInstance["instances"][name]
				return True
			except KeyError:
				try:
					curInstance["locals"][name]
					return False
				except KeyError:
					self.err(self.source_file, line, 3, f"DefinitionError: IC '{curInstance['name']}' has no child IC '{name}'")

	def loadICGroup(self, filepath):
		pass

	def err(self, file, line, code, msg):
		print(f"{file}:{line} - {msg}")
		exit(code)

def buildEnv(env_obj, source):
	return Env(env_obj, source)