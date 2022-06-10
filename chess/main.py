#!/usr/bin/python3
import pyglet
from utils.load_config import load_config
from utils.mouse_square import mouse_square
from pieces import *


light_color, dark_color, win_size, cell_size = load_config()
win = pyglet.window.Window(width=win_size[0], height=win_size[1], caption='Chess')
win.set_icon(pyglet.image.load('WPawn.png'))
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
squares = pyglet.graphics.Batch()


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = None
        if (x + y) % 2 != 0:
            self.color = light_color
        else:
            self.color = dark_color
        self.shape = pyglet.shapes.Rectangle(self.x * cell_size, self.y * cell_size, cell_size, cell_size, color=self.color, batch=squares)

    def make_shape(self):
        self.shape = pyglet.shapes.Rectangle(self.x * cell_size, self.y * cell_size, cell_size, cell_size, color=self.color, batch=squares)


board = [[Cell(i, j) for i in range(8)] for j in range(8)]

board[4][4].piece = King(4, 4, 0)
tmp = board[4][4].piece

@win.event
def on_mouse_press(x, y, button, modifiers):
    goal = mouse_square(x, y)
    options = tmp.find_options(board)
    print(goal, options)
    if goal in options:
        tmp.move([x, y])


@win.event
def on_draw():
    squares.draw()
    for col in board:
        for i in col:
            if i.piece:
                i.piece.show()

pyglet.app.run()