from typing import Tuple, Optional
from It1_interfaces.Command import Command
import math
class Physics:
    SLIDE_CELLS_PER_SEC = 4.0        # tweak to make all pieces slower/faster

    def __init__(self, start_cell: Tuple[int, int],
                 board: "Board", speed_m_s: float = 1.0):
        """Initialize physics with starting cell, board, and speed."""
        self.board = board
        self.cell = start_cell
        self.speed = speed_m_s
        self.pos = self.cell_to_pixel(start_cell)
        self.target_pos = self.pos
        self.start_time = 0
        self.end_time = 0
        self.moving = False

    #*** Convert board cell (col, row) to pixel coordinates (x, y).I add it***
    def cell_to_pixel(self, cell: Tuple[int, int]) -> Tuple[int, int]:
        """Convert board cell (col, row) to pixel coordinates (x, y)."""
        x = cell[0] * self.board.cell_W_pix
        y = cell[1] * self.board.cell_H_pix
        return (x, y)
    
    #***function to calculate distance between two cells I add it***
    def calc_distance(self, from_cell, to_cell):
        dx = to_cell[0] - from_cell[0]
        dy = to_cell[1] - from_cell[1]
        return math.sqrt(dx*dx + dy*dy)
    
    def reset(self, cmd: Command):
        """Reset physics state with a new command."""
        if len(cmd.params) == 2:
            from_cell, to_cell = cmd.params
        elif len(cmd.params) == 1:
            from_cell = to_cell = cmd.params[0]
        else:
            raise ValueError("cmd.params must have at least one cell")
            
        self.cell = from_cell
        self.target_pos = self.cell_to_pixel(to_cell)
        self.start_time = cmd.timestamp
        # חישוב זמן סיום לפי מהירות ומרחק
        distance = self.calc_distance(from_cell, to_cell)
        duration = distance / self.speed
        self.end_time = self.start_time + int(duration * 1000)
        self.moving = True
 
    def update(self, now_ms: int):
        """Update physics state based on current time."""
        if not self.moving:
            return
        if now_ms >= self.end_time:
            # If we reached the target, stop moving
            self.pos = self.target_pos
            self.moving = False
        else:
            progress = (now_ms - self.start_time) / (self.end_time - self.start_time)
            self.pos = (
                self.pos[0] + (self.target_pos[0] - self.pos[0]) * progress,
                self.pos[1] + (self.target_pos[1] - self.pos[1]) * progress
        )
        
       

    def can_be_captured(self) -> bool: 
        """Check if this piece can be captured."""
        return not self.moving
        
    def can_capture(self) -> bool:     
        """Check if this piece can capture other pieces."""
        return not self.moving 

    def get_pos(self) -> Tuple[int, int]:
        """
        Current pixel-space upper-left corner of the sprite.
        Uses the sub-pixel coordinate computed in update();
        falls back to the square's origin before the first update().
        """
        return self.pos
class IdlePhysics(Physics):
    def update(self, now_ms: int) -> Command:
        self.last_update = now_ms
        return self.cmd or Command("idle")

class MovePhysics(Physics):
    def update(self, now_ms: int) -> Command:
        # כאן תוכל לממש מעבר תא בהתאם לזמן ומהירות
        self.last_update = now_ms
        # סימולציה בסיסית להשלמת מעבר
        self.finished = True
        return self.cmd or Command("default_piece", "move", {})
