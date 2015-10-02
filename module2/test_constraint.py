import unittest
from constraint_network import Constraint, ConstraintNetwork


class TestConstraint(unittest.TestCase):
    def test_constraint_methods(self):
        constraint = Constraint(
            name="c1",
            variables=['x', 'y', 'z'],
            expression='x + y > 2 * z'
        )

        self.assertTrue(constraint.is_satisfied(**{
            'x': 10,
            'y': 20,
            'z': 3
        }))
        self.assertFalse(constraint.is_satisfied(**{
            'x': 1,
            'y': 2,
            'z': 3
        }))

        # test with normal args, not keyword args
        self.assertTrue(constraint.is_satisfied(
            *(
                10,
                20,
                3
            )
        ))
        self.assertFalse(constraint.is_satisfied(
            *(
                1,
                2,
                3
            )
        ))

        # test variables passed in a different order
        self.assertTrue(constraint.is_satisfied(**{
            'z': 3,
            'y': 20,
            'x': 10
        }))
        self.assertFalse(constraint.is_satisfied(**{
            'z': 3,
            'y': 2,
            'x': 1
        }))

        with self.assertRaises(TypeError):
            self.assertFalse(constraint.is_satisfied(**{
                'x': 1,
                'y': 2
            }))

        self.assertTrue(constraint.has_input_variable('x'))
        self.assertFalse(constraint.has_input_variable('u'))

        self.assertEquals(
            constraint.get_variables_except_focal_variable('y'),
            ['x', 'z']
        )


class TestConstraintNetwork(unittest.TestCase):
    def test_constraint_network(self):
        constraint_network = ConstraintNetwork(
            constraints={
                "c1": Constraint(
                    name="c1",
                    variables=['x', 'y'],
                    expression='x > y'
                ),
                "c2": Constraint(
                    name="c2",
                    variables=['x', 'y', 'z'],
                    expression='x + y > z'
                ),
                "c3": Constraint(
                    name="c3",
                    variables=['y', 'z'],
                    expression='y > z + 1'
                )
            },
            domains={
                "x": {0, 1, 2, 3},
                "y": {0, 1, 2, 3, 4, 5},
                "z": {4, 5, 6, 7}
            }
        )

        self.assertEquals(
            constraint_network.get_constraints_by_variable_except_current_constraint(
                'x',
                constraint_network.constraints['c1']
            ),
            {constraint_network.constraints['c2']}
        )


if __name__ == '__main__':
    unittest.main()
