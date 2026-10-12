# Coprime-orbit quadratic witnesses and growing feasible vertex denominators

**Status:** PROVISIONAL AUTHOR PROOF — independent mathematical review required; do not count this as accepted STD state.
**Task:** issue #79 (standalone author chat, *not* a managed-agent session).
**Pinned main:** private-history-omitted.
**Dependencies:** accepted PR #6 finite-type cyclic source and Euler support-pair scope (theorem blob private-history-omitted); accepted PR #59 witness-bounds premise (blob private-history-omitted); PR #67 caution about structural versus feasible active minors (blob private-history-omitted); prior #73/#75 family (blob private-history-omitted) is a **different** family.
**Actual managed session ID:** unavailable in this standalone chat. Nonauthor reviewer: not assigned.

## 1. Exact definitions and theorem

Fix any integer \(p\ge2\) and put
\[
q=2p+1,\qquad m=2q+1,\qquad
U_d=0^d1^d\quad (d=p,q).
\]
Take source/output alphabets \(A=B=\{0,1\}\). Let the finite-type source domain \(\mathcal X_p\) consist of **every nonempty finite cyclic binary word, of any positive source length**, whose periodic length-\(m\) windows all belong to
\[
\mathcal W_m=
 \{(U_p^\infty)_{i:i+m}:0\le i<2p\}
 \;\cup\;
 \{(U_q^\infty)_{j:j+m}:0\le j<2q\}.
\]
Here \(U_d^\infty\) denotes the bi-infinite periodic extension; windows wrap when source length is less than \(m\). Distinct roots/rotations are allowed, but all statistics below are **raw cyclic block counts**, not necklace counts. The transformation \(T\) is the total, nonerasing, synchronous **radius-zero identity rule** \(\phi(0)=0,\phi(1)=1\); output is cyclic.

For a nonempty cyclic source \(X\), \(C_h(X)(w)\) counts all periodic \(h\)-windows at source sites. The least histogram horizon \(H_{T,\mathcal X_p}(2)\) is as in accepted PR #6.

**Theorem (candidate, scoped).** For every integer \(p\ge2\):

1. The recurrent length-\(m\) higher-block graph consists of exactly **two disjoint directed simple cycles** with respectively \(2p\) and \(2q\) edge types. Thus the total number of recurrent edge types is
   \[
   E=2p+2q=6p+2.
   \]
   Every admissible cyclic word is a positive power of \(U_p\) or \(U_q\), up to rotation.
2. \(H_{T,\mathcal X_p}(2)=2\). Among pairs of **individually admissible**, nonempty cyclic words \(X,Y\) such that
   \[
     C_1(X)=C_1(Y),\quad C_2(T(X))\ne C_2(T(Y)),
   \]
   the exact minimum of either individual source length is
   \[
   \ell_{\rm int}=2pq=2p(2p+1)
      =\frac{(E-2)(E+1)}9=\Omega(E^2).
   \]
   A shortest pair is \(X=U_p^q,\ Y=U_q^p\).
3. Take the PR #6 normalized rational support-pair LP at higher-block length \(L=m\), \(h=1\), supports \(S\) and \(R\) being the respective two entire cycles, and selected **integer** target row \(F=C_2(T(\cdot))(01)\) with sign \(F(X)-F(Y)\ge1\). (For identity, this is exactly the prefix-two row \(P_2\) on length-\(m\) edges.) This feasible LP is a one-dimensional ray with **exactly one vertex**, at per-edge multiplicities
   \[
   x_e=\alpha=q/p\quad(e\in S),\qquad
   y_f=\beta=1\quad(f\in R).
   \]
   The vertex's *minimal common positive clearing denominator* is exactly \(p\), unbounded as \(E\) grows. Minimum rational individual LP mass is \(2q\); minimum positive *integer* LP mass is \(2pq\), giving an exact integrality ratio \(p=(E-2)/6\) for this normalized LP objective. Every integer full-rank active constraint basis at this vertex has determinant divisible by \(p\).

Part 3 concerns the denominator of the **unique feasible vertex**, not every feasible rational point: in particular the same ray contains the integral feasible point \((\alpha,\beta)=(q,p)\). The example therefore does *not* claim all feasible rational solutions require denominator \(p\).

## 2. Graph structure, including period-shorter-than-window cases

Each periodic orbit \(U_d=(0^d1^d)\) has primitive period \(2d\): one copy has exactly one occurrence of the periodic transition \(01\), so a nontrivial repetition of a shorter word would make that count a multiple greater than one. Hence its starting-position periodic windows of any length at least \(2d\) are pairwise distinct.

All length-\((m-1)=2q\) windows of \(U_q^\infty\) contain an *unsplit* run of \(q\) consecutive zeros or an unsplit run of \(q\) consecutive ones: the window contains a full \(2q\)-period, and at most one of the two constant runs is cut across its boundary. In contrast, no substring of \(U_p^\infty\) has \(q\) consecutive equal bits because its maximal constant run is \(p<q\). Therefore the length-\((m-1)\) window sets of the two orbits are disjoint.

The length-\(m\) windows are precisely the allowed graph edges, from their \((m-1)\)-prefix vertices to their \((m-1)\)-suffix vertices. Within an orbit the prefix vertices are distinct and every vertex has exactly one incoming and one outgoing edge, following its next-periodic-window successor. Across orbits the vertex sets are disjoint, so no edge or vertex joins the two. This proves part 1, with edge counts \(2p,2q\).

A source of length \(n<m\) still induces an \(n\)-step closed walk in this graph by periodic wrapping. A closed walk in the displayed disjoint simple cycles must wind a positive integer number of times around exactly one cycle. Reading the corresponding first symbols gives a rotation of a positive power of \(U_p\) or \(U_q\), without assuming \(n\ge m\).

## 3. Horizon and exact minimum cyclic witnesses

One period of \(U_d\) has
\[
C_1(U_d)=(d,d),\quad C_2(U_d)(01)=C_2(U_d)(10)=1,
\quad C_2(U_d)(00)=C_2(U_d)(11)=d-1.
\]
If two words lie on the same orbit, equality of \(C_1\) forces equal repetition counts, hence equal \(C_2\). A cross-orbit pair must be rotations of \(U_p^a,U_q^b\), for integers \(a,b\ge1\). Equality of \(C_1\) is precisely \(pa=qb\). Since \(q=2p+1\) is coprime to \(p\), the complete set of positive integer solutions is
\[
a=qj,\quad b=pj,\qquad j=1,2,\ldots.
\]
Thus both source lengths are \(2pqj\), and **no smaller witnessing length exists**. At \(j=1\), output \(C_2(01)\) is respectively \(q\) and \(p\), which differ. The exhibited pair is admissible by part 1. Order \(h=1\) therefore fails; source \(C_2\) trivially determines the output \(C_2\) because the transformation is identity, so the exact minimum is \(H_{T,\mathcal X_p}(2)=2\).

Substituting \(E=6p+2\) into \(2p(2p+1)\) yields \((E-2)(E+1)/9\). Both sources are individually realizable closed walks; a disconnected sum of circulations was **not** used as a surrogate for a cyclic witness.

## 4. Full normalized support-pair LP and feasible active basis

For the ordered supports \(S\) (the \(2p\)-cycle) and \(R\) (the \(2q\)-cycle), incidence balance forces every variable on \(S\) to equal one real value \(\alpha\), and every variable on \(R\) to equal one real value \(\beta\). The source \(C_1\) equality row reduces to
\[
p\alpha=q\beta,\qquad\text{thus}\quad \alpha=(q/p)\beta.
\]
The positivity constraints are \(\alpha,\beta\ge1\). For the selected target coordinate \(C_2(01)\), whose edge coefficient is \(1\) precisely on the single \(01\)-starting edge of each orbit and \(0\) otherwise, the signed discrepancy constraint is
\[
\alpha-\beta=(q/p-1)\beta
      =\left(1+\frac1p\right)\beta\ge1.
\]
Since \(q/p=2+1/p\), all constraints except \(\beta\ge1\) are automatically satisfied on the ray, and the complete real/rational feasible set is
\[
(\alpha,\beta)=((q/p)\beta,\beta),\quad\beta\ge1.
\]
The map from this ray into all \(E\) original edge coordinates is affine and injective, so it preserves vertices. The unique vertex is \(\beta=1,\alpha=q/p\). The fraction \(q/p\) is in lowest terms, so its common denominator is exactly \(p\).

Both rational histogram masses are \(2p\alpha=2q\beta\), with minimum \(2q\) attained at this vertex. For integer edge histograms, the equality \(p\alpha=q\beta\) forces \(\beta=pj,\alpha=qj\) for positive integer \(j\), giving exact minimum length \(2pq\). Their ratio is \(p\). Multiplying the rational vertex by \(p\) produces the minimal integer Euler witnesses from Section 3; the target gap scales from \(1+1/p\) to \(p+1\).

Finally, at the unique vertex any full-rank active constraint basis \(A z=b\) drawn from the original LP equality/active-inequality rows has integral \(A,b\), since incidence, source-prefix, target and positivity coefficients are integer. By Cramer's rule, the reduced denominator \(p\) of a coordinate \(q/p\) divides \(|\det A|\). At least one such active full-rank basis exists at a polyhedral vertex. Thus this example has **genuine feasible active bases** with determinant divisible by an unbounded \(p\), stronger than demonstrating merely an arbitrary large structural minor. It does not establish exponential active determinants.

## 5. Minimal adversarial examples

- \(p=2,\ q=5,\ m=11,\ E=14\): \(X=(0011)^5\) and \(Y=(0000011111)^2\) each have length \(20\), source \(C_1=(10,10)\), but output \(C_2(01)=5\) versus \(2\). The unique LP vertex has \((\alpha,\beta)=(5/2,1)\), denominator two.
- \(p=3,\ q=7,\ m=15,\ E=20\): \(X=(000111)^7\), \(Y=(00000001111111)^3\) each have length \(42\) and source \(C_1=(21,21)\). Output \(C_2(01)=7\) versus \(3\); LP vertex \((7/3,1)\), denominator three.
- The fact that the \(p=2\) source orbit period \(4\) is smaller than the context length \(11\) is deliberately covered. Periodic wrapping is essential.

## 6. Author-run finite checks and evidence

A small **author-run, nonindependent** Python standard-library script is at experiments/coprime_orbit_witness_check.py. It builds literal periodic windows and the original overlap graph; checks distinct edge/vertex sets and its two cycles; compares the literal \(C_1,C_2\) counts of proposed witnesses; checks all rooted rotations of each graph cycle through the proposed minimum length; and uses exact fractions for the vertex denominator. It additionally exhausts all \(2+4+\cdots+2^{12}=8190\) binary rooted words at lengths 1..12 for \(p=2\), classifying each by literal admissible \(m\)-windows.

Reproduction on the reviewed branch from the repository root:

~~~sh
python -V
python experiments/coprime_orbit_witness_check.py
~~~

Author's execution: CPython 3.13.5, \(p=2,\dots,12\), all eleven sizes passed; 8,190 completely enumerated binary rooted input words for \(p=2,n\le12\); no failures. No Python -O claim (checks use assert). These checks **do not** establish the theorem for all \(p\), and the derived-orbit enumeration is not an independently written production inverse oracle. The proof is in Sections 2–4; no proof assistant and no external review.

## 7. Limitations and requested follow-up

- This construction is **reducible**: two disjoint directed cycles. It makes no statement about necessary witness lengths for irreducible SFTs.
- The lower bound is quadratic in \(E\), **not exponential**. The context length \(m=4p+3\) also grows with \(p\); explicitly listing \(E\) permitted windows of length \(m\) consumes \(O(E^2)\) symbol slots. Consequently the theorem does **not** establish a superlinear bound in literal serialized input size.
- It is for arbitrary positive cyclic source lengths, not a fixed source population, rooted inverse counting or sorting/positional operations. The target is the binary nonerasing identity at output order two.
- The denominator lower bound is for the **vertex of a particular normalized fixed support-pair LP**; the same LP has larger integral feasible points. No universal exponential lower bound, runtime result or finite-sample extrapolation is claimed.
- Author-generated computation is supporting evidence, not an independent mathematical or implementation audit.

**Requested next owner:** a distinct nonauthor auditor session, assigned by the coordinator, to independently check the two-orbit graph proof, sign and target coefficient convention, LP normalization/reduced vertex, active-basis divisibility, and shortest-word assertion at the *exact published head*. Then a separate engineer can provide genuinely independent literal checks if needed. Do not merge or update consolidated accepted state without review.
