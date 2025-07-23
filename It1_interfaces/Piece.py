from It1_interfaces.Board import Board
from It1_interfaces.Command import Command
from It1_interfaces.State import State
import cv2

class Piece:
    def __init__(self, piece_id: str, init_state: State, player: str):
        self.piece_id = piece_id
        self._state = init_state
        self.position = self._state._physics.cell
        self.player = player  # ← הוספה תקינה

    def on_command(self, cmd: Command, now_ms: int):
        """Handle a command for this piece."""
        if self._state.is_process_command(cmd):
            self._state=self._state.process_command(cmd) 

    def update(self, now_ms: int):
        """Update the piece state based on current time."""
        pass

    def draw_on_board(self, board, now_ms: int):
        img = self._state.get_img()
        if img is not None:
            cell_h, cell_w = board.cell_H_pix, board.cell_W_pix
            sprite = img.img
            sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
            i, j = self.position  # ← שינוי כאן
            x = j * cell_w
            y = i * cell_h
            board.img.img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]

    def draw_on_board_to_img(self, img, board, now_ms: int):
        sprite = self._state.get_img().img
        cell_h, cell_w = board.cell_H_pix, board.cell_W_pix
        sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
        i, j = self.position  # ← שינוי כאן
        x = j * cell_w
        y = i * cell_h
        img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]
        
    def reset(self, now_ms: int):
        """Reset the piece to its initial state (למשחק חדש או תחילת תור)."""
        # אם יש לך לוגיקה של איפוס מצב, כתוב אותה כאן.
        # אם אין, אפשר פשוט pass:
        self.position = self._state._physics.cell  # ← שינוי כאן

    def get_path_to(self, target_pos, board):
        # מסלול אופקי/אנכי פשוט (ללא חוקים)
        path = []
        i0, j0 = self.position
        i1, j1 = target_pos
        if i0 == i1:
            step = 1 if j1 > j0 else -1
            for j in range(j0, j1, step):
                path.append((i0, j))
        elif j0 == j1:
            step = 1 if i1 > i0 else -1
            for i in range(i0, i1, step):
                path.append((i, j0))
        path.append(target_pos)
        return path
    
    def __repr__(self):
        return f"Piece(id={self.piece_id}, pos={self.position}, player={self.player})"