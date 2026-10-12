"""Regression tests for the exact reducible-support worked example."""
import unittest
from collections import Counter
from fractions import Fraction

from experiments.reducible_support_example import (
    S_EDGES, T_EDGES, admissible, cyclic_counts, incidence_balance,
    output_histogram, projected_histogram, transform, verify_example,
)


class ReducibleSupportExample(unittest.TestCase):
    def test_rational_cross_support_point_and_integer_lift(self):
        alpha, beta = Fraction(3, 2), Fraction(3)
        x = {edge: alpha for edge in S_EDGES}
        y = {edge: beta for edge in T_EDGES}

        self.assertFalse(any(incidence_balance(S_EDGES, x).values()))
        self.assertFalse(any(incidence_balance(T_EDGES, y).values()))
        self.assertEqual(
            projected_histogram(S_EDGES, x, 1),
            projected_histogram(T_EDGES, y, 1),
        )
        self.assertEqual(output_histogram(S_EDGES, x)["a"], Fraction(6))
        self.assertEqual(output_histogram(T_EDGES, y)["a"], 0)

        # Common-denominator scaling by two gives exact Euler histograms.
        X, Y = "0011" * 3, "01" * 6
        self.assertEqual(
            cyclic_counts(X, 5),
            Counter({edge: 3 for edge in S_EDGES}),
        )
        self.assertEqual(
            cyclic_counts(Y, 5),
            Counter({edge: 6 for edge in T_EDGES}),
        )
        self.assertEqual(cyclic_counts(X, 1), cyclic_counts(Y, 1))
        self.assertNotEqual(
            cyclic_counts(transform(X), 1),
            cyclic_counts(transform(Y), 1),
        )

    def test_exact_horizon_two(self):
        X, Y = "0011", "0101"
        self.assertTrue(admissible(X))
        self.assertTrue(admissible(Y))

        # h=1 fails across recurrent components.
        self.assertEqual(
            cyclic_counts(X, 1),
            cyclic_counts(Y, 1),
        )
        self.assertNotEqual(
            cyclic_counts(transform(X), 1),
            cyclic_counts(transform(Y), 1),
        )

        # h=2 cross-component equality is impossible: S has a positive 00
        # coordinate while T has none. Within either simple cycle, a balanced
        # positive circulation is one scalar multiple, fixed by C2.
        self.assertEqual(cyclic_counts(X, 2)["00"], 1)
        self.assertEqual(cyclic_counts("01", 2)["00"], 0)
        self.assertEqual(
            cyclic_counts(X, 2),
            Counter({"00": 1, "01": 1, "11": 1, "10": 1}),
        )
        self.assertEqual(
            cyclic_counts("01", 2),
            Counter({"01": 1, "10": 1}),
        )

        report = verify_example()
        self.assertEqual(report["exact_horizon_k1"], 2)
        self.assertEqual(
            report["cross_support_h2_obstruction"],
            "P2(00)=alpha>=1 on S but 0 on T",
        )


if __name__ == "__main__":
    unittest.main()
