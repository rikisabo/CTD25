import pathlib
from typing import Dict, Tuple
from It1_interfaces.Command import Command
from It1_interfaces.Board import Board
from It1_interfaces.Physics import IdlePhysics, MovePhysics, Physics

class PhysicsFactory:      # very light for now
    @staticmethod
    def create_physics(start_cell: Tuple[int, int], cmd: Command, cfg: Dict, board: Board) -> Physics:
        """Create a Physics instance (Idle or Move) based on command type."""
        speed = cfg.get("speed_m_s", 1.0)
        if cmd.type == "move":
            return MovePhysics(start_cell, board, speed)
        else:
            return IdlePhysics(start_cell, board, speed)