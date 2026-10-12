"""Finite property checks for recurrent higher-block irreducibility.

These tests support the graph proof; they are not a substitute for it.
"""
import itertools
import unittest

from std_tools.sft_closure import (
    allowed_blocks,
    recurrent_cyclic_edges,
    strongly_connected,
)


def binary_words(length):
    return ["".join(p) for p in itertools.product("01", repeat=length)]


def constituent_windows(word, length):
    return [word[i:i + length] for i in range(len(word) - length + 1)]


class RecurrentHigherBlockIrreducibility(unittest.TestCase):
    def test_named_periodic_self_loop_and_transient_cases(self):
        cases = [
            (2, {"01", "10"}),       # irreducible period-two core
            (2, {"00"}),             # one recurrent self-loop
            (2, {"00", "01"}),       # raw transient edge 01 trims away
        ]
        for m, allowed in cases:
            base = recurrent_cyclic_edges(
                allowed_blocks("01", allowed, m, m)
            )
            self.assertTrue(strongly_connected(base), (m, allowed, base))
            base_set = set(base)
            for L in range(m, 7):
                raw = allowed_blocks("01", allowed, m, L)
                recurrent = recurrent_cyclic_edges(raw)
                expected = {
                    w for w in raw
                    if all(x in base_set for x in constituent_windows(w, m))
                }
                self.assertEqual(set(recurrent), expected, (allowed, L))
                self.assertTrue(strongly_connected(recurrent), (allowed, L))

        # Explicit short-period wrapping boundary: period 2 < lifted length 6.
        self.assertEqual(
            set(recurrent_cyclic_edges(
                allowed_blocks("01", {"01", "10"}, 2, 6)
            )),
            {"010101", "101010"},
        )

    def test_all_small_binary_presentations(self):
        checks = 0
        for m in (1, 2, 3):
            blocks = binary_words(m)
            for mask in range(1 << len(blocks)):
                allowed = {
                    block for i, block in enumerate(blocks)
                    if mask & (1 << i)
                }
                for s in range(m, 5):
                    raw_s = allowed_blocks("01", allowed, m, s)
                    core_s = recurrent_cyclic_edges(raw_s)
                    if not core_s or not strongly_connected(core_s):
                        continue
                    core_set = set(core_s)

                    for L in range(s, 6):
                        raw_L = allowed_blocks("01", allowed, m, L)
                        core_L = recurrent_cyclic_edges(raw_L)
                        expected = {
                            w for w in raw_L
                            if all(x in core_set
                                   for x in constituent_windows(w, s))
                        }
                        self.assertEqual(
                            set(core_L), expected,
                            (m, tuple(sorted(allowed)), s, L),
                        )
                        self.assertTrue(
                            strongly_connected(core_L),
                            (m, tuple(sorted(allowed)), s, L),
                        )
                        checks += 1

        self.assertGreater(checks, 100)


if __name__ == "__main__":
    unittest.main()
