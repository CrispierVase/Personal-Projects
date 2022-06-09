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

    def find_options(self, grid, get_check=False):
        # This function works for all pieces except for pawns. 
        options = []
        distance = self.directions[0][2]
        for direction in self.directions:
            dist = 1
            while dist <= distance:
                check_x = self.x + (dist * direction[0])
                check_y = self.y + (dist * direction[1])
                if in_range(0, check_x, 7) and in_range(0, check_y, 7):
                    if not grid[check_x][check_y].piece:
                        if not get_check:
                            options.append([check_y, check_x])
                        dist += 1
                    else:
                        if grid[check_x][check_y].piece.color != self.color:
                            options.append([check_y, check_x])
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

class Queen(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-1, 0, 8], [1, 0, 8], [0, -1, 8], [0, 1, 8], [-1, -1, 8], [1, -1, 8], [-1, 1, 8], [1, 1, 8]]
        super().__init__(x, y, color)

class Knight(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-2, -1, 1], [-2, 1, 1], [-1, 2, 1], [1, 2, 1], [2, -1, 1], [2, 1, 1], [-1, -2, 1], [1, -2]]
        super().__init__(x, y, color)

class Pawn(Piece):
    def __init__(self, x, y, color):
        self.directions = [[0, 1, 1]]
        super().__init__(x, y, color)

    def find_options(self, grid):
        # This function will not be here for a while. Pawns are bad lol
        return 


class King(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1], [-1, 0, 1], [1, 0, 1], [0, -1, 1], [0, 1, 1]]
        super().__init__(x, y, color)
        self.fakes = []

    def update_fakes(self):
        self.fakes = [Queen(self.x, self.y, self.color), Knight(self.x, self.y, self.color)]

    def find_check(self, grid):
        options = []
        self.update_fakes()
        for fake in self.fakes:
            options.extend(fake.find_options(grid))
        return options
