import unittest
from priority_set import NodePrioritySet
from two_dee import Point, Rect
from board import Board
from node import Node


class TestNodePrioritySet(unittest.TestCase):
    def setUp(self):
        dimensions = Rect(0, 0, 3, 3)
        start = Point(0, 0)
        goal = Point(2, 0)
        barriers = []
        board = Board(dimensions, start, goal, barriers)

        self.node1 = Node(board, start, 0)
        self.node2 = Node(board, Point(1, 0), 1, None, self.node1)
        self.node3 = Node(board, goal, 2, None, self.node2)
        self.node4 = Node(board, Point(1, 2), 3, None, self.node3)
        self.node5_like_node2 = Node(board, Point(1, 0), 4, self.node4)

    def test_methods(self):
        my_collection = NodePrioritySet()
        my_collection.add(self.node1, 3)
        my_collection.add(self.node2, 1)
        my_collection.add(self.node3, 2)

        self.assertFalse(my_collection.is_empty())

        self.assertTrue(self.node1 in my_collection)
        self.assertTrue(self.node2 in my_collection)
        self.assertTrue(self.node3 in my_collection)
        self.assertFalse(self.node4 in my_collection)
        self.assertTrue(self.node5_like_node2 in my_collection)

        self.assertEquals(my_collection[self.node1], self.node1)
        self.assertEquals(my_collection[self.node5_like_node2], self.node2)

        self.assertEquals(my_collection.pop(), self.node2)
        self.assertEquals(my_collection.pop(), self.node3)
        self.assertEquals(my_collection.pop(), self.node1)

        self.assertTrue(my_collection.is_empty())
        self.assertFalse(self.node1 in my_collection)

if __name__ == '__main__':
    unittest.main()
