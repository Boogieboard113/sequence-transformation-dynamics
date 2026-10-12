"""Exact bounded search for irreducible fractional support-pair vertices.

Issue #88.  Standard library only.

Declared search domain:
- binary length-three de Bruijn edge types;
- every strongly connected ambient edge set with 1..6 edge types;
- every ordered pair of nonempty strongly connected supports S,T inside it;
- every single-edge target indicator from the ambient graph;
- source histogram order h=1;
- original support-pair equalities and normalized inequalities in edge coordinates.

Duplicate (S,T,target) LP instances induced by multiple ambient supersets are
assigned to the lexicographically least smallest strongly connected ambient
graph containing them.  All arithmetic is exact Fraction arithmetic.

This is a finite search oracle, not a universal theorem or a production solver.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import comb, lcm
import argparse
import json


ALL_EDGES = tuple("".join(bits) for bits in product("01", repeat=3))
ACTIVE_SET_CAP = 20_000


def vertices_of(edges):
    return {edge[:2] for edge in edges} | {edge[1:] for edge in edges}


def strongly_connected(edges) -> bool:
    """Strong connectivity on the vertices incident to a nonempty edge set."""
    edges = tuple(edges)
    vertices = vertices_of(edges)
    if not vertices:
        return False
    outgoing = {v: [] for v in vertices}
    incoming = {v: [] for v in vertices}
    for edge in edges:
        outgoing[edge[:2]].append(edge[1:])
        incoming[edge[1:]].append(edge[:2])
    start = min(vertices)
    for adjacency in (outgoing, incoming):
        seen, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            stack.extend(adjacency.get(vertex, ()))
        if seen != vertices:
            return False
    return True


def strongly_connected_subsets(max_edges=6):
    result = []
    for size in range(1, max_edges + 1):
        for edges in combinations(ALL_EDGES, size):
            if strongly_connected(edges):
                result.append(edges)
    return tuple(sorted(result, key=lambda value: (len(value), value)))


def equality_rows(S, T):
    """Original balance + signed source-C1 rows in x-then-y coordinates."""
    S, T = tuple(S), tuple(T)
    ns, nt = len(S), len(T)
    rows = []
    for vertex in sorted(vertices_of(S)):
        rows.append(
            [int(edge[1:] == vertex) - int(edge[:2] == vertex) for edge in S]
            + [0] * nt
        )
    for vertex in sorted(vertices_of(T)):
        rows.append(
            [0] * ns
            + [int(edge[1:] == vertex) - int(edge[:2] == vertex) for edge in T]
        )
    for symbol in "01":
        rows.append(
            [int(edge[0] == symbol) for edge in S]
            + [-int(edge[0] == symbol) for edge in T]
        )
    return rows


def rref(rows, width):
    matrix = [[Fraction(value) for value in row] for row in rows]
    pivots = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (i for i in range(pivot_row, len(matrix)) if matrix[i][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for i in range(len(matrix)):
            if i != pivot_row and matrix[i][column]:
                factor = matrix[i][column]
                matrix[i] = [
                    value - factor * base
                    for value, base in zip(matrix[i], matrix[pivot_row])
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix[:pivot_row], pivots


def rank(rows, width):
    return len(rref(rows, width)[1])


def nullspace_basis(rows, width):
    reduced, pivots = rref(rows, width)
    basis = []
    for free in (j for j in range(width) if j not in pivots):
        vector = [Fraction(0)] * width
        vector[free] = Fraction(1)
        for i, pivot in enumerate(pivots):
            vector[pivot] = -reduced[i][free]
        basis.append(tuple(vector))
    return tuple(basis), tuple(pivots)


def solve_square(rows, rhs):
    n = len(rhs)
    matrix = [
        [Fraction(value) for value in row] + [Fraction(b)]
        for row, b in zip(rows, rhs)
    ]
    for column in range(n):
        pivot = next(
            (i for i in range(column, n) if matrix[i][column]),
            None,
        )
        if pivot is None:
            return None
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [value / scale for value in matrix[column]]
        for i in range(n):
            if i != column and matrix[i][column]:
                factor = matrix[i][column]
                matrix[i] = [
                    value - factor * base
                    for value, base in zip(matrix[i], matrix[column])
                ]
    return tuple(row[-1] for row in matrix)


def target_row(S, T, target):
    return tuple(
        [int(edge == target) for edge in S]
        + [-int(edge == target) for edge in T]
    )


def all_vertices(S, T, target, *, active_set_cap=ACTIVE_SET_CAP):
    """Enumerate every vertex of one normalized original-coordinate LP.

    Equalities:
      D_S x = 0, D_T y = 0, P1_S x = P1_T y.
    Inequalities:
      every coordinate >= 1,
      F_target(x)-F_target(y) >= 1.

    Returns UNRESOLVED_CAP rather than mathematical infeasibility if the
    declared engineering cap would be exceeded.
    """
    S, T = tuple(S), tuple(T)
    width = len(S) + len(T)
    equalities = equality_rows(S, T)
    basis, pivots = nullspace_basis(equalities, width)
    dimension = len(basis)
    if dimension == 0:
        return {
            "status": "OK",
            "equality_rank": len(pivots),
            "dimension": 0,
            "active_sets": 0,
            "feasible_bases": 0,
            "vertices": (),
        }

    constraints = [
        tuple(column[i] for column in basis)
        for i in range(width)
    ]
    raw_target = target_row(S, T, target)
    constraints.append(
        tuple(
            sum(Fraction(coefficient) * column[i]
                for i, coefficient in enumerate(raw_target))
            for column in basis
        )
    )

    active_sets = comb(width + 1, dimension)
    if active_sets > active_set_cap:
        return {
            "status": "UNRESOLVED_CAP",
            "equality_rank": len(pivots),
            "dimension": dimension,
            "active_sets": active_sets,
            "feasible_bases": 0,
            "vertices": (),
        }

    vertices = set()
    feasible_bases = 0
    for active in combinations(range(width + 1), dimension):
        parameters = solve_square(
            [constraints[i] for i in active],
            [1] * dimension,
        )
        if parameters is None:
            continue
        if any(
            sum(a * b for a, b in zip(row, parameters)) < 1
            for row in constraints
        ):
            continue
        point = tuple(
            sum(parameter * column[i]
                for parameter, column in zip(parameters, basis))
            for i in range(width)
        )
        if any(
            sum(Fraction(a) * b for a, b in zip(row, point))
            for row in equalities
        ):
            raise AssertionError("candidate violates original equality system")
        if any(value < 1 for value in point):
            raise AssertionError("candidate violates support positivity")
        if sum(Fraction(a) * b for a, b in zip(raw_target, point)) < 1:
            raise AssertionError("candidate violates target discrepancy")
        feasible_bases += 1
        vertices.add(point)

    return {
        "status": "OK",
        "equality_rank": len(pivots),
        "dimension": dimension,
        "active_sets": active_sets,
        "feasible_bases": feasible_bases,
        "vertices": tuple(sorted(vertices)),
    }


def canonical_instances():
    """Yield each declared (S,T,target) instance exactly once."""
    supports = strongly_connected_subsets(6)
    ambients = supports
    seen = set()
    for ambient in ambients:
        ambient_set = set(ambient)
        contained = [
            support for support in supports
            if set(support) <= ambient_set
        ]
        for S in contained:
            for T in contained:
                for target in ambient:
                    key = (S, T, target)
                    if key in seen:
                        continue
                    seen.add(key)
                    yield ambient, S, T, target


def denominator(point):
    return lcm(*(value.denominator for value in point))


def cyclic_blocks(word, order):
    n = len(word)
    if n == 0:
        raise ValueError("cyclic word must be nonempty")
    return Counter(
        "".join(word[(i + j) % n] for j in range(order))
        for i in range(n)
    )


def euler_word(edges, weights):
    """Independent deterministic Hierholzer lift of a positive circulation."""
    edges = tuple(edges)
    weights = tuple(weights)
    if len(edges) != len(weights):
        raise ValueError("edge/weight length mismatch")
    if any(type(weight) is not int or weight < 1 for weight in weights):
        raise ValueError("positive integer edge weights required")

    outgoing = defaultdict(list)
    for edge, weight in zip(edges, weights):
        outgoing[edge[:2]].extend([edge] * weight)
    for values in outgoing.values():
        values.sort(reverse=True)

    start = min(outgoing)
    vertices = [start]
    prior_edges = []
    tour = []
    while vertices:
        vertex = vertices[-1]
        if outgoing[vertex]:
            edge = outgoing[vertex].pop()
            prior_edges.append(edge)
            vertices.append(edge[1:])
        else:
            vertices.pop()
            if prior_edges:
                tour.append(prior_edges.pop())
    tour.reverse()
    word = "".join(edge[0] for edge in tour)
    expected = Counter(dict(zip(edges, weights)))
    if len(word) != sum(weights):
        raise AssertionError("Euler lift did not use all requested edges")
    if cyclic_blocks(word, 3) != expected:
        raise AssertionError("Euler lift has wrong cyclic triple histogram")
    return word


def active_certificate(S, T, target, point):
    width = len(point)
    equalities = equality_rows(S, T)
    tight_positions = [i for i, value in enumerate(point) if value == 1]
    positivity_rows = [
        [int(i == position) for i in range(width)]
        for position in tight_positions
    ]
    target = target_row(S, T, target)
    gap = sum(Fraction(a) * b for a, b in zip(target, point))
    rows_without_target = equalities + positivity_rows
    rows_with_target = (
        rows_without_target + [list(target)]
        if gap == 1 else rows_without_target
    )
    return {
        "variables": width,
        "equality_rank": rank(equalities, width),
        "tight_positivity_indices": tight_positions,
        "target_gap": str(gap),
        "target_tight": gap == 1,
        "rank_without_target": rank(rows_without_target, width),
        "rank_with_target_if_tight": rank(rows_with_target, width),
    }


def lift_point(S, T, target, point):
    scale = denominator(point)
    x_weights = [int(scale * value) for value in point[:len(S)]]
    y_weights = [int(scale * value) for value in point[len(S):]]
    x = euler_word(S, x_weights)
    y = euler_word(T, y_weights)
    if cyclic_blocks(x, 1) != cyclic_blocks(y, 1):
        raise AssertionError("integer lift lost source C1 equality")
    if cyclic_blocks(x, 3)[target] - cyclic_blocks(y, 3)[target] < scale:
        raise AssertionError("integer lift lost target discrepancy")
    return {
        "scale": scale,
        "x_weights": x_weights,
        "y_weights": y_weights,
        "x_word": x,
        "y_word": y,
        "length": len(x),
        "source_c1": dict(sorted(cyclic_blocks(x, 1).items())),
        "target_counts": [
            cyclic_blocks(x, 3)[target],
            cyclic_blocks(y, 3)[target],
        ],
    }


def literal_shortest_pair(ambient, S, T, target, max_length=14):
    """Complete direct alphabet-product search for one exact support pair."""
    ambient = set(ambient)
    S, T = tuple(S), tuple(T)
    for n in range(1, max_length + 1):
        left = defaultdict(lambda: defaultdict(list))
        right = defaultdict(lambda: defaultdict(list))
        for bits in product("01", repeat=n):
            word = "".join(bits)
            triples = cyclic_blocks(word, 3)
            support = tuple(sorted(edge for edge, count in triples.items() if count))
            if not set(support) <= ambient:
                continue
            c1 = tuple(sorted(cyclic_blocks(word, 1).items()))
            value = triples[target]
            if support == S:
                left[c1][value].append(word)
            if support == T:
                right[c1][value].append(word)
        for c1 in sorted(set(left) & set(right)):
            for x_value in sorted(left[c1]):
                for y_value in sorted(right[c1]):
                    if x_value != y_value:
                        return {
                            "length": n,
                            "x": min(left[c1][x_value]),
                            "y": min(right[c1][y_value]),
                            "source_c1": dict(c1),
                            "target_counts": [x_value, y_value],
                        }
    return None


def encode_point(point):
    return [str(value) for value in point]


def representative_record(hit, *, literal_max=14):
    ambient, S, T, target, point = hit
    return {
        "ambient": list(ambient),
        "S": list(S),
        "T": list(T),
        "target": target,
        "denominator": denominator(point),
        "point": encode_point(point),
        "active_certificate": active_certificate(S, T, target, point),
        "integer_lift": lift_point(S, T, target, point),
        "literal_shortest_through_14": literal_shortest_pair(
            ambient, S, T, target, literal_max
        ),
    }


def scan():
    ambient_counts = Counter()
    for support in strongly_connected_subsets(6):
        ambient_counts[len(support)] += 1

    by_ambient_size = defaultdict(Counter)
    denominator_histogram = Counter()
    fractional_hits = []
    total_instances = total_active_sets = total_vertices = cap_hits = 0

    for ambient, S, T, target in canonical_instances():
        result = all_vertices(S, T, target)
        total_instances += 1
        total_active_sets += result["active_sets"]
        row = by_ambient_size[len(ambient)]
        row["instances"] += 1
        row["active_sets"] += result["active_sets"]
        if result["status"] != "OK":
            cap_hits += 1
            row["cap_hits"] += 1
            continue
        row["vertices"] += len(result["vertices"])
        total_vertices += len(result["vertices"])
        for point in result["vertices"]:
            d = denominator(point)
            denominator_histogram[d] += 1
            if d > 1:
                row["fractional_vertices"] += 1
                fractional_hits.append((ambient, S, T, target, point))

    fractional_hits.sort(
        key=lambda hit: (
            len(hit[0]), hit[0], len(hit[1]), hit[1],
            len(hit[2]), hit[2], hit[3], encode_point(hit[4])
        )
    )
    if not fractional_hits:
        raise AssertionError("declared search unexpectedly found no fractional vertex")

    min_ambient = min(len(hit[0]) for hit in fractional_hits)
    max_denominator = max(denominator(hit[4]) for hit in fractional_hits)
    full = next(
        hit for hit in fractional_hits
        if hit[0] == hit[1] == hit[2]
    )
    proper = next(
        hit for hit in fractional_hits
        if hit[1] != hit[0] and hit[2] != hit[0]
    )

    fractional_support_sizes = Counter(
        (len(hit[1]), len(hit[2])) for hit in fractional_hits
    )
    fractional_ambients = sorted({hit[0] for hit in fractional_hits})

    return {
        "search_scope": {
            "edge_type": "binary length-three de Bruijn edges",
            "ambient_edge_count_range": [1, 6],
            "source_order": 1,
            "target_rows": "all single-edge indicators in canonical ambient",
            "active_set_cap": ACTIVE_SET_CAP,
            "arithmetic": "fractions.Fraction",
            "canonicalization": (
                "least (edge-count,lexicographic) strongly connected ambient "
                "containing each ordered (S,T,target) instance"
            ),
        },
        "ambient_graph_counts": {
            str(size): ambient_counts[size] for size in range(1, 7)
        },
        "summary": {
            "ambient_graphs": sum(ambient_counts.values()),
            "unique_lp_instances": total_instances,
            "active_sets_tested": total_active_sets,
            "cap_hits": cap_hits,
            "feasible_vertices": total_vertices,
            "fractional_vertices": len(fractional_hits),
            "minimum_fractional_ambient_edges": min_ambient,
            "maximum_vertex_denominator": max_denominator,
            "denominator_histogram": {
                str(key): denominator_histogram[key]
                for key in sorted(denominator_histogram)
            },
            "fractional_support_size_histogram": {
                f"{left},{right}": fractional_support_sizes[left, right]
                for left, right in sorted(fractional_support_sizes)
            },
            "fractional_ambient_graphs": [list(value) for value in fractional_ambients],
        },
        "by_ambient_size": {
            str(size): {
                key: by_ambient_size[size][key]
                for key in ("instances", "active_sets", "vertices",
                            "fractional_vertices", "cap_hits")
            }
            for size in range(1, 7)
        },
        "full_support_representative": representative_record(full),
        "proper_support_representative": representative_record(proper),
        "classification": (
            "bounded exact computation only; no denominator-growth or "
            "shortest-witness asymptotic claim"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    text = json.dumps(scan(), indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as stream:
            stream.write(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
