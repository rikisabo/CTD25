import cv2
import inspect
import pathlib
import queue
import threading
import time
import math
from typing import List, Dict, Tuple, Optional
from Board import Board
# from Bus.bus import EventBus, Event
from Command import Command
from Piece import Piece
from It1_interfaces.img import Img
from It1_interfaces.InputHandler import InputHandler


class InvalidBoard(Exception):
    ...


# ────────────────────────────────────────────────────────────────────
class Game:
    def __init__(self, pieces: List[Piece], board: Board):
        """Initialize the game with pieces, board, and optional event bus."""
        self.pieces = {p.piece_id: p for p in pieces}
        print("All piece_ids:", list(self.pieces.keys()))
        print("Total in self.pieces:", len(self.pieces))
        self.board = board
        self.input_handler = InputHandler(board)
        self.focus_a = [0, 0]  # שחקן א'
        self.focus_b = [7, 7]  # שחקן ב'
        self.select_stage_a = 0  # 0=בחירת כלי, 1=בחירת יעד
        self.select_stage_b = 0
        self.user_input_queue = queue.Queue()  # ← הוסף שורה זו

    # ─── helpers ─────────────────────────────────────────────────────────────
    def game_time_ms(self) -> int:
        """Return the current game time in milliseconds."""
        return int(time.time() * 1000)

    def clone_board(self) -> Board:
        """
        Return a **brand-new** Board wrapping a copy of the background pixels
        so we can paint sprites without touching the pristine board.
        """
        pass

    def start_user_input_thread(self):
        """Start the user input thread for mouse handling."""
        pass

    # ─── main public entrypoint ──────────────────────────────────────────────
    def run(self):
        """Main game loop."""
        self.start_user_input_thread()  # QWe2e5

        start_ms = self.game_time_ms()
        for p in self.pieces.values():
            p.reset(start_ms)

        # ─────── main loop ──────────────────────────────────────────────────
        while True:
            self._draw()  # מציג את החלון
            key = cv2.waitKey(200)  # קולט קלט
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
        # ציירי את הכלים על img
        for p in self.pieces.values():
            print(p.piece_id, p._state._physics.cell)
            p.draw_on_board_to_img(img, self.board, now_ms=0)
        # ציירי את הריבועים על img (אחרי הכלים)
        self.input_handler.draw_focus(img)
        cv2.imshow("Game", img)

    def _process_input(self, cmd: Command):
        """Process user input commands."""
        # cmd = ("A"/"B", [row, col], stage)
        # כאן תטפלי בלוגיקת בחירת כלי/יעד לכל שחקן
        print("קלט:", cmd)

    def _show(self) -> bool:
        """Check if the game window is still open."""
        return cv2.getWindowProperty("Game", cv2.WND_PROP_VISIBLE) > 0

    # ─── capture resolution ────────────────────────────────────────────────
    def _resolve_collisions(self):
        """Resolve piece collisions and captures."""
        pass

    # ─── board validation & win detection ───────────────────────────────────
    def _is_win(self) -> bool:
        """Check if the game has ended."""
        return False  # עד שתממשי לוגיקת ניצחון

    def _announce_win(self):
        """Announce the winner."""
        pass
