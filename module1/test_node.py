import unittest
from two_dee import Point, Rect
from board import Board
from node import Node


class TestNode(unittest.TestCase):
    def test_node_extends_point(self):
        dimensions = Rect(0, 0, 12, 12)
        start = Point(3, 4)
        goal = Point(8, 11)
        barriers = []
        board = Board(dimensions, start, goal, barriers)

        position1 = Point(8, 9)
        node1 = Node(board, position1, 0)

        position2 = Point(8, 10)
        node2 = Node(board, position2, 1, None, node1)

        node3 = Node(board, position1, 2, None, node2)

        self.assertTrue(node1.equals(node1))
        self.assertFalse(node1.equals(node2))
        self.assertTrue(node1.equals(node3))

        self.assertEquals(node1.as_tuple(), (8, 9))

        goal_node = Node(board, goal, 3, None, node3)
        self.assertTrue(goal_node.is_solution())


if __name__ == '__main__':
    unittest.main()
