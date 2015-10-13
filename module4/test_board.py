import unittest
from board import Board


class TestBoard(unittest.TestCase):
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

    def test_can_move_4(self):
        board_values = [
            [0, 4, 4, 2],
            [0, 0, 2, 8],
            [2, 0, 8, 32],
            [0, 0, 0, 8]
        ]
        self.board.set_board_values(board_values)
        self.assertTrue(self.board.can_move(Board.UP))
        self.assertTrue(self.board.can_move(Board.RIGHT))
        self.assertTrue(self.board.can_move(Board.DOWN))
        self.assertTrue(self.board.can_move(Board.LEFT))

    def test_do_move_right_1(self):
        board_values = [
            [0, 4, 4, 2],
            [0, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 0]
        ]
        self.board.set_board_values(board_values)
        self.board.move(Board.RIGHT)
        self.assertEqual(
            self.board.board_values,
            [
                [0, 0, 8, 2],
                [0, 0, 0, 0],
                [0, 0, 0, 2],
                [0, 0, 0, 0]
            ]
        )

    def test_do_move_right_2(self):
        board_values = [
            [4, 4, 4, 4],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        self.board.set_board_values(board_values)
        self.board.move(Board.RIGHT)
        self.assertEqual(
            self.board.board_values,
            [
                [0, 0, 8, 8],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        )

    def test_do_move_left_1(self):
        board_values = [
            [0, 4, 4, 2],
            [0, 0, 2, 8],
            [2, 0, 8, 32],
            [0, 0, 0, 8]
        ]
        self.board.set_board_values(board_values)
        self.board.move(Board.LEFT)
        self.assertEqual(
            self.board.board_values,
            [
                [8, 2, 0, 0],
                [2, 8, 0, 0],
                [2, 8, 32, 0],
                [8, 0, 0, 0]
            ]
        )

    def test_do_move_up_1(self):
        board_values = [
            [0, 4, 4, 0],
            [0, 0, 4, 0],
            [0, 2, 0, 0],
            [0, 0, 0, 2]
        ]
        self.board.set_board_values(board_values)
        self.board.move(Board.UP)
        self.assertEqual(
            self.board.board_values,
            [
                [0, 4, 8, 2],
                [0, 2, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        )

    def test_do_move_down_1(self):
        board_values = [
            [2, 4, 4, 2],
            [0, 0, 2, 8],
            [2, 0, 8, 32],
            [0, 0, 0, 8]
        ]
        self.board.set_board_values(board_values)
        self.board.move(Board.DOWN)
        self.assertEqual(
            self.board.board_values,
            [
                [0, 0, 0, 2],
                [0, 0, 4, 8],
                [0, 0, 2, 32],
                [4, 4, 8, 8]
            ]
        )


if __name__ == '__main__':
    unittest.main()
