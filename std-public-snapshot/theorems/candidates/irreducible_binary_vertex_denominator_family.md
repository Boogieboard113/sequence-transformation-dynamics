# Irreducible binary finite-type family with unbounded support-pair vertex denominators

**Researcher E; issue #83; 2026-10-11.** **Status:** candidate analytic theorem, submitted for nonauthor review by Researcher A. No accepted-state promotion or formal verification claimed.

## 1. Exact scope and source conventions

For each integer \(p\ge2\), put \(m=p+1\). Let \(A=\{0,1\}\) and define \(\mathcal W_m\) to be exactly the periodic length-\(m\) factors of

\[
U_p=0^{p+1}1^{p+1}.
\]

The source domain consists of **all nonempty finite cyclic binary words of arbitrary positive lengths** whose periodic length-\(m\) blocks belong to \(\mathcal W_m\). Even when a source length is shorter than \(m\), its windows are evaluated by periodic wrapping. All source/output histograms below are raw periodic counts, not rooted or necklace counts.

Use the complete, nonerasing, radius-zero identity transformation \(T(X)=X\). Compare the source statistic \(C_1\) with the **single integer edge-additive output coordinate**

\[
F(X)=C_m(T(X))(0^m)=C_m(X)(0^m).
\]

This is a direct additive statistic on \(G_m\), with coefficient 1 on the edge \(0^m\) and 0 on all other edges. In particular this proof does **not** require using PR #6's generally nonminimal local-output lookahead \(L=m+(m-1)\) for the identity transformation: the exact additive representation is already available at \(L=m\). PR #6's support-pair/Euler conventions apply to any integer edge-additive statistic on the chosen block graph.

Take the **ordered full-support pair** \(S=T=E(G_m)\), treating its \(x\) and \(y\) variables as separate columns even where they refer to the same edges. Consider exactly the normalized LP

\[
D x=D y=0,\qquad P_1x=P_1y,\qquad x_e,y_e\ge1,
\qquad F(x)-F(y)\ge1.
\tag{LP}_p
\]

No fixed length, inventory, upper count, or extra nonhomogeneous restriction is imposed.

## 2. Strongly connected graph, with explicit edge decomposition

**Lemma 1.** The graph \(G_m\) has exactly \(E_p=2p+2\) edge types. Its edges are the two self-loops

\[
z=0^{p+1},\qquad o=1^{p+1},
\]

together with the following \(2p\) mixed edges:

\[
0^j1^{p+1-j}\quad\text{and}\quad 1^j0^{p+1-j},
\qquad 1\le j\le p.
\]

The mixed edges form **one directed elementary cycle of length \(2p\)** through all \(2p\) distinct length-\(p\) vertices. The pure \(0\)- and \(1\)-edges are self-loops at \(0^p\) and \(1^p\). Thus the full higher-block graph is strongly connected (indeed has period one), and every edge is recurrent.

**Proof.** Moving a length-\(m\) periodic window around \(U_p\) gives the two pure factors and precisely the \(p\) transitions in each direction displayed above, with no repetitions. The mixed edges occur in this cyclic order:

\[
0^p1,\ 0^{p-1}1^2,\ \ldots,\ 01^p,\
1^p0,\ 1^{p-1}0^2,\ \ldots,\ 10^p.
\]

Their successive length-\(p\) suffix/prefix vertices agree. The initial and final vertices agree after completing the list, and all \(2p\) intermediate vertices are distinct (including \(0^p,1^p\)). Hence they form one simple directed cycle. Adding the two pure self-loops preserves strong connectivity and adds directed loops. All displayed edges occur on closed walks, so trimming removes none. \(\square\)

In particular, this is **not** issue #79's reducible two-orbit presentation: there is exactly one recurrent SCC and both \(S\) and \(T\) contain all its edges. It is also distinct from the multi-symbol exponential-minor family of PR #67/#75, whose specified full-support vertices are integral.

## 3. Exact normalized LP and a unique vertex with denominator \(p\)

**Theorem 2 (unbounded necessary vertex denominators in an irreducible binary family).** For every \(p\ge2\), the full-support LP \((LP)_p\) is nonempty and has **exactly one vertex**. This vertex has minimal common coordinate denominator **exactly \(p\)**. Since \(E_p=2p+2\), the necessary vertex denominator grows linearly with the recurrent edge count:

\[
\boxed{D_{\mathrm{vertex}}=p=\frac{E_p-2}{2}.}
\]

**Proof.** On the strongly connected graph of Lemma 1, any balanced circulation assigns the same multiplicity \(a\) to **each** of the \(2p\) mixed-cycle edges: at every vertex other than the two loop vertices, conservation forces equality of successive mixed-edge counts; at a loop vertex the self-loop contributes equally to its incoming and outgoing balance, so conservation still forces equality. The two self-loop multiplicities, \(b\) on \(z=0^m\) and \(c\) on \(o=1^m\), are independent. Conversely every such triple \((a,b,c)\) gives a balanced circulation.

The first-symbol source histogram and the chosen target are exactly

\[
C_1=(pa+b,\ pa+c),\qquad F=b.
\tag{1}
\]

Indeed, \(p\) mixed edges start with 0 and \(p\) with 1, while the corresponding pure self-loop contributes once to its symbol.

Write the two positive circulations as \((a_x,b_x,c_x)\) and \((a_y,b_y,c_y)\). Source-\(C_1\) equality and the target row give

\[
p a_x+b_x=p a_y+b_y,\quad
p a_x+c_x=p a_y+c_y,\quad b_x-b_y\ge1.
\tag{2}
\]

Let \(\tau=a_y-a_x\). Then (2) is equivalent to

\[
b_x=b_y+p\tau,\qquad c_x=c_y+p\tau,\qquad p\tau\ge1.
\tag{3}
\]

By (3), \(\tau\ge1/p>0\). All edge lower bounds \(a_x,a_y,b_x,b_y,c_x,c_y\ge1\) reduce **exactly** to

\[
a_x\ge1,\qquad b_y\ge1,\qquad c_y\ge1,\qquad \tau\ge\frac1p.
\tag{4}
\]

For example, \(a_y=a_x+\tau\ge1\), and both \(b_x=b_y+p\tau\) and \(c_x=c_y+p\tau\) are automatically at least 1 when (4) holds. Conversely (4) with (3) reconstructs every feasible full-support pair. The mapping from the four coordinates \((a_x,b_y,c_y,\tau)\) to **all the original \(2E_p\) edge variables** is an invertible affine parameterization of the equality subspace. Therefore the normalized feasible polyhedron is affinely isomorphic to the four-dimensional translated positive orthant (4), and it has **exactly one extreme point**.

At that extreme point,

\[
a_x=1,\qquad b_y=c_y=1,\qquad \tau=1/p.
\]

Its full edge multiplicities are

\[
\begin{array}{c|ccc}
 & \text{each mixed-cycle edge} & 0^{p+1} & 1^{p+1}\\
\hline
x & 1 & 2 & 2\\
y & 1+1/p & 1 & 1
\end{array}
\tag{5}
\]

and its common individual rational mass is \(2p+4\). All coordinates of (5) are positive. The chosen target gap is \(2-1=1\), so the vertex is feasible. Since \(\gcd(p,p+1)=1\), the least common clearing denominator of (5) is **exactly \(p\)**; no smaller positive integer clears its mixed-edge \(y\)-coordinates.

Every nonsingular integer active constraint basis producing this vertex must consequently have determinant divisible by \(p\), by Cramer's rule; this observation does **not** assert that every feasible point has a fractional denominator. The full original LP has a unique fractional vertex but also infinitely many feasible integer points.

All steps are analytic for arbitrary \(p\), independently of bounded computer enumeration. \(\square\)

**Scope warning.** The alphabet is fixed binary, the graph is strongly connected and recurrent, and the target coefficients are 0 or 1, but the chosen output order \(k=m=p+1\) grows with \(p\). This theorem neither fixes \(k\) nor proves exponential vertex denominators.

## 4. Integer Euler witnesses and a separate exact full-support minimum

**Corollary 3 (linear shortest integer witnesses for this same fixed support pair).** In the above full-support LP, the shortest possible individual source length of an **integer** feasible Euler-witness pair is exactly

\[
\boxed{|X|=|Y|=4p+2.}
\]

**Proof.** If all six circulation parameters are integers, \(\tau=a_y-a_x\) is an integer. Since \(\tau\ge1/p>0\), necessarily \(\tau\ge1\). Then \(a_y=a_x+\tau\ge2\); and positivity requires \(b_y,c_y\ge1\). Thus the individual \(y\)-source length, which equals its total edge multiplicity, satisfies

\[
|Y|=2p a_y+b_y+c_y\ge 4p+2.
\]

Equal \(C_1\) implies \(|X|=|Y|\). Equality is attained by the explicit cyclic words

\[
X_p=0^{\,2p+1}1^{\,2p+1},\qquad
Y_p=0^{\,p+1}1^{\,p+1}0^p1^p.
\tag{6}
\]

Both have \(2p+1\) zeros and \(2p+1\) ones. Every constant run has length at least \(p\), so every periodic length-\(p+1\) window either is pure or crosses exactly one run boundary, hence belongs to the allowed list of Lemma 1. Each mixed edge occurs once in \(X_p\) and twice in \(Y_p\); both have strictly positive multiplicities on the two pure self-loops. In fact, each pure loop has multiplicity \(p+1\) for \(X_p\) and 1 for \(Y_p\). Thus both supports are the **entire strongly connected graph**, their raw \(C_1\) histograms are equal, and

\[
F(X_p)=p+1,\qquad F(Y_p)=1,\qquad F(X_p)-F(Y_p)=p\ge1.
\]

Both words have length \(4p+2\), proving optimality for this *specified full-support pair*. \(\square\)

Scaling the unique rational vertex (5) by its denominator \(p\) instead gives integer circulations of individual length \(p(2p+4)\). Their Euler words are valid, but **not shortest**. The quadratic scaled-vertex mass is not a lower bound on the shortest integer witness. No claim is made about the exact unrestricted minimum when **proper supports** S,T are also permitted.

## 5. Bounded reproducibility and evidence classification

A separate standard-library test file, \`tests/test_irreducible_ring_loops_denominator.py\`, performs exact checks for \(p=2,\ldots,10\):

1. Independently reconstructs allowed edges from periodic length-\(m\) windows and checks the complete graph is strongly connected with \(2p+2\) distinct edges.
2. Forms **original** per-side incidence and signed \(P_1\) rows in \(2E_p\) variables; checks equality rank \(2E_p-4\), exact vertex feasibility, least denominator \(p\), rank \(2E_p-1\) with tight positivity rows, and full rank \(2E_p\) after the selected target row is added.
3. Checks the explicit words (6) by **literal periodic windows**, including full supports, equal \(C_1\), and target gap.
4. Independently exhausts every rooted binary word for \(p=2,3\) through \(4p+2\), including source periods shorter than \(m\), and verifies the first full-support collision is at that analytically predicted length.

Reproduce from the repository root:

~~~sh
python -m unittest discover -s tests -p 'test_irreducible_ring_loops_denominator.py' -v
python -O -m unittest discover -s tests -p 'test_irreducible_ring_loops_denominator.py' -v
~~~

Author local environment: CPython 3.13.5; both normal and optimized runs passed all three tests. This is **bounded supporting evidence only**. The universal vertex and witness conclusions rest on Lemma 1, Theorem 2, and Corollary 3's written analytic proofs, not test-pass claims. No outside review or proof assistant was used.

## 6. Provenance and review handoff

- Task contract: issue #83; owner researcher E; reviewer A after PR #81 handoff.
- Exact original issue input: main \`private-history-omitted\`.
- Current main was reconciled onto E's untouched dedicated branch by a **non-force fast-forward** before its first research commit; no other worker's branch was modified.
- Imported mathematical premises: PR #6 exact support-pair conventions/theorem, theorem blob \`private-history-omitted\`; PR #59 and PR #67 upper bounds only for comparison; PR #75 integral family only for contrast. PR #80's reducible two-orbit construction and PR #81's single finite example are **not** proof premises.
- This packet does not alter the accepted research-state ledger or merge itself.

**Request for independent nonauthor mathematical review (A):** Check (i) the precise de Bruijn graph is one ring plus two self-loops at *all* p, (ii) equality (1) and the affine-orthant reduction (2)--(4) recover the complete **original** full-support LP, (iii) uniqueness/extremality and minimal denominator \(p\), (iv) the literal words and exact shortest full-support *integer* length, (v) avoidance of shortest-over-all-supports or fixed-\(k\) claims, and (vi) the PR #6 additive statistic/horizon-scope dependency. Record the exact reviewed head and theorem blob. Do not count these bounded tests or the author's work as independent verification.
