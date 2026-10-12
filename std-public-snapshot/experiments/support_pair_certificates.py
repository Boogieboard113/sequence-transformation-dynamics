"""Small exact support-pair certificate generator for STD issue #44.

This module treats the accepted reducible support-pair theorem as an input.  It
implements exhaustive support enumeration and exact certificate extraction for
at most eight recurrent L-block edge types.  It is not a proof of that theorem
and is not intended as a large LP solver.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import gcd
from typing import Mapping, Sequence

from experiments.rational_fourier_motzkin import (
    equality_inequalities,
    feasible_point,
    satisfies,
)


MAX_EDGE_TYPES = 8


def endpoints(edge: str) -> tuple[str, str]:
    if not isinstance(edge, str) or not edge:
        raise ValueError("edges must be nonempty source-block strings")
    return edge[:-1], edge[1:]


def cyclic_counts(word: str, order: int) -> Counter:
    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
        raise ValueError("order must be a positive integer")
    if not word:
        return Counter()
    n = len(word)
    return Counter(
        "".join(word[(i + j) % n] for j in range(order))
        for i in range(n)
    )


def strongly_connected_support(edges: Sequence[str]) -> bool:
    """Whether the nonempty edge support is strongly connected on incident vertices."""
    edges = tuple(edges)
    if not edges:
        return False
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming: dict[str, list[str]] = defaultdict(list)
    vertices = set()
    for edge in edges:
        u, v = endpoints(edge)
        vertices.update((u, v))
        outgoing[u].append(v)
        incoming[v].append(u)
    start = next(iter(vertices))
    for adjacency in (outgoing, incoming):
        seen = set()
        stack = [start]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            stack.extend(adjacency[u])
        if seen != vertices:
            return False
    return True


def euler_supports(edges: Sequence[str], *, max_edges: int = MAX_EDGE_TYPES) -> tuple[tuple[str, ...], ...]:
    """Enumerate every nonempty strongly connected edge subset exactly."""
    edges = tuple(sorted(set(edges)))
    if len(edges) == 0:
        return ()
    if len(edges) > max_edges:
        raise ValueError(f"reference support enumeration is capped at {max_edges} edge types")
    supports = []
    for size in range(1, len(edges) + 1):
        for support in combinations(edges, size):
            if strongly_connected_support(support):
                supports.append(support)
    return tuple(supports)


def _vertices(edges: Sequence[str]) -> tuple[str, ...]:
    return tuple(sorted({v for edge in edges for v in endpoints(edge)}))


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def _dot(row: Mapping[str, int | Fraction], vector: Mapping[str, int | Fraction]) -> Fraction:
    return sum((Fraction(row.get(edge, 0)) * Fraction(value) for edge, value in vector.items()), Fraction(0))


def _projection(vector: Mapping[str, int | Fraction], h: int) -> dict[str, Fraction]:
    out: dict[str, Fraction] = defaultdict(Fraction)
    for edge, value in vector.items():
        out[edge[:h]] += Fraction(value)
    return dict(out)


def _balance(vector: Mapping[str, int | Fraction]) -> dict[str, Fraction]:
    out: dict[str, Fraction] = defaultdict(Fraction)
    for edge, value in vector.items():
        u, v = endpoints(edge)
        out[u] -= Fraction(value)
        out[v] += Fraction(value)
    return dict(out)


@dataclass(frozen=True)
class SupportPairCertificate:
    support_s: tuple[str, ...]
    support_t: tuple[str, ...]
    coordinate: str
    sign: int
    rational_s: tuple[tuple[str, Fraction], ...]
    rational_t: tuple[tuple[str, Fraction], ...]
    scale: int
    integer_s: tuple[tuple[str, int], ...]
    integer_t: tuple[tuple[str, int], ...]
    source_s: str
    source_t: str
    target_s: int
    target_t: int

    def as_dict(self) -> dict[str, object]:
        def frac_items(items):
            return {edge: str(value) for edge, value in items}
        return {
            "support_s": list(self.support_s),
            "support_t": list(self.support_t),
            "coordinate": self.coordinate,
            "sign": self.sign,
            "rational_s": frac_items(self.rational_s),
            "rational_t": frac_items(self.rational_t),
            "scale": self.scale,
            "integer_s": dict(self.integer_s),
            "integer_t": dict(self.integer_t),
            "source_s": self.source_s,
            "source_t": self.source_t,
            "target_s": self.target_s,
            "target_t": self.target_t,
        }


def _support_pair_system(
    support_s: Sequence[str],
    support_t: Sequence[str],
    h: int,
    target_row: Mapping[str, int | Fraction],
    sign: int,
):
    if sign not in (-1, 1):
        raise ValueError("sign must be -1 or +1")
    if h < 1:
        raise ValueError("h must be positive")
    s = tuple(support_s)
    t = tuple(support_t)
    n = len(s) + len(t)
    equalities = []

    # D_S x = 0 and D_T y = 0.
    for vertex in _vertices(s):
        row = [0] * n
        for i, edge in enumerate(s):
            u, v = endpoints(edge)
            row[i] = int(v == vertex) - int(u == vertex)
        equalities.append((tuple(row), 0))
    for vertex in _vertices(t):
        row = [0] * n
        for j, edge in enumerate(t):
            u, v = endpoints(edge)
            row[len(s) + j] = int(v == vertex) - int(u == vertex)
        equalities.append((tuple(row), 0))

    # P_h,S x = P_h,T y.
    patterns = sorted({edge[:h] for edge in s + t})
    for pattern in patterns:
        row = [int(edge[:h] == pattern) for edge in s]
        row += [-int(edge[:h] == pattern) for edge in t]
        equalities.append((tuple(row), 0))

    inequalities = equality_inequalities(equalities)

    # Strict support is encoded exactly in the scaled cone as x_e >= 1, y_e >= 1.
    for i in range(n):
        row = [0] * n
        row[i] = -1
        inequalities.append((tuple(row), -1))

    # sign * (F_S x - F_T y) >= 1.
    row = []
    for edge in s:
        row.append(-sign * Fraction(target_row.get(edge, 0)))
    for edge in t:
        row.append(sign * Fraction(target_row.get(edge, 0)))
    inequalities.append((tuple(row), -1))
    return inequalities


def rational_pair_witness(
    support_s: Sequence[str],
    support_t: Sequence[str],
    h: int,
    target_row: Mapping[str, int | Fraction],
    sign: int,
) -> tuple[dict[str, Fraction], dict[str, Fraction]] | None:
    system = _support_pair_system(support_s, support_t, h, target_row, sign)
    point = feasible_point(system, len(support_s) + len(support_t))
    if point is None:
        return None
    if not satisfies(point, system):
        raise AssertionError("support-pair feasibility witness failed exact verification")
    s = tuple(support_s)
    t = tuple(support_t)
    x = {edge: point[i] for i, edge in enumerate(s)}
    y = {edge: point[len(s) + j] for j, edge in enumerate(t)}
    return x, y


def _scaled_integer_pair(
    x: Mapping[str, Fraction], y: Mapping[str, Fraction]
) -> tuple[int, dict[str, int], dict[str, int]]:
    scale = 1
    for value in list(x.values()) + list(y.values()):
        scale = _lcm(scale, Fraction(value).denominator)
    xi = {edge: int(Fraction(value) * scale) for edge, value in x.items()}
    yi = {edge: int(Fraction(value) * scale) for edge, value in y.items()}
    return scale, xi, yi


def _require_integer_counts(histogram: Mapping[str, int]) -> None:
    if any(not isinstance(count, int) or isinstance(count, bool) for count in histogram.values()):
        raise ValueError("edge multiplicities must be integers, not booleans or coerced values")


def euler_circuit(histogram: Mapping[str, int]) -> tuple[str, ...]:
    """Deterministic Hierholzer lift; integer zero entries are ignored.

    Counts must be integers (excluding bool), with nonempty positive support.
    Rational counts must be denominator-cleared before calling this helper.
    """
    _require_integer_counts(histogram)
    hist = Counter({edge: count for edge, count in histogram.items() if count})
    if not hist or any(count < 1 for count in hist.values()):
        raise ValueError("Euler histogram must be nonempty and positive")
    if any(value != 0 for value in _balance(hist).values()):
        raise ValueError("Euler histogram is not balanced")
    if not strongly_connected_support(tuple(hist)):
        raise ValueError("Euler support is not strongly connected")

    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in sorted(hist, reverse=True):
        u, _ = endpoints(edge)
        adjacency[u].extend([edge] * hist[edge])
    # Reverse-sort each bucket so pop() returns lexicographically smallest edge.
    for u in adjacency:
        adjacency[u].sort(reverse=True)

    start = endpoints(min(hist))[0]
    vertex_stack = [start]
    edge_stack: list[str] = []
    circuit: list[str] = []
    while vertex_stack:
        u = vertex_stack[-1]
        if adjacency[u]:
            edge = adjacency[u].pop()
            _, v = endpoints(edge)
            vertex_stack.append(v)
            edge_stack.append(edge)
        else:
            vertex_stack.pop()
            if edge_stack:
                circuit.append(edge_stack.pop())
    circuit.reverse()
    if Counter(circuit) != hist:
        raise AssertionError("Hierholzer lift did not use the requested histogram")
    if circuit:
        for a, b in zip(circuit, circuit[1:] + circuit[:1]):
            if endpoints(a)[1] != endpoints(b)[0]:
                raise AssertionError("Euler circuit endpoints do not match")
    return tuple(circuit)


def source_from_circuit(circuit: Sequence[str]) -> str:
    if not circuit:
        raise ValueError("source circuit must be nonempty")
    return "".join(edge[0] for edge in circuit)


def verify_integer_pair(
    x: Mapping[str, int],
    y: Mapping[str, int],
    h: int,
    target_row: Mapping[str, int | Fraction],
    sign: int,
) -> None:
    """Check integer multiplicities and the support-pair algebraic invariants.

    Noninteger counts raise ValueError; failed algebraic invariants retain
    AssertionError. Euler realizability is checked separately by euler_circuit.
    """
    _require_integer_counts(x)
    _require_integer_counts(y)
    if any(value < 1 for value in x.values()) or any(value < 1 for value in y.values()):
        raise AssertionError("support vector lost strict positivity")
    if any(value != 0 for value in _balance(x).values()):
        raise AssertionError("S integer vector is not balanced")
    if any(value != 0 for value in _balance(y).values()):
        raise AssertionError("T integer vector is not balanced")
    if _projection(x, h) != _projection(y, h):
        raise AssertionError("integer source projections differ")
    delta = _dot(target_row, x) - _dot(target_row, y)
    if sign * delta < 1:
        raise AssertionError("integer target discrepancy was lost")


def make_certificate(
    support_s: Sequence[str],
    support_t: Sequence[str],
    h: int,
    coordinate: str,
    target_row: Mapping[str, int | Fraction],
    sign: int,
    *,
    force_nonintegral_demo: bool = False,
) -> SupportPairCertificate | None:
    witness = rational_pair_witness(support_s, support_t, h, target_row, sign)
    if witness is None:
        return None
    x, y = witness

    # The support-pair system is homogeneous apart from lower bounds >=1.
    # Scaling a feasible point upward therefore preserves feasibility.  This
    # optional factor records denominator clearing explicitly even when the FM
    # routine happens to return an integral boundary point.
    if force_nonintegral_demo and all(v.denominator == 1 for v in (*x.values(), *y.values())):
        x = {edge: Fraction(3, 2) * value for edge, value in x.items()}
        y = {edge: Fraction(3, 2) * value for edge, value in y.items()}
        system = _support_pair_system(support_s, support_t, h, target_row, sign)
        point = tuple(x[edge] for edge in support_s) + tuple(y[edge] for edge in support_t)
        if not satisfies(point, system):
            raise AssertionError("scaled rational demonstration point became infeasible")

    scale, xi, yi = _scaled_integer_pair(x, y)
    verify_integer_pair(xi, yi, h, target_row, sign)
    circuit_s = euler_circuit(xi)
    circuit_t = euler_circuit(yi)
    source_s = source_from_circuit(circuit_s)
    source_t = source_from_circuit(circuit_t)
    order_s = len(next(iter(xi)))
    order_t = len(next(iter(yi)))
    if order_s != order_t:
        raise AssertionError("support-pair edge orders differ")
    if cyclic_counts(source_s, order_s) != Counter(xi):
        raise AssertionError("decoded S source has wrong periodic edge histogram")
    if cyclic_counts(source_t, order_t) != Counter(yi):
        raise AssertionError("decoded T source has wrong periodic edge histogram")
    target_s = _dot(target_row, xi)
    target_t = _dot(target_row, yi)
    if target_s.denominator != 1 or target_t.denominator != 1:
        raise AssertionError("integer circulation produced noninteger target value")
    return SupportPairCertificate(
        support_s=tuple(support_s),
        support_t=tuple(support_t),
        coordinate=coordinate,
        sign=sign,
        rational_s=tuple((edge, x[edge]) for edge in support_s),
        rational_t=tuple((edge, y[edge]) for edge in support_t),
        scale=scale,
        integer_s=tuple((edge, xi[edge]) for edge in support_s),
        integer_t=tuple((edge, yi[edge]) for edge in support_t),
        source_s=source_s,
        source_t=source_t,
        target_s=int(target_s),
        target_t=int(target_t),
    )


def find_certificate(
    edges: Sequence[str],
    h: int,
    target_rows: Mapping[str, Mapping[str, int | Fraction]],
    *,
    max_edges: int = MAX_EDGE_TYPES,
    force_nonintegral_demo: bool = False,
) -> tuple[SupportPairCertificate | None, dict[str, int]]:
    """Exhaust every ordered support pair, target coordinate and discrepancy sign."""
    edges = tuple(sorted(set(edges)))
    supports = euler_supports(edges, max_edges=max_edges)
    stats = {
        "edge_types": len(edges),
        "supports": len(supports),
        "ordered_support_pairs": len(supports) ** 2,
        "lp_instances": 0,
    }
    for support_s in supports:
        for support_t in supports:
            for coordinate in sorted(target_rows):
                row = target_rows[coordinate]
                for sign in (-1, 1):
                    stats["lp_instances"] += 1
                    certificate = make_certificate(
                        support_s,
                        support_t,
                        h,
                        coordinate,
                        row,
                        sign,
                        force_nonintegral_demo=force_nonintegral_demo,
                    )
                    if certificate is not None:
                        return certificate, stats
    return None, stats
