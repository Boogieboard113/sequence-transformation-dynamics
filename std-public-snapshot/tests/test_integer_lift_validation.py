"""Integer-only boundary regressions for support-pair witness lifts (issue #116)."""
from collections import Counter
from fractions import Fraction
from types import MappingProxyType
import unittest

from experiments.support_pair_certificates import (
    cyclic_counts,
    euler_circuit,
    source_from_circuit,
    verify_integer_pair,
)


class IntegerLiftValidation(unittest.TestCase):
    def test_euler_rejects_noninteger_counts_before_conversion(self):
        invalid = (
            True, False, 1.0, 1.9, 0.0, -0.0, -1.9,
            float("inf"), float("nan"), "2", "", None,
            Fraction(3, 2), Fraction(1), Fraction(0),
        )
        for value in invalid:
            with self.subTest(value=repr(value)):
                # A separate valid loop exposes zero/false values that the old
                # truthiness filter silently discarded before validation.
                with self.assertRaisesRegex(ValueError, "multiplicities must be integers"):
                    euler_circuit({"00": 1, "11": value})

    def test_euler_valid_integer_zeros_are_still_ignored(self):
        histogram = {"00": 2, "11": 0}
        self.assertEqual(euler_circuit(histogram), ("00", "00"))
        self.assertEqual(histogram, {"00": 2, "11": 0})

    def test_euler_accepts_readonly_mapping_and_keeps_deterministic_order(self):
        expected = ("00", "01", "10", "01", "11", "10")
        # Retain the deterministic traversal observed in the pinned source.
        histogram = {"00": 1, "01": 2, "10": 2, "11": 1}
        circuit = euler_circuit(MappingProxyType(histogram))
        self.assertEqual(Counter(circuit), Counter(histogram))
        self.assertEqual(circuit, euler_circuit(dict(reversed(list(histogram.items())))))
        self.assertEqual(circuit, expected)

    def test_euler_preserves_cyclic_histogram_for_short_source_period(self):
        for histogram, order in (({"0000": 1}, 4), ({"01010": 1, "10101": 1}, 5)):
            with self.subTest(histogram=histogram):
                word = source_from_circuit(euler_circuit(histogram))
                self.assertLess(len(word), order)
                self.assertEqual(cyclic_counts(word, order), Counter(histogram))

    def test_euler_retains_empty_negative_balance_and_connectivity_rejections(self):
        cases = (
            ({}, "nonempty and positive"),
            ({"00": 0}, "nonempty and positive"),
            ({"00": -1}, "nonempty and positive"),
            ({"01": 2, "10": 1}, "not balanced"),
            ({"00": 1, "11": 1}, "not strongly connected"),
        )
        for histogram, message in cases:
            with self.subTest(histogram=histogram):
                with self.assertRaisesRegex(ValueError, message):
                    euler_circuit(histogram)

    def test_integer_pair_rejects_noninteger_values_in_either_vector(self):
        for convert in (bool, float, str, Fraction):
            for side in ("S", "T"):
                with self.subTest(convert=convert.__name__, side=side):
                    x = dict(cyclic_counts("0011", 2))
                    y = dict(cyclic_counts("0101", 2))
                    if side == "S":
                        x = {edge: convert(value) for edge, value in x.items()}
                    else:
                        y = {edge: convert(value) for edge, value in y.items()}
                    with self.assertRaisesRegex(ValueError, "multiplicities must be integers"):
                        verify_integer_pair(x, y, 1, {"00": 1}, 1)

    def test_integer_pair_rejects_fractional_but_balanced_discrepancy(self):
        x = dict.fromkeys(("00", "01", "10", "11"), Fraction(3, 2))
        y = {"01": 3, "10": 3}
        with self.assertRaisesRegex(ValueError, "multiplicities must be integers"):
            verify_integer_pair(x, y, 1, {"00": 1}, 1)

    def test_integer_pair_rejects_invalid_values_before_arithmetic(self):
        for value in (False, 0.0, Fraction(0), None, float("nan"), float("inf")):
            for side in ("S", "T"):
                with self.subTest(value=repr(value), side=side):
                    x = dict(cyclic_counts("0011", 2))
                    y = dict(cyclic_counts("0101", 2))
                    (x if side == "S" else y)["11"] = value
                    with self.assertRaisesRegex(ValueError, "multiplicities must be integers"):
                        verify_integer_pair(x, y, 1, {"00": 1}, 1)

    def test_integer_pair_preserves_valid_exact_counts_and_rational_target(self):
        # Verification does not allocate expanded Euler walks: include counts
        # above binary64's exact-integer range to protect exact arithmetic.
        for scale in (1, 2**60 + 1):
            x = {edge: scale * count for edge, count in cyclic_counts("0011", 2).items()}
            y = {edge: scale * count for edge, count in cyclic_counts("0101", 2).items()}
            before_x, before_y = dict(x), dict(y)
            self.assertIsNone(verify_integer_pair(MappingProxyType(x), y, 1, {"00": Fraction(3, 2)}, 1))
            self.assertIsNone(verify_integer_pair(y, MappingProxyType(x), 1, {"00": 1}, -1))
            self.assertEqual(x, before_x)
            self.assertEqual(y, before_y)

    def test_integer_pair_retains_algebraic_rejections(self):
        x = dict(cyclic_counts("0011", 2))
        y = dict(cyclic_counts("0101", 2))
        cases = (
            ({**x, "11": 0}, y, 1, 1, "strict positivity"),
            ({**x, "01": 2}, y, 1, 1, "S integer vector is not balanced"),
            (x, {**y, "01": 3}, 1, 1, "T integer vector is not balanced"),
            ({**x, "00": 2}, y, 1, 1, "source projections differ"),
            (x, y, 2, 1, "source projections differ"),
            (x, y, 1, -1, "target discrepancy"),
        )
        for left, right, h, sign, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(AssertionError, message):
                    verify_integer_pair(left, right, h, {"00": 1}, sign)


if __name__ == "__main__":
    unittest.main()
