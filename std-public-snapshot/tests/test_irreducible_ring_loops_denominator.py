"""Issue #83: exact bounded checks for an analytic irreducible denominator family.

These are supporting tests, not a universal proof. Only standard-library Fraction
arithmetic and literal periodic windows are used. No earlier test/solver imported.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import lcm
import unittest


def periodic_counts(word, width):
    if not word:
        raise ValueError("nonempty cyclic word required")
    return Counter("".join(word[(i + j) % len(word)] for j in range(width))
                   for i in range(len(word)))


def recurrent_edges(p):
    m = p + 1
    return tuple(sorted(periodic_counts("0" * m + "1" * m, m)))


def strongly_connected(edges):
    vertices = {e[:-1] for e in edges} | {e[1:] for e in edges}
    if not vertices:
        return False
    for first in vertices:
        visited = {first}
        to_visit = [first]
        while to_visit:
            v = to_visit.pop()
            for edge in edges:
                if edge[:-1] == v and edge[1:] not in visited:
                    visited.add(edge[1:])
                    to_visit.append(edge[1:])
        if visited != vertices:
            return False
    return True


def rank(rows):
    if not rows:
        return 0
    a = [[Fraction(v) for v in row] for row in rows]
    width = len(a[0])
    pivot_row = 0
    for col in range(width):
        i = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if i is None:
            continue
        a[pivot_row], a[i] = a[i], a[pivot_row]
        pivot = a[pivot_row][col]
        a[pivot_row] = [v / pivot for v in a[pivot_row]]
        for i in range(pivot_row + 1, len(a)):
            if a[i][col]:
                factor = a[i][col]
                a[i] = [v - factor * w for v, w in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def original_equalities(edges):
    count = len(edges)
    verts = sorted({e[:-1] for e in edges} | {e[1:] for e in edges})
    d = [[int(e[1:] == v) - int(e[:-1] == v) for e in edges]
         for v in verts]
    return ([row + [0] * count for row in d] +
            [[0] * count + row for row in d] +
            [[int(e[0] == c) for e in edges] +
             [-int(e[0] == c) for e in edges] for c in "01"])


def analytic_vertex(p, edges):
    zero, one = "0" * (p + 1), "1" * (p + 1)
    x = [Fraction(2) if e in (zero, one) else Fraction(1)
         for e in edges]
    y = [Fraction(1) if e in (zero, one) else Fraction(p + 1, p)
         for e in edges]
    return x + y


def literal_pair(p):
    x = "0" * (2 * p + 1) + "1" * (2 * p + 1)
    y = "0" * (p + 1) + "1" * (p + 1) + "0" * p + "1" * p
    return x, y


class IrreducibleRingLoopsTest(unittest.TestCase):
    def test_graph_and_unique_fractional_vertex_rank(self):
        for p in range(2, 11):
            with self.subTest(p=p):
                m = p + 1
                edges = recurrent_edges(p)
                expected = {"0" * m, "1" * m}
                expected |= {"0" * j + "1" * (m - j) for j in range(1, m)}
                expected |= {"1" * j + "0" * (m - j) for j in range(1, m)}
                self.assertEqual(set(edges), expected)
                self.assertEqual(len(edges), 2 * p + 2)
                self.assertTrue(strongly_connected(edges))

                values = analytic_vertex(p, edges)
                n = len(edges)
                eq = original_equalities(edges)
                self.assertEqual(rank(eq), 2 * n - 4)
                self.assertTrue(all(sum(Fraction(a) * b for a, b in zip(row, values)) == 0
                                    for row in eq))
                self.assertTrue(all(v >= 1 for v in values))
                self.assertEqual(lcm(*(v.denominator for v in values)), p)

                target = [0] * (2 * n)
                target[edges.index("0" * m)] = 1
                target[n + edges.index("0" * m)] = -1
                self.assertEqual(sum(a * b for a, b in zip(target, values)), 1)
                tight = [[int(i == j) for i in range(2 * n)]
                         for j, value in enumerate(values) if value == 1]
                self.assertEqual(len(tight), 2 * p + 2)
                self.assertEqual(rank(eq + tight), 2 * n - 1)
                self.assertEqual(rank(eq + tight + [target]), 2 * n)

    def test_literal_witnesses_at_linear_length(self):
        for p in range(2, 11):
            with self.subTest(p=p):
                m = p + 1
                edges = recurrent_edges(p)
                x, y = literal_pair(p)
                self.assertEqual(len(x), 4 * p + 2)
                self.assertEqual(len(y), len(x))
                x_hist = periodic_counts(x, m)
                y_hist = periodic_counts(y, m)
                self.assertEqual(set(x_hist), set(edges))
                self.assertEqual(set(y_hist), set(edges))
                self.assertEqual(periodic_counts(x, 1), periodic_counts(y, 1))
                self.assertEqual((x_hist["0" * m], y_hist["0" * m]), (p + 1, 1))
                for e in edges:
                    self.assertGreater(x_hist[e], 0)
                    self.assertGreater(y_hist[e], 0)

    def test_bounded_rooted_word_minimum_crosscheck(self):
        # Short periods are included: periodic_counts wraps even when n < m.
        for p in (2, 3):
            with self.subTest(p=p):
                edges = set(recurrent_edges(p))
                m = p + 1
                first_full_collision = None
                for n in range(1, 4 * p + 3):
                    groups = {}
                    for symbols in product("01", repeat=n):
                        word = "".join(symbols)
                        histogram = periodic_counts(word, m)
                        if not set(histogram) <= edges or set(histogram) != edges:
                            continue
                        key = (word.count("0"), word.count("1"))
                        f = histogram["0" * m]
                        prev = groups.setdefault(key, {})
                        if f not in prev and prev and first_full_collision is None:
                            first_full_collision = n
                        prev.setdefault(f, word)
                self.assertEqual(first_full_collision, 4 * p + 2)


if __name__ == "__main__":
    unittest.main()
