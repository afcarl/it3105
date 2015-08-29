import unittest
from two_dee import Point, Rect


class TestTwoDee(unittest.TestCase):
    def test_construct_point(self):
        point1 = Point((3, 4))
        self.assertEqual(point1.x, 3)
        self.assertEqual(point1.y, 4)

        point2 = Point(8, 9)
        self.assertEqual(point2.x, 8)
        self.assertEqual(point2.y, 9)

    def test_point_inside(self):
        rect = Rect(2, 2, 5, 5)
        point1 = Point(1, 1)
        point2 = Point(8, 8)
        point3 = Point(4, 8)
        point4 = Point(8, 4)
        point5 = Point(3, 3)
        self.assertFalse(point1.is_inside(rect))
        self.assertFalse(point2.is_inside(rect))
        self.assertFalse(point3.is_inside(rect))
        self.assertFalse(point4.is_inside(rect))
        self.assertTrue(point5.is_inside(rect))


if __name__ == '__main__':
    unittest.main()
