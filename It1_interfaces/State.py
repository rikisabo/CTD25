from It1_interfaces.Command import Command
from It1_interfaces.Moves import Moves
from It1_interfaces.Graphics import Graphics
from It1_interfaces.Physics import Physics
from typing import Dict, Optional


class State:
    """
    Represents a single state in the piece's state machine (e.g., idle, move, long_rest).
    Handles transitions, graphics, and physics for that state.
    """
    def __init__(self, moves: Moves, graphics: Graphics, physics: Physics, cmd: Command):
        self._moves = moves
        self._graphics = graphics
        self._physics = physics
        self._graphics.reset(cmd)
        self._physics.reset(cmd)
        self._transitions: Dict[str, "State"] = {}

    def set_transition(self, event: str, target: "State"):
        """Set a transition from this state to another state on an event (e.g., 'move', 'long_rest')."""
        self._transitions[event] = target

    def reset(self, cmd: Command):
        """Reset the state with a new command (for animation/physics restart)."""
        self._graphics.reset(cmd)
        self._physics.reset(cmd)

    def get_state_after_command(self, cmd: Command, now_ms: int) -> "State":
        """
        Get the next state after processing a command (e.g., move, long_rest).
        Resets the new state with the command.
        """
        if cmd.type not in self._transitions:
            return self  # No transition defined, stay in current state
        next_state = self._transitions[cmd.type]
        next_state.reset(cmd)
        return next_state

    def update(self, now_ms: int) -> "State":
        """
        Update the state based on current time.
        Handles animation and physics, and transitions to the next state if needed.
        """
        self._graphics.update(now_ms)
        cmd = self._physics.update(now_ms)
        if cmd is not None:
            # There is a transition event (e.g., finished moving → long_rest)
            return self.get_state_after_command(cmd, now_ms)
        return self

    def get_img(self):
        """Return the current image for this state (for drawing)."""
        return self._graphics.get_img()