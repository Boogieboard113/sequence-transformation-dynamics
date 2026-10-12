"""Independent finite-state weighted reset-gap audit tools.

This is a closed-run *scalar additive weight* model, not a solver for
arbitrary output-word statistics in Sequence Transformation Dynamics.

Run: python -m unittest discover -s tests -v
"""
from collections import Counter
from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Chart:
    a_next: tuple
    b_next: tuple
    a_weight: tuple
    b_weight: tuple
    q0: int = 0

    def __post_init__(self):
        n = len(self.a_next)
        if n == 0 or len(self.b_next) != n or len(self.a_weight) != n or len(self.b_weight) != n:
            raise ValueError('state arrays must have equal nonzero length')
        if self.q0 not in range(n) or any(t not in range(n) for t in self.a_next + self.b_next):
            raise ValueError('invalid state index')

    def run(self, source, start):
        state, total = start, 0
        for symbol in source:
            if symbol == 'a':
                total += self.a_weight[state]
                state = self.a_next[state]
            elif symbol == 'b':
                total += self.b_weight[state]
                state = self.b_next[state]
            else:
                raise ValueError('source must use a or b')
        return total if state == start else None

    def orbit(self):
        seen, states, state = {}, [], self.q0
        while state not in seen:
            seen[state] = len(states)
            states.append(state)
            state = self.a_next[state]
        return seen[state], len(states) - seen[state], tuple(states)

    def require_reset_on_orbit(self):
        mu, period, states = self.orbit()
        if any(self.b_next[q] != self.q0 for q in states):
            raise ValueError('every b on the q0 a-orbit must reset to q0')
        return mu, period, states

    def gap_weight(self, n):
        if n < 0:
            raise ValueError('gap length must be nonnegative')
        self.require_reset_on_orbit()
        state, total = self.q0, 0
        for _ in range(n):
            total += self.a_weight[state]
            state = self.a_next[state]
        return total + self.b_weight[state]


def exact_orbit_horizon(chart):
    """Exact minimum h on freely concatenable b-bearing reset-orbit cycles.

    None means infinite. This does NOT characterize all closed runs of the
    chart unless the domain is restricted or every b resets globally.
    """
    mu, period, _ = chart.require_reset_on_orbit()
    f = [chart.gap_weight(n) for n in range(mu + period + 2)]
    increments = [f[n + 1] - f[n] for n in range(mu, mu + period)]
    if len(set(increments)) != 1:
        return None
    bad = [n for n in range(mu) if f[n + 2] - 2 * f[n + 1] + f[n] != 0]
    return max(bad, default=-1) + 2


def exact_all_run_horizon_under_global_reset(chart):
    """Exact H over ALL nonempty closed runs when every b resets to q0.

    Unlike exact_orbit_horizon, also checks b-free a-cycles. Returns None if
    the horizon is infinite. Rejects charts lacking the global reset premise.
    """
    if any(t != chart.q0 for t in chart.b_next):
        raise ValueError('all b transitions must reset globally to q0')
    h = exact_orbit_horizon(chart)
    if h is None:
        return None
    seen_global, means = set(), []
    for start in range(len(chart.a_next)):
        if start in seen_global:
            continue
        route, local_index, q = [], {}, start
        while q not in seen_global and q not in local_index:
            local_index[q] = len(route)
            route.append(q)
            q = chart.a_next[q]
        if q in local_index:
            cycle = route[local_index[q]:]
            means.append((sum(chart.a_weight[x] for x in cycle), len(cycle)))
        seen_global.update(route)
    assert means
    numerator, denominator = means[0]
    if any(num * denominator != numerator * den for num, den in means[1:]):
        return None
    return h


def cyclic_histogram(word, order):
    if order < 1:
        raise ValueError('order must be positive')
    length = len(word)
    return Counter(''.join(word[(i + j) % length] for j in range(order))
                   for i in range(length)) if length else Counter()


def curvature_witness(chart, n):
    """If nonzero, equal-C_h witnesses for ALL h<=n+1 on the reset orbit."""
    x = 'b' + 'a' * n + 'b' + 'a' * (n + 2)
    y = 'b' + 'a' * (n + 1) + 'b' + 'a' * (n + 1)
    delta = chart.gap_weight(n) + chart.gap_weight(n + 2) - 2 * chart.gap_weight(n + 1)
    return x, y, delta


def find_collision(chart, order, max_length, orbit_only=False, exactly_one_b=False,
                   include_a_only=False):
    """Exhaustive SMALL LENGTH search; no find does not certify horizon."""
    starts = chart.orbit()[2] if orbit_only else range(len(chart.a_next))
    seen = {}
    for length in range(1, max_length + 1):
        for chars in product('ab', repeat=length):
            word = ''.join(chars)
            if (not include_a_only and 'b' not in word) or (exactly_one_b and word.count('b') != 1):
                continue
            key = tuple(sorted(cyclic_histogram(word, order).items()))
            for state in starts:
                value = chart.run(word, state)
                if value is None:
                    continue
                if key in seen and seen[key][2] != value:
                    return seen[key], (word, state, value)
                seen[key] = (word, state, value)
    return None
