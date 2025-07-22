import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
from img import Img
from It1_interfaces.Board import Board
from It1_interfaces.PieceFactory import PieceFactory
# from Board import Board
import pathlib

def main():
    # Adjust these paths to any test pictures you have
    background = "./board.png"
   # logo = "../pieces/QW/states/jump/sprites/2.png"

    canvas = Img().read(background)  # original size
    # piece = Img().read(logo,
    #                    size=(100, 100),  # resize to 100×100
    #                    keep_aspect=True,  # keep aspect
    #                    interpolation=cv2.INTER_AREA)

    h, w = canvas.img.shape[:2]
    canvas.put_text("Demo", h // 2, w // 2, 3.0,
                    color=(255, 0, 0, 255), thickness=5)  # blue text

   # piece.draw_on(canvas, 50, 50)  # blend top‑left
    board = Board(
        cell_H_pix=100,
        cell_W_pix=100,
        W_cells=8,
        H_cells=8,
        img=canvas
    )
    pieces_root = pathlib.Path("../pieces")
    factory = PieceFactory(board, pieces_root)   
    piece = factory.create_piece("BB", (2, 5))
    piece.draw_on_board(board,0)  # blend top‑left
    canvas.show()
    
if __name__ == "__main__":
    main()
