import node
import edge
class Layer:
	def __init__(self, size):
		self.nodes = [node.Node() for _ in range(size)]
		self.edges = []

	def fully_connect(self, other_layer):
		for _ in range(len(self.nodes):
			for _ in range(other_layer.nodes)
				self.edges.append(edge.Edge())

layer = Layer(5)
for node in layer.nodes:
	print(node.value)