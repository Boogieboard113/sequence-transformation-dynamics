"""Regression cases for the October 10 STD reset-gap scope correction."""
import unittest
from itertools import product
from audits.reset_gap_adversarial import (
    Chart, exact_orbit_horizon, exact_all_run_horizon_under_global_reset,
    cyclic_histogram, curvature_witness, find_collision,
)


class TestResetGapScope(unittest.TestCase):
    def test_minimal_two_state_off_orbit_counterexample(self):
        chart = Chart((0, 1), (0, 1), (0, 0), (0, 1))
        self.assertEqual(chart.orbit(), (0, 1, (0,)))
        self.assertEqual(exact_orbit_horizon(chart), 1)
        self.assertEqual(chart.run('b', 0), 0)
        self.assertEqual(chart.run('b', 1), 1)
        for h in (1, 2, 3, 6, 11):
            self.assertEqual(cyclic_histogram('b', h), cyclic_histogram('b', h))
            self.assertIsNotNone(find_collision(chart, h, 1))
        self.assertIsNone(find_collision(chart, 2, 8, orbit_only=True))

    def test_finite_horizon_two(self):
        chart = Chart((1, 1), (0, 0), (0, 0), (0, 1))
        self.assertEqual(chart.orbit()[:2], (1, 1))
        self.assertEqual(exact_orbit_horizon(chart), 2)
        x, y, delta = curvature_witness(chart, 0)
        self.assertNotEqual(delta, 0)
        self.assertEqual(cyclic_histogram(x, 1), cyclic_histogram(y, 1))
        self.assertIsNotNone(find_collision(chart, 1, 4))
        self.assertIsNone(find_collision(chart, 2, 9))

    def test_finite_horizon_three(self):
        chart = Chart((1, 2, 2), (0, 0, 0), (0, 0, 0), (0, 0, 1))
        self.assertEqual(exact_orbit_horizon(chart), 3)
        x, y, delta = curvature_witness(chart, 1)
        self.assertNotEqual(delta, 0)
        for h in (1, 2):
            self.assertEqual(cyclic_histogram(x, h), cyclic_histogram(y, h))

    def test_periodic_residual_never_closes(self):
        chart = Chart((1, 0), (0, 0), (0, 1), (0, 0))
        self.assertIsNone(exact_orbit_horizon(chart))
        for h in range(1, 9):
            bad_n = next(n for n in range(h - 1, h + 2)
                         if curvature_witness(chart, n)[2] != 0)
            x, y, delta = curvature_witness(chart, bad_n)
            self.assertNotEqual(delta, 0)
            self.assertEqual(cyclic_histogram(x, h), cyclic_histogram(y, h))

    def test_domain_restricted_to_one_b_invalidates_necessity(self):
        chart = Chart((1, 0), (0, 0), (0, 1), (0, 0))
        self.assertIsNone(exact_orbit_horizon(chart))
        self.assertIsNone(find_collision(chart, 1, 10, exactly_one_b=True))

    def test_global_reset_does_not_protect_a_only_cycles(self):
        chart = Chart((0, 1), (0, 0), (0, 1), (0, 0))
        self.assertEqual(exact_orbit_horizon(chart), 1)
        self.assertIsNone(exact_all_run_horizon_under_global_reset(chart))
        self.assertEqual(chart.run('a', 0), 0)
        self.assertEqual(chart.run('a', 1), 1)
        self.assertIsNotNone(find_collision(chart, 1, 1, include_a_only=True))

    def test_global_reset_all_run_mean_condition(self):
        chart = Chart((0, 1), (0, 0), (2, 2), (0, 0))
        self.assertEqual(exact_all_run_horizon_under_global_reset(chart), 1)
        with self.assertRaises(ValueError):
            exact_all_run_horizon_under_global_reset(
                Chart((0, 1), (0, 1), (0, 0), (0, 0)))

    def test_nonreset_edge_on_orbit_rejected(self):
        with self.assertRaises(ValueError):
            exact_orbit_horizon(Chart((1, 1), (1, 0), (0, 0), (0, 0)))

    def test_small_exhaustive_global_reset_survey(self):
        # 64 two-state charts: 4 a-maps x 16 binary weight assignments.
        checked = 0
        for amap in product((0, 1), repeat=2):
            for weights in product((0, 1), repeat=4):
                chart = Chart(amap, (0, 0), weights[:2], weights[2:])
                h = exact_orbit_horizon(chart)
                checked += 1
                if h is not None:
                    self.assertLessEqual(h, 2)
                    self.assertIsNone(find_collision(chart, h, 7))
                    if h > 1:
                        self.assertIsNotNone(find_collision(chart, h-1, 7))
                else:
                    # An explicit curvature witness defeats each tested h.
                    for order in (1, 2, 3):
                        mu, period, _ = chart.orbit()
                        n = next(n for n in range(max(mu, order-1), max(mu, order-1)+period+1)
                                 if curvature_witness(chart, n)[2] != 0)
                        x, y, delta = curvature_witness(chart, n)
                        self.assertNotEqual(delta, 0)
                        self.assertEqual(cyclic_histogram(x, order), cyclic_histogram(y, order))
        self.assertEqual(checked, 64)

    def test_all_binary_weighted_three_state_charts(self):
        # Enumerate all 3^3 * 2^6 = 1,728 total b-reset charts.
        # Finite predictions are checked on every closed run through length 6.
        from collections import Counter
        counts = Counter()
        for amap in product(range(3), repeat=3):
            for weights in product((0, 1), repeat=6):
                chart = Chart(amap, (0, 0, 0), weights[:3], weights[3:])
                h = exact_all_run_horizon_under_global_reset(chart)
                counts[h] += 1
                if h is not None:
                    self.assertIsNone(find_collision(
                        chart, h, 6, include_a_only=True))
        self.assertEqual(dict(counts), {None: 808, 1: 588, 2: 252, 3: 80})


if __name__ == '__main__':
    unittest.main()
