import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
from It1_interfaces.img import Img
from It1_interfaces.Board import Board
from It1_interfaces.PieceFactory import PieceFactory
from It1_interfaces.Game import Game
from It1_interfaces.InputHandler import InputHandler
import pathlib

def main():
    background = "../board.png"
    canvas = Img().read(background)
    h, w = canvas.img.shape[:2]

    board = Board(
        cell_H_pix=100,
        cell_W_pix=100,
        W_cells=8,
        H_cells=8,
        img=canvas
    )
    pieces_root = pathlib.Path("../pieces")
    factory = PieceFactory(board, pieces_root)

    #print("Trying to open:", r'c:\Users\1\Documents\bootkamp\CTD25\pieces\board.csv')
    initial_pieces = board.read_board_csv(r'c:\Users\1\Documents\bootkamp\CTD25\pieces\board.csv')
    #print("initial",initial_pieces)
    pieces = []
    pieces_dict = {}  # Add this line
    for p_type, cell in initial_pieces:
        piece = factory.create_piece(p_type, cell)
        #print(piece.piece_id, cell)  # ← בדוק שכל חייל נוצר
        pieces.append(piece)
        pieces_dict[piece.piece_id] = piece  # Add this line
    #print("Total pieces:", len(pieces))  # ← צריך להיות 32
    game = Game(pieces, board)
    input_handler = InputHandler(board, pieces_dict)  # pieces_dict = {piece_id: piece, ...}
    game.run()

if __name__ == "__main__":
    main()
