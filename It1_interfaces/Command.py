from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class Command:
    timestamp: int #start time      # ms since game start
    piece_id: str  #which piece     # e.g. "e2" or "b1"
    type: str      #type of command         # "Move" | "Jump" | …
    params: List   #start and target      # payload (e.g. ["e2", "e4"]) 
    player:str = ""  # player id, e.g. "a" or "b" (optional, for multiplayer)