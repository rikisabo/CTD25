# main.py
# -------
import sys, os, pathlib
# לאפשר import של It1_interfaces גם אם מריצים מתיקייה אחרת
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
from It1_interfaces.img           import Img
from It1_interfaces.Board         import Board
from It1_interfaces.PieceFactory  import PieceFactory
from It1_interfaces.Game          import Game
# תוספות Pub/Sub
from scoreboard import ScoreBoard
from It1_interfaces.MoveLog      import MoveLog      # ←
from voice      import VoiceSFX
# ────────────────────────────────────────────────────────────────────
def main():
    # --- רקע ולוח ----------------------------------------------------
    background = "../board.png"               # קובץ תמונת הלוח
    canvas     = Img().read(background)
    h, w       = canvas.img.shape[:2]
    board = Board(
        cell_H_pix = 100,
        cell_W_pix = 100,
        W_cells    = 8,
        H_cells    = 8,
        img        = canvas
    )
    # --- יצירת כלים --------------------------------------------------
    pieces_root = pathlib.Path("../pieces")
    factory     = PieceFactory(board, pieces_root)
    csv_path = r'c:\Users\1\Documents\bootkamp\CTD25\pieces\board.csv'
    initial_pieces = board.read_board_csv(csv_path)
    pieces = [factory.create_piece(ptype, cell) for ptype, cell in initial_pieces]
    # --- מודולי Pub/Sub ---------------------------------------------
    scoreboard = ScoreBoard()    # מאזין ל‑piece_captured ומציג ניקוד
    movelog    = MoveLog()       # מאזין ל‑piece_moved ומציג טבלה
    VoiceSFX()                   # מאזין ומשמיע צלילים (אין צורך לשמור משתנה)
    # --- הפעלת המשחק -------------------------------------------------
    game = Game(pieces, board,
                scoreboard=scoreboard,
                movelog=movelog)
    game.run()
# ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()