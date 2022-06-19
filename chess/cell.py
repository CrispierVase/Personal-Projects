import pyglet
from utils.load_config import load_config
light_color, dark_color, win_size, cell_size, squares = load_config()
class Cell:
    def __init__(self, x, y, squares=squares):
        self.x = x
        self.y = y
        self.squares = squares
        self.piece = None
        if (x + y) % 2 != 0:
            self.color = light_color
        else:
            self.color = dark_color
        self.make_shape()

    def make_shape(self):
        self.shape = pyglet.shapes.Rectangle(self.x * cell_size, self.y * cell_size, cell_size, cell_size, color=self.color, batch=self.squares)