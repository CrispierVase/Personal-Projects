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
	visited_color = (int(args[4]), int(args[4]), int(args[4]))
	wall_color = (int(args[5]), int(args[5]), int(args[5]))
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
		pygame.draw.rect(win, self.color, pygame.Rect(self.x * cell_width, self.y * cell_height, cell_width, cell_height))



class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.color = (255, 255, 255)
		self.walls = []
		self.visited = False

	def show(self, win):
		pygame.draw.rect(win, self.color, pygame.Rect(self.x * cell_width, self.y * cell_height, cell_width, cell_height))

	def check_neighbors(self, grid):
		self.index = grid.index(self)
		self.neighbors = []

		# up
		if self.index > maze_width:
			if type(grid[self.index - (2 * maze_width)]) == Cell and grid[self.index - (2 * maze_width)].visited == False:
				self.neighbors.append(grid[self.index - (2 * maze_width)])

		# down
		if self.index < len(grid) - maze_width:
			if type(grid[self.index + (2 * maze_width)]) == Cell and grid[self.index + (2 * maze_width)].visited == False:
				self.neighbors.append(grid[self.index + (2 * maze_width)])

		# left
		if (self.index % maze_width) - 2 < maze_width:
			if type(grid[self.index - 2]) == Cell and not grid[self.index - 2].visited:
				self.neighbors.append(grid[self.index - 2])
		# right
		if (self.index % maze_width) + 2 < maze_width:
			if type(grid[self.index + 2]) == Cell and not grid[self.index + 2].visited:
				self.neighbors.append(grid[self.index + 2])

		if len(self.neighbors) > 0:
			return self.neighbors
		else:
			return False


def backtrack(stack, current):
	while current.check_neighbors(grid) == False:
		stack[-1].color = visited_color
		stack.pop()
		current = stack[-1]
		current.color = (255, 0, 0)

	return current, stack


run = True
grid = [Wall(j, i) if (i % 2 == 1 or j % 2 == 1) else Cell(j, i) for i in range(maze_width) for j in range(maze_height)]
clock = pygame.time.Clock()
idx = 0
current = grid[0]
current.color = (255, 0, 0)
stack = []
done = False
saved = False
updated = False
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
				grid_copy[int(grid.index(current) - maze_width * (y_change /2))] = Cell(current.x, current.y - y_change / 2)
				grid_copy[int(grid.index(current) - maze_width * (y_change /2))].color = visited_color
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
	win = pygame.display.set_mode((maze_width * cell_width, maze_height * cell_height))
	
	if not updated:
		for space in grid:
			space.show(win)
		pygame.display.update()
		updated = True

	keys = pygame.key.get_pressed()
	if not saved:
		if keys[pygame.K_TAB]:
			saved = True
			if len(args) >= 6:
				filename = args[6]
			else:
				filename = f'maze {maze_width}x{maze_height}.txt'
			with open(filename, 'w') as save_file:
				save_file.write(str(grid))


	# get pygame events for quitting 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	clock.tick(1)