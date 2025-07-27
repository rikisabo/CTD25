from It1_interfaces.Board import Board
from It1_interfaces.Command import Command
from It1_interfaces.State import State
import cv2

class Piece:
    """
    Represents a single game piece (chessman).
    Holds its state machine, position, player, and handles updates and drawing.
    """
    def __init__(self, piece_id: str, init_state: State, player: str):
        self.piece_id = piece_id
        self.state = init_state
        self.position = self.state._physics.cell  # Initial position from physics
        self.player = player
        self.last_action_time = 0

    def update(self, now_ms: int):
        """
        Update the piece's state (animation, physics, transitions).
        Also updates the piece's position if the state/physics changed it.
        """
        new_state = self.state.update(now_ms)
        if new_state is not self.state:
            # If state changed (e.g., move finished → long_rest), update state and position
            self.state = new_state
            # Update position if physics changed it (e.g., after move)
            if hasattr(self.state._physics, "cell"):
                self.position = self.state._physics.cell

    def draw_on_board(self, board: Board, now_ms: int):
        """
        Draw the piece on the board image at its current position.
        """
        img = self.state.get_img()
        if img is not None:
            cell_h, cell_w = board.cell_H_pix, board.cell_W_pix
            sprite = img.img
            sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
            i, j = self.position
            x = j * cell_w
            y = i * cell_h
            board.img.img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]

    def draw_on_board_to_img(self, img, board: Board, now_ms: int):
        """
        Draw the piece on a given image (not necessarily the board) at its current position.
        """
        sprite = self.state.get_img().img
        cell_h, cell_w = board.cell_H_pix, board.cell_W_pix
        sprite = cv2.resize(sprite, (cell_w, cell_h), interpolation=cv2.INTER_AREA)
        i, j = self.position
        x = j * cell_w
        y = i * cell_h
        img[y:y+cell_h, x:x+cell_w, :3] = sprite[:, :, :3]

    def reset(self, now_ms: int):
        """
        Reset the piece to its initial state (for new game or turn start).
        """
        self.position = self.state._physics.cell
        self.state.reset(Command(now_ms, self.piece_id, "idle", [self.position]))
        self.last_action_time = 0

    def __repr__(self):
        return f"Piece(id={self.piece_id}, pos={self.position}, player={self.player})"