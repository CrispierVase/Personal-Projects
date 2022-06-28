import pyglet
from utils.load_config import load_config
from utils.limit import limit

def mouse_square(mouse_x, mouse_y, grid=False):
    _, _, win_size, cell_size = load_config()
    if not grid:
        return [limit(0, mouse_x // cell_size, 7), limit(0, mouse_y // cell_size, 7)]
    return grid[limit(0, mouse_x // cell_size, 7)][limit(0, mouse_y // cell_size, 7)]