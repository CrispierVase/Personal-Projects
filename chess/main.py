import pygame
from utils.load_config import load_config
from utils.grid_index import grid_index
from pieces import *


light_color, dark_color, win_size, cell_size = load_config()
win = pygame.display.set_mode(win_size)
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load('WPawn.png'))


class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.piece = None
		if (self.x + self.y) % 2 == 0:
			self.color = light_color
		else:
			self.color = dark_color
	def show(self):
		pygame.draw.rect(win, self.color, pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size))


grid = [[Cell(i, j) for i in range(8)] for j in range(8)]
run = True
for col in grid:
	for spot in col:
		spot.show()
		if spot.piece:
			spot.piece.show(win)
pygame.display.update()
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
