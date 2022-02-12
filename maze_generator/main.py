import pygame
import random

width, height = 400, 400
gap = 10
maze_width = 5
maze_height = 5
x_scale = width // maze_width
y_scale = height // maze_height
win = pygame.display.set_mode((width - gap, height - gap))
stack = []



class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.wall = False
		self.color = (255, 255, 255)
		self.visited = False

	def show(self):
		pygame.draw.rect(win, self.color, pygame.Rect(self.x * x_scale, self.y * y_scale, x_scale - gap, y_scale - gap))

	def set_wall(self):
		self.color = (0, 0, 0)
		self.wall = True

	def un_wall(self):
		self.color = (255, 255, 255)
		self.wall = False
		self.visited = True

	def check_neighbors(self, grid):
		self.neighbors = []
		if self.y > 0:
			if not grid[self.x][self.y - 1].visited and grid[self.x][self.y - 1].wall:
				self.neighbors.append(grid[self.x][self.y - 1])
		if self.y < maze_height - 1:
			if not grid[self.x][self.y + 1].visited and grid[self.x][self.y + 1].wall:
				self.neighbors.append(grid[self.x][self.y + 1])
		if self.x > 0:
			if not grid[self.x - 1][self.y].visited and grid[self.x - 1][self.y].wall:
				self.neighbors.append(grid[self.x - 1][self.y])
		if self.x < maze_width - 1:
			if not grid[self.x + 1][self.y].visited and grid[self.x + 1][self.y].wall:
				self.neighbors.append(grid[self.x + 1][self.y])
		if len(self.neighbors) > 0:
			return self.neighbors
		else:
			print('stuck')
			return [self]


grid = [[Cell(i, j) for j in range(maze_width)] for i in range(maze_width)]
clock = pygame.time.Clock()
current = grid[0][0]
walls = []
for row in grid:
	for cell in row:
		cell.set_wall()
current.un_wall()

run = True
while run:
	win.fill((0, 0, 0))
	current.color = (255, 255, 255)
	tmp = current
	current = random.choice(current.check_neighbors(grid))
	x_dir = current.x - tmp.x
	y_dir = current.y - tmp.y

	current.un_wall()
	stack.append(current)
	for row in grid:
		for cell in row:
			cell.show()
	for wall in walls:
		wall.show()

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	clock.tick(5)