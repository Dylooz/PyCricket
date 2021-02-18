class State:
	def __init__(self, state):
		self.state = state # "l": LOW, "h": HIGH, "z": IMPEDANCE

	def __repr__(self):
		return f"State({self.state})"

	def pullUp(self):
		newState = self.state
		if newState == "z": newState = "h"
		return State(newState)

	def pullDown(self):
		newState = self.state
		if newState == "z": newState = "l"
		return State(newState)