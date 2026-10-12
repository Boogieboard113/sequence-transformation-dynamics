"""Finite adversarial tests: these complement, not replace, the proofs."""
import itertools
import unittest
from collections import Counter

from std_tools import cyclic_block_counts
from std_tools.sft_closure import (allowed_blocks, emission_rows,
    exact_horizon_irreducible, naive_global_rank_test, recurrent_cyclic_edges,
    silent_run_bound, strongly_connected)


def admissible(word, allowed_m, m):
    return all(''.join(word[(i + j) % len(word)] for j in range(m)) in allowed_m
               for i in range(len(word)))


def transform(word, radius, emit):
    return ''.join(emit(''.join(word[(i + j - radius) % len(word)]
                                 for j in range(2 * radius + 1)))
                   for i in range(len(word)))


class SftHorizon(unittest.TestCase):
    def test_full_shift_identity_pair_needs_two(self):
        self.assertEqual(exact_horizon_irreducible('01', {'0','1'}, 1,
                         0, lambda w: w, 2), 2)

    def test_no_00_identity_pair_needs_one_but_triples_three(self):
        allowed = {'01', '10', '11'}
        self.assertEqual(exact_horizon_irreducible('01', allowed, 2, 0,
                         lambda w: w, 2), 1)
        self.assertEqual(exact_horizon_irreducible('01', allowed, 2, 0,
                         lambda w: w, 3), 3)

    def test_no_00_bounded_erasures(self):
        allowed = {'01', '10', '11'}
        emit = lambda w: '' if w == '0' else 'x'
        s = 2
        base = allowed_blocks('01', allowed, 2, s)
        self.assertEqual(silent_run_bound(base, lambda w: emit(w[:1])), 1)
        self.assertEqual(exact_horizon_irreducible('01', allowed, 2, 0, emit, 3), 1)

    def test_silent_loop_needs_scope_exception(self):
        with self.assertRaises(NotImplementedError):
            exact_horizon_irreducible('01', {'0','1'}, 1, 0,
                                      lambda w: '' if w == '0' else 'x', 2)
        # Output single-letter counts are still locally additive even here.
        self.assertEqual(exact_horizon_irreducible('01', {'0','1'}, 1, 0,
                         lambda w: '' if w == '0' else 'x', 1), 1)

    def test_transient_allowed_edge_trimmed_from_cyclic_domain(self):
        # Issue #7: 01 is linearly allowed but lies on no directed cycle.
        # Every admissible cyclic source is therefore 0^n.
        raw = allowed_blocks('01', {'00', '01'}, 2, 2)
        self.assertEqual(raw, ['00', '01'])
        self.assertEqual(recurrent_cyclic_edges(raw), ['00'])
        self.assertEqual(exact_horizon_irreducible(
            '01', {'00', '01'}, 2, 0, lambda w: w, 1), 1)
        # Higher-block trimming must also remove transient extensions.
        self.assertEqual(exact_horizon_irreducible(
            '01', {'00', '01'}, 2, 0, lambda w: w, 2), 1)

    def test_empty_and_reducible_recurrent_cyclic_domains_are_explicit(self):
        # A nonempty linearly allowed graph need not contain any cyclic source.
        with self.assertRaisesRegex(ValueError, "empty cyclic domain"):
            exact_horizon_irreducible(
                '01', {'01'}, 2, 0, lambda w: w, 1)

        # Trimming 01 still leaves two recurrent SCCs, 00 and 11. The
        # irreducible solver must reject this rather than solve SCCs separately:
        # equal source histograms may require cross-support comparison.
        with self.assertRaisesRegex(ValueError, "cross-support compatibility"):
            exact_horizon_irreducible(
                '01', {'00', '01', '11'}, 2, 0, lambda w: w, 1)

    def test_additive_window_identity_short_periods(self):
        allowed = {'01','10','11'}
        emit = lambda w: {'0':'', '1':'a', '2':'b'}[w]
        allowed3 = {a+b for a in '012' for b in '012' if a+b != '00'}
        r, k, m, R = 0, 2, 2, 1
        L = m + (k - 1)*(R + 1)
        edges = allowed_blocks('012', allowed3, m, L)
        F = emission_rows(edges, r, k, R, emit)
        for n in range(1, 8):
            for letters in itertools.product('012', repeat=n):
                w = ''.join(letters)
                if not admissible(w, allowed3, m):
                    continue
                out = transform(w, r, emit)
                direct = cyclic_block_counts(out, k)
                predicted = Counter()
                for start in range(n):
                    e = ''.join(w[(start+j)%n] for j in range(L))
                    col = edges.index(e)
                    for b, row in F.items():
                        predicted[tuple(b)] += row[col]
                self.assertEqual({b:v for b,v in predicted.items() if v}, dict(direct), (w,out))

    def test_radius_one_emissions_with_cyclic_wrap(self):
        # Centered radius-one rule with 0 erased and variable-length output.
        alphabet, m, r, k = '01', 3, 1, 3
        allowed = {''.join(p) for p in itertools.product(alphabet, repeat=m)} - {'000'}
        emit = lambda w: '' if w[1] == '0' else ('ab' if w[0] == '0' else 'b')
        base = allowed_blocks(alphabet, allowed, m, m)
        R = silent_run_bound(base, lambda w: emit(w))
        self.assertEqual(R, 2)
        L = m + (k - 1) * (R + 1)
        edges = allowed_blocks(alphabet, allowed, m, L)
        columns = {w:i for i,w in enumerate(edges)}
        F = emission_rows(edges, r, k, R, emit)
        for n in range(1, 10):
            for letters in itertools.product(alphabet, repeat=n):
                w = ''.join(letters)
                if not admissible(w, allowed, m):
                    continue
                direct = cyclic_block_counts(transform(w, r, emit), k)
                predicted = Counter()
                for start in range(n):
                    e = ''.join(w[(start + j) % n] for j in range(L))
                    col = columns[e]
                    for b, row in F.items():
                        predicted[tuple(b)] += row[col]
                self.assertEqual({b:v for b,v in predicted.items() if v}, dict(direct), w)
        self.assertEqual(exact_horizon_irreducible(alphabet, allowed, m, r, emit, k), 3)

    def test_reducible_rank_false_but_h1_sufficient(self):
        cycles = ('0001','0011','0111')
        orbit_blocks = []
        for p in cycles:
            orbit_blocks.append({''.join(p[(i+j)%4] for j in range(5)) for i in range(4)})
        allowed = set.union(*orbit_blocks)
        edges = allowed_blocks('01', allowed, 5, 5)
        self.assertEqual(len(edges), 12)
        self.assertFalse(strongly_connected(edges))
        output_b = [int(w in orbit_blocks[1]) for w in edges]
        self.assertFalse(naive_global_rank_test(edges, 1, [output_b]))
        # Every legal cyclic word is a power of precisely one of the three
        # primitive cycles. Their 1-count rays (3,1),(2,2),(1,3) are distinct;
        # equal C1 thus implies same orbit and same power, hence equal output.
        seen = {}
        for n in range(1, 17):
            for p in cycles:
                if n % len(p):
                    continue
                w = p*(n//len(p))
                c1 = frozenset(cyclic_block_counts(w,1).items())
                emission = 'b' if p == '0011' else 'a'
                out1 = cyclic_block_counts(emission*n,1)
                if c1 in seen:
                    self.assertEqual(seen[c1],out1)
                seen[c1] = out1
        self.assertEqual(len(seen), 12)


if __name__ == '__main__':
    unittest.main()
