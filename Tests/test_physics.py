from It1_interfaces.PhysicsFactory import PhysicsFactory
from It1_interfaces.Board import Board
from It1_interfaces.img import Img

def test_physics_factory():
    board = Board(10, 10, 8, 8, Img())
    # בדיקה בסיסית - תעדכן לפי המימוש שלך
    # physics = PhysicsFactory.create_physics((0,0), None, {}, board)
    # assert physics is not None