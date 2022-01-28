import numpy
import activation_functions
class Node:
	def __init__(self):
		self.value = 0
		self.inputs = []

	def activate(self):
		self.activated_inputs = []
		for val in self.inputs:
			self.activated_inputs.append(activation_functions.sigmoid(val))
		self.activated = 0
		for val in self.activated_inputs:
			self.activated += val
		# self.value = activation_functions.sigmoid(self.activated)
		self.value = self.activated


n1 = Node()
n1.inputs = [10]
print(n1.inputs)
n1.activate()
print(n1.value)



