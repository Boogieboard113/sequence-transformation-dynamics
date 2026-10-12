"""Independent bounded checks of the accepted PR #67 family; issue #74.

Input main: private-history-omitted.
Family source blob: private-history-omitted.

This module constructs the original incidence/prefix matrix directly from
length-three words. It does not import the proposed reduced-coordinate proof,
the old family tests, or the capped Fourier--Motzkin support-pair solver.
Rank certifies the supplied vertices, not completeness of the vertex list.
Only the stated closed-word ranges are exhaustively enumerated.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys
import unittest


INPUT_MAIN = "private-history-omitted"
FAMILY_BLOB = "private-history-omitted"


def family_edges(t):
    if type(t) is not int or t < 3:
        raise ValueError("the family requires integer t >= 3")
    edges = []
    for i in range(t):
        j = (i + 1) % t
        edges.extend(((i, i, j), (i, j, i), (j, i, j), (i, j, j)))
    return tuple(edges)


def cyclic_histogram(word, order):
    return Counter(
        tuple(word[(i + j) % len(word)] for j in range(order))
        for i in range(len(word))
    )


def literal_output(word):
    """Radius-one rule: emit 1 just at centered context (0, 0, 1)."""
    n = len(word)
    return tuple(
        int(tuple(word[(i + j) % n] for j in (-1, 0, 1)) == (0, 0, 1))
        for i in range(n)
    )


def original_structural_rows(edges, t):
    """D_x, D_y, and signed P_1 equality rows, with all redundancies retained."""
    e = len(edges)
    vertices = sorted({a[:2] for a in edges} | {a[1:] for a in edges})
    rows = []
    for side in (0, 1):
        for vertex in vertices:
            row = [0] * (2 * e)
            for i, edge in enumerate(edges):
                row[side * e + i] = int(edge[1:] == vertex) - int(edge[:2] == vertex)
            rows.append(row)
    for symbol in range(t):
        row = [int(edge[0] == symbol) for edge in edges]
        row += [-int(edge[0] == symbol) for edge in edges]
        rows.append(row)
    return rows


def dot(row, point):
    return sum(a * b for a, b in zip(row, point))


def exact_rank(rows):
    """Rational Gaussian elimination on the original, possibly redundant rows."""
    if not rows:
        return 0
    matrix = [[Fraction(v) for v in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        divisor = matrix[rank][column]
        matrix[rank] = [v / divisor for v in matrix[rank]]
        for i in range(rank + 1, len(matrix)):
            factor = matrix[i][column]
            if factor:
                matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def vertex_record(t, parity_choice=None):
    """Check an explicit proposed point against the full normalized system."""
    edges = family_edges(t)
    x = [v for _ in range(t) for v in (2, 1, 1, 2)]
    if t % 2:
        if parity_choice is not None:
            raise ValueError("odd t has no parity choice")
        y = [v for _ in range(t) for v in (1, 2, 2, 1)]
        label = "odd"
    else:
        if parity_choice not in (-1, 1):
            raise ValueError("even t requires a parity choice -1 or +1")
        y = []
        for i in range(t):
            excursion = 2 + parity_choice * (-1) ** i
            y.extend((1, excursion, excursion, 1))
        label = "even_plus" if parity_choice == 1 else "even_minus"
    point = x + y
    n = len(point)
    structural = original_structural_rows(edges, t)
    if any(dot(row, point) for row in structural):
        raise AssertionError("candidate violates original structural equalities")
    if any(type(value) is not int or value < 1 for value in point):
        raise AssertionError("candidate is not positive integral")
    target = [int(edge == (0, 0, 1)) for edge in edges]
    target += [-int(edge == (0, 0, 1)) for edge in edges]
    gap = dot(target, point)
    if gap < 1:
        raise AssertionError("candidate violates target inequality")
    active = list(structural)
    positivity_active = 0
    for j, value in enumerate(point):
        if value == 1:
            row = [0] * n
            row[j] = 1
            active.append(row)
            positivity_active += 1
    if gap == 1:
        active.append(target)
    rank = exact_rank(active)
    if rank != n:
        raise AssertionError("supplied feasible point is not certified as a vertex")
    return {
        "t": t,
        "candidate": label,
        "variables": n,
        "structural_rows": len(structural),
        "active_positivity_rows": positivity_active,
        "active_target": gap == 1,
        "active_rank": rank,
        "common_denominator": 1,
        "individual_length": sum(x),
    }


def euler_word(edges, counts):
    """Deterministic lift, checked afterward using literal periodic windows."""
    if len(edges) != len(counts) or any(type(c) is not int or c < 0 for c in counts):
        raise ValueError("one nonnegative integer count per edge required")
    adjacency = defaultdict(list)
    expected = Counter({edge: count for edge, count in zip(edges, counts) if count})
    for edge, count in sorted(expected.items(), reverse=True):
        adjacency[edge[:2]].extend([edge] * count)
    if not expected:
        raise ValueError("empty histogram")
    vertices = [min(expected)[:2]]
    edge_stack = []
    circuit = []
    while vertices:
        outgoing = adjacency[vertices[-1]]
        if outgoing:
            edge = outgoing.pop()
            vertices.append(edge[1:])
            edge_stack.append(edge)
        else:
            vertices.pop()
            if edge_stack:
                circuit.append(edge_stack.pop())
    circuit.reverse()
    word = tuple(edge[0] for edge in circuit)
    if cyclic_histogram(word, 3) != expected:
        raise AssertionError("lifted word does not realize the requested exact histogram")
    return word


def witness_record(t, full_support):
    edges = family_edges(t)
    if full_support:
        x = [v for _ in range(t) for v in (2, 1, 1, 2)]
        y = [v for _ in range(t) for v in (1, 2, 2, 1)]
        claimed_length = 6 * t
    else:
        x = [v for _ in range(t) for v in (2, 0, 0, 2)]
        y = [1] * len(edges)
        claimed_length = 4 * t
    source_x = euler_word(edges, x)
    source_y = euler_word(edges, y)
    if len(source_x) != claimed_length or len(source_y) != claimed_length:
        raise AssertionError("unexpected explicit witness length")
    if cyclic_histogram(source_x, 1) != cyclic_histogram(source_y, 1):
        raise AssertionError("literal source C1 counts differ")
    output_x, output_y = literal_output(source_x), literal_output(source_y)
    if (sum(output_x), sum(output_y)) != (2, 1):
        raise AssertionError("literal radius-one target discrepancy is wrong")
    return {
        "t": t,
        "scope": "full_positive_support" if full_support else "arbitrary_support",
        "source_x": list(source_x),
        "source_y": list(source_y),
        "individual_length": claimed_length,
        "source_symbol_counts": dict(sorted(Counter(source_x).items())),
        "output_one_counts": [sum(output_x), sum(output_y)],
        "positive_edge_types": [sum(c > 0 for c in x), sum(c > 0 for c in y)],
    }


def admissible_rooted_words(edges, length):
    """All closed length-n paths, decoded at the marked source site.

    A rooted admissible periodic word fixes its starting two-letter context and
    every following edge, including periods shorter than three. Thus every
    such word occurs once; no quotient by source or output rotation is taken.
    This family has no length-one closed path.
    """
    outgoing = defaultdict(list)
    for edge in edges:
        outgoing[edge[:2]].append(edge)
    for start in sorted(outgoing):
        def visit(vertex, symbols):
            if len(symbols) == length:
                if vertex == start:
                    yield tuple(symbols)
                return
            for edge in outgoing[vertex]:
                yield from visit(edge[1:], symbols + [edge[0]])
        yield from visit(start, [])


def bounded_minimum_record(t, max_length):
    edges = family_edges(t)
    allowed = set(edges)
    rows = []
    first_collision = None
    for length in range(1, max_length + 1):
        # Keep every enumerated word here so an accidental duplicate is caught.
        seen = set()
        groups = {}
        collisions = 0
        for word in admissible_rooted_words(edges, length):
            if word in seen:
                raise AssertionError("rooted enumeration repeated a word")
            seen.add(word)
            if set(cyclic_histogram(word, 3)) - allowed:
                raise AssertionError("enumerated word violates the original domain")
            signature = tuple(word.count(i) for i in range(t))
            target = sum(literal_output(word))
            if signature in groups:
                previous_target, previous_word = groups[signature]
                if previous_target != target:
                    collisions += 1
                    if first_collision is None:
                        first_collision = {
                            "individual_length": length,
                            "source_x": list(previous_word),
                            "source_y": list(word),
                            "source_symbol_counts": list(signature),
                            "output_one_counts": [previous_target, target],
                        }
            else:
                groups[signature] = (target, word)
        rows.append({"length": length, "rooted_words": len(seen), "collision_hits": collisions})
    return {
        "t": t,
        "max_individual_source_length": max_length,
        "all_rooted_words_in_range": sum(row["rooted_words"] for row in rows),
        "length_rows": rows,
        "first_collision": first_collision,
    }


def evidence_packet():
    vertices = []
    for t in range(3, 9):
        choices = (None,) if t % 2 else (-1, 1)
        vertices.extend(vertex_record(t, choice) for choice in choices)
    return {
        "input_main": INPUT_MAIN,
        "family_blob": FAMILY_BLOB,
        "classification": "bounded independent computational evidence, not a general proof",
        "arithmetic": "integers and fractions.Fraction; standard library only",
        "vertex_scope": "rank certifies supplied vertices only; does not exhaust vertices",
        "enumerator_cross_check": {
            "alphabets": [3, 4],
            "lengths": [1, 2, 3, 4, 5, 6],
            "literal_alphabet_words_checked": sum(t ** n for t in (3, 4) for n in range(1, 7)),
            "method": "unit test compares closed-walk output sets with literal alphabet-product filtering",
        },
        "vertex_checks": vertices,
        "literal_witness_checks": [witness_record(t, full) for t in range(3, 9) for full in (False, True)],
        "exhaustive_minimum_checks": [bounded_minimum_record(3, 12), bounded_minimum_record(4, 16)],
    }


class ExponentialMinorFamilyExactWitnesses(unittest.TestCase):
    def test_proposed_vertices_against_original_constraints(self):
        for t in range(3, 9):
            for choice in ((None,) if t % 2 else (-1, 1)):
                with self.subTest(t=t, parity_choice=choice):
                    result = vertex_record(t, choice)
                    self.assertEqual(result["active_rank"], 8 * t)
                    self.assertEqual(result["common_denominator"], 1)
                    self.assertEqual(result["individual_length"], 6 * t)

    def test_literal_shortest_candidate_witnesses(self):
        for t in range(3, 9):
            for full in (False, True):
                with self.subTest(t=t, full_support=full):
                    result = witness_record(t, full)
                    self.assertEqual(result["individual_length"], (6 if full else 4) * t)
                    self.assertEqual(result["output_one_counts"], [2, 1])

    def test_bounded_global_minimum_odd_and_even(self):
        for t, bound in ((3, 12), (4, 16)):
            with self.subTest(t=t, bound=bound):
                result = bounded_minimum_record(t, bound)
                self.assertEqual(result["first_collision"]["individual_length"], 4 * t)
                self.assertTrue(all(row["collision_hits"] == 0 for row in result["length_rows"][:-1]))

    def test_short_period_domain_examples(self):
        # Period two is shorter than the three-letter local window.
        for t in (3, 4):
            words = set(admissible_rooted_words(family_edges(t), 2))
            self.assertEqual(len(words), 2 * t)
            self.assertIn((0, 1), words)
            self.assertIn((1, 0), words)
            self.assertTrue(all(sum(literal_output(word)) == 0 for word in words))
            self.assertEqual(list(admissible_rooted_words(family_edges(t), 1)), [])

    def test_closed_walk_enumerator_matches_literal_alphabet_search(self):
        for t in (3, 4):
            edges = family_edges(t)
            allowed = set(edges)
            for length in range(1, 7):
                with self.subTest(t=t, length=length):
                    direct = {
                        word for word in product(range(t), repeat=length)
                        if set(cyclic_histogram(word, 3)) <= allowed
                    }
                    self.assertEqual(set(admissible_rooted_words(edges, length)), direct)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--report":
        Path(sys.argv[2]).write_text(json.dumps(evidence_packet(), indent=2, sort_keys=True) + "\n")
    else:
        unittest.main()
