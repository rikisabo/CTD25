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

    def load_moves(self) -> List[Tuple[int, int]]:
        """Load moves from a text file."""
        moves = []
        with open(self.txt_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                line = line.split("//")[0].strip()
                parts = line.split(',')
                if len(parts) == 2:
                    try:
                        r = int(parts[0].split(":")[0])
                        c = int(parts[1].split(":")[0])
                        moves.append((r, c))
                    except Exception as e:
                        print(f"Skipped line (parse error): {line} ({e})")
        return moves

    def get_moves(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all possible moves from a given position."""
        self.moves = self.load_moves()
        if not self.moves: 
            return []
        return self.moves