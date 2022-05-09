#!/usr/bin/python3
import pyglet
from utils.load_config import load_config
from utils.in_range import in_range

light_color, dark_color, win_size, cell_size = load_config()



class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.moves = 0
        # self.directions is [[x change, y change, max distance]]
        if not self.directions:
            self.directions = []
        # colors are 1=white,0=black this makes it easier to get pictures
        self.color = color
        self.name = type(self).__name__
        if self.color == 0:
            filename = f'W{self.name}.png'
        else:
            filename = f'B{self.name}.png'
        self.image = pyglet.image.load(filename)

    def find_options(self, grid):
        # This function will only be used for sliding pieces and Kings
        options = []
        if not self.directions:
            print('bad piece, no directions')
            return []
        distance = self.directions[0][2]
        for direction in self.directions:
            dist = 1
            while dist <= distance:
                check_x = self.x + (dist * direction[0])
                check_y = self.y + (dist * direction[1])
                if in_range(0, check_x, 7) and in_range(0, check_y, 7):
                    if not grid[check_x][check_y].piece:
                        options.append([check_x, check_y])
                        dist += 1
                    else:
                        dist = 10
                else:
                    dist = 10
        return options

    def show(self):
        self.image.blit(self.x * cell_size + 13, self.y * cell_size + 10)


class Rook(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-1, 0, 8], [1, 0, 8], [0, -1, 8], [0, 1, 8]]
        super().__init__(x, y, color)


class Bishop(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-1, -1, 8], [1, -1, 8], [-1, 1, 8], [1, 1, 8]]
        super().__init__(x, y, color)