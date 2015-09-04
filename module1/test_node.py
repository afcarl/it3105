import unittest
from rect import Rect
from point import Point
from board import Board
from node import Node


class TestNode(unittest.TestCase):
    def test_node_extends_point(self):
        dimensions = Rect(0, 0, 12, 12)
        start = Point(3, 4)
        goal = Point(8, 11)
        barriers = []
        Node.board = Board(dimensions, start, goal, barriers)

        position1 = Point(8, 9)
        node1 = Node(position1, 0)
        position2 = Point(8, 10)
        node2 = Node(position2, 1, None, node1)
        node3 = Node(position1, 2, None, node2)

        # test equals()
        self.assertTrue(node1.equals(node1))
        self.assertFalse(node1.equals(node2))
        self.assertTrue(node1.equals(node3))

        # test as_tuple()
        self.assertEquals(node1.as_tuple(), (8, 9))

        # test is_solution()
        goal_node = Node(goal, 3, None, node3)
        self.assertTrue(goal_node.is_solution())

        # test get_ancestors()
        ancestors = goal_node.get_ancestors()
        self.assertTrue(ancestors[0].equals(node3))
        self.assertTrue(ancestors[1].equals(node2))
        self.assertTrue(ancestors[2].equals(node1))

if __name__ == '__main__':
    unittest.main()
