import pygame
import random
import time 
import sys

args = sys.argv[1:]

start = time.perf_counter()

# this needs to be double the real width for adding the walls It also should be an odd number. That makes the maze look better. 
if args:
	maze_width = int(args[0])
	maze_height = int(args[1])
	width = int(args[2])
	height = int(args[3])
	if args[4] != 'True':
		visited_color = (int(args[4]), int(args[4]), int(args[4]))
		wall_color = (int(args[5]), int(args[5]), int(args[5]))
	else:
		visited_color = (164,147,147)
		wall_color = (103,89,94)
else:
	maze_width, maze_height = 101, 101
	width, height = 602, 602
	visited_color = (255, 255, 255)
	wall_color = (0, 0, 0)

cell_width, cell_height = round(width / maze_width), round(height / maze_height)


class Wall:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		if self.x % 2 == 1 and self.y % 2 == 1:
			self.permanent = True
		else:
			self.permanent = False
		self.color = wall_color

	def show(self, win):
		pygame.draw.rect(win, self.color, pygame.Rect((self.x * cell_width) + cell_width, (self.y * cell_height) + cell_height, cell_width, cell_height))


class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = (255, 255, 255)
		self.walls = []
		self.visited = False
		self.parent = None

	def show(self, win):
		pygame.draw.rect(win, self.color, pygame.Rect((self.x * cell_width) + cell_width, (self.y * cell_height) + cell_height, cell_width, cell_height))

	def check_neighbors(self, grid, distance=2):
		self.index = grid.index(self)
		self.neighbors = []

		# up
		if self.index > maze_width and self.index - (distance * maze_width) > 0:
			if type(grid[self.index - (distance * maze_width)]) == Cell and not grid[self.index - (distance * maze_width)].visited:
				self.neighbors.append(grid[self.index - (distance * maze_width)])

		# down
		if self.index < len(grid) - distance * maze_width:
			if type(grid[self.index + (distance * maze_width)]) == Cell and not grid[self.index + (distance * maze_width)].visited:
				self.neighbors.append(grid[self.index + (distance * maze_width)])

		# left
		if (self.index % maze_width) - distance >= 0:
			if type(grid[self.index - distance]) == Cell and not grid[self.index - distance].visited:
				self.neighbors.append(grid[self.index - distance])
		# right
		if (self.index % maze_width) + distance < maze_width:
			if type(grid[self.index + distance]) == Cell and not grid[self.index + distance].visited:
				self.neighbors.append(grid[self.index + distance])

		if len(self.neighbors) > 0:
			return self.neighbors
		return False


def backtrack(stack, current):
	while current.check_neighbors(grid) == False:
		stack[-1].color = visited_color
		stack.pop()
		current = stack[-1]
	return current, stack

def fake_walls():
	global fake_end_neighbor
	pygame.draw.rect(win, wall_color, pygame.Rect(0, 0, cell_width, win.get_height()))
	pygame.draw.rect(win, wall_color, pygame.Rect(0, 0, win.get_width(), cell_height))
	pygame.draw.rect(win, wall_color, pygame.Rect(0, win.get_height() - cell_height, win.get_width(), cell_height))
	pygame.draw.rect(win, wall_color, pygame.Rect(win.get_width() - cell_width, cell_height, cell_width, win.get_height() - cell_height))
	fake = Cell(0, -1)
	fake.color = visited_color
	fake.show(win)
	for bottom_cell in grid[-maze_width:][::-1]:
		if type(bottom_cell) == Cell:
			fake_end = Cell(bottom_cell.x, bottom_cell.y + 1)
			fake_end.color = visited_color
			fake_end.show(win)
			fake_end_neighbor = bottom_cell
			break
	return fake_end


run = True
grid = [Wall(j, i) if (i % 2 == 1 or j % 2 == 1) else Cell(j, i) for i in range(maze_width) for j in range(maze_height)]
clock = pygame.time.Clock()
idx = 0
current = grid[0]
stack = []
done = False
saved = False
updated = False
saved = False
solved = False
while run:
	while not done:
		# modify current cell to value of visited cell
		current.color = visited_color
		current.visited = True
		# make a copy of current cell positions for finding of direction ater
		old_pos = [current.x, current.y]
		# get new cell
		neighbors = current.check_neighbors(grid)
		if neighbors:
			current = random.choice(neighbors)
			stack.append(current)
		current.color = (255, 0, 0)
		grid_copy = grid.copy()
		if neighbors:
			x_change = current.x - old_pos[0]
			y_change = current.y - old_pos[1]
			
			# horizontal
			if x_change != 0:
				grid_copy[int(grid.index(current) - x_change / 2)] = Cell(int(current.x - x_change / 2), int(current.y))
				grid_copy[int(grid.index(current) - x_change / 2)].color = visited_color
			# vertical
			elif y_change != 0:
				grid_copy[int(grid.index(current) - maze_width * (y_change / 2))] = Cell(current.x, current.y - y_change / 2)
				grid_copy[int(grid.index(current) - maze_width * (y_change / 2))].color = visited_color
		else:
			if len(stack) > 2:
				try:
					current, stack = backtrack(stack, current)
				except IndexError:
					finish = time.perf_counter()
					print(f'Maze Generation took {finish - start}')
					done = True
			else:
				done = True
		grid = grid_copy.copy()
		all_visited = True
		for space in grid:
			if type(space) == Cell:
				if space.visited == False:
					all_visited = False
					break
		if all_visited:
			finish = time.perf_counter()
			done = True
	# show walls and cells in the maze
	win = pygame.display.set_mode(((maze_width * cell_width) + 2 * cell_width, (maze_height * cell_height) + 2 * cell_height))
	
	if not updated:
		for space in grid:
			space.show(win)
		fake_walls()
		updated = True
		pygame.display.update()

	if not saved:
		saved = True
		if len(args) >= 6:
			filename = args[6]
		else:
			filename = f'maze {maze_width}x{maze_height}.txt'
		with open(filename, 'w') as save_file:
			save_file.write(str(grid))
		pygame.image.save(win, f'{filename}.png')

	if not solved:
		solve_start = time.perf_counter()
		for spot in grid:
			spot.visited = False
		current = grid[0]
		all_neigbors = [current]
		current.visited = True
		stop = False
		while not stop:
			new_stuff = all_neigbors.copy()
			for spot in all_neigbors:
				new = spot.check_neighbors(grid, 1)
				if new:
					for place in new:
						if abs(place.x - spot.x) + abs(place.y - spot.y) > 1:
							new.remove(place)
						else:
							place.visited = True
							place.parent = spot
							place.show(win)
					new_stuff.extend(new)
				else:
					new_stuff.remove(spot)
			all_neigbors = new_stuff.copy()
			if len(all_neigbors) == 0:
				stop = True

		path = []
		current = fake_end_neighbor
		if len(args) > 7:
			path_color = (232,180,184)
		else:
			path_color = (255, 0, 0)
		while current != grid[0]:
			path.insert(0, current)
			current.color = path_color
			current.show(win)
			current = current.parent
		current.color = path_color
		current.show(win)
		fake_end = fake_walls()
		fake_end.color = path_color
		fake_end.show(win)
		pygame.draw.rect(win, path_color, pygame.Rect(cell_width, 0, cell_width, cell_height))
		pygame.display.update()

		solved = True
		solve_finish = time.perf_counter()
		print(f'Solving took {solve_finish - solve_start}')
		pygame.image.save(win, f'{filename}-SOLVED.png')

	# get pygame events for quitting 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	clock.tick(1)