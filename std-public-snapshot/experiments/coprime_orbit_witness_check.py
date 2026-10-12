#!/usr/bin/env python3
"""Bounded literal checks for the proposed two-orbit STD lower-bound family.

Independent of any STD support-pair formula: builds actual periodic windows,
constructs their overlap graph, and compares raw periodic histogram counts.
Checks are author-run finite evidence, not a universal proof or independent review.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import sys


def cyclic_windows(word: str, length: int):
    assert word and length > 0
    n = len(word)
    return ["".join(word[(j + k) % n] for k in range(length)) for j in range(n)]


def raw_count(word: str, k: int):
    return Counter(cyclic_windows(word, k))


def brute_check_small():
    """Unassisted enumeration of every binary rooted word at lengths 1..12."""
    p, q = 2, 5
    m = 2 * q + 1
    u, v = "0" * p + "1" * p, "0" * q + "1" * q
    allowed = set(cyclic_windows(u, m) + cyclic_windows(v, m))
    checked = 0
    for n in range(1, 13):
        actual = set()
        for letters in product("01", repeat=n):
            w = "".join(letters)
            checked += 1
            if all(x in allowed for x in cyclic_windows(w, m)):
                actual.add(w)
        expected = set()
        for base in [u, v]:
            if n % len(base) == 0:
                w = base * (n // len(base))
                expected |= {w[j:] + w[:j] for j in range(len(base))}
        assert actual == expected, (n, actual ^ expected)
    return checked


def check(p: int):
    assert 2 <= p <= 12
    q = 2 * p + 1
    m = 2 * q + 1
    u = "0" * p + "1" * p
    v = "0" * q + "1" * q
    u_edges = cyclic_windows(u, m)
    v_edges = cyclic_windows(v, m)
    assert len(set(u_edges)) == 2 * p
    assert len(set(v_edges)) == 2 * q
    assert set(u_edges).isdisjoint(v_edges)

    u_vertices = {w[:-1] for w in u_edges}
    v_vertices = {w[:-1] for w in v_edges}
    assert len(u_vertices) == 2 * p and len(v_vertices) == 2 * q
    assert u_vertices.isdisjoint(v_vertices)

    # Original higher-block graph: in/out degree one, two separate cycles.
    graph = defaultdict(list)
    indegree = Counter()
    for w in u_edges + v_edges:
        graph[w[:-1]].append(w[1:])
        indegree[w[1:]] += 1
    assert all(len(graph[x]) == 1 and indegree[x] == 1 for x in graph)
    assert len(graph) == 2 * p + 2 * q
    visited = set()
    sizes = []
    for start in graph:
        if start in visited:
            continue
        here = start
        length = 0
        while here not in visited:
            visited.add(here)
            length += 1
            here = graph[here][0]
        assert here == start
        sizes.append(length)
    assert sorted(sizes) == sorted([2 * p, 2 * q])

    # Actual rooted cyclic words: all blocks are periodically wrapped.
    X, Y = u * q, v * p
    assert len(X) == len(Y) == 2 * p * q
    assert raw_count(X, 1) == raw_count(Y, 1)
    assert raw_count(X, 2)["01"] == q
    assert raw_count(Y, 2)["01"] == p
    assert raw_count(X, 2) != raw_count(Y, 2)
    allowed = set(u_edges + v_edges)
    assert all(w in allowed for w in cyclic_windows(X, m))
    assert all(w in allowed for w in cyclic_windows(Y, m))

    # All roots of the two verified graph cycles through shortest length.
    # This loop uses the graph classification; it is not independent proof.
    for n in range(1, 2 * p * q + 1):
        candidates = []
        for base in [u, v]:
            if n % len(base) == 0:
                word = base * (n // len(base))
                candidates.extend(word[j:] + word[:j] for j in range(len(base)))
        candidates = list(dict.fromkeys(candidates))
        for i in range(len(candidates)):
            for j in range(i + 1, len(candidates)):
                a, b = candidates[i], candidates[j]
                if raw_count(a, 1) == raw_count(b, 1) and raw_count(a, 2) != raw_count(b, 2):
                    assert n == 2 * p * q, (p, n, a, b)

    # Rational support-pair vertex; exact Fraction arithmetic.
    vertex_alpha = Fraction(q, p)
    assert vertex_alpha.denominator == p
    assert vertex_alpha >= 1 and vertex_alpha - 1 >= 1
    assert 2 * p * vertex_alpha == 2 * q
    assert 2 * q * 1 == 2 * q
    E = 2 * p + 2 * q
    assert 2 * p * q == (E - 2) * (E + 1) // 9
    return p, q, m, E, vertex_alpha, 2 * p * q, len(graph)


if __name__ == "__main__":
    print("Python", sys.version.split()[0], "exact Fraction checks; p=2..12")
    print("p q m E vertex_alpha shortest_length vertices")
    for p in range(2, 13):
        print(*check(p))
    print("Unassisted rooted binary exhaustive p=2 n=1..12:", brute_check_small(), "words")
    print("PASS: 11 sizes; exact graph/window and full single-orbit checks")
