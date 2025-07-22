from It1_interfaces.Board import Board
from It1_interfaces.img import Img

def test_get_cell_pos():
    board = Board(10, 20, 8, 8, Img())
    x, y = board.get_cell_pos((2, 3))
    assert x == 3 * 20 + 10
    assert y == 2 * 10 + 5