"""Independent exhaustive checks for deterministic cyclic corridor contraction.
Run: PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_structural_reduction.py' -v
"""
from collections import Counter, defaultdict
from itertools import product
from math import inf
import random
import unittest

from std_tools.structural_reduction import (
    all_attainable, cyclic_class, cyclic_erased_max, erased_max_from_reduction,
    erased_signature, exact_pattern_bounds, forbidden_from_reduction,
    forbidden_on_circle, forbidden_summary, join_forbidden, join_signatures, lift_edges,
    raw_histogram,
    reduce_histogram, reduced_circuits, source_from_edges,
)


def oracle_hist(word, h):
    doubled = word * (h // len(word) + 2)
    return Counter(doubled[i:i + h] for i in range(len(word)))


def oracle_run_max(edges, emission):
    flags = [emission[e] == '' for e in edges]
    if all(flags):
        return inf
    run = longest = 0
    for flag in flags * 2:
        run = run + 1 if flag else 0
        longest = max(longest, run)
    return min(longest, len(edges) - 1)


def oracle_output(word, h, emission):
    return ''.join(emission[''.join(word[(i + j) % len(word)]
                                     for j in range(h))]
                   for i in range(len(word)))


def oracle_sets(words, h, emission, cap=None):
    good = []
    for w in words:
        edges = [''.join(w[(i + j) % len(w)] for j in range(h))
                 for i in range(len(w))]
        if cap is None or oracle_run_max(edges, emission) <= cap:
            good.append(w)
    return ({cyclic_class(oracle_output(w, h, emission)) for w in good},
            {oracle_output(w, h, emission) for w in good})


def emission_maps(edge_types):
    edges = sorted(edge_types)
    rng = random.Random('STD-branch-C-2026-10-11')
    maps = []
    for j in range(6):
        choices = ['', 'x', 'xy', 'yxx']
        if j == 0:
            m = {e: 'x' for e in edges}
        elif j == 1:
            m = {e: '' if e[0] == '0' else 'yx' for e in edges}
        elif j == 2:
            m = {e: '' if e[-1] == '1' else 'xy' for e in edges}
        elif j == 3:
            m = {e: 'x' if e.count('1') % 2 else 'xy' for e in edges}
        else:
            m = {e: rng.choice(choices) for e in edges}
        maps.append(m)
    return maps


class TestReduction(unittest.TestCase):
    def test_small_all_binary_words_all_histograms(self):
        # Oracle is a direct enumeration of words, NOT a second graph traversal.
        # Group by histograms to compare *whole attainable output sets*.
        checks = 0
        for n in range(1, 9):
            for h in range(1, 4):
                grouped = defaultdict(list)
                for tup in product('01', repeat=n):
                    w = ''.join(tup)
                    hist = oracle_hist(w, h)
                    grouped[tuple(sorted(hist.items()))].append(w)
                for key, words in grouped.items():
                    red = reduce_histogram(dict(key))
                    self.assertNotEqual(red.kind, 'infeasible')
                    self.assertEqual(red.order, h)
                    for emission in emission_maps(dict(key)):
                        for cap in [None, 0, 1, 2, 3]:
                            cyc, rooted = oracle_sets(words, h, emission, cap)
                            self.assertEqual(all_attainable(red, emission, cap), cyc,
                                             (n, h, key, emission, cap, 'cyclic'))
                            self.assertEqual(all_attainable(red, emission, cap, rooted=True),
                                             rooted, (n, h, key, emission, cap, 'rooted'))
                            checks += 1
        self.assertGreater(checks, 1000)
        print('independent small-word theorem comparisons:', checks)

    def test_ternary_alphabet_and_windows_longer_than_word(self):
        # Covers h>n and directed graphs with greater branching diversity.
        checks = 0
        for n in range(1, 7):
            for h in range(1, 5):
                grouped = defaultdict(list)
                for tup in product('abc', repeat=n):
                    word = ''.join(tup)
                    grouped[tuple(sorted(oracle_hist(word, h).items()))].append(word)
                for key, words in grouped.items():
                    red = reduce_histogram(dict(key))
                    emission = {e: ['', 'y', 'xyx', 'zz'][sum(ord(ch) for ch in e) % 4]
                                for e, _ in key}
                    for cap in (None, 0, 1, 2):
                        oracle_cyclic, oracle_rooted = oracle_sets(words, h, emission, cap)
                        self.assertEqual(all_attainable(red, emission, cap), oracle_cyclic,
                                         ('ternary', n, h, key, cap))
                        self.assertEqual(all_attainable(red, emission, cap, True), oracle_rooted,
                                         ('ternary rooted', n, h, key, cap))
                        checks += 1
        self.assertGreater(checks, 2000)
        print('independent ternary word theorem comparisons:', checks)

    def test_all_small_histogram_vectors_including_unrealizable(self):
        # More adversarial than histograms sampled from existing words:
        # 0..2 for all h=2 and 3 binary edges, n<=7.
        checked = 0
        for h in (2, 3):
            edges = [''.join(p) for p in product('01', repeat=h)]
            words_by_hist = defaultdict(list)
            for n in range(1, 8):
                for tup in product('01', repeat=n):
                    w = ''.join(tup)
                    words_by_hist[tuple(sorted(oracle_hist(w, h).items()))].append(w)
            for counts in product(range(3), repeat=len(edges)):
                n = sum(counts)
                if n < 1 or n > 7:
                    continue
                key = tuple((e, c) for e, c in zip(edges, counts) if c)
                red = reduce_histogram(dict(key))
                expected = words_by_hist.get(key, [])
                self.assertEqual(red.kind != 'infeasible', bool(expected), (h, key))
                if expected:
                    maps = emission_maps(dict(key))
                    # Multi-letter emissions and erasing caps; check all feasible cases.
                    for m in maps[:3]:
                        for cap in (None, 0, 1, 2):
                            cyc, rooted = oracle_sets(expected, h, m, cap)
                            self.assertEqual(all_attainable(red, m, cap), cyc, (h, key, m, cap))
                            self.assertEqual(all_attainable(red, m, cap, True), rooted,
                                             (h, key, m, cap, 'rooted'))
                checked += 1
        self.assertGreater(checked, 2000)
        print('independent histogram feasibility comparisons:', checked)

    def test_real_corridor_sharing_and_lift(self):
        # Two predecessors merge into deterministic 0 and then return to branch.
        # Histogram from word chosen to guarantee branching and sharing.
        w = '0000101'
        red = reduce_histogram(oracle_hist(w, 3))
        self.assertEqual(red.kind, 'branched')
        self.assertEqual(sum(m.count for m in red.macros.values()), 5)
        self.assertEqual(red.macros['001'].path, ('001', '010'))
        self.assertEqual(red.macros['101'].path, ('101', '010'))
        for tour in reduced_circuits(red):
            edges = lift_edges(red, tour)
            self.assertEqual(oracle_hist(source_from_edges(red, edges), 3), red.histogram)

    def test_pure_cycle_not_removed(self):
        red = reduce_histogram({'01': 2, '10': 2})
        self.assertEqual(red.kind, 'cycle')
        self.assertEqual(red.copies, 2)
        self.assertEqual(all_attainable(red, {'01': 'a', '10': 'b'}), {'abab'})
        self.assertEqual(all_attainable(red, {'01': '', '10': ''}, erase_cap=2), set())

    def test_disconnected_imbalanced_and_empty(self):
        for x in ({'00': 1, '11': 1}, {'01': 1}, {}):
            red = reduce_histogram(x)
            self.assertEqual(red.kind, 'infeasible')
            self.assertEqual(all_attainable(red, {}), set())

    def test_cross_macro_cyclic_erasure_run(self):
        # One-erasing macro at each end can create a two-erasure cyclic run.
        red = reduce_histogram({'0': 2, '1': 2})
        self.assertEqual(red.kind, 'branched')
        emission = {'0': '', '1': 'x'}
        maxima = {erased_max_from_reduction(red, seq, emission) for seq in reduced_circuits(red)}
        self.assertEqual(maxima, {1, 2})
        self.assertEqual(all_attainable(red, emission, erase_cap=1), {'xx'})
        self.assertEqual(all_attainable(red, emission, erase_cap=0), set())

    def test_representative_source_cuts_not_all_output_cuts(self):
        red = reduce_histogram({'0': 1})
        emission = {'0': 'ab'}
        self.assertEqual(all_attainable(red, emission, rooted=True), {'ab'})
        self.assertEqual(all_attainable(red, emission), {'ab'})
        self.assertNotIn('ba', all_attainable(red, emission, rooted=True))

    def test_signature_monoid_random_independent(self):
        rng = random.Random(20261011)
        for _ in range(3000):
            flags = [rng.choice((False, True)) for _ in range(rng.randrange(1, 16))]
            i = rng.randrange(len(flags) + 1)
            j = rng.randrange(i, len(flags) + 1)
            left = erased_signature(flags[:i])
            middle = erased_signature(flags[i:j])
            right = erased_signature(flags[j:])
            self.assertEqual(join_signatures(join_signatures(left, middle), right),
                             join_signatures(left, join_signatures(middle, right)))
            self.assertEqual(join_signatures(join_signatures(left, middle), right),
                             erased_signature(flags))
            self.assertEqual(cyclic_erased_max(erased_signature(flags)),
                             oracle_run_max(list(range(len(flags))),
                                            {idx: '' if x else 'x' for idx, x in enumerate(flags)}))

    def test_exact_output_bounds_and_source_restriction(self):
        hist = {'00': 2, '01': 2, '10': 2}
        red = reduce_histogram(hist)
        emission = {'00': '0', '01': '0', '10': '1'}
        self.assertEqual(exact_pattern_bounds(red, emission, ('000', '001')),
                         {'000': (0, 1), '001': (1, 2)})
        self.assertEqual(all_attainable(red, emission,
                                        source_allowed=lambda w: '000' not in (w + w[:2])),
                         {'001001'})
        # A rooted domain is not necessarily closed under source rotation.
        one = reduce_histogram({'0': 1, '1': 1})
        self.assertEqual(all_attainable(one, {'0':'ab', '1':'c'}, rooted=True,
                                        source_allowed=lambda w: w.startswith('0')),
                         {'abc'})
        self.assertEqual(all_attainable(one, {'0':'ab', '1':'c'}, rooted=True,
                                        source_allowed=lambda w: w.startswith('1')),
                         {'cab'})

    def test_centered_rule_root_offset(self):
        # phi depends on the CENTER of an h=3 window; edge e_i spans i..i+2.
        # Its emission occurs at source site i+1, not site i.
        word = '010'
        red = reduce_histogram(oracle_hist(word, 3))
        emission = {e: ('a' if e[1] == '1' else 'b') for e in red.histogram}
        allowed = lambda x: x.startswith('0')
        expected = set()
        for i in range(len(word)):
            rooted = word[i:] + word[:i]
            if allowed(rooted):
                expected.add(''.join('a' if c == '1' else 'b' for c in rooted))
        self.assertEqual(all_attainable(red, emission, rooted=True,
                                        source_allowed=allowed, emission_lag=1), expected)
        self.assertEqual(expected, {'bab', 'bba'})

    def test_finite_type_source_domain_exact(self):
        # The direct oracle checks full cyclic source words and does not call
        # the finite-type monoid summary used by the structural reduction.
        tests = 0
        forbiddens = [('000',), ('101', '11'), ('0',), ('1001',), ('01',)]
        for n in range(1, 9):
            for h in (1, 2, 3):
                grouped = defaultdict(list)
                for tup in product('01', repeat=n):
                    w = ''.join(tup)
                    grouped[tuple(sorted(oracle_hist(w, h).items()))].append(w)
                for key, words in grouped.items():
                    red = reduce_histogram(dict(key))
                    emission = {e: '' if e[-1] == '0' else 'xy' for e, _ in key}
                    for forbidden in forbiddens:
                        direct = []
                        for w in words:
                            if not any(''.join(w[(i + j) % n] for j in range(len(f))) == f
                                       for f in forbidden for i in range(n)):
                                direct.append(w)
                        expected = {cyclic_class(oracle_output(w, h, emission)) for w in direct}
                        self.assertEqual(all_attainable(red, emission,
                                                        forbidden_blocks=forbidden),
                                         expected, (n, h, key, forbidden))
                        tests += 1
        print('finite-type cyclic restriction comparisons:', tests)
        self.assertGreater(tests, 700)

    def test_finite_type_signature_random_associativity(self):
        rng = random.Random(841)
        for _ in range(2500):
            w = ''.join(rng.choice('abc') for _ in range(rng.randrange(1, 20)))
            forbid = ('abc', 'b', 'caac', 'aa')
            a = rng.randrange(len(w) + 1)
            b = rng.randrange(a, len(w) + 1)
            x, y, z = (forbidden_summary(t, forbid)
                       for t in (w[:a], w[a:b], w[b:]))
            l = join_forbidden(join_forbidden(x, y, forbid), z, forbid)
            r = join_forbidden(x, join_forbidden(y, z, forbid), forbid)
            self.assertEqual(l, r)
            self.assertEqual(l, forbidden_summary(w, forbid))
            direct = any(''.join(w[(i + j) % len(w)] for j in range(len(f))) == f
                         for f in forbid for i in range(len(w)))
            self.assertEqual(forbidden_on_circle(l, forbid), direct)

    def test_input_validation(self):
        with self.assertRaises(ValueError):
            reduce_histogram({'00': 2, '010': 1})
        with self.assertRaises(ValueError):
            reduce_histogram({'00': -1})
        with self.assertRaises(ValueError):
            all_attainable(reduce_histogram({'0': 1}), {'0': 'x'}, -1)


if __name__ == '__main__':
    unittest.main()
