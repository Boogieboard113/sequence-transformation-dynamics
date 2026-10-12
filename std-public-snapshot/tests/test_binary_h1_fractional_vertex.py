"""Literal and exact-rational binary cyclic support-pair experiment, issue #78.

Full-support ordered LP: Dx=Dy=0; P1x=P1y; x,y>=1;
x[000]-y[000]>=1. Original length-three edge variables, not the
previous exponential-minor family's reduced parameters. Standard library only.
"""

from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from math import lcm
import argparse
import json
import unittest

EDGES = ("000", "001", "010", "011", "100", "110")
TARGET = "000"
BINARY_TRIPLES = tuple("".join(p) for p in product("01", repeat=3))
VERTEX = tuple(map(Q, ("2", "5/2", "1", "3/2", "5/2", "3/2",
                       "1", "3", "2", "1", "3", "1")))


def strongly_connected(edges):
    vertices = {e[:2] for e in edges} | {e[1:] for e in edges}
    if not vertices:
        return False
    for source in vertices:
        stack, seen = [source], set()
        while stack:
            current = stack.pop()
            if current not in seen:
                seen.add(current)
                stack.extend(e[1:] for e in edges if e[:2] == current)
        if seen != vertices:
            return False
    return True


def equalities(edges):
    """Original balance and signed one-letter prefix rows, in x,y order."""
    m = len(edges)
    vertices = sorted({e[:2] for e in edges} | {e[1:] for e in edges})
    prefixes = sorted({e[0] for e in edges})
    d = [[int(e[1:] == v) - int(e[:2] == v) for e in edges]
         for v in vertices]
    p = [[int(e[0] == c) for e in edges] for c in prefixes]
    return ([row + [0] * m for row in d] +
            [[0] * m + row for row in d] +
            [row + [-val for val in row] for row in p])


def rref(rows, width):
    a = [[Q(v) for v in row] for row in rows]
    pivots = []
    for col in range(width):
        k = len(pivots)
        pivot = next((i for i in range(k, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][col]
        a[k] = [v / scale for v in a[k]]
        for i in range(len(a)):
            if i != k and a[i][col]:
                t = a[i][col]
                a[i] = [v - t * w for v, w in zip(a[i], a[k])]
        pivots.append(col)
        if len(pivots) == len(a):
            break
    return a[:len(pivots)], pivots


def nullspace(edges):
    n = 2 * len(edges)
    reduced, pivots = rref(equalities(edges), n)
    columns = []
    for free in (j for j in range(n) if j not in pivots):
        column = [Q(int(j == free)) for j in range(n)]
        for i, pivot in enumerate(pivots):
            column[pivot] = -reduced[i][free]
        columns.append(column)
    return columns


def solve_square(rows, rhs):
    n = len(rhs)
    a = [[Q(t) for t in row] + [Q(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for i in range(n):
            if i != col and a[i][col]:
                t = a[i][col]
                a[i] = [v - t * w for v, w in zip(a[i], a[col])]
    return [row[-1] for row in a]


def all_vertices(edges, target):
    m = len(edges)
    j = edges.index(target)
    basis = nullspace(edges)
    dim = len(basis)
    if not dim:
        return [], 0, dim
    # Every pointed-polyhedron vertex has dim linearly independent
    # active inequalities; exhaust them, including the target row.
    constraints = [[col[i] for col in basis] for i in range(2 * m)]
    constraints.append([col[j] - col[m + j] for col in basis])
    vertices = set()
    cases = 0
    for active in combinations(range(2 * m + 1), dim):
        cases += 1
        u = solve_square([constraints[i] for i in active], [1] * dim)
        if u is None or any(sum(a * b for a, b in zip(row, u)) < 1
                            for row in constraints):
            continue
        z = tuple(sum(c * col[i] for c, col in zip(u, basis))
                  for i in range(2 * m))
        if any(sum(Q(a) * b for a, b in zip(row, z)) for row in equalities(edges)):
            raise AssertionError("candidate violates original equations")
        vertices.add(z)
    return sorted(vertices), cases, dim


def cyclic_blocks(word, size):
    n = len(word)
    return Counter("".join(word[(i + j) % n] for j in range(size))
                   for i in range(n))


def admissible(word, edges):
    return set(cyclic_blocks(word, 3)) <= set(edges)


def rooted_words(edges, n):
    """Closed de Bruijn walks; emits each rooted word exactly once."""
    if n == 1:
        for c in "01":
            if c * 3 in edges:
                yield c
        return
    vertices = sorted({e[:2] for e in edges} | {e[1:] for e in edges})
    out = {v: sorted(e for e in edges if e[:2] == v) for v in vertices}
    for root in vertices:
        def walk(current, word):
            if len(word) == n:
                if current == root:
                    yield word
                return
            for e in out[current]:
                yield from walk(e[1:], word + e[0])
        yield from walk(root, "")


def euler_word(edges, weights):
    if not all(isinstance(w, int) and w >= 1 for w in weights):
        raise ValueError("positive integer edge weights required")
    outgoing = defaultdict(list)
    for e, w in zip(edges, weights):
        outgoing[e[:2]].extend([e] * w)
    for value in outgoing.values():
        value.sort(reverse=True)
    stack, prior_edges, tour = [min(outgoing)], [], []
    while stack:
        vertex = stack[-1]
        if outgoing[vertex]:
            edge = outgoing[vertex].pop()
            prior_edges.append(edge)
            stack.append(edge[1:])
        else:
            stack.pop()
            if prior_edges:
                tour.append(prior_edges.pop())
    tour.reverse()
    word = "".join(e[0] for e in tour)
    if len(word) != sum(weights):
        raise AssertionError("non-Eulerian/ disconnected input")
    if cyclic_blocks(word, 3) != Counter(dict(zip(edges, weights))):
        raise AssertionError("literal cyclic triple mismatch")
    return word


def witness_search(max_length=14):
    """Literal periodic counts, independently of the LP/equality routines."""
    rows = []
    first_any = None
    first_full = None
    for n in range(1, max_length + 1):
        seen_any, seen_full = {}, {}
        total = full_total = 0
        for word in rooted_words(EDGES, n):
            triples = cyclic_blocks(word, 3)
            if not set(triples) <= set(EDGES):
                raise AssertionError("walk enumerator produced invalid word")
            total += 1
            key = (word.count("0"), word.count("1"))
            target = triples[TARGET]
            any_targets = seen_any.setdefault(key, {})
            if first_any is None and any_targets and target not in any_targets:
                old_target = next(iter(any_targets))
                first_any = (n, any_targets[old_target], word, old_target, target, key)
            any_targets.setdefault(target, word)
            if all(triples[e] > 0 for e in EDGES):
                full_total += 1
                full_targets = seen_full.setdefault(key, {})
                if first_full is None and full_targets and target not in full_targets:
                    old_target = next(iter(full_targets))
                    first_full = (n, full_targets[old_target], word,
                                  old_target, target, key)
                full_targets.setdefault(target, word)
        rows.append((n, total, full_total))
    return rows, first_any, first_full


def smaller_graph_survey():
    results = []
    for size in (3, 4, 5):
        graphs = instances = vertices = fractional = bases = 0
        for edges in combinations(BINARY_TRIPLES, size):
            if not strongly_connected(edges):
                continue
            graphs += 1
            for target in edges:
                points, cases, _ = all_vertices(edges, target)
                instances += 1
                vertices += len(points)
                bases += cases
                fractional += sum(any(p.denominator > 1 for p in point)
                                  for point in points)
        results.append((size, graphs, instances, bases, vertices, fractional))
    return results


class BinaryFractionalVertexTests(unittest.TestCase):
    def test_exact_full_support_lp(self):
        self.assertTrue(strongly_connected(EDGES))
        points, cases, dimension = all_vertices(EDGES, TARGET)
        self.assertEqual((dimension, cases), (4, 715))
        self.assertEqual(points, [VERTEX])
        self.assertEqual(lcm(*(v.denominator for v in VERTEX)), 2)
        self.assertEqual(sum(VERTEX[:6]), sum(VERTEX[6:]))
        self.assertEqual(VERTEX[0] - VERTEX[6], 1)
        active = [i for i, v in enumerate(VERTEX) if v == 1]
        self.assertEqual(active, [2, 6, 9, 11])
        unit_rows = [[int(i == j) for i in range(12)] for j in active]
        target_row = [1] + [0] * 5 + [-1] + [0] * 5
        self.assertEqual(len(rref(equalities(EDGES) + unit_rows, 12)[1]), 11)
        self.assertEqual(len(rref(equalities(EDGES) + unit_rows + [target_row], 12)[1]), 12)

    def test_scaled_vertex_lifts_to_literal_cyclic_words(self):
        x = euler_word(EDGES, [int(2 * v) for v in VERTEX[:6]])
        y = euler_word(EDGES, [int(2 * v) for v in VERTEX[6:]])
        self.assertEqual((len(x), len(y)), (22, 22))
        self.assertTrue(admissible(x, EDGES) and admissible(y, EDGES))
        self.assertEqual(cyclic_blocks(x, 1), cyclic_blocks(y, 1))
        self.assertEqual((cyclic_blocks(x, 3)[TARGET],
                          cyclic_blocks(y, 3)[TARGET]), (4, 2))

    def test_literal_minimum_and_independent_brute_crosscheck(self):
        rows, any_hit, full_hit = witness_search()
        self.assertEqual([r[1] for r in rows],
                         [1, 1, 4, 9, 11, 16, 29, 49, 76, 121, 199, 324, 521, 841])
        self.assertEqual([r[2] for r in rows],
                         [0, 0, 0, 0, 0, 0, 0, 16, 27, 40, 88, 180, 299, 518])
        self.assertEqual(any_hit[0], 6)
        self.assertEqual(full_hit[0], 14)
        for hit, require_full in ((any_hit, False), (full_hit, True)):
            n, x, y, a, b, histogram = hit
            self.assertEqual(len(x), n)
            self.assertEqual(len(y), n)
            self.assertNotEqual(a, b)
            self.assertEqual(cyclic_blocks(x, 1), cyclic_blocks(y, 1))
            self.assertTrue(admissible(x, EDGES) and admissible(y, EDGES))
            self.assertEqual((cyclic_blocks(x, 3)[TARGET],
                              cyclic_blocks(y, 3)[TARGET]), (a, b))
            self.assertEqual(histogram, (x.count("0"), x.count("1")))
            if require_full:
                self.assertTrue(all(cyclic_blocks(x, 3)[e] > 0 for e in EDGES))
                self.assertTrue(all(cyclic_blocks(y, 3)[e] > 0 for e in EDGES))
        for n in range(1, 15):
            literal = {"".join(w) for w in product("01", repeat=n)
                       if admissible("".join(w), EDGES)}
            walks = list(rooted_words(EDGES, n))
            self.assertEqual(len(walks), len(set(walks)))
            self.assertEqual(set(walks), literal)

    def test_all_strongly_connected_smaller_binary_graphs(self):
        self.assertEqual(smaller_graph_survey(),
                         [(3, 2, 6, 42, 0, 0),
                          (4, 5, 20, 612, 0, 0),
                          (5, 6, 30, 4400, 8, 0)])


def report():
    points, cases, dim = all_vertices(EDGES, TARGET)
    rows, any_hit, full_hit = witness_search()
    xs = euler_word(EDGES, [int(2 * v) for v in points[0][:6]])
    ys = euler_word(EDGES, [int(2 * v) for v in points[0][6:]])
    def hit(t):
        n, x, y, a, b, h1 = t
        return dict(length=n, x=x, y=y, target_counts=[a, b], c1=list(h1))
    return dict(graph=list(EDGES), target=TARGET, source_order=1,
                equalities_rank=12-dim, active_sets_tested=cases,
                vertices=[[str(v) for v in p] for p in points],
                all_vertex_denominators=[lcm(*(v.denominator for v in p))
                                         for p in points],
                scaled_vertex_words=dict(x=xs, y=ys, length=len(xs),
                                         target_counts=[cyclic_blocks(xs, 3)[TARGET],
                                                        cyclic_blocks(ys, 3)[TARGET]],
                                         source_c1=[xs.count("0"), xs.count("1")]),
                literal_length_rows=[dict(length=n, rooted_words=c,
                                          both_supports_full=f) for n, c, f in rows],
                first_any_support=hit(any_hit), first_both_full=hit(full_hit),
                smaller_graph_survey=[dict(edge_types=e, graphs=g,
                                           target_instances=i, active_sets=b,
                                           feasible_vertices=v,
                                           fractional_vertices=f)
                                      for e, g, i, b, v, f in smaller_graph_survey()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", help="write deterministic exact JSON report")
    opts, rest = parser.parse_known_args()
    if opts.report:
        with open(opts.report, "w", encoding="utf-8") as stream:
            json.dump(report(), stream, sort_keys=True, indent=2)
            stream.write("\n")
    else:
        unittest.main(argv=[__file__] + rest)
