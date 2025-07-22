from It1_interfaces.Board import Board
from It1_interfaces.Command import Command
from It1_interfaces.State import State
import cv2

class Piece:
    def __init__(self, piece_id: str, init_state: State):
        """Initialize a piece with ID and initial state."""
        self.piece_id = piece_id
        self._state = init_state
        

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
            # שינוי גודל הספרייט לגודל המשבצת
            sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
            i, j = self._state._physics.cell
            x = j * cell_w
            y = i * cell_h
            # הדבקה ישירה (בלי שקיפות)
            board.img.img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]
            
    def draw_on_board_to_img(self, img, board, now_ms: int):
        sprite = self._state.get_img().img
        cell_h, cell_w = board.cell_H_pix, board.cell_W_pix
        sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
        i, j = self._state._physics.cell
        x = j * cell_w
        y = i * cell_h
        img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]
        
    def reset(self, now_ms: int):
        """Reset the piece to its initial state (למשחק חדש או תחילת תור)."""
        # אם יש לך לוגיקה של איפוס מצב, כתוב אותה כאן.
        # אם אין, אפשר פשוט pass:
        pass