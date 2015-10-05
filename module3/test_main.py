import unittest
from main import Main


class TestMain(unittest.TestCase):
    lines = [
        '6 7',
        '6',
        '1 1',
        '1 1',
        '1 1',
        '1 2 1',
        '1 1',
        '2',
        '1 1',
        '1 4',
        '1 1 1',
        '1 1 1',
        '1 4',
        '1 1'
    ]

    def test_parse_lines(self):
        num_cols, num_rows, row_segments, col_segments = Main.parse_lines(self.lines)

        self.assertEqual(num_cols, 6)
        self.assertEqual(num_rows, 7)
        self.assertEqual(len(row_segments), 7)
        self.assertEqual(len(col_segments), 6)
        self.assertEqual(len(row_segments[1]), 2)
        self.assertEqual(len(col_segments[2]), 3)

if __name__ == '__main__':
    unittest.main()
