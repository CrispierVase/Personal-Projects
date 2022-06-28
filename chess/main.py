#!/usr/bin/python3
import pyglet
import string 

from utils.load_config import load_config
from utils.mouse_square import mouse_square
from pieces import *
from cell import Cell
from utils.place import place
from utils.fen import fen

# loading details used for several classes
light_color, dark_color, win_size, cell_size = load_config()

# getting graphics set up
win = pyglet.window.Window(width=win_size[0], height=win_size[1], caption='Chess')
win.set_icon(pyglet.image.load('WPawn.png'))
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

# used in FEN strings and must be used for stalemates etc
half_move = 0
full_move = 1
turn = 0

# producing chess related items

# board = [[Cell(i, j) for i in range(8)] for j in range(8)]
board = fen('1n1qkbn1/3pp3/1p1P1pQ1/p7/8/2N2P1P/PPP2P2/2K1R2R b - - 0 20')

# this will be the list of pieces in the order [[White], [Black]]
pieces = [[], []]

target = None

@win.event
def on_mouse_press(x, y, button, modifiers, grid=board):
    global target
    global turn
    global half_move
    global full_move
    # if there is already a piece waiting to move
    if target:
        # this means a piece has already been picked and is allowed to go now
        if mouse_square(x, y) in target.find_options(grid):
            target.move(grid, mouse_square(x, y))
            if target.color == 1:
                full_move += 1
            half_move += 0.5
            turn += 1
            target = None
    # A new target needs to be assigned 
    elif mouse_square(x, y, grid).piece:
        if turn % 2 == mouse_square(x, y, grid).piece.color:
            target = mouse_square(x, y, grid).piece

@win.event
def on_draw():
    for col in board:
        for i in col:
            i.show()
    for col in board:
        for i in col:
            if i.piece:
                i.piece.show()

pyglet.app.run()