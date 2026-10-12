# Bounded rooted-output inverse-counting oracle

**Researcher:** C (computational mathematics)  
**Date:** 2026-10-11  
**Issue:** #3  
**Status:** bounded exact computational evidence; not a general inverse theorem  
**Experiment input main:** `private-history-omitted`

## Question

Can a small implementation-independent oracle count inverse fibers for **rooted
outputs** of finite-radius cyclic local emission rules, including erasures,
without identifying output rotations?

For a finite set of explicitly requested positive source lengths `L`, the
oracle computes

`#{ x in A^n : n in L and T(x) = y }`

by literal enumeration of rooted source words.

## Model and counted object

- The source alphabet is finite and consists of distinct one-character symbols.
- A source is a **rooted source word** `x in A^n` with `n >= 1`.
- Different rotations are different counted source words unless they are
  literally the same rooted string.
- A radius-`r` rule is a total map `phi: A^(2r+1) -> B*`.
- Contexts are read from the periodic extension of the source, including when
  the source period is shorter than the context window.
- Site emissions are concatenated in source-site order `0,1,...,n-1`.
- An empty site emission consumes one source position and appends no output
  symbols.
- The target comparison is exact rooted-string equality. A rotated output is
  not accepted merely because it is in the same cyclic necklace.

The primary routine exhausts every source word at every explicitly supplied
source length and stops when that finite Cartesian product is exhausted. It
uses exact integer counting and no random sampling.

## Exclusions and interpretation

This oracle does **not**:

- quotient source words by rotation;
- count hidden-state runs separately from source words;
- decide whether an all-length inverse fiber is finite or infinite;
- prove that no longer preimages exist outside the supplied finite length set;
- provide a general inverse theorem;
- silently replace rooted equality by cyclic-necklace equality.

The experiment is therefore evidence only for its declared finite bounds.

## Independent comparison strategy

The reference oracle does not import a production inverse-counting routine.

For radius zero only, a separately written dynamic program counts matching
source prefixes by output position. It does not enumerate source words and is
used only where its scope exactly matches the exhaustive oracle. Contextual
rules are **not** compared against that radius-zero DP.

At the pinned experiment input commit there was no executable production
inverse/preimage/recovery counting implementation to compare against. The
archived recovery note describes such algorithms, but the executable
implementation was absent from the pinned source tree.

This limitation has also been revalidated against current main
`private-history-omitted`: the only path whose name
contains inverse/preimage/recovery is the archived recovery-status Markdown
note. A later production implementation requires a separate oracle comparison;
issue #41 records that blocked follow-up.

## Exact bounded validation

The deterministic validation packet contains **1,325 asserted cases**:

- 52 deletion-rule binomial checks;
- 126 identity-rule singleton checks;
- 16 all-erasure checks;
- 1,125 exhaustive-oracle versus independent radius-zero DP comparisons;
- 6 named regression examples.

No mismatch was found in those bounded assertions.

### Named examples

1. **Multiple preimages with erasure.**  
   Rule `0 -> ""`, `1 -> "1"`, source length 4, target `11`.  
   Exact rooted count: 6.  
   Witnesses: `0011, 0101, 0110, 1001, 1010, 1100`.

2. **Zero preimages.**  
   The same deletion rule at source length 4 cannot emit target `11111`.  
   Exact rooted count: 0.

3. **Unique preimage.**  
   Binary identity at source length 3 and target `010`.  
   Exact rooted count: 1, witness `010`.

4. **All sites erased.**  
   Rule `0 -> ""`, `1 -> ""`, source length 3, empty target.  
   Exact rooted count: 8, namely every binary length-3 source word.

5. **Contextual erasure and short source periods.**  
   Radius 1, emit the center symbol except context `010 -> ""`.  
   For target `0` and source lengths 1 through 8, the bounded fiber is
   exactly `{0, 01, 10}`. Periods 1 and 2 are shorter than the context
   window length 3 and therefore exercise repeated periodic wrapping.
   Researcher D independently extended the literal check through source length
   12 and found no additional target-`0` preimages.

6. **Root-cut trap.**  
   Identity on alphabet `{a,b}`, source length 2, rooted target `ab`.  
   Exact rooted count: 1, from source `ab`.  
   If one incorrectly accepts all output rotations, `ba` is also counted and
   the diagnostic count becomes 2.

## Reproduction

From the repository root on this branch:

```sh
python -m unittest discover -s tests -v
python experiments/rooted_inverse_oracle.py > experiments/data/rooted_inverse_oracle_2026-10-11.json
```

Recorded experiment environment: Python 3.13.5.  
Deterministic seed: none; all primary sweeps are exhaustive.

## Pinned source provenance

Experiment input commit:

- main: `private-history-omitted`

Input blobs read before the experiment:

- `README.md`: `private-history-omitted`
- `AGENTS.md`: `private-history-omitted`
- `docs/RESEARCH_STATE.md`: `private-history-omitted`
- `docs/TASK_BOARD.md`: `private-history-omitted`
- `docs/CONCURRENCY_PROTOCOL.md`: `private-history-omitted`
- `audits/archive/STD_Recovery_Spectrum_Status_2026-10-09.md`:
  `private-history-omitted`
- `std_tools/cyclic.py`: `private-history-omitted`
- `tests/test_cyclic.py`: `private-history-omitted`

PR #8 was checked during the original task and was still open/unmerged at
`private-history-omitted`; it was not used as an input
to this inverse-counting packet.

## Reviewed executable artifacts

The following three artifacts are unchanged by the report repair:

- `experiments/rooted_inverse_oracle.py`
  - Git blob: `private-history-omitted`
- `tests/test_rooted_inverse_oracle.py`
  - Git blob: `private-history-omitted`
- `experiments/data/rooted_inverse_oracle_2026-10-11.json`
  - Git blob: `private-history-omitted`

The report's own content hash is intentionally recorded in the PR/issue handoff
after this file is committed, rather than embedded here as a circular self-hash.

## Review history and limitation

Researcher D independently reviewed the executable packet at original head
`private-history-omitted`. D reproduced the root-cut
semantics, short-period contextual case, erasure examples, all 1,125 radius-zero
DP comparisons, and the total count of 1,325 assertions. The executable review
passed within the bounded scope.

The only blocking defect found in that review was corruption of this Markdown
artifact. This replacement report changes documentation only. The oracle,
tests, and result JSON remain byte-for-byte the reviewed artifacts above.

The final claim remains: **bounded exact computational evidence for rooted
inverse counts under the stated finite source-length bounds, not a general STD
inverse theorem.**
