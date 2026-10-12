# Exact finite horizons on cyclic finite-type source domains

**Date:** 2026-10-11  
**Status:** proved-internal (complete mathematical proofs below; not formally checked or independently peer-reviewed)  
**Research track:** foundations; restricted source domains, finite-horizon closure.  
**Scope:** raw periodic cyclic histograms and synchronous finite-radius rules. The bounded-silence hypothesis is essential to the displayed **uniform bound**, but not to the abstract additive support-cone theorem.

## 1. Question and result

The standard STD rank test for an edge-additive statistic on a strongly connected de Bruijn graph must **not** be applied without qualification to a reducible constrained source language. The obstacle is that a nonnegative circulation on disconnected components is not necessarily the histogram of **one cyclic word**.

This note provides a complete scoped extension:

1. A local output-count formula and explicit finite horizon for a cyclic finite-type (SFT) domain with a bounded run of erased positions.
2. An **exact rational row-rank test**, including constructive witnesses when it fails, if the associated higher-block graph is strongly connected.
3. A **necessary-and-sufficient finite rational linear-feasibility test** for arbitrary reducible higher-block graphs, with single-cycle witness extraction. This avoids the invalid global-row-rank extrapolation.
4. A concrete three-orbit counterexample to that extrapolation, plus edge cases for source-period lengths smaller than the look-ahead and for fixed source lengths.

The graph/linear-algebra ingredients overlap established results for irreducible edge shifts; the main contribution here is a fully scoped synthesis for STD's **finite cyclic words**, including reducible admissibility and erased-run caps. No originality or external verification is claimed.

## 2. Definitions and alignment conventions

Let finite nonempty alphabets be \(A,B\). Fix an integer \(m\ge 1\) and a set \(\mathcal W_m\subseteq A^m\). The **cyclic finite-type domain** \(\mathcal X\) consists of *all* nonempty finite cyclic words \(X=x_0\cdots x_{n-1}\), of arbitrary length \(n\ge1\), such that every periodic length-\(m\) window belongs to \(\mathcal W_m\). Indices are taken modulo \(n\), including when \(m>n\). We assume \(\mathcal X\ne\varnothing\).

Let \(r\ge0\) and \(\phi:A^{2r+1}\to B^*\). Output \(T(X)\) concatenates \(\phi(x_{i-r}\cdots x_{i+r})\) as \(i\) goes around the circle; output may be empty. For \(q\ge1\), \(C_q(X)(w)\) counts the \(n\) starting positions having periodic \(q\)-window \(w\); \(C_q(\epsilon)=0\). The least horizon on this **specified domain** is
\[
H_{T,\mathcal X}(k)=\min\bigl\{h\ge1:\ C_h(X)=C_h(Y)\Longrightarrow C_k(T(X))=C_k(T(Y))\quad\forall X,Y\in\mathcal X\bigr\},
\]
with value infinity if no such \(h\) exists. It is not a finite-sample minimum.

For \(t\ge m\), define the directed **higher-block graph** \(G_t\). Its edges are allowed length-\(t\) words \(w\), i.e. words whose internal \(m\)-windows belong to \(\mathcal W_m\); edge \(w\) joins prefix \(w_0\cdots w_{t-2}\) to suffix \(w_1\cdots w_{t-1}\). For \(t=1\) the common vertex is the empty word. Parallel labeled edges, if present in an equivalent graph presentation, are treated as distinct. A cyclic word yields a closed walk in \(G_t\) and an **edge histogram** \(N_t(X)=C_t(X)\). Conversely every nonempty closed walk in this de Bruijn graph yields a cyclic word, including walks of length less than \(t\).

Put \(s=\max\{m,2r+1\}\), and label each edge \(w\) in \(G_s\) by \(\psi(w)=\phi(w_0\cdots w_{2r})\). Relative to the original centered convention, the starting positions are shifted by \(r\); this merely rotates the concatenated cyclic output and therefore **does not change any** \(C_k(T(X))\).

An edge is **silent** if \(\psi(w)=\epsilon\). Suppose the silent-edge subgraph of \(G_s\) has **no directed cycle**. Let \(R\ge0\) be the maximum number of edges in a path consisting entirely of silent edges, taking \(R=0\) if there are none. The graph is finite, so \(R\) is finite. In particular, no admissible periodic source can emit the empty output.

## 3. The local-output lemma (including short periods)

**Lemma 1 (uniform local additivity).** Under the preceding assumptions, for every \(k\ge1\), set
\[
 d=(k-1)(R+1),\qquad L=s+d.
\]
There is an explicitly computable integer nonnegative matrix \(F_k\), with columns indexed by allowed \(L\)-blocks and rows by \(B^k\), for which
\[
\boxed{\ C_k(T(X))=F_k N_L(X)\quad\text{for every }X\in\mathcal X.\ }
\]
Thus \(H_{T,\mathcal X}(k)\le L\). For \(k=1\) this assertion and \(H_{T,\mathcal X}(1)\le s\) hold **even when silent cycles exist**.

**Construction.** For an allowed \(L\)-block \(w\), form
\[
 u_j=\phi(w_jw_{j+1}\cdots w_{j+2r})\quad(0\le j\le d),\qquad U=u_0u_1\cdots u_d.
\]
For \(b\in B^k\), set \(F_k(b,w)\) equal to the number of offsets \(0\le t<|u_0|\) for which the length-\(k\) substring of \(U\) beginning at \(t\) equals \(b\). If \(u_0\) is empty this contribution is zero.

**Proof.** Consider any starting output symbol emitted at source position \(i\). Its remainder inside \(u_i\) needs at most \(k-1\) further output symbols to form a periodic \(k\)-block. Between any two positive-length emission edges there are at most \(R\) silent edges: a longer run would be a longer silent path in \(G_s\). Therefore the next \(k-1\) required output symbols are available by position \(i+d\), regardless of emission-word lengths. For \(k=1\) no look-ahead is needed and no silence assumption enters. Each output starting position belongs to exactly one emitted \(u_i\). Summing its corresponding \(F_k(b,w)\) contribution over the \(n\) source positions counts each periodic output \(k\)-block exactly once. This argument works even when \(n<L\) and when \(|T(X)|<k\), because both source and output streams are periodically extended. In the no-silent-cycle case \(T(X)\) cannot be empty. Thus the formula holds. Finally \(N_L(X)=C_L(X)\), so equal \(C_L\) gives equal output counts. \(\square\)

**Remarks.** (a) Output blocks may cross many erased source positions but the cap makes their source look-ahead finite. (b) The bound \(L\) need not be minimal. (c) The theorem does **not** say that a silent cycle forces \(H(k)=\infty\); it says only that this local-output construction no longer has the displayed uniform look-ahead bound for \(k>1\).

## 4. Cyclic realizability versus ordinary circulations

Write \(E=E(G_L)\). Define the vertex-edge incidence matrix \(D\in\mathbb Z^{V\times E}\) with column \(e:u\to v\) equal to \(\mathbf 1_v-\mathbf 1_u\). Let \(P_h\in\{0,1\}^{A^h\times E}\) put a 1 in row \(w_0\cdots w_{h-1}\) for each edge \(w\); thus for \(1\le h\le L\),
\[
D N_L(X)=0,\qquad P_hN_L(X)=C_h(X).
\]

**Lemma 2 (single-cycle Euler lifting).** A vector \(x\in\mathbb Z_{\ge0}^E\) is \(N_L(X)\) for a nonempty \(X\in\mathcal X\) **if and only if**

* \(x\ne0\) and \(Dx=0\), and
* the directed graph formed by edges \(e\) with \(x_e>0\), with their incident vertices, is strongly connected.

**Proof.** A cyclic source traverses a single closed walk, which is balanced and has strongly connected positive edge support. Conversely, if \(x\) has the stated properties, replace edge \(e\) by \(x_e\) copies. Every vertex is balanced and all nonisolated vertices lie in a single strongly connected directed component, so Euler's circuit construction traverses every copy exactly once. Consecutive \(L\)-block edges overlap in \(L-1\) symbols. Reading their final symbols around the Euler circuit recovers a cyclic word whose periodic length-\(L\) windows are exactly those edges (also when its length is less than \(L\)). Since all those blocks respect \(\mathcal W_m\), the source is admissible. \(\square\)

Crucially, \(Dx=0\) *alone* is insufficient when the positive support has disconnected components: \(x\) could be a sum of two disjoint cyclic-word histograms, but no individual cyclic source realizes that sum.

## 5. Exact rank theorem for irreducible presentations

**Theorem 3 (irreducible rank criterion with witnesses).** Suppose \(G_L\) is strongly connected. For any \(1\le h\le L\), the following are equivalent:

1. \(C_h(X)=C_h(Y)\) implies \(C_k(T(X))=C_k(T(Y))\) for all nonempty \(X,Y\in\mathcal X\).
2. Every row of \(F_k\) lies in the rational row span of the stacked matrix \(\begin{bmatrix}D\\P_h\end{bmatrix}\).
3. \(\operatorname{rank}_{\mathbb Q}\begin{bmatrix}D\\P_h\\F_k\end{bmatrix}=\operatorname{rank}_{\mathbb Q}\begin{bmatrix}D\\P_h\end{bmatrix}\).

If the rank test fails, two *explicitly constructible, individually admissible single cyclic words* with equal \(C_h\) and different output \(C_k\) witness failure. Consequently, in this scope, scanning \(h=1,\ldots,L\) determines the **exact minimum** \(H_{T,\mathcal X}(k)\) by finite rational linear algebra.

**Proof.** Equivalence of 2 and 3 is elementary row reduction. If 2 holds, write \(F_k=UD+VP_h\) over \(\mathbb Q\). For any source \(X\), \(F_k N_L(X)=VP_hN_L(X)=VC_h(X)\). Thus equality of \(C_h\) implies equality of output \(C_k\).

Conversely suppose 2 fails. Since all matrices are rational, there is an **integer** vector \(v\in\ker D\cap\ker P_h\) with \(F_kv\ne0\): first find a rational nullspace separator and clear denominators. Strong connectivity guarantees a positive integer circulation \(z\in\mathbb Z_{>0}^E\) with \(Dz=0\): for each edge choose a directed cycle containing it and sum the cycle incidence vectors. Choose an integer \(N>0\) large enough that \(x=Nz\) and \(y=Nz+v\) are both strictly positive on every edge. Then \(Dx=Dy=0\), \(P_hx=P_hy\), and \(F_kx\ne F_ky\). Both full supports are strongly connected; by Lemma 2 they lift to *one Euler circuit each*, giving admissible source words \(X,Y\) with the required discrepancy. This contradicts 1. \(\square\)

A convenient witness certificate records the integer \(v,z,N\) and both explicit Euler circuits. Positive scalar multiples of either source's histogram are also realized by repeating its Euler circuit; **this is why the theorem requires all cyclic lengths, not a fixed length or inventory**.

## 6. Exact support-cone theorem for reducible presentations

For an arbitrary finite directed graph \(G_L\), write \(D_S,P_{h,S},F_{k,S}\) for columns restricted to an edge subset \(S\). Call \(S\subseteq E\) an **Euler support** if it is nonempty and its incident-vertex graph is strongly connected. This property can be checked directly without a numerical solver.

**Theorem 4 (reducible closure is finite rational LP).** Let \(F\) be any integer edge-additive target statistic on \(G_L\), in particular \(F=F_k\) from Lemma 1. For \(1\le h\le L\), \(h\)-block sufficiency fails **if and only if** there exist Euler supports \(S,T\), a target coordinate \(b\), and a sign \(\sigma\in\{-1,+1\}\) for which the following finite system is feasible over \(\mathbb Q\) (equivalently over \(\mathbb R\)):
\[
\begin{aligned}
  &D_S x=0,\qquad D_T y=0,\\
  &P_{h,S}x=P_{h,T}y,\\
  &x_e\ge1\ (e\in S),\qquad y_e\ge1\ (e\in T),\\
  &\sigma\big((F_Sx)_b-(F_Ty)_b\big)\ge1.
\end{aligned} \tag{LP}_{S,T,b,\sigma}
\]
Here variables outside the named supports are fixed at zero. In particular, enumerating the finitely many support pairs, target coordinates and signs, and performing **exact rational linear-feasibility checks**, is a terminating decision method. Every feasible instance yields explicit cyclic counterexample witnesses by common-denominator clearing and Euler lifting. If all instances are infeasible, \(h\) is sufficient.

**Proof.** If \(h\) fails, take witnessing cyclic words \(X,Y\) and let \(x=N_L(X),y=N_L(Y)\). Their positive supports \(S,T\) are Euler supports by Lemma 2, their count vectors are integral, and they satisfy the first three lines. Some integer output coordinate differs, so one of the two signs makes the last line at least one. Thus the corresponding LP is feasible.

In the other direction, each LP is a system of rational linear equalities and weak inequalities. Every nonempty rational polyhedron has a rational point: e.g. eliminate variables by Fourier–Motzkin elimination, choosing rational values between rational bounds at each back-substitution, or use basic-feasible-point arguments. Choose such a rational point \((x,y)\), and multiply *both* vectors by a common positive integer clearing all denominators. The scaled values are strictly positive integers on \(S,T\), remain balanced, retain identical \(P_h\) histograms, and retain a strictly positive (indeed at least one) signed output discrepancy. Lemma 2 supplies separate Euler circuits, hence admissible cyclic witnesses. \(\square\)

**Why rational LP, not integer programming?** This equivalence uses unrestricted lengths and **homogeneity** of flow, source histogram and output histogram equalities. Fixed absolute lengths, exact inventories, upper count bounds or other nonhomogeneous requirements invalidate denominator clearing; those domains require integer feasibility (or a different proof). A fixed erased-run cap, by contrast, can be expressed as an ordinary finite-type language (Section 8), so this LP theorem still applies after rebuilding the allowed graph.

**Complexity and certificates.** This enumerative algorithm is finite but potentially exponential in the number of \(L\)-block edges, and rational LP itself may produce large coefficients. A feasible LP point plus the two Euler tours is a succinct positive certificate; exact infeasibility certificates can be obtained from rational linear-inequality duality for each enumerated LP. This note does **not** claim a practical efficient solver for all reducible domains.

## 7. Minimal adversarial examples

### 7.1 Reducible counterexample to global row-span necessity

Let \(A=\{0,1\}\) and choose the allowed length-five blocks to be **exactly** all periodic five-windows of
\[
  p_1=0001,\qquad p_2=0011,\qquad p_3=0111.
\]
The length-four vertices on these three orbits are pairwise disjoint, so \(G_5\) consists of three disconnected directed four-cycles. Every admissible cyclic word is a positive power of one of the \(p_i\), up to rotation. Take \(r=2\) and define \(\phi\) on allowed five-windows to emit \(b\) for windows of \(p_2\) and \(a\) for windows of \(p_1\) or \(p_3\); define it arbitrarily outside the allowed contexts. No edge is silent. For \(k=1\), \(L=5\).

The length-one source-count vectors of one period are
\[
  P_1z_1=(3,1),\quad P_1z_2=(2,2),\quad P_1z_3=(1,3).
\]
No two **positive** multiples of different vectors coincide, so equality of \(C_1\) forces the same orbit and the same number of repetitions. Consequently, **\(H_{T,\mathcal X}(1)=1\)**.

Yet \(v=z_1-2z_2+z_3\) satisfies \(Dv=0\) and \(P_1v=(3,1)-2(2,2)+(1,3)=0\), while the \(b\)-output count obeys \((F_1v)_b=0-2\cdot4+0=-8\). The global row-span test therefore **fails**, although the horizon is one. The false negative arose from subtracting histograms of *disconnected cyclic components*, not from any pair of realizable equal-source-count words.

### 7.2 Strict source-domain improvement of identity horizons

Let \(A=B=\{0,1\}\), \(\phi(a)=a\), and permit exactly cyclic words with no \(00\) pair. Euler balance gives \(C_2(01)=C_2(10)=C_1(0)\), \(C_2(11)=C_1(1)-C_1(0)\), \(C_2(00)=0\). Hence \(H_{\mathrm{id},\mathcal X}(2)=1\), **smaller** than the unrestricted identity's \(H_{\mathrm{id}}(2)=2\).

For \(k=3\), \(X=011101\) and \(Y=011011\) are both admissible, have equal \(C_2\), but different \(C_3\). Thus \(H_{\mathrm{id},\mathcal X}(3)=3\) (the trivial \(C_3\) upper bound attains the lower bound).

### 7.3 Fixed-length pitfall

On *all binary cyclic words of length exactly two*, even identity's second-order histogram is determined by \(C_1\) (\(00,01\sim10,11\) are the only possibilities up to rotation). Thus \(H(2)=1\) on that finite domain. It would be incorrect to use the unrestricted positive-cone/rank argument, which constructs witnesses of **variable** length and gives \(H_{\mathrm{id}}(2)=2\) on the full domain.

## 8. Erased-run caps as finite-type constraints

Suppose the domain is further restricted by the condition that no admissible **periodic** source has more than \(R_0\) consecutive source positions at which \(\phi\) emits \(\epsilon\). This constraint is finite type: a forbidden consecutive run of \(R_0+1\) silent positions is decided by a source block of length \(2r+R_0+1\) (the union of their radius-\(r\) neighborhoods). Take the conjunction with the original allowed-block constraints, using a common block presentation length at least \(\max(m,2r+R_0+1)\).

In the resulting graph no silent directed cycle is possible: repeating such a cycle would create an admissible periodic word with arbitrarily long silent runs. Hence Lemma 1 and Theorems 3–4 apply **without separately assuming** acyclicity in the unconstrained full source shift. This applies to a cap on emitted-empty **source positions**, not a cap on output-symbol runs or a requirement of fixed inventory. The value \(R\) computed from the new finite graph may be \(\le R_0\).

## 9. Algorithms, reproducibility, and limitations

Reference code is **std_tools/sft_closure.py**; regression cases are in **tests/test_sft_closure.py**. The implementation enumerates allowed higher blocks, determines the longest silent path or detects a silent cycle, constructs \(F_k\) from the local-output lemma, and runs exact fractions.Fraction Gaussian elimination. The function **exact_horizon_irreducible** is a **complete exact minimum-horizon solver only for its stated irreducible bounded-silence domain** (also allowing silent cycles at \(k=1\)). It deliberately rejects reducible graphs instead of applying a rank theorem outside its hypotheses. The finite rational LP criterion for reducible graphs is proved in this note; a full generic LP/certificate implementation remains future engineering work.

From the repository root, run:

~~~bash
python -m unittest discover -s tests -v
~~~

The new tests check the exact minima \(2,1,3\) in the unrestricted/forbidden-pair examples, a capped erasure case, a detected unsupported silent cycle, the reducible three-cycle false-rank case, and exhaustive direct-vs-\(F_k N_L\) identities for thousands of short cyclic inputs (including source periods shorter than \(L\)). None of these finite tests is substituted for a theorem proof. The reference implementation assumes source and output symbols are represented by one-character strings, uses exponential higher-block enumeration, and is not optimized for large \(m,r,k\).

**Open follow-ups.** (i) Implement support-pair rational LP certificates and Euler witnesses for reducible shifts; (ii) derive more efficient tests exploiting strongly connected component cones; (iii) extend to restrictions not given by finite forbidden blocks and to unbounded erasure without overclaiming; (iv) formally verify the Euler-lift and cone arguments.

## 10. Dependencies and relation to prior STD results

Reviewed **README.md**, **AGENTS.md**, **docs/RESEARCH_STATE.md**, **docs/TASK_BOARD.md**, **audits/archive/STD_Audit_2026-10-10.txt**, and **audits/archive/STD_Global_Closure_Audit_2026-10-09.md** before deriving this result. These establish the full-shift/local-rule context and warn about a distinct false reset-gap theorem. **Nothing here repairs or reinstates that reset-gap claim**, and no result is promoted to formally verified status. The familiar unrestricted rank criterion is retained only with its connectivity assumptions; the new support-cone formulation makes the required constrained-domain qualification explicit.
