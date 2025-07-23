import cv2
import inspect
import pathlib
import queue
import threading
import time
import math
import os
from typing import List, Dict, Tuple, Optional
from Board import Board
# from Bus.bus import EventBus, Event
from Command import Command
from Piece import Piece
from It1_interfaces.img import Img
from It1_interfaces.InputHandler import InputHandler
from Moves import Moves

# Exception for invalid board state
# class InvalidBoard(Exception):
#     ...

# ────────────────────────────────────────────────────────────────────
class Game:
    def __init__(self, pieces: List[Piece], board: Board):
        """Initialize the game with pieces, board, and optional event bus."""
        self.pieces = {p.piece_id: p for p in pieces}
        self.board = board
        self.input_handler = InputHandler(board, self.pieces)
        self.focus_a = [0, 0]  # Initial position for player A
        self.focus_b = [7, 7]  # Initial position for player B
        self.select_stage_a = 0  # 0=select piece, 1=select target
        self.select_stage_b = 0
        self.user_input_queue = queue.Queue()
        #self.moves = Moves(pathlib.Path("moves.txt"), (board.H_cells, board.W_cells))

    # ─── helpers ─────────────────────────────────────────────────────────────
    def game_time_ms(self) -> int:
        """Return the current game time in milliseconds."""
        return int(time.time() * 1000)

    def clone_board(self) -> Board:
        """
        Return a brand-new Board wrapping a copy of the background pixels
        so we can paint sprites without touching the pristine board.
        """
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
        """Draw the current game state."""
        img = self.board.img.img.copy()
        for p in self.pieces.values():
            p.draw_on_board_to_img(img, self.board, now_ms=0)
        self.input_handler.draw_focus(img)
        cv2.imshow("Game", img)

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
    def _resolve_collisions(self):
        """Resolve piece collisions and captures (not implemented)."""
        pass

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
        print(f"Moving {piece.piece_id} from {piece.position} to {target_pos}")
        piece.position = tuple(target_pos)
        print("All pieces after move:")
        for p in self.pieces.values():
            print(f"{p.piece_id}: {p.position}")
