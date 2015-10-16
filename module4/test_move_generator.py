import unittest
from efficient_mover import EfficientMover
from board import Board


class TestEfficientMover(unittest.TestCase):
    def test_move_generator(self):
        board = Board(size=4)
        efficient_mover = EfficientMover()

        # test move_left
        row = [16, 4, 4, 0]
        row_as_int = board.convert_cells_to_integer(row)
        self.assertTrue(efficient_mover.can_move_left(row_as_int))
        row_moved_left_as_int = efficient_mover.move_left(row_as_int)
        row_moved_left = board.convert_integer_to_cells(row_moved_left_as_int)
        self.assertEqual(row_moved_left, [16, 8, 0, 0])

        # test move_right
        row2 = [16, 16, 0, 32]
        row2_as_int = board.convert_cells_to_integer(row2)
        self.assertTrue(efficient_mover.can_move_right(row2_as_int))
        row2_moved_right_as_int = efficient_mover.move_right(row2_as_int)
        row2_moved_right = board.convert_integer_to_cells(row2_moved_right_as_int)
        self.assertEqual(row2_moved_right, [0, 0, 32, 32])

        # test move_right where nothing moves
        row3 = [16, 4, 2, 32]
        row3_as_int = board.convert_cells_to_integer(row3)
        self.assertFalse(efficient_mover.can_move_right(row3_as_int))
        row3_moved_right_as_int = efficient_mover.move_right(row3_as_int)
        row3_moved_right = board.convert_integer_to_cells(row3_moved_right_as_int)
        self.assertEqual(row3_moved_right, [16, 4, 2, 32])


if __name__ == '__main__':
    unittest.main()
