import unittest
from priority_set import NodePrioritySet
from point import Point
from nav_node import NavNode


class TestNodePrioritySet(unittest.TestCase):
    def test_methods(self):
        self.node1 = NavNode(Point(x=0, y=0), 2, 4)
        self.node1.calculate_f()
        self.node2 = NavNode(Point(x=1, y=0), 2, 3)
        self.node2.calculate_f()
        self.node3 = NavNode(Point(x=2, y=0), 2, 2)
        self.node3.calculate_f()
        self.node4 = NavNode(Point(x=2, y=1), 2, 1)
        self.node4.calculate_f()
        self.node5 = NavNode(Point(x=2, y=0), 3, 2)  # like node3

        my_collection = NodePrioritySet()
        my_collection.add(self.node2, self.node2.f)
        my_collection.add(self.node1, self.node1.f)
        my_collection.add(self.node3, self.node3.f)

        self.assertFalse(my_collection.is_empty())

        self.assertTrue(self.node1 in my_collection)
        self.assertTrue(self.node2 in my_collection)
        self.assertTrue(self.node3 in my_collection)
        self.assertFalse(self.node4 in my_collection)
        self.assertTrue(self.node5 in my_collection)  # node5 has same position as node3

        self.assertEquals(my_collection[self.node1], self.node1)
        self.assertEquals(my_collection[self.node5], self.node3)

        self.assertEquals(my_collection.pop(), self.node3)
        self.assertEquals(my_collection.pop(), self.node2)
        self.assertEquals(my_collection.pop(), self.node1)

        self.assertTrue(my_collection.is_empty())
        self.assertFalse(self.node1 in my_collection)

    def test_first_in_first_out(self):
        self.node1 = NavNode(Point(x=0, y=2), 2, 2)
        self.node2 = NavNode(Point(x=1, y=1), 2, 2)
        self.node3 = NavNode(Point(x=2, y=0), 2, 2)

        my_collection = NodePrioritySet()
        my_collection.add(self.node1, 4)
        my_collection.add(self.node2, 4)
        my_collection.add(self.node3, 4)

        self.assertEquals(my_collection.pop(), self.node3)
        self.assertEquals(my_collection.pop(), self.node2)
        self.assertEquals(my_collection.pop(), self.node1)

if __name__ == '__main__':
    unittest.main()
