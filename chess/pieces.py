import pyglet
from utils.load_config import load_config

light_color, dark_color, win_size, cell_size = load_config()


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.directions = []
        self.moved = False
        if self.color == 1:
            self.image = f'W{type(self).__name__}.png'
        else:
            self.image = f'B{type(self).__name__}.png'
        self.image = pyglet.image.load(self.image)
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

    def find_options(self, grid):
        options = []
        for direction in self.directions:
            check_x = self.x
            check_y = self.y
            num = 0
            while 0 <= check_x + direction[1] < 8 and 0 <= check_y + direction[0] < 8:
                if grid[check_x + direction[1]][check_y + direction[0]].piece is None:
                    check_x += direction[1]
                    check_y += direction[0]
                    options.append([check_x, check_y])
                    num += 1
                if num >= direction[2]:
                    break

        return options

    def show(self):
        self.image.blit(self.x * cell_size + (cell_size // 2), self.y * cell_size + (cell_size // 2))


class King(Piece):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y, color)
        self.distance = 1
        self.directions = [[-1, -1, self.distance], [0, -1, self.distance], [1, -1, self.distance],
                           [-1, 0, self.distance], [1, 0, self.distance], [-1, 1, self.distance],
                           [0, 1, self.distance], [1, 1, self.distance]]


class Queen(Piece):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y, color)
        self.distance = 99
        self.directions = [[-1, -1, self.distance], [0, -1, self.distance], [1, -1, self.distance],
                           [-1, 0, self.distance], [1, 0, self.distance], [-1, 1, self.distance],
                           [0, 1, self.distance], [1, 1, self.distance]]


class Bishop(Piece):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y, color)
        self.distance = 99
        self.directions = [[-1, -1, self.distance], [1, -1, self.distance], [-1, 1, self.distance],
                           [1, 1, self.distance]]


class Rook(Piece):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y, color)
        self.distance = 99
        self.directions = [[0, -1, self.distance], [-1, 0, self.distance], [1, 0, self.distance], [0, 1, self.distance]]


class Knight(Piece):
    def __init__(self, x, y, color):
        self.color = color
        super().__init__(x, y, color)
        self.distance = 1
        self.directions = [[-1, -2, self.distance], [1, -2, self.distance], [2, -1, self.distance],
                           [-2, -1, self.distance], [-2, 1, self.distance], [2, 1, self.distance],
                           [1, 2, self.distance], [-1, 2, self.distance]]


class Pawn(Piece):
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y
        super().__init__(x, y, color)
        self.distance = 1
        self.directions = [[0, 1, self.distance]]

    def find_options(self, grid):
        options = []
        for direction in self.directions:
            check_x = self.x
            check_y = self.y
            num = 0
            while 0 <= check_x + direction[1] < 8 and 0 <= check_y + direction[0] < 8:
                if grid[check_x + direction[1]][check_y + direction[0]].piece is None:
                    check_x += direction[1]
                    check_y += direction[0]
                    options.append([check_x, check_y])
                    num += 1
                if num >= direction[2]:
                    break

        return options
