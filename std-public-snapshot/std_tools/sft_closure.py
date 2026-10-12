"""Exact reference horizon rank test for irreducible cyclic finite-type domains.

Scope: finite alphabets represented by distinct one-character symbols; cyclic
forbidden-m-block presentation; synchronous radius-r emission; every admissible
cyclic source is nonempty. Linearly allowed blocks that lie on no directed
cycle are trimmed before cyclic-domain tests. For k>1 the recurrent cyclic
emission graph must have no all-silent directed cycle. This is NOT a solver
for arbitrary STD rules.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import product


def allowed_blocks(alphabet, allowed_m, m, length):
    """All length-`length` blocks respecting the allowed m-block list."""
    if m < 1 or length < m:
        raise ValueError("require 1 <= m <= length")
    alphabet = tuple(alphabet)
    if not alphabet or len(set(alphabet)) != len(alphabet) or any(len(a) != 1 for a in alphabet):
        raise ValueError("alphabet needs distinct one-character symbols")
    allowed = set(allowed_m)
    if any(len(w) != m or set(w) - set(alphabet) for w in allowed):
        raise ValueError("invalid allowed m-block")
    return ["".join(w) for w in product(alphabet, repeat=length)
            if all("".join(w[j:j + m]) in allowed for j in range(length - m + 1))]


def _endpoints(word):
    return word[:-1], word[1:]


def recurrent_cyclic_edges(edges):
    """Return exactly the edges occurring in some directed closed walk.

    These are the allowed blocks that can occur in a finite cyclic source.
    Edges outside this recurrent cyclic core are transient: every cyclic edge
    histogram has zero in those coordinates.
    """
    edges = list(edges)
    outgoing = defaultdict(list)
    for w in edges:
        u, v = _endpoints(w)
        outgoing[u].append(v)

    def reaches(start, target):
        if start == target:
            return True
        seen, stack = {start}, [start]
        while stack:
            u = stack.pop()
            for v in outgoing[u]:
                if v == target:
                    return True
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return False

    return [w for w in edges
            if reaches(_endpoints(w)[1], _endpoints(w)[0])]


def strongly_connected(edges):
    """Whether all vertices incident to a nonempty edge set form one SCC."""
    if not edges:
        return False
    outgoing, incoming = defaultdict(list), defaultdict(list)
    vertices = set()
    for w in edges:
        u, v = _endpoints(w)
        vertices.update((u, v))
        outgoing[u].append(v)
        incoming[v].append(u)
    start = next(iter(vertices))
    for adjacency in (outgoing, incoming):
        seen, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node not in seen:
                seen.add(node)
                stack.extend(adjacency[node])
        if seen != vertices:
            return False
    return True


def silent_run_bound(edges, emission):
    """Maximum silent directed path length, or None for a silent cycle."""
    adj, vertices = defaultdict(list), set()
    for edge in edges:
        u, v = _endpoints(edge)
        vertices.update((u, v))
        if not emission(edge):
            adj[u].append(v)
    visiting, memo = set(), {}

    def longest(u):
        if u in visiting:
            raise ValueError("silent cycle")
        if u not in memo:
            visiting.add(u)
            memo[u] = max((1 + longest(v) for v in adj[u]), default=0)
            visiting.remove(u)
        return memo[u]

    try:
        return max((longest(v) for v in vertices), default=0)
    except ValueError:
        return None


def _rank(matrix, columns):
    """Exact Gaussian rank over Q for integral/rational row matrices."""
    a = [[Fraction(z) for z in row] for row in matrix]
    pivot_row = 0
    for col in range(columns):
        i = next((i for i in range(pivot_row, len(a)) if a[i][col]), None)
        if i is None:
            continue
        a[pivot_row], a[i] = a[i], a[pivot_row]
        pivot = a[pivot_row][col]
        for i in range(pivot_row + 1, len(a)):
            if a[i][col]:
                factor = a[i][col] / pivot
                for j in range(col, columns):
                    a[i][j] -= factor * a[pivot_row][j]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def _incidence_rows(edges):
    vertices = sorted({p for w in edges for p in _endpoints(w)})
    return [[int(w[1:] == v) - int(w[:-1] == v) for w in edges]
            for v in vertices]


def _prefix_rows(edges, h):
    patterns = sorted({w[:h] for w in edges})
    return [[int(w[:h] == pattern) for w in edges] for pattern in patterns]


def emission_rows(edges, radius, k, gap_bound, emit):
    """Rows F of L-local output-k contribution, indexed by output k-words."""
    d = (k - 1) * (gap_bound + 1)
    counts = defaultdict(lambda: [0] * len(edges))
    for col, w in enumerate(edges):
        parts = [emit(w[j:j + 2 * radius + 1]) for j in range(d + 1)]
        concatenated = "".join(parts)
        for offset in range(len(parts[0])):
            block = concatenated[offset:offset + k]
            if len(block) != k:
                raise AssertionError("silence bound violated by the allowed block")
            counts[block][col] += 1
    return counts


def exact_horizon_irreducible(alphabet, allowed_m, m, radius, emit, k):
    """Return exact H_T(k) for the irreducible recurrent cyclic domain.

    Linearly allowed edges that lie on no directed cycle are discarded first,
    because they occur in no finite cyclic source. For k=1, silent cycles are
    allowed. Raises NotImplementedError when the k>1 bounded-silence hypothesis
    fails, ValueError for an empty cyclic domain, and ValueError when the
    recurrent cyclic core has multiple SCCs. The latter case needs genuine
    cross-support compatibility; treating the SCCs separately is insufficient.
    Uses exact rational rank.
    """
    if k < 1 or radius < 0 or m < 1:
        raise ValueError("k,m must be >=1 and radius >=0")
    s = max(m, 2 * radius + 1)
    base = recurrent_cyclic_edges(allowed_blocks(alphabet, allowed_m, m, s))
    if not base:
        raise ValueError("empty cyclic domain")
    if not strongly_connected(base):
        raise ValueError(
            "reducible recurrent cyclic graph: cross-support compatibility "
            "requires the support-cone LP test"
        )
    r_bound = silent_run_bound(base, lambda w: emit(w[:2 * radius + 1]))
    if k > 1 and r_bound is None:
        raise NotImplementedError("silent cycle: bounded-silence theorem does not apply")
    if r_bound is None:  # k=1: no output look-ahead needed
        r_bound = 0
    L = s + (k - 1) * (r_bound + 1)
    edges = recurrent_cyclic_edges(allowed_blocks(alphabet, allowed_m, m, L))
    if not edges:
        raise AssertionError("nonempty cyclic domain lost under higher-block lifting")
    # Strong connectivity of a nonempty recurrent base core is invariant
    # under higher-block lifting. Keep this check defensively: failure means
    # the path-lift/recurrent-core implementation is inconsistent, not that
    # the user's already-irreducible cyclic domain became reducible.
    if not strongly_connected(edges):
        raise AssertionError(
            "irreducible recurrent base core split under higher-block lifting"
        )
    D = _incidence_rows(edges)
    F = list(emission_rows(edges, radius, k, r_bound, emit).values())
    for h in range(1, L + 1):
        base_rank = _rank(D + _prefix_rows(edges, h), len(edges))
        if _rank(D + _prefix_rows(edges, h) + F, len(edges)) == base_rank:
            return h
    raise AssertionError("L-local output additivity guarantees a horizon <= L")


def naive_global_rank_test(edges, h, rows):
    """Diagnostic only: valid as an iff only if the graph is strongly connected."""
    D, P = _incidence_rows(edges), _prefix_rows(edges, h)
    return _rank(D + P, len(edges)) == _rank(D + P + list(rows), len(edges))
