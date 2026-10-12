"""Exact rational linear-feasibility core for STD experiment issue #44.

Inequalities use the form a.x <= b.  Fourier-Motzkin elimination is exact over
fractions.Fraction and reconstructs one rational witness by reverse
back-substitution.  This is intentionally a small exponential reference
routine, not a practical general LP solver.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable, Sequence


Inequality = tuple[tuple[Fraction, ...], Fraction]


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def _normalize(coefficients: Sequence[Fraction], rhs: Fraction) -> Inequality:
    """Divide an inequality by a positive rational common factor."""
    values = [Fraction(v) for v in coefficients] + [Fraction(rhs)]
    denominator = 1
    for value in values:
        denominator = _lcm(denominator, value.denominator)
    integers = [
        value.numerator * (denominator // value.denominator)
        for value in values
    ]
    common = 0
    for value in integers:
        common = gcd(common, abs(value))
    if common > 1:
        integers = [value // common for value in integers]
    return (
        tuple(Fraction(value) for value in integers[:-1]),
        Fraction(integers[-1]),
    )


def _simplify(
    inequalities: Iterable[Inequality], nvars: int
) -> list[Inequality] | None:
    """Drop tautologies and exact duplicates; return None on contradiction."""
    unique: dict[Inequality, None] = {}
    for coefficients, rhs in inequalities:
        if len(coefficients) != nvars:
            raise ValueError("coefficient vector length does not match nvars")
        row = _normalize(coefficients, rhs)
        coefficients, rhs = row
        if all(value == 0 for value in coefficients):
            if rhs < 0:
                return None
            continue
        unique.setdefault(row, None)
    return list(unique)


def equality_inequalities(
    equalities: Iterable[tuple[Sequence[int | Fraction], int | Fraction]],
) -> list[tuple[tuple[Fraction, ...], Fraction]]:
    """Convert exact equalities a.x = b into paired <= inequalities."""
    result = []
    for coefficients, rhs in equalities:
        coefficients = tuple(Fraction(value) for value in coefficients)
        rhs = Fraction(rhs)
        result.append((coefficients, rhs))
        result.append((tuple(-value for value in coefficients), -rhs))
    return result


def satisfies(
    point: Sequence[Fraction],
    inequalities: Iterable[tuple[Sequence[int | Fraction], int | Fraction]],
) -> bool:
    """Check a candidate point against every a.x <= b inequality exactly."""
    point = tuple(Fraction(value) for value in point)
    for coefficients, rhs in inequalities:
        coefficients = tuple(Fraction(value) for value in coefficients)
        if len(coefficients) != len(point):
            raise ValueError("coefficient vector length does not match point")
        if sum(a * x for a, x in zip(coefficients, point)) > Fraction(rhs):
            return False
    return True


def feasible_point(
    inequalities: Iterable[
        tuple[Sequence[int | Fraction], int | Fraction]
    ],
    nvars: int,
    *,
    max_constraints: int = 100_000,
) -> tuple[Fraction, ...] | None:
    """Return one exact rational feasible point, or None if infeasible.

    Variables are eliminated from index 0 upward.  Each elimination stage is
    retained so a witness can be reconstructed in reverse order.  Constraints
    are non-strict; STD support positivity is encoded later as x_e >= 1.

    The routine is exponential in the worst case.  max_constraints is an
    engineering guard only; hitting it raises RuntimeError rather than being
    misclassified as mathematical infeasibility.
    """
    if not isinstance(nvars, int) or isinstance(nvars, bool) or nvars < 0:
        raise ValueError("nvars must be a nonnegative integer")
    if (
        not isinstance(max_constraints, int)
        or isinstance(max_constraints, bool)
        or max_constraints < 1
    ):
        raise ValueError("max_constraints must be a positive integer")

    original: list[Inequality] = []
    for coefficients, rhs in inequalities:
        coefficients = tuple(Fraction(value) for value in coefficients)
        if len(coefficients) != nvars:
            raise ValueError("coefficient vector length does not match nvars")
        original.append((coefficients, Fraction(rhs)))

    current = _simplify(original, nvars)
    if current is None:
        return None

    stages: list[list[Inequality]] = []
    for variable in range(nvars):
        stages.append(current)
        positive: list[Inequality] = []
        negative: list[Inequality] = []
        zero: list[Inequality] = []
        for row in current:
            coefficient = row[0][variable]
            if coefficient > 0:
                positive.append(row)
            elif coefficient < 0:
                negative.append(row)
            else:
                zero.append(row)

        next_rows = list(zero)
        if positive and negative:
            for p_coefficients, p_rhs in positive:
                p = p_coefficients[variable]
                for n_coefficients, n_rhs in negative:
                    n = n_coefficients[variable]  # n < 0
                    coefficients = tuple(
                        (-n) * p_coefficients[j] + p * n_coefficients[j]
                        for j in range(nvars)
                    )
                    rhs = (-n) * p_rhs + p * n_rhs
                    next_rows.append((coefficients, rhs))
                    if len(next_rows) > max_constraints:
                        raise RuntimeError(
                            "Fourier-Motzkin constraint cap exceeded"
                        )
        # If only upper or only lower bounds exist, existential elimination can
        # always choose this variable far enough in the permitted direction.
        current = _simplify(next_rows, nvars)
        if current is None:
            return None

    point = [Fraction(0) for _ in range(nvars)]
    for variable in reversed(range(nvars)):
        lower: Fraction | None = None
        upper: Fraction | None = None
        for coefficients, rhs in stages[variable]:
            remainder = sum(
                coefficients[j] * point[j]
                for j in range(variable + 1, nvars)
            )
            coefficient = coefficients[variable]
            if coefficient > 0:
                bound = (rhs - remainder) / coefficient
                if upper is None or bound < upper:
                    upper = bound
            elif coefficient < 0:
                bound = (rhs - remainder) / coefficient
                if lower is None or bound > lower:
                    lower = bound
            elif remainder > rhs:
                raise AssertionError(
                    "Fourier-Motzkin back-substitution invariant failed"
                )

        if lower is not None and upper is not None and lower > upper:
            raise AssertionError(
                "Fourier-Motzkin reconstructed inconsistent bounds"
            )
        if lower is None and upper is None:
            chosen = Fraction(0)
        elif lower is None:
            chosen = upper
        elif upper is None:
            chosen = lower
        else:
            chosen = (lower + upper) / 2
        point[variable] = chosen

    result = tuple(point)
    if not satisfies(result, original):
        raise AssertionError("reconstructed point does not satisfy input system")
    return result
