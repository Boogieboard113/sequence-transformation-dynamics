"""Exact fixed-length cyclic horizon checks for STD issue #87.

Model:
- binary alphabet
- identity transformation
- target statistic C_2
- allowed periodic 7-blocks from U=0011 and V=000111

The universal result is proved in the accompanying candidate theorem note.
This module supplies independent bounded exact checks and a deterministic JSON
packet. Standard library only; all counts are integers.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import product
import json

U = "0011"
V = "000111"
M = 7


def cyclic_blocks(word: str, order: int) -> Counter:
    if not word:
        raise ValueError("source word must be nonempty")
    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
        raise ValueError("order must be a positive integer")
    n = len(word)
    return Counter(
        "".join(word[(i + j) % n] for j in range(order))
        for i in range(n)
    )


def periodic_windows(word: str, order: int) -> tuple[str, ...]:
    counts = cyclic_blocks(word, order)
    # Recover the rooted phase windows rather than only their multiplicities.
    n = len(word)
    return tuple(
        "".join(word[(i + j) % n] for j in range(order))
        for i in range(n)
    )


def rotations(word: str) -> set[str]:
    return {word[i:] + word[:i] for i in range(len(word))}


ALLOWED = frozenset(periodic_windows(U, M) + periodic_windows(V, M))


def admissible(word: str) -> bool:
    return bool(word) and set(periodic_windows(word, M)) <= ALLOWED


def predicted_domain(length: int) -> set[str]:
    """Domain predicted by the two-cycle graph theorem at one fixed length."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    answer: set[str] = set()
    for base in (U, V):
        if length % len(base) == 0:
            word = base * (length // len(base))
            answer.update(rotations(word))
    return answer


def literal_domain(length: int) -> set[str]:
    """Literal independent filter over all 2^length rooted binary words."""
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    return {
        "".join(bits)
        for bits in product("01", repeat=length)
        if admissible("".join(bits))
    }


def graph_components() -> list[tuple[str, ...]]:
    """Return directed simple cycles in the literal allowed 7-block graph."""
    outgoing: dict[str, list[str]] = defaultdict(list)
    incoming = Counter()
    edge_by_pair: dict[tuple[str, str], str] = {}
    for edge in sorted(ALLOWED):
        source, target = edge[:-1], edge[1:]
        outgoing[source].append(target)
        incoming[target] += 1
        edge_by_pair[source, target] = edge

    vertices = set(outgoing) | set(incoming)
    if any(len(outgoing[v]) != 1 or incoming[v] != 1 for v in vertices):
        raise AssertionError("allowed graph is not disjoint directed cycles")

    visited: set[str] = set()
    cycles: list[tuple[str, ...]] = []
    for start in sorted(vertices):
        if start in visited:
            continue
        here = start
        edges = []
        local = set()
        while here not in local:
            if here in visited:
                raise AssertionError("cycle traversal entered an earlier component")
            local.add(here)
            visited.add(here)
            nxt = outgoing[here][0]
            edges.append(edge_by_pair[here, nxt])
            here = nxt
        if here != start:
            raise AssertionError("component did not close at its start")
        cycles.append(tuple(edges))
    return sorted(cycles, key=len)


def exact_horizon_on_words(words: set[str]) -> int | None:
    """Exact H_N(2) for a finite nonempty fixed-length identity domain."""
    if not words:
        return None
    targets = {word: tuple(sorted(cyclic_blocks(word, 2).items())) for word in words}
    for h in (1, 2):
        seen = {}
        for word in words:
            key = tuple(sorted(cyclic_blocks(word, h).items()))
            target = targets[word]
            if key in seen and seen[key] != target:
                break
            seen[key] = target
        else:
            return h
    raise AssertionError("identity transformation must have horizon at most 2")


def predicted_horizon(length: int) -> int | None:
    if not isinstance(length, int) or isinstance(length, bool) or length < 1:
        raise ValueError("length must be a positive integer")
    if length % 4 and length % 6:
        return None
    return 2 if length % 12 == 0 else 1


def fixed_length_row(length: int, *, literal: bool) -> dict:
    domain = literal_domain(length) if literal else predicted_domain(length)
    horizon = exact_horizon_on_words(domain)
    row = {
        "length": length,
        "rooted_words": len(domain),
        "predicted_horizon": predicted_horizon(length),
        "computed_horizon": horizon,
    }
    if domain:
        families = {
            "U": sorted(word for word in domain if word in rotations(U * (length // 4)))
            if length % 4 == 0 else [],
            "V": sorted(word for word in domain if word in rotations(V * (length // 6)))
            if length % 6 == 0 else [],
        }
        row["orbit_family_sizes"] = {name: len(words) for name, words in families.items()}
    return row


def validation_packet() -> dict:
    cycles = graph_components()
    if sorted(map(len, cycles)) != [4, 6]:
        raise AssertionError("unexpected allowed-graph cycle sizes")

    brute_rows = []
    for n in range(1, 13):
        actual = literal_domain(n)
        expected = predicted_domain(n)
        if actual != expected:
            raise AssertionError(("literal/predicted domain mismatch", n, actual ^ expected))
        h = exact_horizon_on_words(actual)
        if h != predicted_horizon(n):
            raise AssertionError(("fixed-length horizon mismatch", n, h))
        brute_rows.append(fixed_length_row(n, literal=True))

    formula_rows = []
    for n in range(1, 49):
        words = predicted_domain(n)
        h = exact_horizon_on_words(words)
        if h != predicted_horizon(n):
            raise AssertionError(("predicted-family horizon mismatch", n, h))
        formula_rows.append(fixed_length_row(n, literal=False))

    x = U * 3
    y = V * 2
    if len(x) != 12 or len(y) != 12:
        raise AssertionError("bad N=12 witness length")
    if not admissible(x) or not admissible(y):
        raise AssertionError("N=12 witness outside domain")
    if cyclic_blocks(x, 1) != cyclic_blocks(y, 1):
        raise AssertionError("N=12 witness does not collide at C1")
    if cyclic_blocks(x, 2) == cyclic_blocks(y, 2):
        raise AssertionError("N=12 witness does not separate at C2")

    return {
        "model": {
            "alphabet": ["0", "1"],
            "U": U,
            "V": V,
            "window_order": M,
            "allowed_windows": sorted(ALLOWED),
            "transformation": "identity",
            "target_order": 2,
        },
        "graph_cycle_sizes": sorted(map(len, cycles)),
        "brute_force_lengths_1_to_12": brute_rows,
        "predicted_family_lengths_1_to_48": formula_rows,
        "n12_witness": {
            "x": x,
            "y": y,
            "source_c1": dict(sorted(cyclic_blocks(x, 1).items())),
            "x_c2": dict(sorted(cyclic_blocks(x, 2).items())),
            "y_c2": dict(sorted(cyclic_blocks(y, 2).items())),
        },
        "scope_note": (
            "Finite checks support only the stated model; the universal "
            "fixed-length classification comes from the two-cycle/divisibility proof."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    encoded = json.dumps(validation_packet(), indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as stream:
            stream.write(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
