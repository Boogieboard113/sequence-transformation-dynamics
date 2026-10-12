# STD3 Engineering — literal cyclic-orbit oracle (issue #108)

**Evidence category:** independent *bounded computation*, not a proof or an independent review of mathematical work. The source implementation was authored in the ordinary **STD3-Engineering** chat on 2026-10-11; no stable platform chat/session ID was exposed. Shared account access is not evidence of reviewer independence.

## Inputs and question

- Repository: `STD sanitized snapshot`, current fetched `main` at start `private-history-omitted` (documentation integration #109); prior task pin `private-history-omitted`.
- Contract: #104 and #108. Existing reviewed example PR #100, theorem blob `private-history-omitted`.
- Separate *literal path*: enumerate all rooted words in `A^N` for each declared alphabet/length, filter each cyclic `m`-window, emit each centered-radius context site-by-site, then count raw cyclic output `C_k` and search source `h=1..m` by actual source-histogram collision. No cycle formula or PR #100 checker is imported into this path.
- Separate *candidate path*: build the allowed higher-block digraph, discard an edge iff its endpoint cannot return to its start, check that the recurrent graph has in-degree and out-degree exactly one per active vertex, derive labeled primitive cycles, compare cross-multiplied per-site source/output histogram densities for every active cycle pair. Exact integers throughout; no floats.
- The candidate is **not assumed true** in the literal path. Domain-orbit equality, output scaling, rooted rotations, horizon equality, and bounded repeated-residue consistency are checked separately. Contradictions stop the run with a named fixture, length and discrepancy.

## Fixed declared coverage

- 8 fixtures: six binary presentations over `N=1..12`, one ternary over `N=1..8`, one unary over `N=1..8`.
- Fixed source orders `m=1,2,3,4,7`; emission radii `r=0,1,2`; output orders among `k=1,2,3,4,5` as declared in the code; total nonerasing context-table entries emit 1 or 2 letters.
- **58,988** candidate rooted words tested for periodic admissibility; **146** admitted; **88** length domains tested, of which 160 `(N,k)` checks were nonempty; **260** total `(N,k)` checks including empty-length sentinels. **113** output rotation/repetition checks. **40** comparisons of horizon profiles at distinct nonempty lengths having the same residue mod component-period LCM.
- **Zero mismatches** between literal horizons and candidate densities or literal rooted domains and predicted orbit sets. **Seven unittest tests** pass in normal and optimized `-O` mode, and generated JSON files match byte-for-byte across those modes.
- Negative fixtures: branching recurrent graph, vertex-overlapping cycles, malformed window lengths, invalid source symbols, empty recurrent core and erasing emissions are rejected with explicit messages, not silently classified as positive cases.

## Named witnesses and limits

- Reconstructs PR #100 literally: `m=7`, seeds `0011` (period 4) and `000111` (period 6), `k=2`, identity emission, rooted domain counts for `N=1..12` equal `[0,0,0,4,0,6,0,4,0,0,0,10]`. At `N=12`, source `C_1=(6,6)` agrees for `X=(0011)^3`, `Y=(000111)^2`, but `C_2(01)` is 3 versus 2; exact literal horizon 2. The all-lengths-`H=1` shortcut fails.
- New adversarial bounded fixture: binary `m=7`, seeds `0000101` and `0001001` (two vertex-disjoint period-7 cycles), equal raw `C_2` but unequal `C_3`; identity output order `k=3` needs **h=3** already at `N=7`. A shortcut `H<=2` fails even under the graph precondition.
- Variable-length emission regression: binary `m=4`, cycles seeded by `0011` and `01`, radius-1 context table emitting `0` for center 0 and `11` for center 1. At `N=4`, `k=2`, literal horizon is 2; emitted lengths vary, and a source rotation need not fix an output-character root.
- Short wrap: binary `m=3`, `r=2`, source `N=1`, output contexts length 5; output order `k=3` is counted periodically even on 2-character output. Transient allowed edge `01` between the two length-2 fixed-point supports is ignored by the recurrent graph but still evaluated in every literal word's membership test.
- Branching negative: allowed binary bigrams `{00,01,10}` admit the length-3 rooted word `001`, but the recurrent graph branches at vertex 0. It is not in the claimed simple-cycle class.

**Limits:** finite alphabets, chosen graph fixtures, source lengths only up to the declared caps, fixed small radii/orders, no erasure, raw cyclic counts and no rooted output position claims. Successful finite enumeration cannot establish the universal formula, the bound `H_N(k)<=m`, or a minimal period, and does not review STD3-Theory's future proof. No extra cases or historical review ownership were silently assumed.

## Reproduction from repository root

```bash
python -m unittest discover -s tests -p 'test_std3_cycle_spectrum_oracle.py' -v
python -O -m unittest discover -s tests -p 'test_std3_cycle_spectrum_oracle.py' -v
python experiments/std3_cycle_spectrum_oracle.py --output /tmp/std3.json
python -O experiments/std3_cycle_spectrum_oracle.py --output /tmp/std3-opt.json
cmp /tmp/std3.json /tmp/std3-opt.json
cmp /tmp/std3.json experiments/data/std3_cycle_spectrum_oracle_2026-10-11.json
```

Execution environment: **CPython 3.13.5**, Linux x86_64, GCC 14.2.0; repository CI declares CPython 3.12 via `actions/setup-python@v5`. No external dependencies; only Python standard library.

Checksums for the exported source, tests, and data are recorded in the snapshot root `SHA256SUMS`.
