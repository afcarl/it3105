import unittest
from rect import Rect
from point import Point


class TestTwoDee(unittest.TestCase):
    def test_construct_point(self):
        point2 = Point(8, 9)
        self.assertEqual(point2.x, 8)
        self.assertEqual(point2.y, 9)

    def test_construct_rect_negative_width(self):
        with self.assertRaises(Exception):
            Rect(2, 3, -3, 5)

    def test_construct_rect(self):
        rect = Rect(2, 3, 4, 5)
        self.assertEqual(rect.x, 2)
        self.assertEqual(rect.y, 3)
        self.assertEqual(rect.width, 4)
        self.assertEqual(rect.height, 5)

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

    def test_border_tiles(self):
        rect = Rect(0, 0, 3, 3)
        border_tiles = rect.get_border_tiles()
        self.assertTrue((0, 0) in border_tiles)
        self.assertTrue((1, 0) in border_tiles)
        self.assertTrue((2, 0) in border_tiles)
        self.assertTrue((1, 0) in border_tiles)
        self.assertTrue((1, 2) in border_tiles)
        self.assertTrue((2, 0) in border_tiles)
        self.assertTrue((2, 1) in border_tiles)
        self.assertTrue((2, 2) in border_tiles)
        self.assertFalse((1, 1) in border_tiles)  # middle
        self.assertFalse((3, 1) in border_tiles)  # out of bounds

        rect = Rect(1, 7, 1, 2)
        border_tiles = rect.get_border_tiles()
        self.assertEqual(len(border_tiles), 2)


if __name__ == '__main__':
    unittest.main()
