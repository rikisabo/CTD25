# Moves.py  – drop-in replacement
import pathlib
from typing import List, Tuple

class Moves:
   
    def __init__(self, txt_path: pathlib.Path, dims: Tuple[int, int]):
        """Initialize moves with rules from text file and board dimensions."""
        self.txt_path = txt_path
        self.dims = dims
        self.moves = self.load_moves()
        if not self.moves:
            raise ValueError(f"No valid moves found in {txt_path}")

    def load_moves(self) -> List[str]:
        """Load moves from a text file as raw lines."""
        moves = []
        with open(self.txt_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                line = line.split("//")[0].strip()
                moves.append(line)
        return moves

    def get_moves(self, row, col, has_moved=False, capture=False):
        moves = []
        for line in self.moves:
            dx, dy, move_type = parse_line(line)
            if move_type == "1st" and has_moved:
                continue
            if move_type == "capture" and not capture:
                continue
            moves.append((row + dx, col + dy))
        return moves

def parse_line(line):
    # דוגמה: "1,0:non_capture"
    parts = line.split(":")
    coords = parts[0].split(",")
    dx = int(coords[0])
    dy = int(coords[1])
    move_type = parts[1] if len(parts) > 1 else "non_capture"
    return dx, dy, move_type