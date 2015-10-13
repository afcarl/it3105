import unittest
from board import Board
from node import Node


class TestNode(unittest.TestCase):
    def test_can_move_1(self):
        board1 = Board()
        board1_values = [
            [0, 8, 4, 2],
            [0, 2, 0, 16],
            [0, 0, 0, 2],
            [0, 0, 0, 0]
        ]
        board1.set_board_values(board1_values)

        board2_values = [
            [0, 8, 4, 2],
            [0, 0, 0, 16],
            [0, 0, 0, 4],
            [0, 0, 0, 0]
        ]
        board2 = Board()
        board2.set_board_values(board2_values)

        node1 = Node(board=board1)
        node2 = Node(board=board2)

        self.assertGreater(node2.get_heuristic(), node1.get_heuristic())


if __name__ == '__main__':
    unittest.main()
