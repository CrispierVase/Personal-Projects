import pyglet
from utils.load_config import load_config
from utils.grid_index import grid_index
from pieces import *

light_color, dark_color, win_size, cell_size = load_config()
win = pyglet.window.Window(width=win_size[0], height=win_size[1], caption='Chess')
win.set_icon(pyglet.image.load('WPawn.png'))
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


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
        pyglet.shapes.Rectangle(self.x * cell_size, self.y * cell_size, cell_size, cell_size, self.color).draw()


grid = [[Cell(i, j) for i in range(8)] for j in range(8)]
run = True


@win.event
def on_draw():
    win.clear()
    for col in grid:
        for spot in col:
            spot.show()
            if spot.piece:
                spot.piece.show()


pyglet.app.run()
