"""Bounded rooted-output inverse-counting oracle for STD issue #3.

This module is deliberately independent of any production inverse-counting code.
It performs literal exhaustive enumeration of rooted source words over explicitly
requested positive source lengths.  It is evidence for those finite bounds only;
it is not a general inverse theorem or an all-length decision procedure.
"""
from __future__ import annotations

from itertools import product
from math import comb
from typing import Iterable, Mapping, Sequence


def _validate_alphabet(alphabet: Sequence[str]) -> tuple[str, ...]:
    symbols = tuple(alphabet)
    if not symbols:
        raise ValueError("alphabet must be nonempty")
    if len(set(symbols)) != len(symbols):
        raise ValueError("alphabet symbols must be distinct")
    if any(not isinstance(a, str) or len(a) != 1 for a in symbols):
        raise ValueError("alphabet symbols must be one-character strings")
    return symbols


def _contexts(alphabet: Sequence[str], radius: int) -> tuple[str, ...]:
    if not isinstance(radius, int) or isinstance(radius, bool) or radius < 0:
        raise ValueError("radius must be a nonnegative integer")
    symbols = _validate_alphabet(alphabet)
    width = 2 * radius + 1
    return tuple("".join(t) for t in product(symbols, repeat=width))


def validate_rule(
    alphabet: Sequence[str], radius: int, emission: Mapping[str, str]
) -> tuple[str, ...]:
    """Validate a total local rule and return the normalized source alphabet."""
    symbols = _validate_alphabet(alphabet)
    expected = set(_contexts(symbols, radius))
    if set(emission) != expected:
        missing = sorted(expected - set(emission))
        extra = sorted(set(emission) - expected)
        raise ValueError(f"emission must be total: missing={missing}, extra={extra}")
    if any(not isinstance(v, str) for v in emission.values()):
        raise ValueError("every emitted value must be a string")
    return symbols


def periodic_context(word: str, center: int, radius: int) -> str:
    """Literal periodic source context, including repeated wrap for short words."""
    if not word:
        raise ValueError("oracle domain uses positive source lengths")
    return "".join(word[(center + offset) % len(word)] for offset in range(-radius, radius + 1))


def emit_rooted(
    word: str,
    alphabet: Sequence[str],
    radius: int,
    emission: Mapping[str, str],
) -> str:
    """Apply the local rule at source sites 0..n-1 and retain the source cut."""
    symbols = validate_rule(alphabet, radius, emission)
    if not isinstance(word, str) or not word:
        raise ValueError("word must be a nonempty string")
    if any(ch not in symbols for ch in word):
        raise ValueError("word contains a symbol outside the source alphabet")
    return "".join(
        emission[periodic_context(word, i, radius)] for i in range(len(word))
    )


def enumerate_rooted_preimages(
    alphabet: Sequence[str],
    radius: int,
    emission: Mapping[str, str],
    target: str,
    lengths: Iterable[int],
) -> tuple[str, ...]:
    """Enumerate rooted source words mapping exactly to ``target``.

    Counted objects are source words x in A^n. Rotations of x are distinct unless
    they are literally the same word. The output cut is retained: a rotated output
    is not accepted unless it equals ``target`` as a string.
    """
    symbols = validate_rule(alphabet, radius, emission)
    if not isinstance(target, str):
        raise ValueError("target must be a string")
    ns = tuple(lengths)
    if not ns:
        raise ValueError("at least one source length is required")
    if any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in ns):
        raise ValueError("all source lengths must be positive integers")
    if len(set(ns)) != len(ns):
        raise ValueError("source lengths must be distinct")

    preimages: list[str] = []
    for n in sorted(ns):
        for letters in product(symbols, repeat=n):
            word = "".join(letters)
            if emit_rooted(word, symbols, radius, emission) == target:
                preimages.append(word)
    return tuple(preimages)


def count_rooted_preimages(
    alphabet: Sequence[str],
    radius: int,
    emission: Mapping[str, str],
    target: str,
    lengths: Iterable[int],
) -> int:
    """Return the bounded exhaustive rooted-source count."""
    return len(enumerate_rooted_preimages(alphabet, radius, emission, target, lengths))


def distinct_rotations(word: str) -> tuple[str, ...]:
    if not word:
        return ("",)
    return tuple(sorted({word[i:] + word[:i] for i in range(len(word))}))


def count_output_rotation_equivalent(
    alphabet: Sequence[str],
    radius: int,
    emission: Mapping[str, str],
    target: str,
    lengths: Iterable[int],
) -> int:
    """Diagnostic only: count sources whose output is any rotation of target.

    This is intentionally *not* the issue-#3 rooted oracle.  It exists solely to
    preserve examples where quotienting the output cut gives a different answer.
    """
    return sum(
        count_rooted_preimages(alphabet, radius, emission, z, lengths)
        for z in distinct_rotations(target)
    )


def _radius0_dp_count_reference(
    alphabet: Sequence[str], emission: Mapping[str, str], target: str, n: int
) -> int:
    """Independent exact comparator for radius 0 only.

    dp[t][j] counts length-t source prefixes whose concatenated emissions equal
    target[:j].  Empty emissions advance t without advancing j.  This algorithm
    does not enumerate source words, and is used only in its declared r=0 scope.
    """
    symbols = _validate_alphabet(alphabet)
    if set(emission) != set(symbols):
        raise ValueError("radius-0 emission keys must equal source symbols")
    if any(not isinstance(v, str) for v in emission.values()):
        raise ValueError("every emitted value must be a string")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")

    dp = [0] * (len(target) + 1)
    dp[0] = 1
    for _ in range(n):
        nxt = [0] * (len(target) + 1)
        for j, ways in enumerate(dp):
            if not ways:
                continue
            for a in symbols:
                u = emission[a]
                if target.startswith(u, j):
                    j2 = j + len(u)
                    if j2 <= len(target):
                        nxt[j2] += ways
        dp = nxt
    return dp[len(target)]


def _center_identity_rule(alphabet: Sequence[str], radius: int) -> dict[str, str]:
    return {ctx: ctx[radius] for ctx in _contexts(alphabet, radius)}


def _contextual_010_erasure_rule() -> dict[str, str]:
    rule = _center_identity_rule(("0", "1"), 1)
    rule["010"] = ""
    return rule


def named_examples() -> dict[str, object]:
    deletion = {"0": "", "1": "1"}
    identity = {"0": "0", "1": "1"}
    all_erase = {"0": "", "1": ""}
    contextual = _contextual_010_erasure_rule()
    ab_identity = {"a": "a", "b": "b"}

    examples: dict[str, object] = {}
    for name, alphabet, radius, emission, target, lengths in (
        ("deletion_multiple", ("0", "1"), 0, deletion, "11", (4,)),
        ("deletion_zero", ("0", "1"), 0, deletion, "11111", (4,)),
        ("identity_unique", ("0", "1"), 0, identity, "010", (3,)),
        ("all_erased", ("0", "1"), 0, all_erase, "", (3,)),
        ("contextual_short_period", ("0", "1"), 1, contextual, "0", (1, 2, 3, 4, 5, 6, 7, 8)),
        ("rooted_cut", ("a", "b"), 0, ab_identity, "ab", (2,)),
    ):
        pre = enumerate_rooted_preimages(alphabet, radius, emission, target, lengths)
        examples[name] = {
            "alphabet": "".join(alphabet),
            "radius": radius,
            "target": target,
            "lengths": list(lengths),
            "count": len(pre),
            "preimages": list(pre),
        }

    examples["rooted_cut"]["rotation_equivalent_count"] = count_output_rotation_equivalent(
        ("a", "b"), 0, ab_identity, "ab", (2,)
    )
    return examples


def run_validation() -> dict[str, object]:
    """Run deterministic bounded checks and return exact coverage statistics."""
    deletion = {"0": "", "1": "1"}
    identity = {"0": "0", "1": "1"}
    all_erase = {"0": "", "1": ""}

    formula_cases = 0
    for n in range(1, 9):
        for k in range(0, n + 2):
            target = "1" * k
            got = count_rooted_preimages(("0", "1"), 0, deletion, target, (n,))
            expected = comb(n, k) if k <= n else 0
            if got != expected:
                raise AssertionError(("deletion", n, target, got, expected))
            formula_cases += 1

    identity_cases = 0
    for n in range(1, 7):
        for letters in product(("0", "1"), repeat=n):
            target = "".join(letters)
            got = count_rooted_preimages(("0", "1"), 0, identity, target, (n,))
            if got != 1:
                raise AssertionError(("identity", n, target, got, 1))
            identity_cases += 1

    all_erasure_cases = 0
    for n in range(1, 9):
        got_empty = count_rooted_preimages(("0", "1"), 0, all_erase, "", (n,))
        got_nonempty = count_rooted_preimages(("0", "1"), 0, all_erase, "0", (n,))
        if got_empty != 2**n or got_nonempty != 0:
            raise AssertionError(("all_erase", n, got_empty, got_nonempty))
        all_erasure_cases += 2

    # Cross-check the exhaustive oracle against a non-enumerating exact DP only
    # in the DP's declared radius-0 scope.
    dp_cases = 0
    emission_words = ("", "0", "1", "00", "01")
    targets = ("", "0", "1", "00", "01", "10", "11", "000", "101")
    for image0 in emission_words:
        for image1 in emission_words:
            emission = {"0": image0, "1": image1}
            for n in range(1, 6):
                for target in targets:
                    brute = count_rooted_preimages(("0", "1"), 0, emission, target, (n,))
                    dp = _radius0_dp_count_reference(("0", "1"), emission, target, n)
                    if brute != dp:
                        raise AssertionError(("r0_dp", emission, n, target, brute, dp))
                    dp_cases += 1

    examples = named_examples()
    expected_named = {
        "deletion_multiple": 6,
        "deletion_zero": 0,
        "identity_unique": 1,
        "all_erased": 8,
        "contextual_short_period": 3,
        "rooted_cut": 1,
    }
    for name, expected in expected_named.items():
        got = examples[name]["count"]
        if got != expected:
            raise AssertionError(("named", name, got, expected))
    if examples["rooted_cut"]["rotation_equivalent_count"] != 2:
        raise AssertionError(("rooted_cut_rotation", examples["rooted_cut"]))

    return {
        "status": "pass",
        "provenance": {
            "repository": "STD sanitized snapshot",
            "base_main_commit": "private-history-omitted",
            "branch": "experiments/c-rooted-inverse-oracle",
            "issue": 3,
            "input_blobs": {
                "README.md": "private-history-omitted",
                "AGENTS.md": "private-history-omitted",
                "docs/RESEARCH_STATE.md": "private-history-omitted",
                "docs/TASK_BOARD.md": "private-history-omitted",
                "docs/CONCURRENCY_PROTOCOL.md": "private-history-omitted",
                "audits/archive/STD_Recovery_Spectrum_Status_2026-10-09.md": "private-history-omitted",
                "std_tools/cyclic.py": "private-history-omitted",
                "tests/test_cyclic.py": "private-history-omitted",
            },
            "production_inverse_comparator_on_pinned_main": None,
            "reference_archive_claim_used_only_for_named_fixture": "target 0 under contextual 010 erasure has reported complete fiber {0,01,10}; oracle checks lengths 1..8 only",
        },
        "counted_objects": "rooted source words",
        "source_lengths": "positive integers explicitly supplied to each bounded query",
        "output_equality": "exact rooted string equality",
        "erasure_semantics": "empty site emissions consume one source site and append no output symbols",
        "exact_arithmetic": True,
        "deterministic_seed": None,
        "coverage": {
            "deletion_formula_cases": formula_cases,
            "identity_formula_cases": identity_cases,
            "all_erasure_formula_cases": all_erasure_cases,
            "radius0_dp_crosscheck_cases": dp_cases,
            "named_examples": len(examples),
            "total_asserted_cases": formula_cases + identity_cases + all_erasure_cases + dp_cases + len(examples),
        },
        "named_examples": examples,
        "limitations": [
            "finite exhaustive source-length bounds only",
            "no source-rotation quotient; source words are counted",
            "no all-length finiteness/infinity decision",
            "radius-0 DP comparator is not used for contextual rules",
            "no production inverse-counting implementation exists on pinned main to cross-check",
        ],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_validation(), indent=2, sort_keys=True))
