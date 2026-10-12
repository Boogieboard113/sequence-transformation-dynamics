import json
from pathlib import Path
import unittest
from fractions import Fraction

from experiments.irreducible_fractional_vertex_search import (
    ALL_EDGES,
    all_vertices,
    cyclic_blocks,
    scan,
    strongly_connected,
    strongly_connected_subsets,
)


FULL_E = ("000", "001", "010", "011", "100", "110")
PROPER_S = ("000", "001", "011", "100", "110")
PROPER_T = ("001", "010", "011", "100", "110")
DATA = (
    Path(__file__).resolve().parents[1]
    / "experiments/data/irreducible_fractional_vertex_search_2026-10-11.json"
)


class IrreducibleFractionalVertexSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = scan()

    def test_declared_ambient_domain_counts(self):
        self.assertEqual(
            self.packet["ambient_graph_counts"],
            {"1": 2, "2": 1, "3": 2, "4": 5, "5": 6, "6": 6},
        )
        self.assertEqual(len(strongly_connected_subsets(6)), 22)

    def test_complete_summary(self):
        summary = self.packet["summary"]
        self.assertEqual(summary["ambient_graphs"], 22)
        self.assertEqual(summary["unique_lp_instances"], 1594)
        self.assertEqual(summary["active_sets_tested"], 101536)
        self.assertEqual(summary["cap_hits"], 0)
        self.assertEqual(summary["feasible_vertices"], 244)
        self.assertEqual(summary["fractional_vertices"], 32)
        self.assertEqual(summary["minimum_fractional_ambient_edges"], 6)
        self.assertEqual(summary["maximum_vertex_denominator"], 2)
        self.assertEqual(summary["denominator_histogram"], {"1": 212, "2": 32})
        self.assertEqual(
            summary["fractional_support_size_histogram"],
            {"5,5": 4, "5,6": 4, "6,4": 4, "6,5": 12, "6,6": 8},
        )

    def test_by_ambient_size(self):
        expected = {
            "1": {"instances": 2, "active_sets": 6, "vertices": 0,
                  "fractional_vertices": 0, "cap_hits": 0},
            "2": {"instances": 2, "active_sets": 10, "vertices": 0,
                  "fractional_vertices": 0, "cap_hits": 0},
            "3": {"instances": 6, "active_sets": 42, "vertices": 0,
                  "fractional_vertices": 0, "cap_hits": 0},
            "4": {"instances": 130, "active_sets": 1142, "vertices": 0,
                  "fractional_vertices": 0, "cap_hits": 0},
            "5": {"instances": 374, "active_sets": 12952, "vertices": 32,
                  "fractional_vertices": 0, "cap_hits": 0},
            "6": {"instances": 1080, "active_sets": 87384, "vertices": 212,
                  "fractional_vertices": 32, "cap_hits": 0},
        }
        self.assertEqual(self.packet["by_ambient_size"], expected)

    def test_full_support_representative_original_lp(self):
        result = all_vertices(FULL_E, FULL_E, "000")
        expected = (
            Fraction(2), Fraction(5, 2), Fraction(1), Fraction(3, 2),
            Fraction(5, 2), Fraction(3, 2),
            Fraction(1), Fraction(3), Fraction(2), Fraction(1),
            Fraction(3), Fraction(1),
        )
        self.assertEqual(result["status"], "OK")
        self.assertEqual(result["active_sets"], 715)
        self.assertEqual(result["vertices"], (expected,))
        record = self.packet["full_support_representative"]
        self.assertEqual(record["denominator"], 2)
        self.assertEqual(record["active_certificate"]["rank_without_target"], 11)
        self.assertEqual(record["active_certificate"]["rank_with_target_if_tight"], 12)
        self.assertEqual(record["integer_lift"]["length"], 22)
        self.assertEqual(record["literal_shortest_through_14"]["length"], 14)

    def test_proper_support_fractional_representative(self):
        result = all_vertices(PROPER_S, PROPER_T, "000")
        expected = (
            Fraction(1), Fraction(3, 2), Fraction(3, 2),
            Fraction(3, 2), Fraction(3, 2),
            Fraction(2), Fraction(1), Fraction(1), Fraction(2), Fraction(1),
        )
        self.assertIn(expected, result["vertices"])
        record = self.packet["proper_support_representative"]
        self.assertEqual(tuple(record["S"]), PROPER_S)
        self.assertEqual(tuple(record["T"]), PROPER_T)
        self.assertEqual(record["denominator"], 2)
        self.assertEqual(record["active_certificate"]["rank_without_target"], 10)
        self.assertEqual(record["integer_lift"]["length"], 14)
        self.assertEqual(record["literal_shortest_through_14"]["length"], 10)
        self.assertEqual(record["literal_shortest_through_14"]["target_counts"], [2, 0])

    def test_short_period_wrapping_is_literal(self):
        self.assertTrue(strongly_connected(("000",)))
        self.assertEqual(cyclic_blocks("0", 3), {"000": 1})
        self.assertEqual(cyclic_blocks("01", 3), {"010": 1, "101": 1})
        self.assertEqual(set(ALL_EDGES), {
            "000", "001", "010", "011", "100", "101", "110", "111"
        })

    def test_committed_packet_matches_full_regeneration(self):
        committed = json.loads(DATA.read_text(encoding="utf-8"))
        self.assertEqual(committed, self.packet)


if __name__ == "__main__":
    unittest.main()
