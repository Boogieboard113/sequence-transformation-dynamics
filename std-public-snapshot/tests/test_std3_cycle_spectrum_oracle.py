"""Focused independent-oracle regressions for STD3 Engineering issue #108."""
import hashlib
import json
from pathlib import Path
import sys
import unittest
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from std3_cycle_spectrum_oracle import (  # noqa: E402
    FIXTURES, allowed_words, candidate_horizon, counts_via_padding,
    direct_admissible, direct_horizon, negative_regressions, recurrent_cycles,
    rooted_domain, rule_table, run_experiments, transform_literal, windows_modulo,
)

DATA = ROOT / "experiments/data/std3_cycle_spectrum_oracle_2026-10-11.json"


def fixture(name):
    return next(f for f in FIXTURES if f["name"] == name)


class Std3LiteralOracleTests(unittest.TestCase):
    def test_periodic_wrap_is_raw_even_for_short_periods(self):
        self.assertEqual(Counter(windows_modulo("01", 3)), {"010": 1, "101": 1})
        self.assertEqual(Counter(windows_modulo("0", 7)), {"0000000": 1})
        for word in ("0", "01", "0011", "000111"):
            for order in range(1, 10):
                self.assertEqual(Counter(windows_modulo(word, order)),
                                 counts_via_padding(word, order))

    def test_accepted_pr100_example_reconstructed_without_checker(self):
        f = fixture("pr100_identity")
        allowed = allowed_words(f)
        counts = [len(rooted_domain("01", allowed, 7, n)) for n in range(1, 13)]
        self.assertEqual(counts, [0, 0, 0, 4, 0, 6, 0, 4, 0, 0, 0, 10])
        table = rule_table("01", 0, "identity")
        words = rooted_domain("01", allowed, 7, 12)
        horizon, failure = direct_horizon(words, 0, table, 2, 7)
        self.assertEqual(horizon, 2)
        self.assertEqual(failure["h"], 1)
        self.assertEqual(Counter(windows_modulo(failure["left"], 1)),
                         Counter(windows_modulo(failure["right"], 1)))
        self.assertNotEqual(Counter(windows_modulo(failure["left"], 2)),
                            Counter(windows_modulo(failure["right"], 2)))
        x, y = "0011" * 3, "000111" * 2
        self.assertTrue(direct_admissible(x, set(allowed), 7))
        self.assertTrue(direct_admissible(y, set(allowed), 7))
        self.assertEqual(Counter(windows_modulo(x, 1)), {"0": 6, "1": 6})
        self.assertEqual(Counter(windows_modulo(y, 1)), {"0": 6, "1": 6})
        self.assertEqual(Counter(windows_modulo(x, 2))["01"], 3)
        self.assertEqual(Counter(windows_modulo(y, 2))["01"], 2)

    def test_separation_only_at_order_three(self):
        f = fixture("higher_order_separation")
        a, b = f["seeds"]
        self.assertEqual(Counter(windows_modulo(a, 2)),
                         Counter(windows_modulo(b, 2)))
        self.assertNotEqual(Counter(windows_modulo(a, 3)),
                            Counter(windows_modulo(b, 3)))
        allowed = allowed_words(f)
        cycles, recurrent = recurrent_cycles(allowed, "01", 7)
        self.assertEqual(len(recurrent), 14)
        words = rooted_domain("01", allowed, 7, 7)
        self.assertEqual(len(words), 14)
        table = rule_table("01", 0, "identity")
        for k, expected in ((1, 1), (2, 1), (3, 3), (4, 3)):
            self.assertEqual(direct_horizon(words, 0, table, k, 7)[0], expected)
            self.assertEqual(candidate_horizon(cycles, 7, 0, table, k, 7), expected)
        # The tempting unconditional H<=2 shortcut is false even here.
        self.assertNotEqual(direct_horizon(words, 0, table, 3, 7)[0], 2)

    def test_short_period_contexts_and_unequal_emissions(self):
        f = fixture("short_period_radius_two")
        table = rule_table("01", 2, f["rule"])
        self.assertEqual(len(table), 32)  # all binary 5-letter contexts
        self.assertEqual(transform_literal("1", 2, table), "00")
        self.assertEqual(transform_literal("11", 2, table), "0000")
        self.assertEqual(Counter(windows_modulo(transform_literal("1", 2, table), 3)),
                         {"000": 2})
        for n in (1, 2):
            words = rooted_domain("01", allowed_words(f), 3, n)
            self.assertEqual(words, ["1" * n])
        g = fixture("binary_variable_emission")
        phi = rule_table("01", 1, g["rule"])
        self.assertEqual(transform_literal("0011", 1, phi), "001111")
        self.assertEqual(transform_literal("01", 1, phi), "011")
        self.assertEqual(transform_literal("10", 1, phi), "110")
        self.assertEqual(transform_literal("00110011", 1, phi), "001111001111")
        allowed = allowed_words(g)
        self.assertEqual(direct_horizon(rooted_domain("01", allowed, 4, 4),
                                        1, phi, 2, 4)[0], 2)

    def test_transient_edge_is_not_in_recurrent_cycle_support(self):
        f = fixture("transient_noncyclic_edge")
        cycles, recurrent = recurrent_cycles(allowed_words(f), "01", 2)
        self.assertEqual(recurrent, ("00", "11"))
        self.assertEqual([c["period"] for c in cycles], [1, 1])
        self.assertEqual(rooted_domain("01", allowed_words(f), 2, 3),
                         ["000", "111"])

    def test_negative_preconditions_and_erasure(self):
        failures = negative_regressions()
        self.assertEqual(len(failures), 6)
        self.assertTrue(all(f["precondition"] == "REJECTED" for f in failures))
        with self.assertRaisesRegex(ValueError, "simple directed cycles"):
            recurrent_cycles(("00", "01", "10"), "01", 2)
        self.assertTrue(direct_admissible("001", {"00", "01", "10"}, 2))
        with self.assertRaises(ValueError):
            transform_literal("0", 0, {"0": ""})

    def test_committed_packet_full_regeneration(self):
        expected = DATA.read_bytes()
        actual = (json.dumps(run_experiments(), sort_keys=True, indent=2) + "\n").encode()
        self.assertEqual(hashlib.sha256(actual).digest(),
                         hashlib.sha256(expected).digest())
        self.assertEqual(actual, expected)
        packet = json.loads(expected)
        self.assertEqual(packet["totals"]["disagreements"], 0)
        self.assertEqual(packet["totals"]["nonempty_horizon_checks"], 160)
        self.assertEqual(packet["totals"]["all_horizon_checks"], 260)


if __name__ == "__main__":
    unittest.main()
