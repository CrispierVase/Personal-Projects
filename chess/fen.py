from cell import Cell
def fen(fen_string):
    board = [[Cell(i, j) for i in range(8)] for j in range(8)]
    
