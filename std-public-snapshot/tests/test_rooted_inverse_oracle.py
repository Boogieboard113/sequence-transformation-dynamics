import unittest

from experiments.rooted_inverse_oracle import (
    count_output_rotation_equivalent,
    count_rooted_preimages,
    emit_rooted,
    enumerate_rooted_preimages,
    run_validation,
)


class TestRootedInverseOracle(unittest.TestCase):
    def test_deletion_multiple_preimages(self):
        rule = {"0": "", "1": "1"}
        self.assertEqual(
            enumerate_rooted_preimages(("0", "1"), 0, rule, "11", (4,)),
            ("0011", "0101", "0110", "1001", "1010", "1100"),
        )

    def test_zero_preimage(self):
        rule = {"0": "", "1": "1"}
        self.assertEqual(count_rooted_preimages(("0", "1"), 0, rule, "11111", (4,)), 0)

    def test_all_erasing_rule_counts_words(self):
        rule = {"0": "", "1": ""}
        self.assertEqual(count_rooted_preimages(("0", "1"), 0, rule, "", (3,)), 8)
        self.assertEqual(count_rooted_preimages(("0", "1"), 0, rule, "0", (3,)), 0)

    def test_contextual_erasure_and_short_periods(self):
        alphabet = ("0", "1")
        rule = {
            "000": "0", "001": "0", "010": "", "011": "1",
            "100": "0", "101": "0", "110": "1", "111": "1",
        }
        self.assertEqual(emit_rooted("0", alphabet, 1, rule), "0")
        self.assertEqual(emit_rooted("01", alphabet, 1, rule), "0")
        self.assertEqual(emit_rooted("10", alphabet, 1, rule), "0")
        self.assertEqual(
            enumerate_rooted_preimages(alphabet, 1, rule, "0", (1, 2, 3, 4, 5, 6, 7, 8)),
            ("0", "01", "10"),
        )

    def test_rooted_cut_is_not_output_necklace(self):
        rule = {"a": "a", "b": "b"}
        rooted = count_rooted_preimages(("a", "b"), 0, rule, "ab", (2,))
        rotated = count_output_rotation_equivalent(("a", "b"), 0, rule, "ab", (2,))
        self.assertEqual(rooted, 1)
        self.assertEqual(rotated, 2)

    def test_validation_packet(self):
        result = run_validation()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["coverage"]["total_asserted_cases"], 1325)

    def test_rejects_empty_source_length_domain(self):
        rule = {"0": "0", "1": "1"}
        with self.assertRaises(ValueError):
            count_rooted_preimages(("0", "1"), 0, rule, "", (0,))


if __name__ == "__main__":
    unittest.main()
