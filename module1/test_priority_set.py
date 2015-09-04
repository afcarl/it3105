import unittest
from priority_set import PrioritySet


class TestPrioritySet(unittest.TestCase):
    def test_methods(self):
        my_collection = PrioritySet()
        my_collection.add('yo', 3)
        my_collection.add('dats', 1)
        my_collection.add('kool', 2)

        self.assertTrue(my_collection.exists('yo'))
        self.assertTrue(my_collection.exists('dats'))
        self.assertTrue(my_collection.exists('kool'))
        self.assertFalse(my_collection.exists('bro'))

        self.assertEquals(my_collection.pop(), 'dats')
        self.assertEquals(my_collection.pop(), 'kool')
        self.assertEquals(my_collection.pop(), 'yo')

if __name__ == '__main__':
    unittest.main()
