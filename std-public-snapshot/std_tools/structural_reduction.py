"""Exact forced-continuation contraction for finite cyclic block histograms.

A reduced edge is a path of original h-block edges. Only *distinct positive
edge types* determine branching: multiplicity is not a new choice. Every
output and constraint claim refers to cyclic walks, including wraparound.
Standard library only. This is not a general-purpose optimizer for arbitrary
nonlocal source domains; unencoded predicates must be checked after lifting.
"""
from collections import Counter, defaultdict
from dataclasses import dataclass
from math import inf


@dataclass(frozen=True)
class Macro:
    start: str
    end: str
    path: tuple[str, ...]
    count: int


@dataclass
class Reduction:
    kind: str                       # infeasible, cycle, branched
    histogram: Counter
    order: int
    macros: dict[str, Macro]         # named by first h-block edge
    cycle: tuple[str, ...]          # one full period if kind == cycle
    copies: int                     # number of repeated periods
    branches: tuple[str, ...]


def raw_histogram(word: str, h: int) -> Counter:
    """Independent baseline; cyclic counts even when h > len(word)."""
    if h < 1:
        raise ValueError('h must be positive')
    return Counter(''.join(word[(i + j) % len(word)] for j in range(h))
                   for i in range(len(word))) if word else Counter()


def _new(kind, hist, h, macros=None, cycle=(), copies=0, branches=()):
    return Reduction(kind, hist, h, macros or {}, tuple(cycle), copies,
                     tuple(sorted(branches)))


def reduce_histogram(histogram) -> Reduction:
    """Certificate-producing deterministic corridor reduction.

    Invalid (unbalanced or disconnected) edge multisets are represented by
    'infeasible', not silently repaired. Empty source is excluded.
    """
    hist = Counter({e: c for e, c in histogram.items() if c != 0})
    if any(not isinstance(e, str) or not e or not isinstance(c, int) or c < 0
           for e, c in histogram.items()):
        raise ValueError('edges must be nonempty strings with nonnegative integer counts')
    if not hist:
        return _new('infeasible', hist, 0)
    h = len(next(iter(hist)))
    if any(len(e) != h for e in hist):
        raise ValueError('edge lengths must coincide')
    outs = defaultdict(list)
    ins = Counter()
    outcounts = Counter()
    undirected = defaultdict(set)
    for e, c in sorted(hist.items()):
        u, v = e[:-1], e[1:]
        outs[u].append(e)
        outcounts[u] += c
        ins[v] += c
        undirected[u].add(v)
        undirected[v].add(u)
    vertices = set(ins) | set(outcounts)
    if any(ins[v] != outcounts[v] for v in vertices):
        return _new('infeasible', hist, h)
    start = min(vertices)
    reached = {start}
    stack = [start]
    while stack:
        for v in undirected[stack.pop()]:
            if v not in reached:
                reached.add(v)
                stack.append(v)
    if reached != vertices:
        return _new('infeasible', hist, h)
    # Balanced and weakly connected positive support => strongly connected.
    branch = tuple(sorted(v for v in vertices if len(outs[v]) > 1))
    if not branch:
        # The support is a single directed cycle (possibly a self-loop).
        v = start
        path = []
        seen = set()
        while v not in seen:
            seen.add(v)
            e = outs[v][0]
            path.append(e)
            v = e[1:]
        if v != start or len(seen) != len(vertices):
            raise AssertionError('balanced connected deterministic support must be a cycle')
        copies = hist[path[0]]
        if any(hist[e] != copies for e in path):
            raise AssertionError('cycle flow not constant')
        return _new('cycle', hist, h, cycle=path, copies=copies)

    macros = {}
    branch_set = set(branch)
    for u in branch:
        for first in outs[u]:
            e = first
            path = [e]
            visited = set()
            v = e[1:]
            while v not in branch_set:
                if v in visited or len(outs[v]) != 1:
                    raise AssertionError('nonbranch deterministic cycle in strongly connected support')
                visited.add(v)
                e = outs[v][0]
                path.append(e)
                v = e[1:]
            macros[first] = Macro(u, v, tuple(path), hist[first])

    coverage = Counter()
    for macro in macros.values():
        for e in macro.path:
            coverage[e] += macro.count
    if coverage != hist:
        raise AssertionError(f'bad flow certificate: {coverage} != {hist}')
    reduced_in = Counter()
    reduced_out = Counter()
    for macro in macros.values():
        reduced_out[macro.start] += macro.count
        reduced_in[macro.end] += macro.count
    if any(reduced_in[v] != reduced_out[v] for v in branch):
        raise AssertionError('reduction changed degree balance')
    return _new('branched', hist, h, macros=macros, branches=branch)


def reduced_circuits(red: Reduction):
    """Enumerate edge-type Euler circuits anchored at the least branch vertex.

    Exponential reference algorithm, appropriate only for small instances.
    Pure-cycle cases have no macro-circuits and must be handled separately.
    """
    if red.kind != 'branched':
        return
    at = red.branches[0]
    start = at
    left = {k: macro.count for k, macro in red.macros.items()}
    total = sum(left.values())
    prefix = []
    def visit(v):
        if len(prefix) == total:
            if v == start:
                yield tuple(prefix)
            return
        for k in sorted(left):
            m = red.macros[k]
            if left[k] and m.start == v:
                left[k] -= 1
                prefix.append(k)
                yield from visit(m.end)
                prefix.pop()
                left[k] += 1
    yield from visit(at)


def lift_edges(red: Reduction, macro_circuit=()) -> tuple[str, ...]:
    """Canonical edge-type lift, anchored at a branch or periodic-cycle vertex."""
    if red.kind == 'infeasible':
        raise ValueError('histogram has no cyclic source realization')
    if red.kind == 'cycle':
        return red.cycle * red.copies
    return tuple(e for name in macro_circuit for e in red.macros[name].path)


def source_from_edges(red: Reduction, edges) -> str:
    """Construct and verify a cyclic source word from a purported Euler walk."""
    edges = tuple(edges)
    if not edges or any(len(e) != red.order for e in edges):
        raise ValueError('no complete source walk')
    if any(a[1:] != b[:-1] for a, b in zip(edges, edges[1:] + edges[:1])):
        raise ValueError('edge walk is not cyclically consecutive')
    if Counter(edges) != red.histogram:
        raise ValueError('edge walk has wrong multiplicities')
    word = ''.join(e[0] for e in edges)
    if raw_histogram(word, red.order) != red.histogram:
        raise AssertionError('Euler-walk reconstruction failed')
    return word


def cyclic_class(word: str) -> str:
    """Canonical rotation; empty output is an explicit singleton."""
    return min((word[i:] + word[:i] for i in range(len(word))), default='')


def emission_of_edges(edges, emission) -> str:
    return ''.join(emission[e] for e in edges)


def erased_signature(flags):
    """Finite linear interval signature (length, prefix, suffix, maximum)."""
    flags = tuple(flags)
    n = len(flags)
    p = next((i for i, x in enumerate(flags) if not x), n)
    s = next((i for i, x in enumerate(reversed(flags)) if not x), n)
    run = longest = 0
    for x in flags:
        run = run + 1 if x else 0
        longest = max(longest, run)
    return (n, p, s, longest)


def join_signatures(a, b):
    """Associative signature product for adjoining two intervals."""
    n, p, s, maximum = a
    m, q, t, other = b
    return (n + m, p + q if p == n else p,
            t + s if t == m else t, max(maximum, other, s + q))


def cyclic_erased_max(sign):
    """Maximal erased run in a bi-infinite periodic extension.

    All-erased cyclic words have an unbounded run (infinity).
    """
    n, p, s, maximum = sign
    if n == 0 or p == n:
        return inf
    return max(maximum, s + p)


def macro_signature(macro: Macro, emission):
    return erased_signature(emission[e] == '' for e in macro.path)


def erased_max_from_reduction(red: Reduction, macro_circuit, emission):
    """Erased-run cap tested without expanding macro paths."""
    if red.kind == 'infeasible':
        raise ValueError('no source word')
    if red.kind == 'cycle':
        base = erased_signature(emission[e] == '' for e in red.cycle)
        sign = (0, 0, 0, 0)
        for _ in range(red.copies):
            sign = join_signatures(sign, base)
        return cyclic_erased_max(sign)
    sign = (0, 0, 0, 0)
    for key in macro_circuit:
        sign = join_signatures(sign, macro_signature(red.macros[key], emission))
    return cyclic_erased_max(sign)


@dataclass(frozen=True)
class ForbiddenSummary:
    """Composable source-word summary for a fixed finite forbidden-word set."""
    length: int
    prefix: str
    suffix: str
    bad: bool


def _forbidden_set(forbidden_blocks):
    words = frozenset(forbidden_blocks)
    if any(not isinstance(w, str) or not w for w in words):
        raise ValueError('forbidden source blocks must be nonempty strings')
    return words


def forbidden_summary(word: str, forbidden_blocks) -> ForbiddenSummary:
    """Linear-word finite-type constraint summary. Independent of cut."""
    words = _forbidden_set(forbidden_blocks)
    width = max(map(len, words), default=1) - 1
    return ForbiddenSummary(len(word), word[:width], word[-width:] if width else '',
                            any(f in word for f in words))


def join_forbidden(a: ForbiddenSummary, b: ForbiddenSummary, forbidden_blocks):
    """Associative on summaries made for the *same* forbidden set."""
    words = _forbidden_set(forbidden_blocks)
    width = max(map(len, words), default=1) - 1
    boundary = a.suffix + b.prefix
    p = (a.prefix + b.prefix)[:width] if width else ''
    s = (a.suffix + b.suffix)[-width:] if width else ''
    return ForbiddenSummary(a.length + b.length, p, s,
                            a.bad or b.bad or any(f in boundary for f in words))


def forbidden_on_circle(sig: ForbiddenSummary, forbidden_blocks) -> bool:
    """Check all cyclic forbidden windows, including windows longer than n."""
    words = _forbidden_set(forbidden_blocks)
    if not words:
        return False
    if sig.length == 0:
        return False              # the model separately disallows empty source
    width = max(map(len, words))
    if sig.length < width:
        # The entire word fits into prefix (width-1). Repeat it periodically.
        word = sig.prefix
        periodic = word * (width // len(word) + 2)
        return any(periodic[i:i + len(f)] == f
                   for i in range(len(word)) for f in words)
    return sig.bad or any(f in sig.suffix + sig.prefix for f in words)


def forbidden_from_reduction(red: Reduction, macro_circuit, forbidden_blocks):
    """Evaluate a cyclic finite-type source constraint without full lifting."""
    if red.kind == 'infeasible':
        raise ValueError('no source word')
    words = _forbidden_set(forbidden_blocks)
    if not words:
        return False
    sig = forbidden_summary('', words)
    if red.kind == 'cycle':
        base = forbidden_summary(''.join(e[0] for e in red.cycle), words)
        for _ in range(red.copies):
            sig = join_forbidden(sig, base, words)
    else:
        for key in macro_circuit:
            path = red.macros[key].path
            sig = join_forbidden(sig,
                                 forbidden_summary(''.join(e[0] for e in path), words),
                                 words)
    return forbidden_on_circle(sig, words)


def all_attainable(red: Reduction, emission, erase_cap=None, rooted=False,
                   source_allowed=None, emission_lag=0, forbidden_blocks=()):
    """Exact small-instance outputs using macro tours and canonical lifts.

    By default yields cyclic output rotation classes. rooted=True adds all
    source-letter cuts, NOT all arbitrary output-letter cuts. Optional
    source_allowed(rooted_word) is an *exact* fallback for arbitrary source
    predicates, including those not invariant under cyclic rotation. It may
    require fully lifting each witness. emission_lag is the number of
    source sites *after* the starting h-block edge at which its emission is
    indexed (e.g. r for psi(e)=phi(e[:2*r+1]) from a centered radius-r
    local rule). It matters only for rooted outputs with root-sensitive
    predicates. forbidden_blocks is a finite cyclic source-type
    restriction certified via monoid summaries *without full source lifting*.
    Exponential in the number of reduced tours.
    """
    if erase_cap is not None and (not isinstance(erase_cap, int) or erase_cap < 0):
        raise ValueError('erase_cap must be a nonnegative integer or None')
    forbidden_blocks = _forbidden_set(forbidden_blocks)
    if red.kind == 'infeasible':
        return set()
    circuits = [()] if red.kind == 'cycle' else reduced_circuits(red)
    answers = set()
    for path in circuits:
        if erase_cap is not None and erased_max_from_reduction(red, path, emission) > erase_cap:
            continue
        if forbidden_blocks and forbidden_from_reduction(red, path, forbidden_blocks):
            continue
        edges = lift_edges(red, path)
        source = source_from_edges(red, edges)   # certificate check
        if source_allowed is None:
            valid_roots = range(len(edges)) if rooted else (0,)
        else:
            valid_roots = [i for i in range(len(edges))
                           if source_allowed(source[i:] + source[:i])]
        if rooted:
            for i in valid_roots:
                j = (i - emission_lag) % len(edges)
                answers.add(emission_of_edges(edges[j:] + edges[:j], emission))
        elif valid_roots:
            answers.add(cyclic_class(emission_of_edges(edges, emission)))
    return answers


def exact_pattern_bounds(red: Reduction, emission, patterns, erase_cap=None,
                         source_allowed=None, forbidden_blocks=()):
    """Return (minimum, maximum) raw cyclic output counts for each pattern.

    Raises ValueError for an empty admissible source domain (no extrema).
    Brute-force over *reduced* circuits and therefore exponential in their
    number; exact arithmetic and no approximation.
    """
    words = all_attainable(red, emission, erase_cap, source_allowed=source_allowed,
                           forbidden_blocks=forbidden_blocks)
    if not words:
        raise ValueError('no admissible cyclic output')
    result = {}
    for p in patterns:
        if not p:
            raise ValueError('output pattern must be nonempty')
        counts = [raw_histogram(w, len(p))[p] for w in words]
        result[p] = (min(counts), max(counts))
    return result
