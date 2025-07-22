from It1_interfaces.Moves import Moves
import tempfile
import pathlib

def test_load_moves():
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("1,0\n2,0\n-1,0\n")
        f.flush()
        moves = Moves(pathlib.Path(f.name), (8, 8))
        assert (1, 0) in moves.moves
        assert (2, 0) in moves.moves
        assert (-1, 0) in moves.moves