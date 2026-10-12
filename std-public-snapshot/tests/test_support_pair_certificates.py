import unittest
from collections import Counter

from experiments.support_pair_certificates import (
    cyclic_counts,
    euler_supports,
    find_certificate,
    make_certificate,
)


S = ("00110", "01100", "11001", "10011")
T = ("01010", "10101")
PR25_EDGES = S + T
PR25_A_ROW = {edge: int(edge in S) for edge in PR25_EDGES}


def pr25_emit(context):
    return "b" if context in T else "a"


def pr25_transform(word):
    n = len(word)
    return "".join(
        pr25_emit("".join(word[(i + j - 2) % n] for j in range(5)))
        for i in range(n)
    )


class SupportPairCertificates(unittest.TestCase):
    def test_pr25_support_enumeration_exact(self):
        self.assertEqual(set(euler_supports(PR25_EDGES)), {tuple(sorted(S)), tuple(sorted(T))})

    def test_pr25_h1_certificate_and_literal_outputs(self):
        certificate, stats = find_certificate(
            PR25_EDGES,
            1,
            {"a": PR25_A_ROW},
            force_nonintegral_demo=True,
        )
        self.assertIsNotNone(certificate)
        self.assertEqual(stats["supports"], 2)
        self.assertTrue(
            any(value.denominator > 1 for _, value in certificate.rational_s + certificate.rational_t)
        )
        self.assertGreater(certificate.scale, 1)
        self.assertEqual(cyclic_counts(certificate.source_s, 1), cyclic_counts(certificate.source_t, 1))
        self.assertNotEqual(
            cyclic_counts(pr25_transform(certificate.source_s), 1),
            cyclic_counts(pr25_transform(certificate.source_t), 1),
        )

    def test_pr25_h2_is_infeasible(self):
        certificate, stats = find_certificate(PR25_EDGES, 2, {"a": PR25_A_ROW})
        self.assertIsNone(certificate)
        self.assertEqual(stats["lp_instances"], 8)  # 2x2 support pairs x 1 row x 2 signs

    def test_full_binary_bigrams_exercise_proper_subsupports(self):
        edges = ("00", "01", "10", "11")
        supports = set(euler_supports(edges))
        self.assertIn(("00",), supports)
        self.assertIn(("11",), supports)
        self.assertIn(("01", "10"), supports)
        self.assertIn(tuple(edges), supports)
        self.assertGreater(len(supports), 4)

        # One output symbol b is emitted exactly at source bigram 00.
        row = {edge: int(edge == "00") for edge in edges}
        certificate, stats = find_certificate(edges, 1, {"b": row})
        self.assertIsNotNone(certificate)
        self.assertGreater(stats["supports"], 1)
        self.assertEqual(cyclic_counts(certificate.source_s, 1), cyclic_counts(certificate.source_t, 1))
        self.assertNotEqual(cyclic_counts(certificate.source_s, 2)["00"], cyclic_counts(certificate.source_t, 2)["00"])

        certificate2, stats2 = find_certificate(edges, 2, {"b": row})
        self.assertIsNone(certificate2)
        self.assertGreater(stats2["lp_instances"], 0)

    def test_edge_cap_is_loud(self):
        edges = tuple(f"{i:02d}" for i in range(9))
        with self.assertRaises(ValueError):
            euler_supports(edges, max_edges=8)


if __name__ == "__main__":
    unittest.main()
