"""Deterministic result packet for STD issue #44 support-pair certificates."""
from __future__ import annotations

from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from experiments.support_pair_certificates import (
    cyclic_counts,
    euler_supports,
    find_certificate,
)

PINNED_MAIN = "private-history-omitted"
PR6_MERGE = "private-history-omitted"
PR25_MERGE = "private-history-omitted"

S = ("00110", "01100", "11001", "10011")
T = ("01010", "10101")
PR25_EDGES = S + T
PR25_ALLOWED = set(PR25_EDGES)
PR25_A_ROW = {edge: int(edge in S) for edge in PR25_EDGES}


def admissible_pr25(word: str) -> bool:
    return set(cyclic_counts(word, 5)).issubset(PR25_ALLOWED)


def transform_pr25(word: str) -> str:
    n = len(word)
    return "".join(
        "b" if "".join(word[(i + j - 2) % n] for j in range(5)) in T else "a"
        for i in range(n)
    )


def binary_words(max_length: int):
    for n in range(1, max_length + 1):
        for letters in product("01", repeat=n):
            yield "".join(letters)


def bounded_collision(words, h, target):
    """Find first equal-C_h pair with different exact integer target, if any."""
    seen = {}
    checked = 0
    for word in words:
        checked += 1
        key = tuple(sorted(cyclic_counts(word, h).items()))
        value = int(target(word))
        if key in seen and seen[key][1] != value:
            first, first_value = seen[key]
            return {
                "checked_words_until_witness": checked,
                "witness": [first, word],
                "target_values": [first_value, value],
            }
        seen.setdefault(key, (word, value))
    return {"checked_words": checked, "witness": None}


def pr25_packet():
    h1, stats1 = find_certificate(
        PR25_EDGES, 1, {"a": PR25_A_ROW}, force_nonintegral_demo=True
    )
    h2, stats2 = find_certificate(PR25_EDGES, 2, {"a": PR25_A_ROW})
    if h1 is None or h2 is not None:
        raise AssertionError("PR25 exact solver decisions disagree with named fixture")

    admissible = [word for word in binary_words(12) if admissible_pr25(word)]
    direct_h1 = bounded_collision(
        admissible, 1, lambda word: Counter(transform_pr25(word))["a"]
    )
    direct_h2 = bounded_collision(
        admissible, 2, lambda word: Counter(transform_pr25(word))["a"]
    )
    if direct_h1["witness"] is None or direct_h2["witness"] is not None:
        raise AssertionError("PR25 bounded direct enumeration disagrees with expected pattern")

    direct_s = Counter(transform_pr25(h1.source_s))["a"]
    direct_t = Counter(transform_pr25(h1.source_t))["a"]
    if (direct_s, direct_t) != (h1.target_s, h1.target_t):
        raise AssertionError("PR25 certificate target row disagrees with literal local rule")

    return {
        "edge_types": len(PR25_EDGES),
        "supports": [list(support) for support in euler_supports(PR25_EDGES)],
        "h1_exact_support_pair_decision": "insufficient",
        "h1_solver_stats_until_first_certificate": stats1,
        "h1_certificate": h1.as_dict(),
        "h1_bounded_direct": direct_h1,
        "h2_exact_support_pair_decision": "sufficient",
        "h2_solver_stats": stats2,
        "h2_bounded_direct": direct_h2,
        "bounded_direct_domain": {
            "max_source_length": 12,
            "admissible_rooted_words": len(admissible),
        },
        "interpretation": (
            "h2 sufficiency is theorem-backed by exhaustive exact support-pair infeasibility; "
            "the bounded word search is supporting evidence only"
        ),
    }


def full_bigram_packet():
    edges = ("00", "01", "10", "11")
    row = {edge: int(edge == "00") for edge in edges}
    h1, stats1 = find_certificate(edges, 1, {"b": row})
    h2, stats2 = find_certificate(edges, 2, {"b": row})
    if h1 is None or h2 is not None:
        raise AssertionError("full-bigram exact solver decisions are wrong")

    words = list(binary_words(8))
    target = lambda word: cyclic_counts(word, 2)["00"]
    direct_h1 = bounded_collision(words, 1, target)
    direct_h2 = bounded_collision(words, 2, target)
    if direct_h1["witness"] is None or direct_h2["witness"] is not None:
        raise AssertionError("full-bigram bounded direct enumeration disagrees")
    if cyclic_counts(h1.source_s, 2)["00"] != h1.target_s:
        raise AssertionError("full-bigram S certificate target mismatch")
    if cyclic_counts(h1.source_t, 2)["00"] != h1.target_t:
        raise AssertionError("full-bigram T certificate target mismatch")

    return {
        "edge_types": 4,
        "support_count": len(euler_supports(edges)),
        "supports": [list(support) for support in euler_supports(edges)],
        "h1_exact_support_pair_decision": "insufficient",
        "h1_solver_stats_until_first_certificate": stats1,
        "h1_certificate": h1.as_dict(),
        "h1_bounded_direct": direct_h1,
        "h2_exact_support_pair_decision": "sufficient",
        "h2_solver_stats": stats2,
        "h2_bounded_direct": direct_h2,
        "bounded_direct_domain": {"max_source_length": 8, "rooted_words": len(words)},
        "interpretation": (
            "proper strongly connected sub-supports are enumerated explicitly; "
            "bounded direct enumeration is not the proof of h2 sufficiency"
        ),
    }


def main():
    packet = {
        "status": "pass",
        "issue": 44,
        "pinned_main": PINNED_MAIN,
        "accepted_support_pair_theorem_merge": PR6_MERGE,
        "reviewed_worked_example_merge": PR25_MERGE,
        "arithmetic": "fractions.Fraction only",
        "random_seed": None,
        "edge_type_cap": 8,
        "pr25_fixture": pr25_packet(),
        "full_binary_bigram_fixture": full_bigram_packet(),
        "limitations": [
            "implementation is a small exact reference solver, not a practical general LP engine",
            "edge supports are exhaustively enumerated only up to eight recurrent edge types",
            "fixed length, fixed inventory, upper count bounds, and other nonhomogeneous domains are excluded",
            "bounded direct-word searches are supporting evidence and are not substituted for the accepted theorem",
        ],
    }
    print(json.dumps(packet, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
