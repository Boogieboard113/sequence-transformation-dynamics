# Canonical forced-continuation contraction of cyclic block histograms

**Status:** proved-internal (full argument and independently formulated brute-force regression oracle; not externally peer-reviewed or proof-assistant checked)  
**Date:** 2026-10-11  
**Track:** Researcher C / Issue #2 / `experiments/structural-reduction`

## 1. Model and conventions

Fix a finite alphabet \(A\), an integer \(h\ge 1\), and a finite, nonzero histogram
\(m:A^h\to\mathbb Z_{\ge0}\). Write \(n=\sum_e m(e)>0\). A *source* is a rooted
length-\(n\) word \(x\) with periodic wraparound; its raw cyclic histogram is
\(C_h(x)(e)=\#\{i\bmod n:x_i\cdots x_{i+h-1}=e\}\), **even if \(h>n\)**.
For cyclic source and output *classes*, identify words under cyclic rotation,
but do **not** silently identify rooted linear outputs.

The positive-support directed block graph \(G_m\) has vertex set of occupied
\((h-1)\)-blocks, and one *edge type* \(e=a_0\cdots a_{h-1}\) from
\(s(e)=a_0\cdots a_{h-2}\) to \(t(e)=a_1\cdots a_{h-1}\), with multiplicity
\(m(e)>0\). For \(h=1\), the unique vertex is the empty word. Edges of the
same type are indistinguishable; an edge with multiplicity 5 is **one choice
of continuation**, not five. A cyclic Euler word is an ordered cyclic list of
edge *types* using type \(e\) exactly \(m(e)\) times, with adjacent endpoints
matching. A cyclic Euler word uniquely reconstructs a cyclic source class by
reading the **first symbol** of each edge (including in the \(n<h\) case).

An edge-local emission assignment is any \(\psi:E^+\to B^*\), where \(B\) is
a finite output alphabet and the emitted cyclic output is the cyclic class of
\(\psi(e_0)\psi(e_1)\cdots\psi(e_{n-1})\). Erasure is \(\psi(e)=\varepsilon\).
If all emissions are empty, the output is the singleton empty word.

For STD's centered radius-\(r\) emission rule \(\phi:A^{2r+1}\to B^*\), choose
\(h\ge2r+1\) and set \(\psi(e)=\phi(e_0\ldots e_{2r})\). This indexing emits
at source site \(i+r\) for the block starting at \(i\), so it agrees **as a
cyclic output class**, and agrees as a *rooted* output after correcting the
source-to-emission offset by \(r\) sites (see §5). No assumption of a
nonerasing map or positive output length is made.

## 2. The canonical exact-reduction theorem

**Theorem (forced-continuation contraction).** Let \(G_m\) be as above.

1. A source with \(C_h(x)=m\) exists **if and only if** every occupied vertex
   has weighted indegree equal to weighted outdegree and the underlying
   undirected graph on the occupied vertices is connected. If either condition
   fails, the admissible source set is empty; no componentwise Euler walks may
   be glued into a fictitious single cyclic source.
2. Suppose these conditions hold. Put
   \(S=\{v:\#\{e\in E^+:s(e)=v\}\ge2\}\) (count *distinct positive edge
   types*, not copies). If \(S=\varnothing\), the positive support is a single
   directed simple cycle \(P\), possibly a self-loop, and all its edge
   multiplicities are equal to some \(q\ge1\). The unique cyclic edge-type
   realization is \(P^q\).
3. Suppose \(S\ne\varnothing\). For each positive edge type \(a\) leaving a
   vertex in \(S\), follow \(a\) and then the unique positive outgoing type
   from each subsequent vertex outside \(S\) until the path next reaches
   \(S\). This finite deterministic *corridor* is \(P_a\), which starts and
   ends in \(S\), and has no internal vertex in \(S\). Create a macro-edge
   \(a\) from the initial to terminal vertex of \(P_a\), assign multiplicity
   \(\mu(a)=m(a)\), and preserve its **entire path** for lifting.
   The reduced macro graph has an Euler circuit. Expansion
   \(a\mapsto P_a\) establishes a **bijection between cyclic edge-type Euler
   words of the reduced and original graphs**. In particular,
   \[
       \forall e\in E^+,\qquad
       \sum_{a\text{ leaving }S}\mu(a)\,\#_e(P_a)=m(e).\tag{coverage}
   \]
   This identity is a concrete, machine-checkable lift certificate, even
   when different corridors *share* forced edge types.
4. The correspondence preserves, exactly, the attainable cyclic output classes
   for **every** edge emission \(\psi:E^+\to B^*\), by labeling macro \(a\)
   with the concatenated word \(\Psi(a)=\prod_{e\in P_a}\psi(e)\). Consequently
   it preserves every attainable raw cyclic output block histogram and its
   exact minima/maxima (where the admissible set is nonempty), including
   windows longer than the output and empty output words.
5. Let \(D\) be **any** predicate on the full rooted source word (not
   necessarily rotation-invariant). Each reduced cyclic tour, expanded and
   combined with a choice of *original source-edge cut*, yields exactly the
   permitted rooted sources by retaining only those cuts satisfying \(D\).
   Thus every arbitrary source-domain restriction can be handled exactly by
   pulling it back through the lift. This may require full reconstruction;
   only suitably summarized constraints enjoy a computational speedup.

**Maximality within the stipulated method.** All surviving vertices have at
least two distinct outgoing edge types. Thus no further vertex can be removed
by the same *state-only, unique-next-edge-type* forced-continuation rule.
Different nonlocal or state-augmented reductions are not ruled out; uniqueness
of outgoing type is **not** asserted to be necessary for arbitrary semantic
output-preserving reductions.

**Size formula.** The number of traversed macro edges is exactly
\(N_{\rm macro}=\sum_{v\in S}\deg^+_m(v)\), the count of original edges leaving
branch vertices, counting multiplicities. This is strictly less than \(n\)
whenever some occupied nonbranch vertex exists, and is independent of the
particular Euler circuit.

### Proof

**(1) Euler criterion and source decoding.** Source windows form an Euler tour,
so equality of degrees and weak connectivity are necessary. Conversely, a
finite balanced, weakly connected digraph of positive edges is strongly
connected: its condensation is a weakly connected DAG, and the weighted
zero-net-flow condition implies no source condensation component can have an
outgoing edge. Hence it has one SCC; the directed Euler theorem supplies a
closed tour. The h-block overlap at consecutive edges, *including the final
edge with the first*, guarantees that the first-edge-symbol sequence has
exactly the prescribed periodic h-blocks. This also holds when \(n<h\).

**(2) Pure cycle.** With one outgoing positive type per occupied vertex,
every vertex has one support successor. A strongly connected finite functional
digraph is a directed cycle. At each cycle vertex balance forces equality of
the multiplicities on its unique incoming and outgoing edges. Every edge tour
traverses this cycle \(q\) times, unique modulo cyclic rotation. It would be
wrong to discard this component as an empty reduced graph.

**(3) Termination of corridors and bijection.** Starting from an outgoing edge
at a marked vertex, if deterministic continuation never reached a marked
vertex, some unmarked vertex would repeat. The repeated segment would be a
closed positive directed subgraph with unique outgoing type at every vertex,
with **no** exit to a marked vertex. Strong connectivity of \(G_m\) forbids
this. Therefore every corridor terminates. Every original Euler tour visits
some marked vertex (it uses all supported edges), and is uniquely cut just
before each departure from a marked vertex. Between successive marks its
continuation is forced and equals \(P_a\) for the departure type \(a\).
Thus collapse produces a macro Euler word using exactly \(m(a)=\mu(a)\)
occurrences of each \(a\). Conversely, expand any reduced macro Euler word.
Path endpoints match cyclically; each type \(e\) occurs the number specified
by (coverage), proved by decomposing **one** existing original Euler tour.
As the count is independent of macro order, every expansion is a valid
original Euler word. Parsing and expansion are inverse operations modulo
rotation. Corridors may merge; the corresponding forced shared edge is
traversed once **per entering macro occurrence**, and (coverage) prevents
overcounting or missing copies. Reduced balance and connectivity also follow
from collapsing one original Euler tour.

**(4) Emission.** Expansion replaces every macro \(a\) by its identical
ordered original path \(P_a\); replacing macro labels by their concatenated
original labels gives precisely the same emitted output (for a compatible
cyclic cut), even when some labels are empty. Raw cyclic k-block counts are
rotation-invariant for all positive \(k\). Taking identical attainable sets
preserves every exact extremal statistic.

**(5) Domains.** A rooted original Euler word is a cut of an original cyclic
edge word. The established bijection reconstructs every original cyclic edge
word; trying each original edge boundary gives every rooted source word.
Apply \(D\) to each reconstructed source cut. Conversely every admitted cut
comes from an original Euler word with prescribed histogram. No extra
rooted words are created and none are lost. This proves exactness of domain
pullback, not its computational efficiency.

## 3. Necessary-and-sufficient certificate for a proposed macro atlas

This is a **general candidate-reduction test**, not a claim that the local
forced-outgoing hypothesis characterizes all possible reductions.

Let \(S\ne\varnothing\) be a chosen set of marked original vertices. Give one
candidate macro path \(P_a\) per positive edge type \(a\) with tail in \(S\).
Each path must start with \(a\), end on its *first* return to \(S\), and have
all interior vertices outside \(S\). Give macro \(a\) multiplicity \(m(a)\).
Assume at least one macro Euler word exists.

* **All-macro-tour soundness** (every macro tour lifts to an original Euler
  tour) holds **iff** the path coverage identity above holds. The endpoints
  already ensure a closed original walk, and the identity gives precisely
  the required original counts. Necessity follows by taking any macro tour.
* Under soundness, **completeness** of edge-tour sets holds **iff** every
  original Euler word follows the prescribed path \(P_a\) between consecutive
  marked vertices after departing on \(a\). This condition is finite and
  decidable by exhaustive tour enumeration for fixed \(m\). Because first
  edge types identify macros and no internal marked vertex occurs, parsing
  is unique. In the canonical construction above, uniqueness of the active
  outgoing edge type at every unmarked vertex is a cheap **sufficient local
  certificate** for this condition.
* For a general candidate, preservation of cyclic attainable outputs for
  **every possible** emission \(\psi\) is **iff** the expanded edge-type
  necklace set equals the original edge-type necklace set. Forward: use
  one unique output symbol per original edge type, which makes emitted output
  necklaces precisely edge-type necklaces. Reverse: apply any emission
  substitution to the equal sets. For a *single fixed* emission, collisions
  can conceal missing tours; structural conditions need not be necessary.

Thus the proposal has both a locally provable exact sufficient construction
and a precise necessary/sufficient semantic test. It does **not** smuggle the
claim that forcing is necessary for every conceivable smaller model.

## 4. Cyclic erased-run caps, no expansion required

A source site's edge is *silent* iff its emission is empty. For a nonempty
periodic source, define the longest consecutive run of silent sites in its
**bi-infinite cyclic repetition**. In particular, a wholly silent source has
run length \(\infty\) and fails every finite cap \(R\). This convention must
not be confused with the largest silent interval in a *single finite cut*.

For a finite binary silence segment \(w\), use the signature
\(\sigma(w)=(\ell,p,s,M)\): length, erased prefix length, erased suffix
length, and largest internal erased run. Concatenation is governed by
\[
\begin{aligned}
 \ell &=\ell_1+\ell_2,\\
 p&=\begin{cases}\ell_1+p_2,&p_1=\ell_1\\p_1,&\text{otherwise},\end{cases}\\
 s&=\begin{cases}\ell_2+s_1,&s_2=\ell_2\\s_2,&\text{otherwise},\end{cases}\\
 M&=\max(M_1,M_2,s_1+p_2).
\end{aligned}
\]
This operation is associative because it computes the true signature of
concatenated strings. The maximum *cyclic* silent run is \(\infty\) if
\(p=\ell\), otherwise \(\max(M,s+p)\). Consequently the cap
\(\max\_\mathrm{cyclic\ silent}\le R\) can be tested **exactly on the reduced
macro word** by composing precomputed macro signatures. Shared corridors,
empty output, boundary wrapping, and multiple silent macro edges are covered.
The cap is a predicate on the sequence of site emissions, not on runs of
zero characters in the output.

## 5. Finite-type source restrictions and rooted emission alignment

For any finite set \(F\subset A^+\) of forbidden cyclic source blocks, put
\(d=\max_{f\in F}|f|\). For every macro source-letter string \(w\), store
\(\tau_F(w)=(|w|,\mathrm{prefix}_{d-1}(w),\mathrm{suffix}_{d-1}(w),b)\), where
\(b\) records whether an occurrence of any \(f\in F\) is present in the
*linear* string. The signature product concatenates lengths, truncates
prefixes and suffixes, and checks a new forbidden substring in
\(\mathrm{suffix}_{d-1}(u)\,\mathrm{prefix}_{d-1}(v)\). This product is
associative (it equals the signature of \(uv\)). For a cyclic source of length
\(n\ge d\), additionally check that combined final suffix + initial prefix
contains no forbidden word. If \(n<d\), the **entire source** fits in the
stored prefix; test its periodic repetition for all \(n\) starting sites.
This is an exact finite-state summary of cyclic finite-type restrictions
without lifting a full source for the predicate. Different finite forbidden
sets induce different summary monoids.

For *rooted* outputs, choose an **original source-edge index** \(i\), not an
arbitrary character index inside an output macro-label. When \(\psi(e_j)\)
is indexed to source site \(j+\lambda\), the output for the source rooted at
\(i\) begins with the label of edge \(j=i-\lambda\pmod n\). In particular,
\(\lambda=r\) for the centered-radius construction at the beginning of this
note. With a root-sensitive predicate \(D(x)\), check \(D\) on the source
rotated to \(i\), then emit starting from \(j=i-\lambda\). Failing to carry
this offset makes rooted claims false even if cyclic output classes agree.

## 6. Exact example, counterexamples, and certificates

**Nontrivial bound preservation.** At \(h=2\), take
\(m(00)=m(01)=m(10)=2\), and \(\psi(e)\) equal to the first source symbol
of \(e\). The only branch vertex is \(0\). Macros are
\(M_{00}=[00]\), multiplicity 2, and \(M_{01}=[01,10]\), multiplicity 2.
Original length 6 contracts to 4 macro traversals. The exact attainable
output necklaces are **`000101`** and **`001001`**. Thus the raw cyclic
count of the length-3 pattern `000` has exact extrema **0 and 1**; the
corresponding extrema for `001` are **1 and 2**. There is no choice of output
cut that changes these counts.

**Merging corridors (critical).** At \(h=3\), the cyclic word `0000101`
has histogram `000:2, 001:1, 010:2, 100:1, 101:1`. The forced edge `010`
is shared between the paths `[001,010]` and `[101,010]`; the three other
supported edges `000` (two copies) and `100` (one copy) form additional
macros. Thus length 7 contracts to **5** traversed macros, *without*
incorrectly duplicating or discarding the shared edge type.

**Pure cycle.** Histogram `01:2, 10:2` at \(h=2\) has no branch and does
not reduce to the empty source: it uniquely reconstructs cyclic `0101`.
For emission `01 -> a, 10 -> b`, the output is cyclic `abab`.

**Connectivity.** Histogram `00:1, 11:1` is balanced but disconnected; no
single cyclic source realizes it. A reduction that merges component words
would assert a false witness.

**Erasure wrapping.** At \(h=1\), histogram `0:2, 1:2`, `0 -> empty`,
`1 -> x`, a source with two adjacent zeros has erased-run maximum 2,
whereas alternating zeros and ones has maximum 1. A cap \(R=1\) must remove
the former, including runs crossing the chosen cyclic cut.

**Rooted-output warning.** Histogram `0:1` with `0 -> ab` permits rooted
output `ab`, **not** `ba`. The cyclic output necklace happens to be the same.
This is why a cyclic-output theorem cannot silently claim rooted linear
output equality by rotating output characters arbitrarily.

### Reproduction

From repository root, using Python 3.12 or later, standard library only:

```sh
python -m unittest discover -s tests -v
python experiments/structural_reduction_certificates.py
```

The independent direct-word oracle tests:

- **5,730** comparisons across all binary source words of lengths 1..8,
  orders 1..3, fixed histogram classes, six deterministic/seeded edge
  emissions, and caps `None,0,1,2,3`; both cyclic and rooted output sets
  are compared (two assertions per comparison).
- **2,868** analogous comparisons across ternary source words of lengths
  1..6 and orders 1..4, including \(h>n\), with one multicharacter erasing
  emission and four caps.
- **2,805** independent binary histogram feasibility comparisons for
  \(h=2,3\), multiplicities in `0..2`, and total length `1..7`, including
  impossible balanced disconnected cases; feasible instances also have
  output-set comparisons.
- **955** direct checks for five finite forbidden-block sets on all binary
  source words of lengths 1..8 and \(h\in\{1,2,3\}\).
- **3,000** randomized erasure-signature and **2,500** randomized finite-
  type-summary associativity and direct-word checks, plus named regression
  witnesses above.

Finite checks do not prove the theorem universally. The proof is a separate
mathematical argument; programs/certificates provide independently computed
examples and regression protection.

## 7. Scope boundaries and open work

- Fixed **one** complete cyclic \(h\)-block histogram and a deterministic
  finite-radius/edge-local rule. The theorem does not independently prove
  STD's finite- or global-horizon closure claims over **all** histograms.
- Every macro retains an ordered original edge path, its multiplicity, and
  the original source-site cut when rooted semantics are needed. Storing
  only endpoints or emitted labels is generally insufficient.
- The required Euler criterion is for one connected cyclic realization;
  collections of disjoint Eulerian components are not admissible sources.
- Arbitrary post-lift source predicates are exact but may eliminate any
  computational benefit. The two specific finite-state summaries here cover
  erased-run caps and finite forbidden-block sets, not every regular or
  context-sensitive constraint.
- Enumerating reduced Euler circuits still has exponential worst-case cost.
  No polynomial-time algorithm for all attainable outputs is asserted.
- No general necessity of unique outgoing type for *other* possible reduction
  mechanisms is claimed; no external originality or formal verification is
  claimed. The October 10 reset-gap erratum is not repaired by this theorem.

**References:** `README.md`, `docs/RESEARCH_STATE.md`, `docs/TASK_BOARD.md`,
`audits/archive/STD_Audit_2026-10-10.txt`, Issue #2. No historical theorem
status was silently promoted.
