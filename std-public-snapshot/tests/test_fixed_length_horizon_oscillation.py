import json
from pathlib import Path
import unittest

from experiments.fixed_length_horizon_oscillation import (
    ALLOWED,
    U,
    V,
    admissible,
    cyclic_blocks,
    exact_horizon_on_words,
    graph_components,
    literal_domain,
    predicted_domain,
    predicted_horizon,
    validation_packet,
)


DATA = (
    Path(__file__).resolve().parents[1]
    / "experiments/data/fixed_length_horizon_oscillation_2026-10-11.json"
)


class FixedLengthHorizonOscillation(unittest.TestCase):
    def test_allowed_graph_is_exactly_two_cycles(self):
        self.assertEqual(len(ALLOWED), 10)
        self.assertEqual(sorted(map(len, graph_components())), [4, 6])

    def test_literal_domain_matches_two_cycle_prediction_through_12(self):
        expected_counts = [0, 0, 0, 4, 0, 6, 0, 4, 0, 0, 0, 10]
        for n, count in enumerate(expected_counts, start=1):
            with self.subTest(length=n):
                actual = literal_domain(n)
                predicted = predicted_domain(n)
                self.assertEqual(actual, predicted)
                self.assertEqual(len(actual), count)
                self.assertEqual(exact_horizon_on_words(actual), predicted_horizon(n))

    def test_n12_exact_counterexample_and_n4_horizon_one(self):
        x, y = U * 3, V * 2
        self.assertTrue(admissible(x) and admissible(y))
        self.assertEqual(cyclic_blocks(x, 1), cyclic_blocks(y, 1))
        self.assertNotEqual(cyclic_blocks(x, 2), cyclic_blocks(y, 2))
        self.assertEqual(cyclic_blocks(x, 2)["01"], 3)
        self.assertEqual(cyclic_blocks(y, 2)["01"], 2)
        self.assertEqual(exact_horizon_on_words(predicted_domain(12)), 2)
        self.assertEqual(exact_horizon_on_words(predicted_domain(4)), 1)

    def test_formula_pattern_through_48(self):
        for n in range(1, 49):
            with self.subTest(length=n):
                words = predicted_domain(n)
                self.assertEqual(exact_horizon_on_words(words), predicted_horizon(n))
                if words:
                    self.assertEqual(predicted_horizon(n), 2 if n % 12 == 0 else 1)

    def test_validation_packet(self):
        packet = validation_packet()
        self.assertEqual(packet["graph_cycle_sizes"], [4, 6])
        self.assertEqual(
            [row["rooted_words"] for row in packet["brute_force_lengths_1_to_12"]],
            [0, 0, 0, 4, 0, 6, 0, 4, 0, 0, 0, 10],
        )

    def test_committed_packet_matches_regeneration_semantically(self):
        committed = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertEqual(committed, validation_packet())


if __name__ == "__main__":
    unittest.main()
