import pathlib
from typing import Dict, Tuple
import json
from It1_interfaces.Command import Command
from It1_interfaces.Board import Board
from It1_interfaces.Graphics import Graphics    
from It1_interfaces.GraphicsFactory import GraphicsFactory
from It1_interfaces.Moves import Moves
from It1_interfaces.PhysicsFactory import PhysicsFactory
from It1_interfaces.Piece import Piece
from It1_interfaces.State import State


class PieceFactory:
    def __init__(self, board: Board, pieces_root: pathlib.Path):
        """Initialize piece factory with board and 
        generates the library of piece templates from the pieces directory.."""
        self.board = board
        self.pieces_root = pieces_root

    def _build_state_machine(self, piece_dir: pathlib.Path, cell: Tuple[int, int], cmd: Command, cfg: Dict) -> State:
        moves = Moves(piece_dir / "moves.txt", [self.board.cell_H_pix, self.board.cell_W_pix])
        graphics = GraphicsFactory.create_graphics(piece_dir/"states"/cmd.type/ "sprites", self.board.cell_H_pix)
        physics = PhysicsFactory.create_physics(cell, cmd, cfg, self.board)
        return State(moves, graphics, physics,cmd)

    #PieceFactory.py  – replace create_piece(...)
    def create_piece(self, p_type: str, cell: Tuple[int, int]) -> Piece:
        folder = self.pieces_root / p_type
        if not folder.exists():
            raise ValueError(f"Piece type '{p_type}' does not exist in {self.pieces_root}")
        if not folder.is_dir():
            raise ValueError(f"Expected a directory for piece type '{p_type}' at {folder}")

        moves_path = folder / "moves.txt"
        print(f"Trying to load moves from: {moves_path}")
        moves = Moves(moves_path, [self.board.H_cells, self.board.W_cells])
        moves.get_moves(cell[0], cell[1])
        print(f"Loaded moves for {p_type} from {moves_path}")

        states={}
        states_folder=folder/"states"

        for sub_folder in states_folder.iterdir():
            name = sub_folder.name
            if sub_folder.is_dir():
                cfg_path = sub_folder / "config.json"
                cfg = json.load(open(cfg_path, 'r')) if cfg_path.exists() else {}
                cmd = Command(timestamp=0, piece_id=p_type, type=name, params=[cell, cell])
                states[name] = self._build_state_machine(folder, cell, cmd, cfg)
        # Create the piece with its initial state
        states["idle"].set_transition("Move", states["move"])
        states["idle"].set_transition("jump", states["jump"])

        states["move"].set_transition("long_rest", states["long_rest"])
        
        states["jump"].set_transition("short_rest", states["short_rest"])
        states["long_rest"].set_transition("idle", states["idle"])
        states["short_rest"].set_transition("idle", states["idle"])

        # קביעת שחקן לפי סוג הכלי (B=אדום/A, W=לבן/B)
        player = "A" if p_type.endswith("B") else "B"
        piece_id = f"{p_type}_{cell[0]}_{cell[1]}"

        print(f"Created piece: {piece_id}, player: {player}, cell: {cell}")
        return Piece(
            piece_id=piece_id,
            init_state=states["idle"],
            player=player
        )
