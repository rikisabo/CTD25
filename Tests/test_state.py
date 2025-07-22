from It1_interfaces.State import State

class DummyGraphics:
    def reset(self, cmd): pass

class DummyMoves: pass

class DummyPhysics:
    def reset(self, cmd): pass

class DummyCommand: pass

def test_state_init():
    state = State(DummyMoves(), DummyGraphics(), DummyPhysics(), DummyCommand())
    assert state is not None
