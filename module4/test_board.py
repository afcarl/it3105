import unittest
from board import Board


class TestMain(unittest.TestCase):
    def setUp(self):
        self.board = Board(size=4)

    def test_can_move_1(self):
        board_values = [
            [0, 0, 0, 2],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.board.set_board_values(board_values)
        self.assertFalse(self.board.can_move(Board.UP))
        self.assertFalse(self.board.can_move(Board.RIGHT))
        self.assertTrue(self.board.can_move(Board.DOWN))
        self.assertTrue(self.board.can_move(Board.LEFT))

    def test_can_move_2(self):
        board_values = [
            [2, 0, 0, 0],
            [2, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.board.set_board_values(board_values)
        self.assertTrue(self.board.can_move(Board.UP))
        self.assertTrue(self.board.can_move(Board.RIGHT))
        self.assertTrue(self.board.can_move(Board.DOWN))
        self.assertFalse(self.board.can_move(Board.LEFT))

    def test_can_move_3(self):
        board_values = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [2, 0, 0, 0],
            [4, 2, 0, 2]
        ]
        self.board.set_board_values(board_values)
        self.assertTrue(self.board.can_move(Board.UP))
        self.assertTrue(self.board.can_move(Board.RIGHT))
        self.assertFalse(self.board.can_move(Board.DOWN))
        self.assertTrue(self.board.can_move(Board.LEFT))

if __name__ == '__main__':
    unittest.main()
