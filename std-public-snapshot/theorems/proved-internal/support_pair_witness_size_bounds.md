# Explicit size bounds for support-pair certificates

**Date:** 2026-10-11  
**Status:** proved-internal draft; analytic proof complete, nonauthor review pending.  
**Task:** issue #58.  

## 1. Scope

This note takes the accepted unrestricted-positive-length support-pair theorem from PR #6 as an input. It does not re-prove that theorem.

Fix one support-pair LP instance \((S,T,b,\sigma)\). Let

\[
N=|S|+|T|
\]

be its total number of positive edge-multiplicity variables, collected into one vector
\(z=(x,y)\in\mathbb R^N\).

The normalized feasible system has the exact PR #6 form

\[
\begin{aligned}
D_Sx&=0,\\
D_Ty&=0,\\
P_{h,S}x-P_{h,T}y&=0,\\
z_i&\ge 1\qquad(1\le i\le N),\\
\sigma\big((F_Sx)_b-(F_Ty)_b\big)&\ge 1.
\end{aligned}
\]

Here \(F\) is integer-valued. Define

\[
B=\max\left(1,\max_{e\in S\cup T}|F_b(e)|\right).
\]

All balance and source-projection rows have coefficients in \(\{0,\pm1\}\); each positivity row is a signed unit row; and there is exactly one target-discrepancy row, whose coefficients have absolute value at most \(B\).

The unrestricted-length and homogeneous hypotheses are essential. This note does not extend the result to fixed absolute source length, fixed inventory, upper-count bounds, or other nonhomogeneous constraints.

## 2. Bounded basic feasible point

**Lemma 1 (bounded basic feasible point).**  
Assume the fixed support-pair system above is feasible. Then it has a feasible vertex \(z^*\) for which there exist \(N\) linearly independent active constraint rows forming an integer nonsingular matrix \(M\in\mathbb Z^{N\times N}\) and an integer right-hand side \(q\in\{0,\pm1\}^N\) such that

\[
Mz^*=q.
\]

Let

\[
\Delta_N(B)=N^{N/2}B.
\]

Then

\[
1\le |\det M|\le \Delta_N(B)
\]

and every Cramer numerator satisfies

\[
|\det M_i|\le \Delta_N(B),
\]

where \(M_i\) is obtained from \(M\) by replacing column \(i\) by \(q\).

Consequently every coordinate of \(z^*\) is rational with the common denominator
\(D=|\det M|\le\Delta_N(B)\), and after multiplying all coordinates by \(D\),

\[
Z_i:=Dz_i^*
\]

is a positive integer satisfying

\[
1\le Z_i\le \Delta_N(B).
\]

### Proof

Let \(P\subseteq\mathbb R^N\) be the feasible polyhedron.

Set

\[
m(z)=\sum_{i=1}^N z_i.
\]

Choose any feasible \(z^{(0)}\in P\). Because every feasible coordinate satisfies \(z_i\ge1\), the sublevel set

\[
K=P\cap\{z:m(z)\le m(z^{(0)})\}
\]

is closed and contained in the bounded box \([1,m(z^{(0)})]^N\). Hence \(K\) is compact and nonempty, so \(m\) attains its minimum \(m_*\) on \(P\).

The minimizing set

\[
Q=P\cap\{z:m(z)=m_*\}
\]

is a nonempty compact polyhedron, hence a polytope and therefore has a vertex \(z^*\).

Moreover \(Q\) is an exposed face of \(P\), so every vertex of \(Q\) is a vertex of \(P\). Indeed, if
\(z^*=\lambda u+(1-\lambda)v\) with \(u,v\in P\) and \(0<\lambda<1\), then
\(m(u),m(v)\ge m_*\), while their convex combination has mass \(m_*\). Thus
\(m(u)=m(v)=m_*\), so \(u,v\in Q\); vertexhood in \(Q\) forces \(u=v=z^*\).

Now collect all equality rows and all inequalities active at \(z^*\). Their normals span \(\mathbb R^N\). Otherwise there is a nonzero direction \(d\) annihilated by every equality row and active inequality row. Every inactive inequality has positive slack at \(z^*\), so for sufficiently small \(\varepsilon>0\), both \(z^*+\varepsilon d\) and \(z^*-\varepsilon d\) remain feasible. This contradicts vertexhood.

Hence one may select \(N\) linearly independent active rows and write them as

\[
Mz^*=q.
\]

All entries are integral. Equality rows have right-hand side \(0\); an active positivity inequality has right-hand side \(\pm1\) depending on orientation; and the active target row, if selected, has right-hand side \(\pm1\). Therefore every entry of \(q\) has absolute value at most \(1\).

Among all possible active rows, at most one—the target-discrepancy row—can contain coefficients with magnitude larger than \(1\). Thus its Euclidean norm is at most \(\sqrt N\,B\), while every other selected row has Euclidean norm at most \(\sqrt N\). Hadamard's inequality yields

\[
|\det M|
\le
(\sqrt N\,B)(\sqrt N)^{N-1}
=
N^{N/2}B
=
\Delta_N(B).
\]

If the target row is not selected, the sharper bound \(N^{N/2}\) holds, so the displayed uniform bound still follows because \(B\ge1\). Since \(M\) is an integer nonsingular matrix, \(|\det M|\ge1\).

For a fixed column \(i\), replace that column by \(q\), forming \(M_i\). For every non-target row, the replacement entry has magnitude at most \(1\), so its row norm remains at most \(\sqrt N\). For the target row, the unreplaced entries have magnitude at most \(B\) and the replacement entry has magnitude at most \(1\le B\), so its row norm remains at most \(\sqrt N\,B\). Hence Hadamard gives

\[
|\det M_i|\le N^{N/2}B=\Delta_N(B)
\]

for every \(i\).

By Cramer's rule,

\[
z_i^*=\frac{\det M_i}{\det M}.
\]

Put \(D=|\det M|\). Because \(z_i^*\ge1\), the signed numerator and denominator have the same sign, so

\[
Dz_i^*=|\det M_i|\in\mathbb Z_{>0}.
\]

Therefore

\[
1\le D\le\Delta_N(B),
\qquad
1\le Dz_i^*\le\Delta_N(B).
\]

This proves the lemma. \(\square\)

## 3. Explicit bounded Euler witnesses

**Theorem 2 (fixed-support witness-size bound).**  
If the fixed support-pair LP \((S,T,b,\sigma)\) is feasible, then there exist admissible cyclic source witnesses \(X,Y\) with

\[
C_h(X)=C_h(Y)
\]

and different target coordinate \(F_b\), such that

\[
|X|+|Y|
\le
N^{N/2+1}B.
\]

More precisely, each positive edge multiplicity in the two Euler histograms is at most
\(\Delta_N(B)=N^{N/2}B\), and

\[
|X|\le |S|\,\Delta_N(B),
\qquad
|Y|\le |T|\,\Delta_N(B).
\]

### Proof

Take the feasible vertex \(z^*=(x^*,y^*)\) from Lemma 1 and scale by the common positive integer

\[
D=|\det M|.
\]

Set

\[
\widehat x=Dx^*,
\qquad
\widehat y=Dy^*.
\]

Every coordinate is a positive integer and at most \(\Delta_N(B)\).

Because all balance and source-histogram constraints are homogeneous equalities,

\[
D_S\widehat x=0,
\qquad
D_T\widehat y=0,
\qquad
P_{h,S}\widehat x=P_{h,T}\widehat y.
\]

Because every coordinate is positive, the positive supports remain exactly \(S\) and \(T\). By definition these are Euler supports, so PR #6 Lemma 2 supplies one Euler circuit on each scaled multigraph and hence one admissible cyclic source word \(X\) and one admissible cyclic source word \(Y\) with

\[
N_L(X)=\widehat x,
\qquad
N_L(Y)=\widehat y.
\]

The number of traversed \(L\)-block edges in an Euler circuit equals the total edge multiplicity. Therefore

\[
|X|=\sum_{e\in S}\widehat x_e,
\qquad
|Y|=\sum_{e\in T}\widehat y_e.
\]

Since every scaled coordinate is at most \(\Delta_N(B)\),

\[
|X|\le |S|\Delta_N(B),
\qquad
|Y|\le |T|\Delta_N(B).
\]

Moreover, every \(L\)-edge contributes to exactly one \(h\)-prefix coordinate, so summing all coordinates of the equality

\[
P_{h,S}\widehat x=P_{h,T}\widehat y
\]

gives

\[
\sum_{e\in S}\widehat x_e
=
\sum_{e\in T}\widehat y_e.
\]

Hence the Euler witnesses have equal source length:

\[
|X|=|Y|.
\]

Combining equality of lengths with the total-mass bound gives the sharper individual estimate

\[
|X|=|Y|
\le
\frac{N}{2}\Delta_N(B)
=
\frac12 N^{N/2+1}B.
\]

In particular,

\[
|X|+|Y|
\le
N\Delta_N(B)
=
N^{N/2+1}B.
\]

Finally the target inequality survives scaling:

\[
\sigma\big((F_S\widehat x)_b-(F_T\widehat y)_b\big)
=
D\,\sigma\big((F_Sx^*)_b-(F_Ty^*)_b\big)
\ge D\ge1.
\]

Thus the two Euler words have equal source \(h\)-histograms and genuinely different target coordinate \(b\). \(\square\)

## 4. Graph-wide counterexample cutoff

Let the recurrent \(L\)-block graph after transient-edge trimming have \(E\ge1\) recurrent edge types. Let \(F\) be an integer edge-additive target with finitely many coordinates, and define

\[
B_{\max}
=
\max\left(1,\max_{b,e}|F_b(e)|\right),
\]

where \(e\) ranges over recurrent \(L\)-edges.

**Corollary 3 (uniform finite counterexample cutoff).**  
If \(h\)-block sufficiency fails in the unrestricted-positive-length PR #6 domain, then there exist admissible cyclic source witnesses \(X,Y\) with equal \(C_h\), different target statistic \(F\), and

\[
\boxed{
|X|+|Y|
\le
(2E)^{E+1}B_{\max}.
}
\]

The two witnesses can in fact be chosen with equal length and the sharper individual bound

\[
\boxed{
|X|=|Y|
\le
E(2E)^E B_{\max}.
}
\]

### Proof

By PR #6 Theorem 4, failure yields some ordered Euler-support pair \(S,T\), some target coordinate \(b\), and some sign \(\sigma\) for which the normalized support-pair LP is feasible.

Both supports lie in the recurrent \(L\)-edge set, so

\[
N=|S|+|T|\le2E.
\]

Theorem 2 gives

\[
|X|+|Y|\le N^{N/2+1}B
\]

with \(B\le B_{\max}\).

For real \(n\ge1\), set \(f(n)=n^{n/2+1}\). Then

\[
\frac{d}{dn}\log f(n)
=
\frac12\log n+\frac12+\frac1n
>0.
\]

Thus \(f\) is strictly increasing on \([1,\infty)\). Therefore

\[
N^{N/2+1}
\le
(2E)^{(2E)/2+1}
=
(2E)^{E+1}.
\]

Combining the inequalities proves the combined cutoff.

For the individual cutoff, Theorem 2 gives

\[
|X|=|Y|
\le
\frac12 N^{N/2+1}B.
\]

Using the same monotonicity and \(N\le2E\),

\[
|X|=|Y|
\le
\frac12(2E)^{E+1}B_{\max}
=
E(2E)^E B_{\max}.
\]

This proves the corollary. \(\square\)

These are witness-length bounds, not bounds on the histogram order \(h\) or on the minimum horizon itself.

## 5. Finite exhaustive completeness corollary

**Corollary 4 (finite brute-force completeness for a fixed additive statistic).**  
Under the hypotheses of Corollary 3, define

\[
C_{\mathrm{ind}}=E(2E)^E B_{\max}.
\]

For a fixed \(h\), \(h\)-block sufficiency holds globally if and only if no counterexample pair occurs among admissible nonempty cyclic source words whose individual lengths are at most \(C_{\mathrm{ind}}\).

### Proof

If a bounded counterexample is found, global sufficiency fails trivially.

Conversely, if global sufficiency fails, Corollary 3 supplies an equal-length counterexample pair with each individual source length at most \(C_{\mathrm{ind}}\). Hence exhaustive enumeration through length \(C_{\mathrm{ind}}\) must encounter a counterexample. \(\square\)

This gives a finite but generally astronomical alternative decision procedure. It is not claimed to be computationally practical.

## 6. Local-emission specialization

For PR #6 Lemma 1, let

\[
M_\phi
=
\max |\phi(a)|
\]

over allowed centered source contexts \(a\in A^{2r+1}\).

For the local output matrix \(F_k\), the entry \(F_k(b,w)\) counts offsets

\[
0\le t<|u_0|
\]

whose output \(k\)-block equals \(b\). Hence

\[
0\le F_k(b,w)\le |u_0|\le M_\phi.
\]

Therefore

\[
B_{\max}\le \max(1,M_\phi).
\]

If the recurrent \(L\)-block core has \(E\) edges and an \(h\le L\) sufficiency claim fails, then one may choose equal-length witnesses with

\[
|X|=|Y|
\le
E(2E)^E\max(1,M_\phi),
\]

and therefore also

\[
|X|+|Y|
\le
(2E)^{E+1}\max(1,M_\phi).
\]

For \(k>1\), this specialization uses the accepted bounded-silence/no-recurrent-silent-cycle hypothesis needed to construct \(F_k\). For \(k=1\), PR #6 Lemma 1 does not require that silence hypothesis.

If \(M_\phi=0\), every allowed local emission is empty. The output statistic is constant, so there is no failure to witness; the displayed bound with \(\max(1,M_\phi)\) is harmless but vacuous.

## 7. Exact-horizon finite-sample completeness

In the local-emission setting, let

\[
L=\max(m,2r+1)+(k-1)(R+1)
\]

for \(k>1\), using the accepted recurrent silent-run bound \(R\). For \(k=1\), take

\[
L=\max(m,2r+1).
\]

Let \(E\) be the number of recurrent \(L\)-edge types and let

\[
C_{\mathrm{ind}}
=
E(2E)^E\max(1,M_\phi).
\]

PR #6 Lemma 1 gives

\[
H_{T,\mathcal X}(k)\le L.
\]

The same \(L\)-graph and the same \(F_k\) serve every candidate source-histogram order \(h=1,\ldots,L\). Therefore one finite exhaustive data set suffices:

1. enumerate every admissible nonempty cyclic source word with length at most \(C_{\mathrm{ind}}\);
2. compute \(C_h(X)\) for every \(h=1,\ldots,L\);
3. compute \(C_k(T(X))\);
4. for each \(h\), test whether some equal-\(C_h\) pair has unequal output \(C_k\).

If any \(h\le L\) failed globally, Corollary 3 would provide an equal-length witnessing pair whose individual lengths are at most \(C_{\mathrm{ind}}\). Hence the least \(h\) with no bounded collision is the exact global horizon.

This is a finite-sample completeness theorem, not a practical complexity result.

Since

\[
E\le |A|^L,
\]

one obtains the parameter-only coarsening

\[
C_{\mathrm{ind}}
\le
|A|^L\bigl(2|A|^L\bigr)^{|A|^L}\max(1,M_\phi).
\]

The allowed finite-type language can only reduce the actual recurrent-edge count \(E\).

### Presentation-only coarsening

Put

\[
s=\max(m,2r+1).
\]

For \(k>1\), acyclic silence in the recurrent \(G_s\) core means a silent path cannot repeat a vertex. The canonical word-labeled \(G_s\) has at most \(|A|^{s-1}\) vertices, so

\[
R\le |A|^{s-1}-1.
\]

Therefore

\[
L
=
s+(k-1)(R+1)
\le
s+(k-1)|A|^{s-1}.
\]

For \(k=1\), the same upper bound reduces to \(L=s\).

Define

\[
Q
=
|A|^{\,s+(k-1)|A|^{s-1}}.
\]

Since the canonical word higher-block presentation has at most \(|A|^L\) length-\(L\) edges,

\[
E\le |A|^L\le Q.
\]

The function \(g(x)=x(2x)^x\) is strictly increasing for \(x\ge1\), because

\[
\frac{d}{dx}\log g(x)
=
\frac1x+\log(2x)+1
>0.
\]

Hence every failed \(h\le L\) has equal-length witnesses obeying the presentation-only bound

\[
\boxed{
|X|=|Y|
\le
Q(2Q)^Q\max(1,M_\phi).
}
\]

This bound uses the canonical word-labeled presentation. It is intentionally enormous and is not a practical complexity claim.

## 8. Numeric bit-length consequences

For one fixed support-pair LP, the common denominator and every scaled integer multiplicity are at most

\[
\Delta_N(B)=N^{N/2}B.
\]

Thus one numerator, denominator, or scaled multiplicity needs at most

\[
O(N\log N+\log B)
\]

bits. The total explicit encoding of all \(N\) scaled multiplicities is therefore

\[
O(N^2\log N+N\log B)
\]

bits, ignoring graph-label overhead.

The explicit Euler words themselves may be enormously longer: their combined length is bounded by

\[
N^{N/2+1}B.
\]

No polynomial-time or practical-smallness claim follows from these estimates. The support-pair enumeration is separately exponential in the graph size.

## 9. Robustness and exclusions

- **Self-loops:** zero incidence contributions merely create dependent/zero balance rows; active-basis selection discards dependencies.
- **Repeated/dependent constraints:** harmless for the same reason.
- **Lower-dimensional feasible sets:** the minimizing-face argument and active-normal rank proof do not assume full dimensionality.
- **One-edge supports:** covered by the same determinant proof.
- **Inactive target inequality:** gives an active basis with no large row, so the uniform bound remains valid.
- **Negative integer target coefficients:** only their absolute magnitude enters \(B\).
- **Several simultaneous large target rows:** not covered by the linear-in-\(B\) determinant estimate; the row-structure bound must be re-derived.
- **Rational target statistics:** not covered as stated; clear denominators first and account for them in the integer coefficient bound.
- **Transient edges:** excluded from \(E\), because no Euler support can contain an edge that lies on no directed closed walk.
- **Fixed length, fixed inventory, upper-count constraints, or other nonhomogeneous domains:** excluded. The denominator-clearing argument is specific to the unrestricted homogeneous PR #6 setting.
- **Rooted source/output observables:** not implied by this cyclic histogram theorem.

## 10. PR #25 sanity example

For the reviewed PR #25 support pair, \(N=6\) and the relevant target coefficients have \(B=1\). The fixed-support theorem gives

\[
\Delta_6(1)=6^3=216
\]

and the coarse combined source-length bound

\[
6\cdot216=1296.
\]

The actual preserved witness is tiny by comparison. This is only a sanity illustration and is not evidence for the proof.

## 11. Evidence classification

The determinant, scaling, Euler-length, graph-wide cutoff, and finite-sample completeness arguments above are analytic proofs conditional on the accepted PR #6 support-pair theorem.

No proof assistant or external peer review has been applied. C's issue #44 / PR #57 certificate implementation is independent execution evidence and is not used to prove these universal bounds.
