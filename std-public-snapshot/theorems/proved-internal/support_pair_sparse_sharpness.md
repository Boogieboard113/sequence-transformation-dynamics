# Sparse-matrix sharpening and non-unimodularity of STD support-pair LPs

**Researcher E candidate mathematical packet, 2026-10-11.** Issue #64; branch research/e-support-pair-sharpness. **Status:** analytic derivation offered for independent nonauthor review; not an accepted-state claim.

**Pinned source:** task-start main private-history-omitted; merged PR #59 reviewed head private-history-omitted; exact note blob private-history-omitted. Theorem 4 and Euler lifting of PR #6 are imported, not audited or reproved here; the separate mathematical audit is B's issue #31. At manuscript preparation, latest main had moved to private-history-omitted by documentation-only changes.

## 1. Constraint matrix and orientation

Fix a **feasible** normalized ordered Euler-support-pair instance (S,T,b,sigma) of PR #6, with N=|S|+|T| >= 2, variables z=(x,y), and integer additive target coefficient bound

\[
B=\max(1,\max_{e\in S\cup T}|F_b(e)|).
\]

Its equalities are D_S x=0, D_T y=0 and P_{h,S}x-P_{h,T}y=0. The inequalities are z_j>=1 for each variable, and the **single** target row sigma((F_S x)_b-(F_T y)_b)>=1. Equality right-hand sides are zero. Orient active positivity rows as z_j=1 and the active target as fz=1.

In each column of the **structural** block (balance + source-prefix equality, with positivity and target rows omitted), there are at most three nonzeros, all in {+1,-1}: at most two incidences at the head/tail and exactly one signed h-prefix coordinate. Incidence of a self-loop is zero. A positivity row is a unit row, with its single 1 in its own variable's column. There is at most one target row with entries in [-B,B].

These facts hold with overlapping or identical S and T: x and y are separate columns, and each has its own incidence equations. They also hold with repeated/dependent rows and with noncanonical but explicitly defined labeled-edge graphs, provided every edge is assigned precisely one source-prefix row.

## 2. Improved numerator, denominator and source-length bound

**Theorem E1 (sparse support-pair bound; conditional on PR #6).** Every feasible fixed support-pair instance above has a rational feasible vertex and a common-denominator clearing factor D such that all scaled multiplicities Z_j=D z_j are positive integers satisfying

\[
1\le D,\ Z_j\le
\widetilde\Delta_N(B):=
2NB\,3^{(N-2)/2}.
\]

The original PR #59 bound is also valid, so one can simultaneously use

\[
\Delta_N^{\rm joint}(B)
=B\min\left\{N^{N/2},\ 2N\,3^{(N-2)/2}\right\}.
\]

In particular the resulting two Euler sources satisfy

\[
|X|+|Y|\le N\Delta_N^{\rm joint}(B),
\qquad
|X|=|Y|\le\tfrac12N\Delta_N^{\rm joint}(B).
\]

For a fixed support pair the coordinate bit cost improves asymptotically from O(N log N+log B) to **O(N+log N+log B)**. The estimate is a worst-case *upper* bound; no matching lower bound on feasible vertex denominators is asserted.

**Proof.** Existence of a vertex, including lower-dimensional/unbounded feasible polyhedra, follows from the compact mass-minimizing-face argument of merged PR #59. Select any nonsingular N-row active integer basis Mz=q at that vertex. Let p of its selected rows be positivity equations on p distinct coordinates, and put m=N-p.

After permuting rows and columns and orienting positivity equations positively, the selected system has block form

\[
M=\begin{pmatrix}I_p&0\\C&A\end{pmatrix},
\qquad
q=\begin{pmatrix}{\bf1}_p\\q_R\end{pmatrix},
\]

where A is m-by-m, det M=det A up to sign, and every entry of q_R is zero except possibly one entry 1 belonging to the selected target-discrepancy row. The p fixed coordinates equal 1. The remaining m coordinates solve

\[
Az_U=q_R-C{\bf1}_p.
\]

If m=0, M is a signed permutation matrix, D=1 and every scaled coordinate is 1; the claimed bound is immediate. Assume m>=1.

**Structural minor estimate.** Any m-by-m submatrix H assembled from the m selected *non-positivity* rows and any m distinct edge-variable columns has

\[
|\det H|\le mB\,3^{(m-1)/2}.
\tag{*}
\]

Indeed, after deleting the at-most-one target row, each remaining column has at most three entries of magnitude 1, hence Euclidean norm <=sqrt(3). If the target row is present, expand its determinant along that row: at most m terms, each with coefficient <=B and an (m-1)-column Hadamard cofactor <=3^((m-1)/2). If there is no target row, column Hadamard gives 3^(m/2), which is <=mB 3^((m-1)/2) for m>=2. The residual m=1 case is a single 0,+1,-1 entry and is <=B. This proves (*).

Apply (*) to A. We obtain

\[
1\le D:=|\det A|\le mB\,3^{(m-1)/2}.
\]

For one *free* coordinate j, the Cramer numerator is the determinant obtained by substituting q_R-C 1_p for column j in A. By determinant multilinearity, this is a sum of (at most) p terms each obtained by substituting one column C_\ell of C, and one term from q_R. Each C_\ell term is an m-by-m minor of the kind in (*). If q_R is nonzero, it is a unit vector at the target row: expansion along that substituted column leaves a target-free (m-1)-square minor bounded by 3^((m-1)/2); when no target is selected q_R=0. Thus

\[
|\det A_j(q_R-C1_p)|
\le (1+pmB)\,3^{(m-1)/2}
\le (p+1)mB\,3^{(m-1)/2},
\]

using mB>=1. This is exactly |D z_j|, a *positive integer* since z_j>=1. For any of the p fixed coordinates, |D z_j|=D obeys the same upper bound. This controls **numerators as well as the denominator**, without erroneously treating the dense substituted right-hand-side column as 3-sparse.

Finally m<=N and, for every integer p>=0,

\[
(p+1)3^{(1-p)/2}\le 2.
\]

The maximum occurs at p=1 (at p=0 the value is sqrt(3); from p>=1 successive ratios are at most 3/(2 sqrt(3))<1). Therefore

\[
(p+1)mB\,3^{(m-1)/2}
\le 2NB\,3^{(N-2)/2}.
\]

This proves the claimed denominator and all scaled-multiplicity bounds. Using the **same** factor D on x and y preserves the homogeneous equalities, positive support and target discrepancy. PR #6's Euler-support lifting supplies two actual cyclic witnesses whose edge counts are Z; their combined length is the total Z mass. Summing the P_h rows proves their lengths are equal. Combining this estimate with the previously proved PR #59 Hadamard bound gives the displayed minimum. QED.

**Example of a genuine sharpening.** For N=6, B=1, PR #59 used Delta_6=216; here the sparse estimate gives 2*6*3^2=108. For N=8, B=1, it gives 432 versus 4096. The exact values need not be integers on the right-hand side; D and Z_j are integers below those real bounds.

## 3. Sharper graph and local-emission consequences

For E>=1 recurrent L-edge types and B_max=max(1,max_(b,e)|F_b(e)|), the same PR #6 support-pair reduction has N<=2E. Since n^2 3^((n-2)/2) is increasing for real n>=2, the uniform **equal individual source-length** cutoff is

\[
|X|=|Y|\le
B_{\max}\min\{E(2E)^E,\ 4E^2 3^{E-1}\}.
\tag{**}
\]

The combined length is at most twice this cutoff. The second term strictly improves the first for all E>=3; for E=1,2 the old term is retained. This also sharpens the finite-exhaustive-completeness cutoff of PR #59, but **not** the histogram order h.

For its local output F_k, retain exactly PR #59's scoped estimate B_max<=max(1,M_phi), including its bounded-silence condition for k>1 (not required for k=1). If using the canonical word-labeled presentation and its previously established E<=Q bound, replace E by Q in either increasing term in (**), giving the analogous presentation-only cutoff. No claim of efficient enumeration is implied.

## 4. Obstruction: the structural block is not totally unimodular

Even **without** the target row and positivity rows, the coupled incidence/prefix block can contain a 2-by-2 determinant equal to 2. For binary source alphabet, L=3 and h=1, take x-edge columns 001 and 010, the balance row D_x at vertex 01, and the signed source-prefix row for 0. Their displayed minor is

\[
\begin{pmatrix}
+1&-1\\
+1&+1
\end{pmatrix},
\qquad\det=2.
\]

This is a minimal-size obstruction to total unimodularity, not a proof that every feasible LP requires fractional vertices.

**Exponential-minor family.** For every integer t>=3 take alphabet A={a_0,...,a_(t-1)}, indices modulo t, L=3, h=1, and allow exactly these 4t distinct recurrent length-3 edge types:

\[
s_i=a_i a_i a_{i+1},\quad
t_i=a_i a_{i+1}a_i,\quad
u_i=a_{i+1}a_i a_{i+1},\quad
v_i=a_i a_{i+1}a_{i+1}.
\]

The graph vertices v0_i=a_i a_i, w_i=a_i a_{i+1}, z_i=a_{i+1}a_i are distinct for t>=3. Edges follow v0_i -> w_i -> v0_(i+1) using s_i,v_i, and w_i -> z_i -> w_i using t_i,u_i. Thus the graph is strongly connected and every displayed edge recurrent.

Take the **feasible** ordered support pair S=T equal to this 4t-edge set, with the x and y variables kept distinct. Select from the structural block the t x-balance rows at w_i, the t source-prefix-equality rows for a_i, and the 2t x-columns corresponding to (s_i,t_i). Other selected column entries vanish across distinct i; the 2t-square minor is block diagonal with t copies of the displayed determinant-2 matrix. Therefore

\[
|\det(\text{selected structural minor})|=2^t=2^{N/8},
\qquad N=|S|+|T|=8t.
\]

**Actual normalized feasibility, not just a formal matrix:** Define positive balanced x,y by assigning each s_i and v_i multiplicities (x,y)=(2,1), and each t_i and u_i multiplicities (x,y)=(1,2). Every balance is zero. The source C_1 prefix count of each a_i is 6 for both x and y, and both have length 6t. Choose the integer target coordinate F_b(e)=1 exactly on s_0 and 0 on other edges; then F_b x-F_b y=1. Hence the normalized support-pair LP is feasible, with S=T strongly connected. This also has a genuine radius-one, non-erasing, local-emission realization: set m=3, r=1, k=1, output alphabet {0,1}, emit symbol 1 only on context s_0 and symbol 0 on every other length-3 context. The cyclic output 1-count is precisely the s_0 edge count.

Consequently the family rules out total unimodularity and any **universal polynomial upper bound on all minors of the structural constraint matrices** when the alphabet/presentation size varies. It does **not** by itself rule out a separate polynomial existence bound for *feasible vertex denominators* or *minimum witness sizes*: the exponentially large minors need not be extendable to active full-rank bases at feasible vertices. Those are distinct open questions. In particular no determinant lower bound for the Cramer bases selected in Section 2 is claimed.

## 5. Evidence, reproducibility and exclusions

The upper bound and the family-minor identity are **analytic proofs**. The separate standard-library regression in tests/test_support_pair_sparse_sharpness.py exactly checks t=3,4,5,6, the minor determinants, incidence balance, equal source projections, feasibility, and strong connectivity; these finite tests do not prove the general claims. Run from repository root:

~~~shell
python -m unittest discover -s tests -p 'test_support_pair_sparse_sharpness.py' -v
python -m unittest discover -s tests -v
~~~

The only imported mathematical premises for the **witness translation** are the accepted unrestricted-length support-pair iff and Euler lifting from PR #6 (issue #31 independently audits them). The determinant estimates themselves are elementary and independent of that iff. This work does not apply unmodified to fixed source length, fixed inventories, upper bounds, nonhomogeneous constraints, rooted output equivalence, rational F before denominator clearing, or systems with multiple independently selected large target rows. No proof assistant, external review, or practical polynomial-time guarantee is claimed.

**Requested reviewer:** Researcher B after issue #31, with the precise tests: scrutinize the 3-sparsity after positivity elimination, the q_R-C1 numerator argument, the p/m uniform inequality, and the family 2^t minor while distinguishing minors from *active feasible* Cramer bases.
