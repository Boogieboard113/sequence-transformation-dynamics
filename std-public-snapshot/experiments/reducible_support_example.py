"""Exact worked reducible-support example for cyclic finite-type STD.

This module is intentionally self-contained.  It does not import the candidate
support-cone implementation from PR #6; it verifies the finite calculation
directly with exact Fraction arithmetic.

Domain:
    binary nonempty cyclic words whose periodic length-5 windows lie in ALLOWED.
Rule:
    radius-2 total local rule; the 01-cycle component emits "b" and every other
    context emits "a".  On the stated domain this means the 0011 component emits
    only "a" and the 01 component emits only "b".

Reproduce:
    python experiments/reducible_support_example.py
"""
from collections import Counter
from fractions import Fraction
import json


S_EDGES = ("00110", "01100", "11001", "10011")
T_EDGES = ("01010", "10101")
ALLOWED = frozenset(S_EDGES + T_EDGES)


def endpoints(edge):
    return edge[:-1], edge[1:]


def cyclic_counts(word, order):
    if not word or order < 1:
        raise ValueError("require a nonempty word and positive order")
    n = len(word)
    return Counter(
        "".join(word[(i + j) % n] for j in range(order))
        for i in range(n)
    )


def admissible(word):
    return set(cyclic_counts(word, 5)).issubset(ALLOWED)


def emit(context):
    """Total radius-2 local rule on all binary five-letter contexts."""
    if len(context) != 5 or set(context) - {"0", "1"}:
        raise ValueError("context must be a binary word of length five")
    return "b" if context in T_EDGES else "a"


def transform(word):
    if not word:
        raise ValueError("source must be nonempty")
    n = len(word)
    return "".join(
        emit("".join(word[(i + j - 2) % n] for j in range(5)))
        for i in range(n)
    )


def incidence_balance(edges, weights):
    balance = Counter()
    for edge in edges:
        flow = weights[edge]
        u, v = endpoints(edge)
        balance[u] -= flow
        balance[v] += flow
    return balance


def projected_histogram(edges, weights, order):
    """P_h times an edge-weight vector, using the edge's length-h prefix."""
    out = Counter()
    for edge in edges:
        out[edge[:order]] += weights[edge]
    return out


def output_histogram(edges, weights):
    """F_1 times an edge-weight vector for the shifted radius-2 labeling."""
    out = Counter()
    for edge in edges:
        out[emit(edge)] += weights[edge]
    return out


def _all_zero(counter):
    return all(value == 0 for value in counter.values())


def verify_example():
    # The two edge sets are vertex-disjoint directed cycles.
    s_vertices = {v for edge in S_EDGES for v in endpoints(edge)}
    t_vertices = {v for edge in T_EDGES for v in endpoints(edge)}
    assert s_vertices.isdisjoint(t_vertices)
    assert [endpoints(e) for e in S_EDGES] == [
        ("0011", "0110"),
        ("0110", "1100"),
        ("1100", "1001"),
        ("1001", "0011"),
    ]
    assert [endpoints(e) for e in T_EDGES] == [
        ("0101", "1010"),
        ("1010", "0101"),
    ]

    # A proper nonempty subset of either simple cycle cannot be a strongly
    # connected positive balanced support. Hence the only Euler supports are
    # the full S cycle and the full T cycle.
    p, q = "0011", "01"
    assert admissible(p)
    assert admissible(q)
    assert set(cyclic_counts(p, 5)) == set(S_EDGES)
    assert set(cyclic_counts(q, 5)) == set(T_EDGES)
    assert transform(p) == "a" * 4
    assert transform(q) == "b" * 2

    # h=1 support-pair LP.  Balance forces x_e=alpha on S and y_e=beta on T.
    # P_1 equality is (2 alpha, 2 alpha)=(beta,beta), i.e. beta=2 alpha.
    alpha = Fraction(3, 2)
    beta = 2 * alpha
    x = {edge: alpha for edge in S_EDGES}
    y = {edge: beta for edge in T_EDGES}
    assert _all_zero(incidence_balance(S_EDGES, x))
    assert _all_zero(incidence_balance(T_EDGES, y))
    assert min(x.values()) >= 1 and min(y.values()) >= 1
    assert projected_histogram(S_EDGES, x, 1) == projected_histogram(T_EDGES, y, 1)
    fx = output_histogram(S_EDGES, x)
    fy = output_histogram(T_EDGES, y)
    assert fx["a"] - fy["a"] == 6 >= 1

    # Clear the common denominator 2.  The scaled circulations lift to literal
    # Euler circuits: each S edge is used 3 times; each T edge is used 6 times.
    scale = 2
    x_integer = {edge: int(scale * value) for edge, value in x.items()}
    y_integer = {edge: int(scale * value) for edge, value in y.items()}
    X = p * 3
    Y = q * 6
    assert cyclic_counts(X, 5) == Counter(x_integer)
    assert cyclic_counts(Y, 5) == Counter(y_integer)
    assert cyclic_counts(X, 1) == cyclic_counts(Y, 1) == Counter({"0": 6, "1": 6})
    assert transform(X) == "a" * 12
    assert transform(Y) == "b" * 12
    assert cyclic_counts(transform(X), 1) != cyclic_counts(transform(Y), 1)

    # There is also a primitive/minimal integer witness alpha=1, beta=2.
    X_min, Y_min = "0011", "0101"
    assert admissible(X_min) and admissible(Y_min)
    assert cyclic_counts(X_min, 1) == cyclic_counts(Y_min, 1) == Counter({"0": 2, "1": 2})
    assert transform(X_min) == "a" * 4
    assert transform(Y_min) == "b" * 4

    # h=2 cross-support infeasibility is exact: on S, P_2 has positive row
    # 00=alpha (and 11=alpha), while T has 00=11=0. The LP requires alpha>=1,
    # so equality is impossible.  Same-support pairs force the same scalar,
    # hence the same output histogram. Therefore h=2 is sufficient globally.
    s_h2 = cyclic_counts(p, 2)
    t_h2 = cyclic_counts(q, 2)
    assert s_h2 == Counter({"00": 1, "01": 1, "11": 1, "10": 1})
    assert t_h2 == Counter({"01": 1, "10": 1})
    assert s_h2["00"] == 1 and t_h2["00"] == 0

    # Direct exact-horizon witnesses: h=1 fails, h=2 separates the two rays.
    assert cyclic_counts(X_min, 1) == cyclic_counts(Y_min, 1)
    assert cyclic_counts(X_min, 2) != cyclic_counts(Y_min, 2)

    return {
        "allowed_edges": list(S_EDGES + T_EDGES),
        "rational_lp_point": {
            "alpha": str(alpha),
            "beta": str(beta),
            "P1": {k: str(v) for k, v in sorted(projected_histogram(S_EDGES, x, 1).items())},
            "a_discrepancy": str(fx["a"] - fy["a"]),
        },
        "integer_scale": scale,
        "scaled_euler_sources": {"X": X, "Y": Y},
        "minimal_sources": {"X": X_min, "Y": Y_min},
        "cross_support_h2_obstruction": "P2(00)=alpha>=1 on S but 0 on T",
        "exact_horizon_k1": 2,
    }


if __name__ == "__main__":
    print(json.dumps(verify_example(), indent=2, sort_keys=True))
