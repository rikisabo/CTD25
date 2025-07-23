import cv2
import time
from Command import Command

class InputHandler:
    def __init__(self, board, pieces):
        self.board = board
        self.pieces = pieces
        self.focus_a = [0, 0]  # שחקן A'
        self.focus_b = [7, 7]  # שחקן B'
        self.stage_a = 0  # 0=בחירת כלי, 1=בחירת יעד
        self.stage_b = 0
        self.selected_a = None
        self.selected_b = None

    def handle_keyboard(self, key):
        now_ms = int(time.time() * 1000)
        cmd = None

        # תזוזת פוקוס לשחקן A
        if key == ord('l'):
            self.focus_a[1] = max(0, self.focus_a[1] - 1)
        if key == ord("'"):
            self.focus_a[1] = min(self.board.W_cells-1, self.focus_a[1] + 1)
        if key == ord('p'):
            self.focus_a[0] = max(0, self.focus_a[0] - 1)
        if key == ord(';'):
            self.focus_a[0] = min(self.board.H_cells-1, self.focus_a[0] + 1)

        # בחירת כלי או יעד לשחקן A
        if key == 13:
            if self.stage_a == 0:
                piece = self._get_piece_at(self.focus_a, "A")
                if piece is not None:
                    self.selected_a = piece  # שמור את הכלי שנבחר!
                    print(f"Selected piece: {piece}")
                    cmd = Command(
                        timestamp=now_ms,
                        player="A",
                        type="Select",
                        piece_id=piece.piece_id,
                        params=[self.focus_a]
                    )
                    self.stage_a = 1
                else:
                    print("No piece found at", self.focus_a)
            elif self.stage_a == 1:
                # כאן לא מחפשים שוב כלי! משתמשים ב-selected_a שנשמר
                print("selected_a before move:", self.selected_a)
                if self.selected_a is not None:
                    cmd = Command(
                        timestamp=now_ms,
                        player="A",
                        type="Move",
                        piece_id=self.selected_a.piece_id,
                        params=[self.focus_a]  # המשבצת החדשה!
                    )
                else:
                    print("ERROR: No piece selected for move!")
                self.stage_a = 0

        # תזוזת פוקוס לשחקן B
        if key == ord('a'):
            self.focus_b[1] = max(0, self.focus_b[1] - 1)
        if key == ord('d'):
            self.focus_b[1] = min(self.board.W_cells-1, self.focus_b[1] + 1)
        if key == ord('w'):
            self.focus_b[0] = max(0, self.focus_b[0] - 1)
        if key == ord('s'):
            self.focus_b[0] = min(self.board.H_cells-1, self.focus_b[0] + 1)

        # בחירת כלי או יעד לשחקן B
        if key == 32:
            if self.stage_b == 0:
                piece = self._get_piece_at(self.focus_b, "B")
                if piece is not None:
                    self.selected_b = piece
                    cmd = Command(
                        timestamp=now_ms,
                        player="B",
                        type="Select",
                        piece_id=piece.piece_id,
                        params=[self.focus_b]
                    )
                    self.stage_b = 1
                else:
                    print("No piece found at", self.focus_b)
            elif self.stage_b == 1:
                # כאן לא מחפשים שוב כלי! משתמשים ב-selected_b שנשמר
                if self.selected_b is not None:
                    cmd = Command(
                        timestamp=now_ms,
                        player="B",
                        type="Move",
                        piece_id=self.selected_b.piece_id,
                        params=[self.focus_b]
                    )
                else:
                    print("ERROR: No piece selected for move!")
                self.stage_b = 0

        return cmd

    def draw_focus(self, img):
        cell_h, cell_w = self.board.cell_H_pix, self.board.cell_W_pix
        y, x = self.focus_a
        cv2.rectangle(img, (x*cell_w, y*cell_h), ((x+1)*cell_w-1, (y+1)*cell_h-1), (0,0,255), 8)
        # שחקן ב' - ריבוע ירוק עבה
        y, x = self.focus_b
        cv2.rectangle(
            img,
            (x * cell_w, y * cell_h),
            ((x + 1) * cell_w - 1, (y + 1) * cell_h - 1),
            (0, 255, 0), 8
        )

    def _get_piece_at(self, pos, player=None):
        for p in self.pieces.values():
            if hasattr(p, "position") and tuple(p.position) == tuple(pos):
                if player is None or p.player == player:
                    print(p)
                    return p
        return None