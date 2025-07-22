from dataclasses import dataclass
import csv
from It1_interfaces.img import Img

@dataclass
class Board:
    cell_H_pix: int
    cell_W_pix: int
    W_cells: int
    H_cells: int
    img: Img
    #self.canvas: Img ()
    # convenience, not required by dataclass
    def clone(self) -> "Board":
        """Clone the board with a copy of the image."""
        return Board(
            cell_H_pix=self.cell_H_pix,
            cell_W_pix=self.cell_W_pix,
            W_cells=self.W_cells,
            H_cells=self.H_cells,
            img=self.img.clone(),
        )

    def get_cell_pos(self, cell):
        """Convert cell indices (row, col) to pixel coordinates (x, y) on the board."""
        i, j = cell
        x = j * self.cell_W_pix + self.cell_W_pix // 2
        y = i * self.cell_H_pix + self.cell_H_pix // 2
        return x, y

    @staticmethod
    #initial in the starting position
    def read_board_csv(path):
        print("Reading board from:", path)
        pieces = []
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                print("row", i, row)
                for j, cell in enumerate(row):
                    if cell.strip():
                        pieces.append((cell.strip(), (i, j)))
        return pieces