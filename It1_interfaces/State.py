from It1_interfaces.Command import Command
from It1_interfaces.Moves import Moves
from It1_interfaces.Graphics import Graphics
from It1_interfaces.Physics import Physics
from typing import Dict
import time


class State:
    def __init__(self, moves: Moves, graphics: Graphics, physics: Physics, cmd: Command):
        self._moves = moves
        self._graphics = graphics
        self._physics = physics
        self._graphics.reset(cmd)
        self._physics.reset(cmd)
        self._transitions: Dict[str, "State"] = {}

    def set_transition(self, event: str, target: "State"):
        """Set a transition from this state to another state on an event."""
        self._transitions[event] = target


    def reset(self, cmd: Command):
        """Reset the state with a new command."""
        self._graphics.reset(cmd)
        self._physics.reset(cmd)

    def can_transition(self, now_ms: int) -> bool:           # customise per state
        """Check if the state can transition."""
        pass

    def get_state_after_command(self, cmd: Command, now_ms: int) -> "State":
        """Get the next state after processing a command."""
        res=self._transitions[cmd.type]
        res.reset(cmd)
        return res

    def update(self, now_ms: int) -> "State":
        """Update the state based on current time."""
        # עדכון הגרפיקה לפי הזמן
        self._graphics.update(now_ms)
        # עדכון הפיזיקה לפי הזמן, ייתכן ותחזיר פקודה חדשה (cmd) אם יש שינוי
        cmd = self._physics.update(now_ms)
        if cmd is not None:
            return self.get_state_after_command(cmd, now_ms)
        return self  

    def get_command(self) -> Command:
        """Get the current command for this state."""
        pass
    def get_img(self):
        """Return the current image for this state."""
        return self._graphics.get_img()