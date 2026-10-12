"""Bounded exact checks for issue #64; supporting evidence, not a general proof.

Checks the explicit non-TU support-pair minor family from
theorems/proved-internal/support_pair_sparse_sharpness.md.
No external packages or floating point are used.
"""

from collections import Counter
import unittest


def family(t):
    """Four distinct length-three edge types per symbol; t >= 3."""
    if t < 3:
        raise ValueError("t must be at least 3")
    edges = []
    for i in range(t):
        j = (i + 1) % t
        edges.extend(((i, i, j), (i, j, i), (j, i, j), (i, j, j)))
    return edges


def exact_determinant(rows):
    """Integer fraction-free Bareiss determinant."""
    n = len(rows)
    if n == 0:
        return 1
    a = [list(row) for row in rows]
    if any(len(row) != n for row in a):
        raise ValueError("square matrix required")
    sign = 1
    prior = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            substitute = next((i for i in range(k + 1, n) if a[i][k]), None)
            if substitute is None:
                return 0
            a[k], a[substitute] = a[substitute], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                if numerator % prior:
                    raise ArithmeticError("non-exact Bareiss division")
                a[i][j] = numerator // prior
        for i in range(k + 1, n):
            a[i][k] = 0
        prior = pivot
    return sign * a[-1][-1]


def incidence_at(vertex, edge):
    return int(edge[1:] == vertex) - int(edge[:2] == vertex)


def structural_minor(t):
    edges = family(t)
    rows = []
    for i in range(t):
        vertex = (i, (i + 1) % t)
        # x-side balance row and x-side P_h, h=1, signed prefix row
        rows.append([incidence_at(vertex, edge) for edge in edges])
        rows.append([int(edge[0] == i) for edge in edges])
    selected_columns = [4 * i + delta for i in range(t) for delta in (0, 1)]
    return [[row[j] for j in selected_columns] for row in rows]


def graph_is_strongly_connected(edges):
    vertices = {edge[:2] for edge in edges} | {edge[1:] for edge in edges}
    adjacency = {v: set() for v in vertices}
    for edge in edges:
        adjacency[edge[:2]].add(edge[1:])
    for source in vertices:
        seen = {source}
        pending = [source]
        while pending:
            for destination in adjacency[pending.pop()]:
                if destination not in seen:
                    seen.add(destination)
                    pending.append(destination)
        if seen != vertices:
            return False
    return True


def circulation_balance(edges, weights):
    balance = Counter()
    for edge, count in zip(edges, weights):
        balance[edge[:2]] -= count
        balance[edge[1:]] += count
    return all(value == 0 for value in balance.values())


def prefix_histogram(edges, weights):
    counts = Counter()
    for edge, count in zip(edges, weights):
        counts[edge[0]] += count
    return counts


class SupportPairSparseSharpnessTests(unittest.TestCase):
    def test_smallest_structural_nontu_minor(self):
        edges = ((0, 0, 1), (0, 1, 0))
        matrix = [
            [incidence_at((0, 1), edge) for edge in edges],
            [int(edge[0] == 0) for edge in edges],
        ]
        self.assertEqual(matrix, [[1, -1], [1, 1]])
        self.assertEqual(exact_determinant(matrix), 2)

    def test_connected_feasible_exponential_minors(self):
        for t in (3, 4, 5, 6, 7):
            with self.subTest(t=t):
                edges = family(t)
                self.assertEqual(len(edges), 4 * t)
                self.assertEqual(len(set(edges)), 4 * t)
                self.assertTrue(graph_is_strongly_connected(edges))
                matrix = structural_minor(t)
                self.assertEqual(exact_determinant(matrix), 2 ** t)

                for i in range(t):
                    block = [
                        row[2 * i : 2 * i + 2]
                        for row in matrix[2 * i : 2 * i + 2]
                    ]
                    self.assertEqual(block, [[1, -1], [1, 1]])
                    for j in range(t):
                        if j == i:
                            continue
                        self.assertEqual(
                            [
                                row[2 * j : 2 * j + 2]
                                for row in matrix[2 * i : 2 * i + 2]
                            ],
                            [[0, 0], [0, 0]],
                        )

                # x: (s_i, t_i, u_i, v_i) = (2,1,1,2)
                # y: (s_i, t_i, u_i, v_i) = (1,2,2,1)
                x = [count for _ in range(t) for count in (2, 1, 1, 2)]
                y = [count for _ in range(t) for count in (1, 2, 2, 1)]
                self.assertTrue(circulation_balance(edges, x))
                self.assertTrue(circulation_balance(edges, y))
                self.assertEqual(prefix_histogram(edges, x), Counter({i: 6 for i in range(t)}))
                self.assertEqual(prefix_histogram(edges, x), prefix_histogram(edges, y))
                self.assertEqual(sum(x), 6 * t)
                self.assertEqual(sum(y), 6 * t)
                self.assertTrue(all(value >= 1 for value in x + y))
                self.assertEqual(x[0] - y[0], 1)  # F_b = 1 on s_0 only


if __name__ == "__main__":
    unittest.main()
