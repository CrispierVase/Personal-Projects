import random


class spot:
	def __init__(self, distance):
		self.distance = distance

neighbors = [spot(random.randint(0, 5)) for i in range(5, 0, -1)]
for neighbor in neighbors:
	print(neighbor.distance)
print('-')
def my_sort(neighbors):
	new = []
	done = False
	while not done:
		lowest = None
		for i in neighbors:
			if lowest == None:
				lowest = i
			elif i.distance < lowest.distance:
				lowest = i
		if lowest == None:
			done = True
		else:
			neighbors.remove(lowest)
			new.insert(0, lowest)
	return new[::-1]


neighbors = my_sort(neighbors)
for i in neighbors:
	print(i.distance)
