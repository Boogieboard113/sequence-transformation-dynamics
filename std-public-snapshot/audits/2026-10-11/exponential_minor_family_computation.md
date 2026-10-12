# Independent exact family checks (issue #74)

Engineer session: managed worker `internal worker`, 2026-10-11. Input main:
`private-history-omitted`; accepted PR #67 family theorem blob:
`private-history-omitted`. This packet adds bounded computational
evidence for the new family-specific theorem; it does not reopen PR #67's
accepted structural-minor result or independently establish a general theorem.

## Method and independence

The new standard-library test constructs the original length-three edges,
incidence rows, source-prefix rows, positivity rows, and single target row
directly. It imports neither the author's reduced-coordinate proof nor the old
family regression or Fourier--Motzkin solver. Candidate formulas were shared
between team members; this was independent implementation, not a blinded study.
All rank arithmetic uses `fractions.Fraction`.

A separate deterministic Hierholzer traversal constructs actual cyclic source
words from integer edge histograms. Literal periodic three-letter windows
recover their exact histograms; a centered radius-one emission rule emits 1
only at context `(0,0,1)`, and direct output-symbol counting checks the target.
This verifies realizability rather than only abstract balance equations.

For bounded minimality, the code visits every closed path of each length in the
original two-letter-vertex graph. Each admissible rooted periodic source word
determines exactly one starting context and edge sequence. No rotation quotient
is applied. Grouping by literal source-symbol histogram detects any unequal
output-one count. Duplicate rooted outputs of the enumerator are rejected.
A separate alphabet-product search agrees with these enumerated sets for
`t=3,4`, each length 1 through 6 (6,552 unrestricted alphabet words inspected).

## Observed results

Python 3.12.14, five targeted unittest methods PASS in normal and optimized
(`python -O`) mode. Explicit raises and unittest checks remain live under
optimization. The deterministic JSON reports generated in the two modes are
byte-identical.

| Check | Range | Result |
|---|---|---|
| Original full-system feasibility and active-row rank | Nine supplied odd/even candidate points, `t=3..8` | Every point integral, target gap 1, exact active rank `8t` |
| Literal arbitrary-support witnesses | Six pairs, `t=3..8` | Individual length `4t`, equal source C1, output-one counts 2 versus 1 |
| Literal full-positive-support witnesses | Six pairs, `t=3..8` | Individual length `6t`, equal source C1, output-one counts 2 versus 1 |
| Exhaustive odd-family rooted search | `t=3`, all lengths 1..12 | 252 admissible rooted words; first collision at length 12 |
| Exhaustive even-family rooted search | `t=4`, all lengths 1..16 | 1,080 admissible rooted words; first collision at length 16 |
| Short-period boundary | `t=3,4`, lengths 1 and 2 | No length-one words; exactly `2t` length-two words, each with output-one count zero |

The explicit first collision words, all per-length counts, the twelve lifted
pairs, and nine rank records are retained in
`experiments/data/exponential_minor_family_exact_witnesses_2026-10-11.json`.
The `collision_hits` field counts words differing from the first stored target
in their histogram bucket; it is not a count of all ordered colliding pairs.

## Reproduction

From repository root:

```sh
python -m unittest discover -s tests -p 'test_exponential_minor_family_exact_witnesses.py' -v
python -O -m unittest discover -s tests -p 'test_exponential_minor_family_exact_witnesses.py' -v
python tests/test_exponential_minor_family_exact_witnesses.py --report /tmp/std-family-normal.json
python -O tests/test_exponential_minor_family_exact_witnesses.py --report /tmp/std-family-optimized.json
cmp /tmp/std-family-normal.json /tmp/std-family-optimized.json
cmp /tmp/std-family-normal.json experiments/data/exponential_minor_family_exact_witnesses_2026-10-11.json
```

Frozen artifact identities before nonauthor review:

| Artifact | SHA-256 | Git blob |
|---|---|---|
| New test module | `historical-checksum-omitted` | `private-history-omitted` |
| JSON evidence | `historical-checksum-omitted` | `private-history-omitted` |

## Limits

Active rank proves that each supplied feasible point is a vertex; these checks
do not enumerate or exclude other vertices. The author's analytic proof and
independent audit must supply the all-vertices classification and all-`t`
minimality. Full-support minimality is not exhaustively searched here; the
literal pairs establish attainment in the checked cases. Only `t=3,4` have
exhaustive arbitrary-support shortest-witness searches, within the explicit
bounds. No broad denominator lower bound, fixed-inventory extension, rooted
output theorem, production solver, or practical complexity claim follows.
The accepted eight-edge support-enumeration cap is unchanged and is not bypassed.
