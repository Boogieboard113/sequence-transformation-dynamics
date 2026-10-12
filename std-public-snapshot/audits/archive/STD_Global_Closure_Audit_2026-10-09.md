# STD audit and a constructive global-closure theorem

**Date:** October 9, 2026  
**Status:** Self-contained derivations and executable exact checks. This is an internal mathematical audit, not independent peer review. Priority and originality have not been established.

## Executive result

For the current STD model—an explicitly specified finite-radius synchronous local emission rule on **all nonempty finite cyclic source words**, with finite alphabets and raw periodic block counts—the global closure question is decidable by a finite graph-and-word test.

The test does not invoke the previous weighted-automaton fixed-k theorem. It proves that one of the following occurs:

1. The silent-edge graph is acyclic. All output sizes have finite horizons, with an explicit linear-in-k upper bound.
2. A silent cycle exists, and all cyclic outputs follow one fixed periodic word, up to rotation and repetition. Every horizon equals the horizon of the local output-length statistic.
3. A silent cycle exists and the periodic-output condition fails. A finite output size has infinite horizon, with explicit source counterexamples for every proposed source horizon.

Write M for the maximum emitted word length and r for the source radius. If M>=1, the following finite test principle holds:

    H_T((8r+2)M) < infinity
       if and only if
    H_T(k) < infinity for every k>=1.

The direct graph test is preferable to constructing the possibly large fixed-k matrix at that bound. This result settles all-k *decidability* in the stated model. It does not give a closed form for every infinite horizon spectrum or settle arbitrary nonlocal programs, restricted languages, or sieve limits.

## 1. Audit scope and findings

The complete text of `STD_Comprehensive_Advance_2026-10-09.md` and `STD_Audit_2026-10-09.md` was inspected. The executable general-horizon package supplied in this conversation was extracted and its actual code and certificate files used in the checks below.

### 1.1 Retained results

The cyclic additive rank criterion is retained under its full-source and additive-representation hypotheses. For a known L-local coefficient matrix F, h-block sufficiency is equivalent to

    rank([D_L;P_h]) = rank([D_L;P_h;F]),

or equivalently F=U D_L+G P_h. Here D_L is the source de Bruijn incidence matrix and P_h projects L-block counts to h-block counts.

The general fixed-k proof was checked through its five substantive steps:

- Exact homogeneity Q(X^t)=t Q(X), together with a bounded concatenation defect.
- Extension of a histogram-dependent Q to a rational linear functional on the source circulation space.
- Construction of a protected guard with immutable output, including short source periods and empty outputs.
- Equivalence between finite local additivity and eventual vanishing of guarded two-ended differences.
- Exact stabilization/annihilation of the descending reachable tail spaces.

No counterexample or proof gap was found in these steps under the stated hypotheses. In particular, necessity uses protected output on both cyclic arcs; a one-sided guard argument would not suffice. This remains an internal proof audit, not external certification.

The 81-rule all-k classification was independently matched by the new graph test. Its 81 triple classifications were recomputed with the saved fixed-k method, and 248 saved rational reconstruction identities were actually replayed. These are newly run checks, not repetitions of the old report's test totals.

### 1.2 Scope corrections retained

Finite H_T(k) for each k is not the existence of one source horizon for all k. The identity has H_T(k)=k. A finite-state evaluator of an ordered input is not, by itself, a finite-histogram predictor. Failure to finish a computation is not mathematical infinity.

The common-period condition below applies to *return-walk output words*, not necessarily to every individual emitted image. Context can enforce phase alignment even when individual emissions do not commute.

The new global theorem supersedes the earlier status statement that general all-k decidability was not established. It does not turn the current model into a theory of arbitrary positional or nonlocal transformations.

## 2. Definitions

Let A and B be finite nonempty alphabets and let

    phi: A^(2r+1) -> B*,    r>=0.

At each position of a source circle X, evaluate phi on the original radius-r context and concatenate the emitted words in cyclic order. Empty words are permitted emissions. The result T(X) can be empty.

For a nonempty cyclic word X, C_h(X) is the raw histogram of h-blocks beginning at each source position, using periodic extension even if h>|X|. The empty output has zero counts. Consequently sum_w C_h(X)[w]=|X|.

Define H_T(k) as the least h>=1 for which C_h(X)=C_h(Y) implies C_k(TX)=C_k(TY) for all source pairs, or infinity if none exists. Define

    K_T = sup{k>=1 : H_T(k)<infinity}.

Output marginalization gives H_T(k+1)>=H_T(k). The output single-symbol histogram is a (2r+1)-local sum, so H_T(1)<=2r+1. Therefore finite output sizes form {1,...,K_T} when K_T is finite, and all positive integers otherwise.

### 2.1 The labeled source graph

Let G have vertices A^(2r) and edges A^(2r+1). Edge e goes from its length-2r prefix to its length-2r suffix and has output label phi(e). For r=0 the graph has a single empty vertex.

The graph is strongly connected. In fact any vertex can reach any other by appending the target vertex's 2r letters, so its directed diameter is at most 2r.

A closed walk specifies a cyclic source word by reading the last source letter of each edge. The emitted edge labels agree with T's emissions up to a cyclic rotation. Thus all output block counts agree exactly. This remains true for walks shorter than 2r.

A **silent edge** has empty output. Let G_0 be the graph consisting of these edges. A silent directed cycle can be repeated arbitrarily many times without emitting output. Equivalently, a silent cycle supplies a nonempty periodic source circle whose entire output is empty.

## 3. An elementary output-word lemma

For nonempty finite words u,v, put n=|u|+|v|. Then

    C_n(uv)=C_n(u)+C_n(v)
        if and only if
    uv=vu.

### Proof

If u and v are powers of the same primitive word p, the equality holds at every block size. The elementary commutation theorem uv=vu implies exactly this common-root property; it follows by successively canceling the shorter prefix, or by the Euclidean word argument.

For the reverse implication, suppose the histogram equality holds and write W=uv. Every n-block of the two-sided periodic word u^infinity occurs among the cyclic rotations of W, because C_n(u) has nonnegative coordinates and is a summand of C_n(W).

All rotations of W have the same single-letter counts. Hence every n-window in u^infinity has the same single-letter counts. Comparing windows starting at i and i+1 forces the departing and entering letters to be equal. Thus n is a period of u^infinity.

Let d be its primitive period. Since |u| and n are periods, d divides both, and therefore divides |v|=n-|u|. At least one n-window of u^infinity is a rotation of W. As d divides n, W itself is d-periodic. Its prefix u fixes its phase: W is the length-n prefix of u^infinity starting with u. Therefore v is a power of the same primitive word as u, and uv=vu. QED.

In particular, noncommuting u,v have a nonzero integer additive defect

    D_k(u,v)=C_k(uv)-C_k(u)-C_k(v)

for some 2<=k<=|u|+|v|. Testing the finite words finds such a k; k=n always works.

## 4. Silent padding turns that defect into infinite horizon

Suppose Z is a nonempty silent closed walk based at q. Let P,Q be closed walks at q, with nonempty output labels u,v. If D_k(u,v) is nonzero, then H_T(k)=infinity.

### Proof and explicit witnesses

Fix any proposed source horizon h. Repeat Z enough times to form S=Z^m with at least h source edges. Let

    t=4(k-1)+1.

Consider the closed source walks

    X_h=(P S Q S)^t,
    Y_h=(P S)^t (Q S)^t.

Read their source words as in Section 2.1. They have identical h-block histograms: each contains t copies of each island P,Q and the same 2t separators S. An h-window cannot touch two islands, because every separator has at least h letters. Contributions near an island depend only on that island and the fixed separator, not on the order of the islands; windows wholly inside separators also agree.

Every piece is a valid closed walk at q, so no source-context assumptions are introduced at the joins. The outputs are cyclically (uv)^t and u^t v^t.

There is an error vector E satisfying

    C_k(u^t v^t)=t C_k(u)+t C_k(v)+E,
    ||E||_1 <= 4(k-1).

Indeed, the two output joins change at most 2(k-1) block starts, each replacing one histogram entry by another. Here t>=k ensures each nonempty piece u^t,v^t is long enough for this direct boundary count.

Consequently

    C_k(TX_h)-C_k(TY_h)=t D_k(u,v)-E.

A nonzero integer coordinate of D_k has magnitude at least one; t exceeds the entire error bound. The output histograms therefore differ for every h. QED.

This argument establishes infinite horizon without relying on the previous fixed-k weighted-automaton theorem or an unbounded search.

## 5. Finite phase test for all return words

Fix a vertex q in the strongly connected source graph. Choose shortest paths A_v from q to each vertex v and B_v from v to q; at q choose empty paths. Let a_v,b_v denote their output words.

Form the finite family of closed walks

    A_v B_v                              for every vertex v,
    A_tail(e) e B_head(e)                 for every edge e.

Call their output words the **test words**. Unless every edge emits nothing, at least one test word u is nonempty. Let p be the primitive root of u and d=|p|.

The following are equivalent:

1. Every test word belongs to p*.
2. Every closed walk based at q has output in p*.
3. There is a phase assignment theta(v) in Z/dZ with theta(q)=0 such that each edge e:v->w satisfies

       phi(e)[j] = p[(theta(v)+j) mod d]  for 0<=j<|phi(e)|,
       theta(w) = theta(v)+|phi(e)| mod d.

### Proof

Conditions 3=>2=>1 follow by reading the periodic letters and telescoping the phases.

For 1=>3, define theta(v)=|a_v| mod d. The test a_v b_v in p* gives

    |b_v| = -theta(v) mod d.

For an edge e:v->w, the test a_v phi(e) b_w in p* shows both that phi(e) follows p at phase theta(v), and that

    theta(v)+|phi(e)|+|b_w|=0 mod d.

Substitute the preceding relation for b_w to get the required phase update. QED.

Every cycle starting at v therefore emits a whole number of periods of the rotation of p at theta(v), or emits nothing. As cyclic histograms ignore rotation, for every source X and k>=1,

    C_k(TX) = |TX|/|p| * C_k(p).

The source-graph phase is internal to the rule certificate. It is not an extra absolute position or residue label supplied with the source histogram.

If a test word v does not belong to p*, it is nonempty and does not commute with u. Thus the output-word lemma and silent-padding construction provide an infinite-horizon certificate whenever q lies on a silent cycle.

## 6. Global-closure theorem

**Theorem.** For the full cyclic source model above, K_T=infinity if and only if either

- G_0 is acyclic; or
- the periodic phase condition in Section 5 holds for the full labeled graph.

The all-erasing rule is included as a trivial globally closing case; any one-letter period with constant phase certifies it.

If G_0 contains a cycle, the phase condition is necessary and sufficient. If it fails, a noncommuting pair of test return words produces some k with H_T(k)=infinity.

### 6.1 The bounded-silence branch

If G_0 is acyclic, let g be the maximum number of edges in a silent path. Then g is finite, at most |A|^(2r)-1. On any cyclic source, successive nonempty emissions are separated by at most g silent emissions, so their source centers are at distance at most g+1.

Assign each output k-block to the source position emitting its first symbol. Since every nonempty emission supplies at least one symbol, at most k-1 later active centers are needed. Including the rule contexts gives the explicit local window length

    L_k = 2r+1+(k-1)(g+1).

Thus

    H_T(k) <= L_k   for every k.

The finite formula is constructed by collecting all output blocks starting inside the central emission. Periodic extension handles short source words. A wholly silent source circle cannot occur in this branch because it would give a silent directed cycle.

### 6.2 The silent-cycle, periodic-output branch

If the phase condition holds, define the local output-length statistic

    ell(X)=|TX|=sum_i |phi(X_(i-r)...X_(i+r))|.

The formula in Section 5 shows that ell(X) determines every output histogram. Conversely, every raw output histogram determines ell(X) by summing its coordinates. Hence

    H_T(k)=H_ell   for every k>=1,
    H_ell<=2r+1.

The exact constant H_ell is computed by the earlier additive rank test applied to the scalar table |phi(e)|.

### 6.3 The silent-cycle, nonperiodic branch

Choose q on a silent cycle and perform the finite test of Section 5. If it fails, the words u,v do not commute. Sections 3 and 4 give a finite k and all-h source witnesses. Therefore K_T is finite.

Conversely, a passed test or acyclic silence graph proves finite horizons for all k, as just shown. These cases exhaust all rules. QED.

### Interpretation

An arbitrarily repeatable erased source region hides the order of arbitrary excursions from that region. Global statistical closure then forces those excursion outputs to commute. Strong connectivity propagates this constraint to a common periodic output pattern throughout the graph.

Bounded silent regions do not produce this obstruction: output patterns can always be traced back through a bounded number of source positions.

## 7. A finite bound on the first failure

Let M=max_e |phi(e)|>=1. The full source graph has diameter at most 2r, so each chosen outward or inward shortest path has at most 2r edges. Vertex test loops have at most 4r edges; edge test loops have at most 4r+1.

Thus every test word has length at most (4r+1)M. In a failed test, the noncommuting u,v therefore satisfy

    |u|+|v| <= (8r+2)M.

Sections 3 and 4 imply

    K_T finite  =>  K_T <= (8r+2)M-1.

Equivalently, setting B_T=(8r+2)M,

    H_T(B_T)<infinity  <=>  K_T=infinity.

The implemented bound may be smaller, using shortest paths of length at most min(2r,|A|^(2r)-1). A further improvement comes from the actual returned pair and its first nonzero additive defect. These witness sizes are upper bounds on the *first* infinite output size, not automatically the exact first failure.

For a radius-zero morphism with an available eraser, the theorem reduces to:

    global closure <=> all nonempty images are powers of one common word.

In that case every horizon is 1. Otherwise failure occurs by output size 2M. Without an eraser every non-erasing radius-zero morphism has finite horizons for all k.

The arbitrarily delayed reset-padding examples do not contradict the finite bound: their maximum image length M grows with their padding parameter. There is no assertion of one test size independent of the rule.

## 8. Exact cutoff and spectrum computation

The graph procedure settles K_T=infinity or K_T<infinity directly. It uses graph traversal, primitive-root computation, and finite word comparisons; it is polynomial in the explicit rule table and emitted-word data. It does not build the k-dependent weighted state space.

For a nonclosing rule, it returns k_0 with H_T(k_0)=infinity. Since H_T(1) is finite and the horizons are nondecreasing, binary search in [1,k_0] using the audited fixed-k decision procedure gives the exact K_T in O(log k_0) calls. This is implemented as the optional --exact-cutoff mode.

Each finite H_T(k) can then be computed by the existing exact rank method after obtaining a local formula. In the acyclic-silence branch the direct bound L_k gives such a formula without guards. In the periodic-output branch all horizons equal H_ell, so one scalar rank problem settles the whole spectrum.

This is an algorithmic classification, not a promised closed-form asymptotic formula for H_T(k) in every bounded-silence rule.

## 9. Examples and safeguards against overgeneralization

### Identity

There are no silent edges. Global closure holds, while H_T(k)=k on an alphabet with at least two symbols. Thus global closure does not imply a uniformly bounded source horizon.

### An erasing rule with bounded silent runs

On binary radius-one inputs, erase precisely context 010 and otherwise emit the center bit. Its only silent edge is 01->10, so the silent graph is acyclic with g=1. Therefore H_T(k)<=2k+1 for every k. Erasure itself is not an obstruction; repeatable silence is the key issue.

### Context-enforced alternating output

On alphabet {e,a}, erase every e-center and use

    eae -> empty, eaa -> 0, aae -> 1, aaa -> empty.

Every a-run of length at least two emits 01; shorter runs emit nothing. Every output is (01)^R with R=C_3(X)[eaa]. The source cycles eaeaaa and eaaeaa have equal pair histograms but R=1 and R=2, respectively. Thus H_T(k)=3 for all k.

The individual nonempty images 0 and 1 do not commute. Rejecting this rule on that basis would be wrong. Its return-walk outputs commute, and graph phases enforce the correct alternation.

### Separator deletion

The radius-zero rule e->empty, 0->0, 1->1 has a silent cycle and noncommuting return labels 0,1. Its spectrum is 1,infinity,infinity,... .

### Delayed cutoff

For e->empty and b->#^s b #^s, b in {0,1}, the earlier exact spectrum is H_T(k)=1 for k<=2s+1 and infinity for k>=2s+2. The new graph procedure reproduces the first failed size 2s+2 for the checked values s=1,...,6.

## 10. New checks actually completed

The graph implementation and its local certificate verifier were written for this audit. Their finite/infinite certificates do not use the earlier guarded representation. The fixed-k code was used for cross-checks and optional exact-cutoff refinement.

| Check | Completed result |
|---|---:|
| Saved exact rational reconstruction identities replayed | 248 |
| Small-word commutation/additivity lemma checks | 900 |
| All binary radius-one rules with each of eight contexts emitting empty, 0, or 1 | 6,561 graph classifications, each certificate verified |
| Explicit equal-source-histogram/unequal-output witness pairs at h=1,3,7 | 11,046 |
| Periodic-output formulas checked directly, including k longer than the source/output | 13,380 |
| Prior 81-rule all-k profiles matched | 81 |
| Prior triple decisions recomputed | 81, including direct all-erasing case |
| Prior triple tail certificates replayed | 80 |
| Additional varied graph versus guarded fixed-k decisions | 31 |
| Direct guarded-model versus cyclic-transform comparisons | 1,665 |
| Variable-length rules at radii 0,1,2 with graph certificates | 48 |
| Variable-length source witness pairs | 75 |
| Reset-padding cutoff families | 6, with 18 source witness pairs |
| Exact closure cutoffs recomputed for the prior run family | 81, all agree |

The complete 6,561-rule global classification is:

| Outcome | Number |
|---|---:|
| Bounded-silence graph: all k finite | 2,432 |
| Silent cycle with a nonempty periodic-output certificate: all k finite | 446 |
| All-erasing rule: all k finite | 1 |
| Silent cycle with a noncommuting obstruction: finite cutoff | 3,682 |

Thus 2,879 globally close and 3,682 do not, in this exact family. For this family the universal test bound is 10; the constructed failure certificates happened to use output sizes 2 through 8. Those constructed sizes are not asserted to be the exact cutoffs of all 3,682 rules.

Every universal statement above is justified by a proof; these computations check the implementation and supply independently replayable finite certificates. They are not a statistical substitute for the proof or external peer review.

## 11. Files and reproduction

The accompanying ZIP contains:

- `std_global_closure.py`: standalone graph decision, verifier, explicit source-witness construction, and optional exact cutoff.
- `run_audit_checks.py`: reproduction of the checks, using the bundled earlier fixed-k files for comparisons.
- `STD_Global_Graph_Certificates.json`: all 6,561 decisions and certificates.
- `STD_Global_Additional_Checks.json` and `check_summary.json`: variable-length examples, padding examples, and actual check totals.
- Example rule JSON files and output certificates.
- `prior_fixed_k/`: the unmodified earlier modules and data needed to reproduce cross-checks and run exact-cutoff refinement.
- This report and a README.

Example:

    python std_global_closure.py example_rule_0001.json --exact-cutoff --witness-h 5 --out result.json

This returns exact K_T=3 and a witness that source 5-block counts cannot determine output 4-block counts. Every finite fixed-k result for that rule below the cutoff is consistent with this: its triple horizon is 5.

The original audit and research files are left unchanged; this is a separate research addition.

## 12. Literature and remaining scope

Relevant established background includes:

- Karhumaki, Puzynina, Rao and Whiteland, *On cardinalities of k-abelian equivalence classes*, arXiv:1605.03319: factor-count equivalence and de Bruijn graph structure.
- Kiefer, *Notes on Equivalence and Minimization of Weighted Automata*, arXiv:2009.01217: exact finite-dimensional methods for weighted automata.
- *Combinatorics on Words Basics*, Archive of Formal Proofs: primitive roots, commutation, conjugation, and periodicity.

These primary-source pages were consulted for background. They are not being cited as proofs of the global-closure theorem derived here. A targeted literature and external proof review is needed before any originality claim.

The full-source assumption is essential. The source graph's strong connectivity and admissibility of every constructed padded closed walk drive necessity. The explicit (8r+2)M bound additionally uses the diameter of the full de Bruijn graph. It must not be transferred unchanged to arbitrary restricted source languages.

Also outside this result are arbitrary nonlocal programs, unbounded-alphabet transformations, infinite positional sieves, and automatic theorems on prime distribution. Infinite source frequencies require separate existence and normalization assumptions.

The next useful mathematical question is no longer whether all-k closure is decidable in this model. It is the finer growth and compression of the finite horizon spectrum in the bounded-silence branch, together with external verification of this theorem and practical certificate-efficient implementations.

### Primary-source links

- https://arxiv.org/abs/1605.03319
- https://arxiv.org/abs/2009.01217
- https://isa-afp.org/entries/Combinatorics_Words.html