import unittest
from fractions import Fraction

from experiments.rational_fourier_motzkin import (
    equality_inequalities,
    feasible_point,
    satisfies,
)


class RationalFourierMotzkin(unittest.TestCase):
    def test_one_sided_lower_bound(self):
        system = [((-1,), -1)]  # x >= 1
        point = feasible_point(system, 1)
        self.assertIsNotNone(point)
        self.assertGreaterEqual(point[0], 1)
        self.assertTrue(satisfies(point, system))

    def test_one_sided_upper_bound(self):
        system = [((1,), -2)]  # x <= -2
        point = feasible_point(system, 1)
        self.assertIsNotNone(point)
        self.assertLessEqual(point[0], -2)

    def test_contradictory_bounds(self):
        self.assertIsNone(
            feasible_point([((-1,), -1), ((1,), 0)], 1)
        )

    def test_contradictory_equality_and_support_positivity(self):
        system = equality_inequalities([((1,), 0)])
        system.append(((-1,), -1))  # x >= 1
        self.assertIsNone(feasible_point(system, 1))

    def test_exact_equality_and_redundancy(self):
        system = equality_inequalities([((1, -1), 0)])
        system += [
            ((-1, 0), -1),  # x >= 1
            ((0, -1), -1),  # y >= 1
            ((2, -2), 0),   # redundant equality direction
            ((1, -1), 0),
        ]
        point = feasible_point(system, 2)
        self.assertIsNotNone(point)
        self.assertEqual(point[0], point[1])
        self.assertGreaterEqual(point[0], 1)
        self.assertTrue(satisfies(point, system))

    def test_nontrivial_rational_witness(self):
        system = [
            ((1, 1), 3),    # x+y <= 3
            ((-1, 0), -1),  # x >= 1
            ((0, -1), -1),  # y >= 1
        ]
        point = feasible_point(system, 2)
        self.assertIsNotNone(point)
        self.assertTrue(satisfies(point, system))
        self.assertTrue(any(value.denominator > 1 for value in point))

    def test_zero_variable_systems(self):
        self.assertEqual(feasible_point([], 0), ())
        self.assertIsNone(feasible_point([((), -1)], 0))

    def test_invalid_shapes_and_caps(self):
        with self.assertRaises(ValueError):
            feasible_point([((1, 2), 0)], 1)
        with self.assertRaises(ValueError):
            feasible_point([], -1)
        with self.assertRaises(ValueError):
            feasible_point([], 0, max_constraints=0)

    def test_constraint_cap_is_not_infeasibility(self):
        # Eliminating x from two upper and two lower bounds creates four pairs.
        system = [
            ((1, 1), 10),
            ((1, -1), 10),
            ((-1, 1), 10),
            ((-1, -1), 10),
        ]
        with self.assertRaises(RuntimeError):
            feasible_point(system, 2, max_constraints=3)


if __name__ == "__main__":
    unittest.main()
