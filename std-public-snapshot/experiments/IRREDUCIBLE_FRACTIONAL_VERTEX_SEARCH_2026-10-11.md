# Bounded search for irreducible fractional support-pair vertices

**Issue:** #88  
**Status:** bounded exact computational evidence; no universal denominator-growth claim  
**Pinned input main:** `private-history-omitted`

## Freshness note

This search was predeclared and substantially executed before E's issue #83
universal family completed. While this packet was being finalized, PR #97 was
independently proved, nonauthor-reviewed, and merged as
`private-history-omitted`.

PR #97 is therefore **not** an input to the search outcomes below, and this
bounded computation should not be credited as a premise for that theorem.
Its remaining role is independent small-case evidence and scope contrast:

- the bounded binary-triple domain first becomes fractional at six ambient edges;
- both full and proper positive supports already show denominator two;
- the accepted PR #97 family supplies the stronger full-support irreducible
  unbounded-denominator theorem.

## Search domain

The search exhausts the predeclared binary length-three domain:

- every strongly connected ambient de Bruijn edge set with 1 through 6 edge types;
- every ordered pair of nonempty strongly connected positive supports S,T inside the ambient;
- source order h=1;
- every single-edge indicator target from the ambient;
- original balance/source-prefix equalities in edge coordinates;
- normalized support positivity and signed target discrepancy, all with right-hand side 1.

Duplicate (S,T,target) LPs induced by multiple ambient supersets are assigned to
the least ambient by edge count and lexicographic order. Arithmetic is exact
`fractions.Fraction`. Candidate active-set enumeration is complete whenever
the per-instance cap of 20,000 is not hit; this run has zero cap hits.

A single-edge target has a literal total radius-one binary realization: emit
output 1 on the selected triple context and 0 on every other triple. Raw output
C1(1) is the selected source C3 count up to cyclic site reindexing.

## Exact search result

The declared domain contains **22** strongly connected ambient graphs:

| ambient edges | graphs |
|---:|---:|
| 1 | 2 |
| 2 | 1 |
| 3 | 2 |
| 4 | 5 |
| 5 | 6 |
| 6 | 6 |

Canonical LP coverage:

- **1,594** unique ordered support/target instances;
- **101,536** candidate active sets tested;
- **0** cap hits;
- **244** feasible vertices;
- denominator histogram: **212 integral**, **32 denominator 2**;
- no denominator above 2;
- **no fractional vertex in any ambient graph with at most 5 edge types**;
- first fractional vertices occur only at ambient size 6.

By ambient size:

| ambient edges | LP instances | active sets | vertices | fractional |
|---:|---:|---:|---:|---:|
| 1 | 2 | 6 | 0 | 0 |
| 2 | 2 | 10 | 0 | 0 |
| 3 | 6 | 42 | 0 | 0 |
| 4 | 130 | 1,142 | 0 | 0 |
| 5 | 374 | 12,952 | 32 | 0 |
| 6 | 1,080 | 87,384 | 212 | 32 |

Fractional support-size pairs are not only full/full:
`(5,5):4, (5,6):4, (6,4):4, (6,5):12, (6,6):8`.

Four of the six strongly connected six-edge ambient graphs contain fractional
hits. The full list is in the machine-readable packet.

## Representative full-support hit

Ambient/support:
`E=S=T={000,001,010,011,100,110}`, target `000`.

Unique preserved vertex:
[
x=(2,5/2,1,3/2,5/2,3/2),quad
y=(1,3,2,1,3,1).
]

- denominator 2;
- equality rank 8;
- tight positivity indices 2,6,9,11;
- equality + tight positivity rank 11;
- adding the tight target row gives rank 12.

Doubling gives literal Euler witnesses of length 22:

- `0000001001001100110011`
- `0000100100100100110011`

with equal source C1=(14,8) and selected target counts 4 versus 2.

A separate complete literal binary-word search through length 14 finds a shorter
full-support witness at length 14, so vertex clearing is not a
shortest-witness procedure.

## Representative proper-support hit

Same irreducible six-edge ambient, but

- `S={000,001,011,100,110}`;
- `T={001,010,011,100,110}`;
- target `000`.

Preserved vertex:
[
x=(1,3/2,3/2,3/2,3/2),quad
y=(2,1,1,2,1).
]

It also has denominator 2. Here the equality rows plus tight positivity rows
already have full variable rank 10; the tight target row is redundant for
vertex extremality.

Doubling gives length-14 Euler witnesses with equal C1=(8,6) and target counts
2 versus 0.

The independent literal search finds an exact-support witness already at
length 10:

- `0000110011`
- `0010010011`

with equal C1=(6,4) and target counts 2 versus 0.

## Relation to the accepted irreducible family

The accepted PR #97 theorem is stronger than this search:

- it gives an infinite irreducible **full-support** family;
- its unique normalized vertex has denominator
  `p=(E-2)/2`, unbounded with graph size;
- it proves exact full-support integer witness length `4p+2` for that family.

The present packet does not re-prove or independently review PR #97. It merely
shows that the smallest declared binary-triple search already contains
denominator-two instances in both full and proper supports, and that no smaller
ambient graph in this bounded domain does.

## Short-period semantics

All cyclic block counters use literal periodic wrapping. The tests include one-
and two-symbol words, e.g. `C3(0)={000:1}` and
`C3(01)={010:1,101:1}`. Finite witness searches therefore do not assume
source length at least the block width.

## Reproduction

From repository root:

```sh
python -m unittest discover -s tests -p 'test_irreducible_fractional_vertex_search.py' -v
python -O -m unittest discover -s tests -p 'test_irreducible_fractional_vertex_search.py' -v
python experiments/irreducible_fractional_vertex_search.py --output /tmp/irreducible-fractional.json
```

The committed JSON packet records the complete aggregate counts and preserved
representatives and is compared against a full regeneration in the tests.

## Classification and limitations

This is **bounded exact computation only**.

It does not establish:

- denominator growth;
- a new irreducible family theorem;
- any structural-minor implication;
- shortest-witness asymptotics;
- a fixed-length or fixed-inventory result.

Those stronger questions require analytic results such as the separately
accepted PR #97 theorem.