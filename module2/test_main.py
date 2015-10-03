import unittest
from main import Main


class TestMain(unittest.TestCase):
    lines1 = [
        '3 3',
        '0 2.5 1.5',
        '1 4.0 4.0',
        '2 5.5 1.5',
        '0 1',
        '0 2',
        '1 2'
    ]

    def test_parse_lines(self):
        num_vertices, num_edges, vertices, edges = Main.parse_lines(self.lines1)

        self.assertEqual(num_vertices, 3)
        self.assertEqual(num_edges, 3)
        self.assertEqual(len(vertices), 3)
        self.assertEqual(len(edges), 3)

if __name__ == '__main__':
    unittest.main()
