import node
import edge
class Layer:
	def __init__(self, size):
		self.nodes = [node.Node() for _ in range(size)]
		self.edges = []

	def fully_connect(self, other_layer):
		self.idx = 0
		for _ in range(len(self.nodes)):
			for _ in range(other_layer.nodes):
				self.edges.append(edge.Edge())
		for 


layer = Layer(5)
layer2 = Layer(5)
layer.fully_connect(layer2)
print(layer.edges)
for node in layer.nodes:
	print(node.value)
