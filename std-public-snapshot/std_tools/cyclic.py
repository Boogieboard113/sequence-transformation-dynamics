"""Finite cyclic block counts and bounded finite-sample horizon checks.
Neither function is a general decision procedure for STD.
"""
from collections import Counter

def cyclic_block_counts(word, order):
    """Raw cyclic k-block counts, including for k > len(word)."""
    if not isinstance(order, int) or order < 1:
        raise ValueError("order must be a positive integer")
    n = len(word)
    if n == 0:
        return Counter()
    return Counter(tuple(word[(i + j) % n] for j in range(order)) for i in range(n))

def empirical_min_horizon(source_words, transform, output_order, max_h):
    """Return first sample-supported h, or None; None is NOT an infinity certificate."""
    if not isinstance(max_h, int) or max_h < 1:
        raise ValueError("max_h must be a positive integer")
    words = list(source_words)
    if any(len(w) == 0 for w in words):
        raise ValueError("source words must be nonempty")
    targets = [cyclic_block_counts(transform(w), output_order) for w in words]
    for h in range(1, max_h + 1):
        seen = {}
        consistent = True
        for w, tgt in zip(words, targets):
            key = frozenset(cyclic_block_counts(w, h).items())
            if key in seen and seen[key] != tgt:
                consistent = False
                break
            seen[key] = tgt
        if consistent:
            return h
    return None
