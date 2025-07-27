import cv2
import inspect
import pathlib
import queue
import threading
import time
import math
import os
import numpy as np
from typing import List, Dict, Tuple, Optional
from Board import Board
from Command import Command
from Piece import Piece
from It1_interfaces.img import Img
from It1_interfaces.InputHandler import InputHandler
from Moves import Moves
from bus import publish

# Exception for invalid board state
# class InvalidBoard(Exception):
#     ...

# ────────────────────────────────────────────────────────────────────
class Game:
    def __init__(self, pieces: List[Piece], board: Board,scoreboard=None, movelog=None):
        """Initialize the game with pieces, board, and optional event bus."""
        self.pieces = {p.piece_id: p for p in pieces}
        self.board = board
        self.input_handler = InputHandler(board, self.pieces)
        self.focus_a = [0, 0]  # Initial position for player A
        self.focus_b = [7, 7]  # Initial position for player B
        self.select_stage_a = 0  # 0=select piece, 1=select target
        self.select_stage_b = 0
        self.user_input_queue = queue.Queue()
        self.scoreboard = scoreboard if scoreboard else None  # Optional scoreboard
        self.movelog    = movelog

        # Load background image once
        self.background_img = cv2.imread("../background.png")
        if self.background_img is None:
            print("Warning: background image not found, using white background")
            self.background_img = 255 * np.ones((1080, 1920, 3), dtype=np.uint8)
        else:
            self.background_img = cv2.resize(self.background_img, (1920, 1080))

    # ─── helpers ─────────────────────────────────────────────────────────────
    def game_time_ms(self) -> int:
        """Return the current game time in milliseconds."""
        return int(time.time() * 1000)

    def clone_board(self) -> Board:
        """
        Return a brand-new Board wrapping a copy of the background pixels
        so we can paint sprites without touching the pristine board.
        """
        # Implement if needed
        pass

    def start_user_input_thread(self):
        """Start the user input thread for mouse handling (not implemented)."""
        pass

    # ─── main public entrypoint ──────────────────────────────────────────────
    def run(self):
        """Main game loop."""
        self.start_user_input_thread()
        start_ms = self.game_time_ms()

        # Reset all pieces to their initial state
        for p in self.pieces.values():
            p.reset(start_ms)

        # Main loop: draw, handle input, process commands
        while True:
            self._draw()  # Display the window
            key = cv2.waitKey(200)  # Handle keyboard input
            cmd = self.input_handler.handle_keyboard(key)
            if cmd:
                self._process_input(cmd)
            if key == 27 or not self._show():
                break

        cv2.destroyAllWindows()

    # ─── drawing helpers ────────────────────────────────────────────────────
    def _draw(self):
        background = self.background_img.copy()

        img = self.board.img.img.copy()
        img = cv2.copyMakeBorder(img,
                                 top=0, bottom=0, left=0, right=220,
                                 borderType=cv2.BORDER_CONSTANT,
                                 value=(40, 40, 40))
        for p in self.pieces.values():
            p.draw_on_board_to_img(img, self.board, now_ms=0)
        self.input_handler.draw_focus(img)

        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        h, w = img.shape[:2]
        H, W = background.shape[:2]

        # הרבה שמאלה (x קטן), ולמעלה (y קטן)
        x = 40    # אפשר גם 0 או ערך שלילי אם צריך עוד יותר שמאלה
        y = 30    # קרוב לחלק העליון

        background[y:y+h, x:x+w] = img

        if self.scoreboard:
            self.scoreboard.draw(background, origin=(x + w + 10, y + 30))
        if self.movelog:
            self.movelog.draw(background, origin=(x + w + 10, y + 90))

        cv2.imshow("Game", background)

    # ─── input processing ───────────────────────────────────────────────────
    def _process_input(self, cmd: Command):
        """Process a command: enqueue, handle selection and movement."""
        self._enqueue_command(cmd)
        if cmd.type == "Select":
            self._handle_select(cmd)
        elif cmd.type == "Move":
            self._handle_move(cmd)

    def _enqueue_command(self, cmd: Command):
        """Add the command to the queue (for move order logic)."""
        self.user_input_queue.put(cmd)

    def _handle_select(self, cmd: Command):
        """Update focus and selected piece only if there's a piece at the focus."""
        if cmd.player == "A":
            self.input_handler.focus_a = list(cmd.params[0])
            piece = self._get_piece_at(cmd.params[0], "A")
            if piece is not None:
                self.input_handler.selected_a = piece
                print(f"Selected piece: {piece}")
            else:
                print(f"No piece found at {cmd.params[0]} for player A")
        elif cmd.player == "B":
            self.input_handler.focus_b = list(cmd.params[0])
            piece = self._get_piece_at(cmd.params[0], "B")
            if piece is not None:
                self.input_handler.selected_b = piece
                print(f"Selected piece: {piece}")
            else:
                print(f"No piece found at {cmd.params[0]} for player B")

    def _handle_move(self, cmd: Command):
        """Check move validity and move the piece."""
        piece = None
        if cmd.player == "A":
            piece = self.input_handler.selected_a
        elif cmd.player == "B":
            piece = self.input_handler.selected_b

        if not piece:
            print("No piece selected for move.")
            return

        if not self._can_move(piece, cmd.params[0]):
            print(f"Move not allowed for {piece.piece_id} to {cmd.params[0]}")
            return

        self._try_move(piece, cmd.params[0])
        self._update_focus_after_move(cmd.player, piece)  # כאן מאפסים אחרי ההזזה

    def _update_focus_after_move(self, player, piece):
        """Update focus and selection after moving a piece."""
        if player == "A":
            self.input_handler.focus_a = list(piece.position)
            self.input_handler.selected_a = None
        else:
            self.input_handler.focus_b = list(piece.position)
            self.input_handler.selected_b = None

    def _can_move(self, piece, target_pos):
        """
        Check if the piece can move to the target position using its own moves.txt.
        Uses a relative path so it works on any computer.
        """
        print("piece_id:", piece.piece_id)
        piece_type = piece.piece_id.split('_')[0]
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        moves_path = os.path.join(base_dir, "pieces", piece_type, "moves.txt")
        moves = Moves(moves_path, (self.board.H_cells, self.board.W_cells))
        possible_moves = moves.get_moves(*piece.position)
        print("possible_moves:", possible_moves)
        return tuple(target_pos) in possible_moves

    def _show(self) -> bool:
        """Check if the game window is still open."""
        return cv2.getWindowProperty("Game", cv2.WND_PROP_VISIBLE) > 0

    # ─── capture resolution ────────────────────────────────────────────────
    def _resolve_collisions(self, just_moved_piece=None):
        """בדוק האם יש שני כלים באותה משבצת, והכרע מי אוכל את מי."""
        positions = {}
        to_remove = []
        for p in self.pieces.values():
            pos = tuple(p.position)
            if pos in positions:
                other = positions[pos]
                # אם יש כלי שהרגע זז למשבצת הזו – הוא אוכל את העומד
                if just_moved_piece and p.piece_id == just_moved_piece.piece_id:
                    print(f"{p.piece_id} eats {other.piece_id}")
                    publish("piece_captured", {"victim": other})
                    to_remove.append(other.piece_id)
                elif just_moved_piece and other.piece_id == just_moved_piece.piece_id:
                    print(f"{other.piece_id} eats {p.piece_id}")
                    publish("piece_captured", {"victim": p})
                    to_remove.append(p.piece_id)
                # אם שניהם זזו – מי שlast_action_time קטן יותר אוכל
                elif p.last_action_time < other.last_action_time:
                    print(f"{p.piece_id} eats {other.piece_id}")
                    publish("piece_captured", {"victim": other})
                    to_remove.append(other.piece_id)
                else:
                    print(f"{other.piece_id} eats {p.piece_id}")
                    publish("piece_captured", {"victim": p})
                    to_remove.append(p.piece_id)
            else:
                positions[pos] = p
       
        for pid in to_remove:
            if pid in self.pieces:
                del self.pieces[pid]

    # ─── board validation & win detection ───────────────────────────────────
    def _is_win(self) -> bool:
        """Check if the game has ended."""
        return False  # Implement win logic here

    def _announce_win(self):
        """Announce the winner (not implemented)."""
        pass

    def _get_piece_at(self, pos, player):
        """Find a piece at the given position and player."""
        for p in self.pieces.values():
            if hasattr(p, "position") and p.position == pos and getattr(p, "player", None) == player:
                return p
        return None

    def _try_move(self, piece, target_pos):
        piece.position = tuple(target_pos)
        piece.last_action_time = time.time()
        publish("piece_moved", {"piece": piece,      
                                "to":   tuple(target_pos)})

        self._resolve_collisions(just_moved_piece=piece)
