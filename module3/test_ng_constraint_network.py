import unittest
from ng_constraint_network import NgConstraintNetwork


class TestConstraint(unittest.TestCase):
    def test_combinations(self):
        size = 10
        segments = (2, 1, 3)

        domains = NgConstraintNetwork.get_start_index_domains(size=size, segments=segments)
        self.assertEqual(domains, [[0, 1, 2], [3, 4, 5], [5, 6, 7]])

        combinations = NgConstraintNetwork.get_possible_combinations(size, segments, domains)
        self.assertEqual(
            set(combinations),
            {
                (1, 1, 0, 1, 0, 1, 1, 1, 0, 0),
                (1, 1, 0, 1, 0, 0, 1, 1, 1, 0),
                (1, 1, 0, 1, 0, 0, 0, 1, 1, 1),
                (1, 1, 0, 0, 1, 0, 1, 1, 1, 0),
                (1, 1, 0, 0, 1, 0, 0, 1, 1, 1),
                (1, 1, 0, 0, 0, 1, 0, 1, 1, 1),
                (0, 1, 1, 0, 1, 0, 1, 1, 1, 0),
                (0, 1, 1, 0, 1, 0, 0, 1, 1, 1),
                (0, 1, 1, 0, 0, 1, 0, 1, 1, 1),
                (0, 0, 1, 1, 0, 1, 0, 1, 1, 1)
            }
        )


if __name__ == '__main__':
    unittest.main()
