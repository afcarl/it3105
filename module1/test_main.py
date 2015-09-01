import unittest
from main import Main


class TestMain(unittest.TestCase):
    lines1 = [
        '(6,9)',
        '(1,0) (5,5)',
        '(3,2,2,2)',
        '(0,3,1,3)',
        '(2,0,4,2)',
        '(2,5,2,1)'
    ]

    def test_parse_lines(self):
        dimensions, start, goal, barriers = Main.parse_lines(self.lines1)
        self.assertEqual(dimensions.width, 6)
        self.assertEqual(dimensions.height, 9)
        self.assertEqual(start.x, 1)
        self.assertEqual(start.y, 0)
        self.assertEqual(goal.x, 5)
        self.assertEqual(goal.y, 5)
        self.assertEqual(len(barriers), 4)
        self.assertEqual(barriers[0].x, 3)
        self.assertEqual(barriers[0].y, 2)
        self.assertEqual(barriers[0].width, 2)
        self.assertEqual(barriers[0].height, 2)
        self.assertEqual(barriers[1].x, 0)
        self.assertEqual(barriers[1].y, 3)
        self.assertEqual(barriers[1].width, 1)
        self.assertEqual(barriers[1].height, 3)

if __name__ == '__main__':
    unittest.main()
