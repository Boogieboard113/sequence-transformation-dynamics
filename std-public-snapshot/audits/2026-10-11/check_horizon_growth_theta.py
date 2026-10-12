#!/usr/bin/env python3
"""Independent finite checks for the October 9 STD horizon-growth theorem.

Supporting evidence only, not a proof. This file deliberately reimplements the
small combinatorics and binary radius-one graph test using only the standard
library; it does not import STD production/audit code.
"""
from collections import Counter, defaultdict, deque
from itertools import product
import json


def words(alphabet, min_len, max_len):
    for n in range(min_len, max_len + 1):
        for w in product(alphabet, repeat=n):
            yield "".join(w)


def cyclic_counts(word, k):
    if not word:
        return Counter()
    n = len(word)
    return Counter(
        "".join(word[(i + j) % n] for j in range(k))
        for i in range(n)
    )


def primitive_root(word):
    for d in range(1, len(word) + 1):
        if len(word) % d == 0 and word == word[:d] * (len(word) // d):
            return word[:d]
    raise AssertionError("nonempty word has no primitive root")


def commutes(u, v):
    return u + v == v + u


def is_pstar(word, p):
    return not word or (
        len(word) % len(p) == 0 and word == p * (len(word) // len(p))
    )


def check_word_lemma():
    pair_count = 0
    instance_count = 0
    all_words = list(words("01", 1, 5))
    for u in all_words:
        for v in all_words:
            if commutes(u, v):
                continue
            pair_count += 1
            for h in range(1, 7):
                a = len(v) // len(u) + 2
                m = h + a
                W = u * (m + a) + v + u * (m - a) + v
                Z = (u * m + v) * 2
                L = m * len(u) + len(v)
                assert len(W) == len(Z) == 2 * L
                assert W[:L] != W[L:], (u, v, h)
                assert cyclic_counts(W, 2 * L) != cyclic_counts(Z, 2 * L)
                instance_count += 1
    return {
        "noncommuting_pairs": pair_count,
        "horizon_instances": instance_count,
    }


def check_source_histogram_lemma():
    pair_count = 0
    instance_count = 0
    source_words = list(words("01", 1, 4))
    for p in source_words:
        for q in source_words:
            pair_count += 1
            for h in range(1, 7):
                for a in range(1, 6):
                    m = h + a
                    X = p * (m + a) + q + p * (m - a) + q
                    Y = (p * m + q) * 2
                    assert cyclic_counts(X, h) == cyclic_counts(Y, h), (
                        p, q, h, a
                    )
                    instance_count += 1
    return {
        "source_word_pairs": pair_count,
        "instances": instance_count,
    }


VERTICES = ["".join(w) for w in product("01", repeat=2)]
EDGES = ["".join(w) for w in product("01", repeat=3)]
TAIL = {e: e[:2] for e in EDGES}
HEAD = {e: e[1:] for e in EDGES}
OUT = defaultdict(list)
for edge in EDGES:
    OUT[TAIL[edge]].append(edge)
for vertex in OUT:
    OUT[vertex].sort()


def shortest_path(start, target):
    if start == target:
        return []
    queue = deque([(start, [])])
    seen = {start}
    while queue:
        vertex, path = queue.popleft()
        for edge in OUT[vertex]:
            nxt = HEAD[edge]
            if nxt == target:
                return path + [edge]
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [edge]))
    raise AssertionError("full binary de Bruijn graph should be strongly connected")


BASE = "00"
A_PATH = {v: shortest_path(BASE, v) for v in VERTICES}
B_PATH = {v: shortest_path(v, BASE) for v in VERTICES}
TEST_WALKS = [A_PATH[v] + B_PATH[v] for v in VERTICES]
TEST_WALKS += [
    A_PATH[TAIL[e]] + [e] + B_PATH[HEAD[e]]
    for e in EDGES
]


def emitted(walk, labels):
    return "".join(labels[e] for e in walk)


def phase_test_pair(labels):
    outputs = [emitted(walk, labels) for walk in TEST_WALKS]
    first = next((i for i, out in enumerate(outputs) if out), None)
    if first is None:
        return True, None
    u = outputs[first]
    p = primitive_root(u)
    bad = next(
        (i for i, out in enumerate(outputs) if not is_pstar(out, p)),
        None,
    )
    if bad is None:
        return True, None
    v = outputs[bad]
    assert v
    return False, (TEST_WALKS[first], TEST_WALKS[bad], u, v)


def silent_acyclic(labels):
    adjacency = defaultdict(list)
    for edge in EDGES:
        if labels[edge] == "":
            adjacency[TAIL[edge]].append(HEAD[edge])

    visiting = set()
    done = set()

    def visit(vertex):
        if vertex in visiting:
            return False
        if vertex in done:
            return True
        visiting.add(vertex)
        for nxt in adjacency[vertex]:
            if not visit(nxt):
                return False
        visiting.remove(vertex)
        done.add(vertex)
        return True

    return all(visit(v) for v in VERTICES)


def source_word(walk):
    # Reading the final source symbol of each higher-block edge yields the
    # cyclic source word; any context shift is irrelevant to raw histograms.
    return "".join(edge[-1] for edge in walk)


def check_radius_one_rules():
    phase_pass = 0
    phase_fail = 0
    silent_acyclic_count = 0
    all_finite_by_graph_test = 0
    nonperiodic_all_finite = 0
    witness_checks = 0

    for values in product(("", "0", "1"), repeat=len(EDGES)):
        labels = dict(zip(EDGES, values))
        acyclic = silent_acyclic(labels)
        if acyclic:
            silent_acyclic_count += 1

        passed, pair = phase_test_pair(labels)
        if passed:
            phase_pass += 1
        else:
            phase_fail += 1
            P, Q, u, v = pair
            assert not commutes(u, v), (u, v)
            if acyclic:
                nonperiodic_all_finite += 1

            for h in (1, 2, 5):
                a = len(v) // len(u) + 2
                m = h + a
                X = P * (m + a) + Q + P * (m - a) + Q
                Y = (P * m + Q) * 2

                assert cyclic_counts(source_word(X), h) == cyclic_counts(
                    source_word(Y), h
                )

                Xout = emitted(X, labels)
                Yout = emitted(Y, labels)
                k = 2 * len(u) * h + 2 * a * len(u) + 2 * len(v)
                assert len(Xout) == len(Yout) == k
                assert cyclic_counts(Xout, k) != cyclic_counts(Yout, k)
                witness_checks += 1

        if acyclic or passed:
            all_finite_by_graph_test += 1

    result = {
        "rules": 3 ** len(EDGES),
        "phase_pass": phase_pass,
        "phase_fail_nonperiodic": phase_fail,
        "silent_acyclic": silent_acyclic_count,
        "all_finite_by_graph_test": all_finite_by_graph_test,
        "nonperiodic_all_finite": nonperiodic_all_finite,
        "constructed_witness_checks": witness_checks,
    }

    assert result == {
        "rules": 6561,
        "phase_pass": 525,
        "phase_fail_nonperiodic": 6036,
        "silent_acyclic": 2432,
        "all_finite_by_graph_test": 2879,
        "nonperiodic_all_finite": 2354,
        "constructed_witness_checks": 18108,
    }
    return result


def main():
    result = {
        "word_lemma": check_word_lemma(),
        "source_histogram_lemma": check_source_histogram_lemma(),
        "binary_radius_one": check_radius_one_rules(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
