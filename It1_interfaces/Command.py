from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

@dataclass
class Command:
    timestamp: int #זמן התחלה         # ms since game start
    piece_id: str  #איזה כלי
    type: str      #סוג פקודה          # "Move" | "Jump" | …
    params: List   # מאיפה לאיפה       # payload (e.g. ["e2", "e4"]) 