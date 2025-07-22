import pytest
from It1_interfaces.Piece import Piece
import numpy as np

class DummyState:
    def __init__(self):
        self._physics = type("P", (), {"cell": (0, 0)})()
    def get_img(self):
        class DummyImg:
            def __init__(self):
                self.img = np.ones((10, 10, 3), dtype=np.uint8) * 255
        return DummyImg()

def test_draw_on_board():
    from It1_interfaces.img import Img
    arr = np.zeros((100, 100, 3), dtype=np.uint8)
    board = type("Board", (), {
        "cell_H_pix": 10,
        "cell_W_pix": 10,
        "img": type("ImgWrap", (), {"img": arr.copy()})()
    })()
    piece = Piece("test", DummyState())
    piece.draw_on_board(board, now_ms=0)
    assert board.img.img.sum() > 0