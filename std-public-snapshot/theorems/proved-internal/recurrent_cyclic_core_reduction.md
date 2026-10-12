# Recurrent cyclic-core reduction for finite-type STD

**Date:** 2026-10-11  
**Status:** proved-internal; amendment/strengthening of the finite-type theorem in PR #6; not externally peer reviewed or formally verified.  
**Trigger:** issue #7.

## 1. Domain and conventions

Let \(A\) be a finite nonempty source alphabet, let \(m\ge 1\), and let \(\mathcal W_m\subseteq A^m\). The source domain \(\mathcal X\) is the set of all **nonempty finite cyclic words of arbitrary positive length** whose periodic length-\(m\) windows all lie in \(\mathcal W_m\). Periodic windows are used even when the source period is shorter than \(m\). No root or distinguished cut is part of the source object for the theorems below.

For \(t\ge m\), let \(G_t\) be the usual higher-block directed graph: a linearly allowed word \(w\in A^t\) is an edge from \(w_0\cdots w_{t-2}\) to \(w_1\cdots w_{t-1}\). A cyclic source \(X\) gives the edge histogram \(N_t(X)=C_t(X)\).

Let \(T\) be a synchronous radius-\(r\) local emission rule \(\phi:A^{2r+1}\to B^*\), where erasure is allowed. Outputs are cyclic concatenations, and all output statistics in this note are raw periodic block counts. Rooted output words are outside the statement.

## 2. Recurrent cyclic core

Define
\[
E_t^\circ=\{e\in E(G_t): e\text{ lies on a directed closed walk}\}.
\]
The subgraph on these edges and their incident vertices is the **recurrent cyclic core** \(G_t^\circ\). An edge outside \(E_t^\circ\) is **cyclic-transient**.

For an edge \(e:u\to v\), the following are equivalent:

1. \(e\in E_t^\circ\);
2. \(e\) lies on a directed closed walk;
3. \(v\) reaches \(u\);
4. \(u\) and \(v\) lie in the same strongly connected component.

This is a property of the finite graph and is exactly checkable.

## 3. Exact cyclic-core reduction theorem

**Theorem A (transient-edge elimination is exact).** For every \(t\ge m\):

1. A linearly allowed \(t\)-block occurs as a periodic \(t\)-window of some \(X\in\mathcal X\) if and only if its edge lies in \(E_t^\circ\).
2. Hence \(N_t(X)\) is identically zero on \(E(G_t)\setminus E_t^\circ\) for every \(X\in\mathcal X\).
3. Deleting all cyclic-transient edges changes neither the set of finite cyclic source words nor the set of attainable recurrent edge histograms.
4. Any edge-additive cyclic statistic may be restricted to columns \(E_t^\circ\) without changing its value on any admissible source.
5. The cyclic source domain is empty if and only if \(E_t^\circ\) is empty.

**Proof.** If an allowed \(t\)-block occurs in a cyclic source, following successive periodic \(t\)-windows of that source gives a directed closed walk containing the corresponding edge. Thus occurrence implies membership in \(E_t^\circ\).

Conversely, suppose an edge lies on a directed closed walk. Successive higher-block edges overlap in \(t-1\) symbols. Reading the final source symbols around the closed walk gives a finite cyclic word. Its periodic \(t\)-windows are precisely the traversed higher-block edges, including when the cyclic period is shorter than \(t\). Each traversed edge is linearly allowed, so all periodic \(m\)-windows belong to \(\mathcal W_m\); hence the resulting source lies in \(\mathcal X\). This proves the equivalence and the zero-coordinate claim. The remaining statements follow because every cyclic source walk uses only recurrent edges, while every recurrent edge belongs to at least one admissible cyclic source walk. \(\square\)

## 4. Consequence for finite-type horizon rank tests

Let \(s=\max(m,2r+1)\). Apply Theorem A before any connectivity or silence test.

A finite cyclic domain is called **irreducible for the reference solver** when \(G_s^\circ\) is nonempty and strongly connected. For output order \(k>1\), compute the silent-run bound using only recurrent edges of \(G_s^\circ\). Cyclic-transient silent paths are irrelevant because no cyclic source traverses them.

If the recurrent silent-edge subgraph is acyclic with maximum silent path length \(R\), set
\[
L=s+(k-1)(R+1).
\]
For \(k=1\), no silence bound is needed and \(L=s\).

Construct the local output matrix \(F_k\) only on recurrent \(L\)-block edges \(E_L^\circ\), or equivalently construct it on all linearly allowed \(L\)-blocks and delete transient columns. Let \(D\) be incidence on \(G_L^\circ\), and let \(P_h\) project an \(L\)-edge histogram to its source \(h\)-block histogram.

**Theorem B (rank criterion on the recurrent core).** If \(G_L^\circ\) is strongly connected, then for \(1\le h\le L\),
\[
C_h(X)=C_h(Y)\Longrightarrow C_k(T(X))=C_k(T(Y))
\]
for all \(X,Y\in\mathcal X\) if and only if every row of \(F_k\) lies in the rational row span of \([D;P_h]\), equivalently
\[
\operatorname{rank}_{\mathbb Q}[D;P_h;F_k]
=
\operatorname{rank}_{\mathbb Q}[D;P_h].
\]

Therefore scanning \(h=1,\ldots,L\) gives the exact minimum horizon in this irreducible recurrent-core scope.

**Proof.** Sufficiency is unchanged from the PR #6 theorem because every admissible \(N_L(X)\) is supported on \(E_L^\circ\) and satisfies \(DN_L(X)=0\).

For necessity, a failed row-span condition yields an integer vector \(v\in\ker D\cap\ker P_h\) with \(F_kv\ne0\). Strong connectivity of \(G_L^\circ\) gives a strictly positive integer circulation \(z\) on every recurrent edge by summing directed cycles containing the edges. For sufficiently large \(N\), both \(Nz\) and \(Nz+v\) are strictly positive balanced integer circulations. Their supports are the whole strongly connected recurrent core, so each lifts to a single Euler circuit and therefore to one admissible cyclic source. They have equal \(C_h\) and different output \(C_k\), establishing necessity. No transient coordinate is required. \(\square\)

The original PR #6 theorem with the stronger hypothesis that the **raw** \(G_L\) is strongly connected remains a valid sufficient special case; Theorem B strictly widens the accepted presentations by deleting coordinates that are impossible for cyclic sources.

## 5. Reducible recurrent cores and cross-support compatibility

If \(G_L^\circ\) has multiple SCCs, the irreducible reference solver must not report an exact global answer from independent per-SCC calculations.

Every single cyclic source has an Euler support contained in one SCC, but two sources being compared may lie in **different** SCCs. Global \(h\)-block sufficiency therefore requires comparing source-count cones across support pairs.

Precisely, retain the support-pair rational feasibility theorem from PR #6, but apply it after transient edges are removed. For Euler supports \(S,T\subseteq E_L^\circ\), one must test the cross-support equality
\[
P_{h,S}x=P_{h,T}y
\]
together with balance, strict positivity on the named supports, and a nonzero target-coordinate discrepancy. The supports \(S\) and \(T\) need not belong to the same SCC.

**Limitation.** Treating each surviving SCC separately verifies only within-SCC pairs. It does **not** establish compatibility between different recurrent supports and is not a replacement for the support-pair theorem.

## 6. Issue #7 regression and boundaries

Take \(A=\{0,1\}\), \(m=2\), and \(\mathcal W_2=\{00,01\}\). The raw graph has edges \(00:0\to0\) and \(01:0\to1\). Edge \(01\) lies on no directed closed walk, so
\[
E_2^\circ=\{00\}.
\]
Thus every admissible cyclic source is \(0^n\). Under identity emission, \(C_1(0)=n\) determines every output block count, so the exact horizon for \(k=1\) is \(1\). The previous rejection of this input was an API/domain-classification error, not a counterexample to the rank proof.

Two boundary cases are intentionally distinct:

- If \(\mathcal W_2=\{01\}\), the raw graph is nonempty but the recurrent cyclic core is empty. There is no nonempty admissible cyclic source.
- If \(\mathcal W_2=\{00,01,11\}\), transient edge \(01\) is removed but loops \(00\) and \(11\) survive in different SCCs. The cyclic domain is nonempty and genuinely reducible. Cross-support compatibility remains necessary.

The executable regression in tests/test_sft_closure.py covers the reported \(k=1\) case, higher-block trimming at \(k=2\), the empty-core boundary, and the multiple-recurrent-SCC boundary.

## 7. Erasure assumptions

Theorem A itself is independent of erasure.

For the local finite-lookahead construction at \(k>1\), the silent-edge subgraph of the **recurrent cyclic core** must have no directed cycle. This is the exact cyclic condition relevant to the reference construction. A silent linearly allowed path that is cyclic-transient cannot appear in a source and must not enlarge the cyclic silence bound.

For \(k=1\), silent cycles are allowed because no output lookahead is needed.

A prescribed finite cap on consecutive erased source positions may still be encoded as a finite-type source restriction as in PR #6; after forming that constrained presentation, take its recurrent cyclic core before applying the rank/support theorems.

## 8. Source-domain and root limitations

These results require:

- all nonempty finite cyclic sources of arbitrary positive lengths satisfying the stated finite-type restriction;
- periodic source windows, including periods shorter than the presentation length;
- raw cyclic output block counts;
- no fixed absolute source length or fixed inventory in the rational-scaling witness arguments.

They do not by themselves prove statements for rooted source words, fixed cuts, partial source domains, nonhomogeneous inventory constraints, or arbitrary restrictions outside the finite-type presentation. Rooted outputs require a separate alignment/lifting statement.

## 9. Pinned evidence

Inputs re-read before this task:

- main commit: private-history-omitted
- PR #6 pre-repair head: private-history-omitted
- API repair commit: private-history-omitted
- regression commit: private-history-omitted

This amendment is separate from the reset-gap work in PR #5 and from the forced-continuation reduction in PR #8. Candidate dependencies remain provisional until coordinator review and merge.
