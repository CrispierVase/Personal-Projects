#!/usr/bin/python3
import pyglet
from utils.load_config import load_config
from utils.in_range import in_range

light_color, dark_color, win_size, cell_size = load_config()



class Piece:
    def __init__(self, x, y, color, moves=0):
        self.x = x
        self.y = y
        # this is only an option so pawns can promote
        self.moves = moves
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
                            options.append([check_x, check_y])
                        dist += 1
                    else:
                        if grid[check_x][check_y].piece.color != self.color:
                            if not get_check:
                                options.append([check_x, check_y])
                            elif type(grid[check_x][check_y].piece) == type(self):
                                options.append([check_x, check_y])

                        dist = 10
                else:
                    dist = 10

        return options

    def show(self):
        self.image.blit(self.x * cell_size + 13, self.y * cell_size + 10)

    def move(self, grid, new_location):
        # pass good moves into this function. It will let you move the piece literally anywhere if you don't
        grid[self.x][self.y].piece = None
        self.x = new_location[0]
        self.y = new_location[1]
        grid[self.x][self.y].piece = self
        self.moves += 1
        self.show()
        return


class Rook(Piece):
    def __init__(self, x, y, color, moves=0):
        self.directions = [[-1, 0, 8], [1, 0, 8], [0, -1, 8], [0, 1, 8]]
        super().__init__(x, y, color)


class Bishop(Piece):
    def __init__(self, x, y, color, moves=0):
        self.directions = [[-1, -1, 8], [1, -1, 8], [-1, 1, 8], [1, 1, 8]]
        super().__init__(x, y, color)

class Queen(Piece):
    def __init__(self, x, y, color, moves=0):
        self.directions = [[-1, 0, 8], [1, 0, 8], [0, -1, 8], [0, 1, 8], [-1, -1, 8], [1, -1, 8], [-1, 1, 8], [1, 1, 8]]
        super().__init__(x, y, color)

class Knight(Piece):
    def __init__(self, x, y, color, moves=0):
        self.directions = [[-2, -1, 1], [-2, 1, 1], [-1, 2, 1], [1, 2, 1], [2, -1, 1], [2, 1, 1], [-1, -2, 1], [1, -2]]
        super().__init__(x, y, color)

class Pawn(Piece):
    def __init__(self, x, y, color):
        self.directions = [[0, 1, 1]]
        super().__init__(x, y, color)
        self.attacks = [[-1, 1], [1, 1]]
        if self.color == 1:
            self.directions = [[0, -1, 1]]
            self.attacks[0][1] = -1
            self.attacks[1][1] = -1

    def find_options(self, grid):
        options = []
        # checking if the piece can move forward
        if in_range(0, self.y, 7):
            options.append([self.x, self.y + self.directions[0][1]])
        # looking at attacks
        # this means that the pawn can attack to the left from the perspective of white
        if 1 <= self.x and  in_range(1, self.y + self.attacks[0][1], 7):
            if grid[self.x - 1][self.y + self.attacks[0][1]].piece:
                if grid[self.x - 1][self.y + self.attacks[0][1]].piece.color != self.color:
                    options.append([self.x - 1, self.y + self.attacks[0][1]])
        # this means that the pawn can attack to the left from the perspective of white
        if self.x <= 6 and  in_range(1, self.y + self.attacks[1][1], 7):
            if grid[self.x + 1][self.y + self.attacks[1][1]].piece:
                if grid[self.x + 1][self.y + self.attacks[1][1]].piece.color != self.color:
                    options.append([self.x + 1, self.y + self.attacks[1][1]])
        # check if a double move is possible
        if self.moves:
            pass

        return options


class King(Piece):
    def __init__(self, x, y, color):
        self.directions = [[-1, -1, 1], [1, -1, 1], [-1, 1, 1], [1, 1, 1], [-1, 0, 1], [1, 0, 1], [0, -1, 1], [0, 1, 1]]
        super().__init__(x, y, color)
        self.fakes = []

    def update_fakes(self):
        for piece in self.fakes:
            del piece
        self.fakes = [Queen(self.x, self.y, self.color), Knight(self.x, self.y, self.color), Pawn(self.x, self.y, self.color)]

    def find_check(self, grid):
        options = []
        self.update_fakes()
        for fake in self.fakes:
            options.extend(fake.find_options(grid, get_check=True))
        return len(options) >= 1

class Passent:
    def __init__(self, x, y, color, placed_on, parent):
        self.x = x
        self.y = y 
        self.color = color
        self.placed_on = placed_on
        self.parent = parent

    def update(self, turn):
        if turn != self.placed_on:
            del self