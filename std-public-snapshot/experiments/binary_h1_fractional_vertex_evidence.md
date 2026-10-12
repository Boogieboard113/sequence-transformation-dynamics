# Six-edge binary full-support LP with a necessary denominator-two vertex

**Engineering research packet, issue #78, 2026-10-11.** Owner: this separate engineer chat, session label `std-engineer-binary-h1-20261011`. This is **not** a continuation of the previously completed managed `internal worker` session. Independent nonauthor mathematical/implementation review is **pending**. Do not merge or update accepted-state documentation on the strength of this packet alone.

## Inputs and exact conventions

- Task-start `main`: `private-history-omitted`.
- Accepted PR #6 premise: `theorems/proved-internal/finite_type_exact_horizon.md`, blob `private-history-omitted`. Accepted PR #67 structural-minor context: blob `private-history-omitted`. PR #75 family-specific contrast: blob `private-history-omitted`. The code imports none of their algorithms.
- Alphabet `A={0,1}`, allowed periodic length-three windows `E=(000,001,010,011,100,110)`, in this order. Source domain: all nonempty finite cyclic words of arbitrary positive lengths with all wraparound triples in `E`; rooted words are distinguished by their listed first position **during enumeration**, but all tested raw cyclic histograms are rotation-invariant.
- Every edge `abc` goes from vertex `ab` to `bc`. The six-edge graph is strongly connected and recurrent. S=T=E are **both full positive supports** for the LP, and source histogram order is `h=1`.
- Total, nonerasing, binary radius-one emission rule: emit `1` at site with triple context `000`, `0` at every other context. For all cyclic sources, the target output-one count equals `F(X)=C_3(X)(000)`; the center-versus-forward window choice changes only the site indexing, not the raw count.
- Original LP edge variables `z=(x_{000},x_{001},x_{010},x_{011},x_{100},x_{110},y_{000},y_{001},y_{010},y_{011},y_{100},y_{110})`. Require `D x=0`, `D y=0`, `P_1 x=P_1 y`, every coordinate `z_i>=1`, and `x_{000}-y_{000}>=1`. No total-length normalization or prescribed fixed source length; matching `C_1` already forces equal individual lengths.

## Exact computation and result

A new standard-library implementation builds the **original** incidence and prefix matrices and computes their rational nullspace with `fractions.Fraction`. The ten written equality rows have rank eight, leaving four free variables. It enumerates all `binom(13,4)=715` four-element candidate active sets: twelve lower-bound inequalities plus one target-discrepancy inequality. Each nonsingular candidate is solved exactly and tested against **every** original inequality and equality. Identical solutions are deduplicated as rational vectors.

**Result: exactly one vertex**, with coordinates in the specified order:

```text
x = (2, 5/2, 1, 3/2, 5/2, 3/2)
y = (1, 3,   2, 1,   3,   1)
```

All lower bounds and target gap are feasible; `sum(x)=sum(y)=11` and `x_000-y_000=1`. Its minimal common denominator is **2**. The tight positivity rows are at zero-based indices `2,6,9,11`; together with the original equalities they have rank **11**, and including the tight target row yields full rank **12**. An earlier local assertion incorrectly expected rank 12 without the target row and **failed**; the test was corrected to require 11 without it and 12 with it, and rerun successfully before publication. No such assertion remains silently disabled under `python -O`.

This is a small, **computer-assisted exact finite-dimensional counterexample** to the idea that every feasible full-support normalized support-pair LP has an integral vertex. Exhaustion of the stated 715 combinations depends on correctness of this inspectable code and still needs nonauthor review. It is not a lower bound that grows with graph size, does not claim all feasible points are fractional, and does not assert that scaling this vertex gives the shortest integer witnesses.

A cheap **separate bounded** survey built from all three-, four-, and five-edge subsets of the eight binary triples retained only strongly connected whole-graph supports. For each such graph it tested every single-edge indicator target under the same `h=1`, `S=T=E` convention. Summary:

| Edge types | Connected graphs | Target instances | Candidate active sets | Feasible vertices | Fractional vertices |
|---:|---:|---:|---:|---:|---:|
| 3 | 2 | 6 | 42 | 0 | 0 |
| 4 | 5 | 20 | 612 | 0 | 0 |
| 5 | 6 | 30 | 4,400 | 8 | 0 |

This survey says nothing about different alphabets, different `h`, asymmetric supports, other emission coefficients, or any untested graph with fewer than three edges.

## Independent literal-word checks

A **different** algorithm enumerates rooted closed walks on the original length-two-vertex graph for individual word lengths `1..14`. It does not use the LP nullspace, rational vertices, or equality solver. It computes every word's raw cyclic source `C_1`, six triple counts and target `F` by direct periodic indexing. To independently check this enumerator, the tests enumerate the entire `{0,1}^n` alphabet product for **every** `n=1..14` (32,766 candidate binary words) and filter by direct periodic triple membership. These two sets agree exactly at every length, including `n=1,2` where the source period is shorter than the triple width; no duplicate rooted words occur.

Across `n=1..14`, there are 2,202 admissible rooted words, 1,168 of them with all six edges present. The first target discrepancy between equal-`C_1` words with arbitrary supports is at length **6**, and with **both positive supports full** at length **14**. Concrete literal words:

| Allowed support scope | Word X | Word Y | Common raw C1 (zeros,ones) | Output-one counts |
|---|---|---|---|---|
| Arbitrary | `000011` | `001001` | `(4,2)` | `(2,0)` |
| Both full | `00000100110011` | `00010010010011` | `(9,5)` | `(3,1)` |

Thus the exact finite search establishes **the minimum for this particular literal word domain** provided that its independent complete enumerators are correct: a witness exists at length 14 and none below. It does not entail a family-wide or general shortest-witness theorem.

The integer-scaled unique LP vertex, by contrast, has positive triple counts

```text
2x = (4,5,2,3,5,3)
2y = (2,6,4,2,6,2)
```

A deterministic Euler traversal emits the following actual cyclic words of individual length **22**:

```text
X = 0000001001001100110011
Y = 0000100100100100110011
C1(X) = C1(Y) = (14,8), F(X)=4, F(Y)=2.
```

Both cyclic triple histograms were recovered *literally* and matched exactly to the desired edge multiplicities. This also exhibits why **vertex-denominator clearing need not give the shortest integer cyclic witness** (22 versus 14).

## Reproducibility, classification, limitations

Python **3.13.5**; standard library only for the committed checker, without float arithmetic or optional packages. An exploratory, *non-evidentiary* search used SciPy **1.17.0** to nominate the candidate; all published feasibility, all-vertex exhaustion and witnesses were rechecked by the separate exact standard-library implementation.

From repository root:

```sh
python -m unittest discover -s tests -p 'test_binary_h1_fractional_vertex.py' -v
python -O -m unittest discover -s tests -p 'test_binary_h1_fractional_vertex.py' -v
python tests/test_binary_h1_fractional_vertex.py --report /tmp/std-binary-vertex.json
python -O tests/test_binary_h1_fractional_vertex.py --report /tmp/std-binary-vertex-opt.json
cmp /tmp/std-binary-vertex.json /tmp/std-binary-vertex-opt.json
cmp /tmp/std-binary-vertex.json experiments/data/binary_h1_fractional_vertex_2026-10-11.json
```

**Observed execution:** 4/4 tests pass in normal mode and 4/4 pass under `-O`; both normal- and optimized-mode generated JSON outputs match each other and the committed report byte-for-byte. The initial incorrect rank assertion failed as disclosed above and was repaired *before* the pinned artifact. No remaining mismatches or regression failures.

**Frozen artifact identities before nonauthor review:**

| Artifact | Git blob SHA-1 | SHA-256 |
|---|---|---|
| `tests/test_binary_h1_fractional_vertex.py` | `private-history-omitted` | `historical-checksum-omitted` |
| `experiments/data/binary_h1_fractional_vertex_2026-10-11.json` | `private-history-omitted` | `historical-checksum-omitted` |

**Evidence classification:** bounded exact-rational/combinatorial computation for a single finite LP; bounded exhaustive literal cyclic-word enumeration; direct execution and byte-reproduction evidence. **Not:** independent mathematical peer review, proof-assistant verification, a proof about unbounded families, or an exponential/superlinear growth theorem.

**Next owner:** coordinator should arrange a new, identified **nonauthor auditor session** to review this frozen PR head, with special attention to all-vertex active-set completeness, short-period wraparound, the original-matrix rank/target-row distinction, and the difference between a fraction-only vertex and shortest integer witness. Do not merge or modify the accepted-state summary before that review.
