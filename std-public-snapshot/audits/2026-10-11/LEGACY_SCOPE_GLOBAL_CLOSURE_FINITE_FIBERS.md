# Source-backed scope audit: global closure and all-length finite inverse fibers

**Date:** 2026-10-11  
**Researcher:** B, independent audit track  
**Task:** issue #27  
**Status:** provenance/scope audit only. This memo does not promote any theorem to external peer review or formal verification, and it does not modify the canonical research-state ledger.

## 1. Pinned primary sources

This audit uses the literal October 9 proof sources on main `private-history-omitted`:

1. `audits/archive/STD_Global_Closure_Audit_2026-10-09.md`, Git blob `private-history-omitted`.
2. `audits/archive/STD_Ten_Problems_Results_2026-10-09.md`, Git blob `private-history-omitted`.

A later consistency check used `audits/archive/STD_Recovery_Spectrum_Status_2026-10-09.md`, blob `private-history-omitted`. That later note restates the same full-cyclic closure convention and rooted-recovery convention; it is not substituted for the two primary proofs above.

The primary notes classify themselves as self-contained internal mathematical derivations with executable checks, not external peer review, proof-assistant verification, or established originality. This memo preserves that evidence classification.

## 2. Common local-rule model

Both claims below concern a **complete finite-radius synchronous local emission rule**

    phi: A^(2r+1) -> B*,   r >= 0,

over finite nonempty alphabets. Every source center reads its context from the original periodically extended cyclic source and emits a finite word; an emission may be empty.

The underlying source family is the **full family of all nonempty finite cyclic words of arbitrary positive length** over A. The sources are not restricted by a finite-type language, fixed inventory, fixed absolute length, or an external phase/origin condition.

This common model has two different observables, and the distinction is essential:

- **Forward closure:** source and output statistics are raw cyclic block histograms. A cut is irrelevant.
- **Inverse fibers:** source and output words are rooted. The output cut is immediately before the emission of source position zero, even if that emission is empty. Source rotations are not automatically identified.

## 3. Claim A: global closure finite graph test

### Exact statement retained from the primary source

For a nonempty cyclic source X, let C_h(X) be the raw periodic h-block histogram, including repeated wrapping when h > |X|. The empty output has zero block counts. Define

    H_T(k) = min { h >= 1 :
        C_h(X) = C_h(Y) implies C_k(TX) = C_k(TY)
        for all source pairs X,Y },

with value infinity when no such h exists, and let

    K_T = sup { k >= 1 : H_T(k) < infinity }.

Form the full de Bruijn source graph with vertices A^(2r), edges A^(2r+1), and edge labels phi(e). Let G_0 be its subgraph of silent edges, i.e. edges with empty emission.

The primary global-closure theorem states:

    K_T = infinity

if and only if at least one of the following holds:

1. G_0 is acyclic; or
2. the full labeled source graph satisfies the periodic phase condition of the proof.

The periodic phase condition is a condition on **closed return-walk output words**, equivalently on a graph phase assignment relative to one primitive output period. It is not the assertion that every individual nonempty edge image must commute with every other edge image. Context can enforce phase alignment even when individual images do not commute.

The all-erasing rule is included separately as a trivial globally closing case.

### Quantitative consequences and their exact hypotheses

If G_0 is acyclic and g is the maximum number of silent edges in a directed silent path, then for every k >= 1,

    H_T(k) <= 2r + 1 + (k - 1)(g + 1).

If a silent cycle exists and the periodic phase condition holds, then all cyclic output histograms are determined by the local output-length statistic ell(X) = |T(X)|, and

    H_T(k) = H_ell <= 2r + 1

for every k >= 1.

If a silent cycle exists and the periodic phase condition fails, the proof constructs a finite output order with infinite horizon.

Let

    M = max_e |phi(e)|.

Only when M >= 1, the primary source gives the finite all-k test bound

    H_T((8r + 2)M) < infinity
        iff
    H_T(k) < infinity for every k >= 1.

The all-erasing case has M = 0 and is handled as a separate trivial case; the displayed cutoff must not be miswritten as a statement about H_T(0).

### Scope corrections that must stay attached

The theorem does **not** say:

- that one fixed source horizon works for every output order. The identity map already has H_T(k) = k;
- that arbitrary positional, sorting, nonlocal, or general program transformations satisfy the graph criterion;
- that the same necessity theorem automatically applies on restricted source languages, finite-type subshifts, fixed-length domains, or fixed inventories;
- that a failed computation proves an infinite horizon;
- that the common-period condition can be checked by requiring all individual emitted edge words to commute.

The primary document reports large finite implementation checks, including a complete 6,561-rule binary radius-one family, but explicitly treats those computations as checks/certificates for the implementation rather than substitutes for the analytic proof.

## 4. Claim B: finite rooted inverse fibers across all source lengths

### Exact rooted convention

Fix a rooted finite output word Y = y_0 ... y_(m-1). The primary inverse construction uses the product graph with states (v,j), where v is a source-context vertex and 0 <= j <= m. A source edge with emitted word u advances

    (v,j) -> (w,j+|u|)

only when the corresponding substring of Y equals u. An empty emission consumes one source site while leaving j unchanged.

For a positive source length n, the product graph counts **rooted** source words X in A^n satisfying T(X) = Y. There is no quotient by source rotation or by output rotation in this default theorem.

### Exact all-length finiteness criterion

For the same complete finite-radius local-rule class, the following are equivalent:

1. every rooted output has finitely many rooted source preimages across **all positive source lengths**;
2. the empty rooted output has finitely many rooted source preimages across all positive source lengths;
3. the silent source graph has no directed cycle;
4. there exists a constant d such that

       |X| <= d |T(X)|

   for every nonempty source X.

If a silent directed cycle exists with source word U, then U^j gives infinitely many distinct positive source lengths mapping to the empty output.

Conversely, if the silent graph is acyclic and z is its longest silent path length, then one may take d = z+1. Every fixed rooted output of length m then has preimages only among the finitely many source lengths at most d m.

Equivalently, for a particular rooted target Y, the product-graph fiber is infinite exactly when a directed cycle occurs on a successful path that starts and finishes with the **same retained source base context**. Reachability from one base and returnability to a different base cannot be mixed.

### Relationship to global closure

Acyclic silence implies both the finite-all-length rooted-fiber property above and global statistical closure, with the same bounded-silence estimate yielding

    H_T(k) <= (k - 1)(z + 1) + 2r + 1.

The converse is false. A rule can have globally predictable periodic outputs while having infinitely many sources mapping to the empty output. Therefore “global closure” and “all rooted fibers finite” must not be treated as equivalent.

### Scope corrections that must stay attached

The finite-fiber theorem does **not** say:

- that erasure itself causes an infinite fiber; only a repeatable **silent directed cycle** creates the all-length obstruction;
- that the theorem is about cyclic necklaces or source/output words modulo rotation;
- that a fixed-length inverse problem is infinite merely because the all-length fiber is infinite;
- that a resource limit, timeout, or incomplete search proves an infinite fiber;
- that the criterion applies to arbitrary positional or nonlocal transformations outside the complete finite-radius local-rule class.

The quantifier “across all positive source lengths” is essential. At any fixed source length, the source set is finite.

## 5. Source-backed disposition

| Historical shorthand | Source-backed disposition |
|---|---|
| “Global closure is decidable.” | **Retain only with scope:** complete finite-radius local emission rules on all nonempty finite cyclic source words, raw periodic block counts. |
| “No silent cycle implies all horizons finite.” | **Retain.** Acyclic silence gives the explicit linear-in-k upper bound above. |
| “A silent cycle means closure fails.” | **Reject as overbroad.** The periodic-output/phase branch and all-erasing rule are globally closing silent-cycle cases. |
| “All nonempty emissions must commute.” | **Reject as the theorem statement.** The condition is on return-walk output words / graph phases. |
| “One finite test decides all output orders.” | **Retain with M >= 1:** test order (8r+2)M; all-erasing M=0 is separate. |
| “Every output has finitely many preimages iff there is no erasure.” | **Reject.** Erasures are allowed; the exact obstruction is a silent directed cycle. |
| “Finite inverse fibers are a necklace theorem.” | **Reject.** The primary theorem is rooted and does not quotient rotations. |
| “Finite fibers and global closure are equivalent.” | **Reject.** Finite all-length rooted fibers imply global closure, but not conversely. |

## 6. Limits of this audit

This packet repairs provenance and scope presentation only. It does not:

- fill any of the repository's inherited empty scope fields by inference;
- reclassify an internal proof as external peer review or formal verification;
- extend the full-source theorem to constrained finite-type domains;
- change `docs/RESEARCH_STATE.md`, the consolidated claim ledger, or any theorem source;
- claim independent reproduction of every historical numerical total.

The two primary proof sources are present and sufficiently explicit to support the scope statements in this memo. No missing-source limitation applies to these two claims.
