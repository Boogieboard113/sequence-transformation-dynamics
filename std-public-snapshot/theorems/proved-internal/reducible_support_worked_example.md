# Worked exact reducible-support example: cross-SCC compatibility

**Date:** 2026-10-11  
**Status:** proved-internal worked example; exact arithmetic regression supplied; not externally peer reviewed or formally verified.  
**Candidate dependency:** the general reducible support-pair theorem in PR #6 is provisional until accepted. The calculation below is self-contained and does not require that theorem for correctness.

## 1. Purpose

This example isolates the point that is easy to miss in a reducible cyclic finite-type domain:

> each recurrent SCC may have a perfectly well behaved horizon internally, while two different SCCs can still realize the same source histogram and different output statistics.

Thus an exact global solver needs a **cross-support compatibility** check. Running an irreducible test independently on each SCC is not sufficient.

The example also shows, in full, how a rational feasible support-pair point scales to integer circulations and then to literal single-cycle Euler witnesses.

## 2. Source domain

Let the source alphabet be
\[
A=\{0,1\}.
\]
Use a length-five finite-type presentation, so \(m=5\). Let the allowed five-blocks be
\[
\mathcal W_5=S\sqcup T,
\]
where
\[
S=\{00110,01100,11001,10011\},
\]
and
\[
T=\{01010,10101\}.
\]

The directed higher-block graph has length-four vertices. The \(S\)-edges form the directed four-cycle
\[
0011\to0110\to1100\to1001\to0011,
\]
while the \(T\)-edges form the directed two-cycle
\[
0101\to1010\to0101.
\]
The two vertex sets are disjoint. Hence the presentation consists of exactly two recurrent SCCs and no transient edges.

The source domain \(\mathcal X\) is **all nonempty finite cyclic words of arbitrary positive length** whose periodic five-windows lie in \(\mathcal W_5\), with periodic wrapping even when the source period is shorter than five.

Because every vertex in either component has one incoming and one outgoing edge, every source in \(\mathcal X\), up to cyclic rotation, is exactly one of
\[
(0011)^\alpha,\qquad \alpha\in\mathbb Z_{>0},
\]
or
\[
(01)^\beta,\qquad \beta\in\mathbb Z_{>0}.
\]

There is no distinguished root in the theorem. All source and output statistics are raw cyclic block counts.

## 3. Local rule and erasure convention

Take output alphabet
\[
B=\{a,b\}.
\]
Use a total radius-two local rule
\[
\phi:\{0,1\}^5\to\{a,b\}
\]
defined by
\[
\phi(w)=
\begin{cases}
b,&w\in T,\\
a,&w\notin T.
\end{cases}
\]

Thus every allowed \(S\)-context emits \(a\), and every allowed \(T\)-context emits \(b\). The values outside \(\mathcal W_5\) make the rule total but are irrelevant on the stated source domain.

There is **no erasure**. Hence for output order \(k=1\) the local additive presentation length is already \(L=5\).

For a source in the \(S\)-component,
\[
T((0011)^\alpha)=a^{4\alpha},
\]
and for a source in the \(T\)-component,
\[
T((01)^\beta)=b^{2\beta}.
\]

Our target statistic is the output single-symbol histogram \(C_1(T(X))\).

## 4. The two support cones

Let \(x\) be a positive balanced edge circulation supported on \(S\). Since \(S\) is a simple directed cycle, balance forces all four edge variables to equal one scalar:
\[
x_e=\alpha>0 \qquad(e\in S).
\]
Likewise every positive balanced circulation on \(T\) has
\[
y_e=\beta>0 \qquad(e\in T).
\]

These are not merely convenient parameterizations. A proper nonempty subset of either simple directed cycle cannot be a strongly connected balanced positive support. Therefore the only Euler supports in this presentation are \(S\) and \(T\) themselves.

The source one-symbol projections are
\[
P_{1,S}x=(2\alpha,2\alpha),
\]
because two \(S\)-edges begin with \(0\) and two begin with \(1\), and
\[
P_{1,T}y=(\beta,\beta).
\]

The output one-symbol projections are
\[
F_Sx=(4\alpha,0)
\]
in coordinates \((a,b)\), and
\[
F_Ty=(0,2\beta).
\]

## 5. Exact h=1 support-pair feasibility

For a cross-support pair \(S,T\), equality of source \(C_1\) is exactly
\[
(2\alpha,2\alpha)=(\beta,\beta),
\]
or
\[
\boxed{\beta=2\alpha.}
\]

The positivity constraints in the support-pair formulation are
\[
\alpha\ge1,\qquad \beta\ge1.
\]

Choose the exact rational point
\[
\alpha=\frac32,\qquad \beta=3.
\]
Then
\[
P_{1,S}x=P_{1,T}y=(3,3),
\]
but the output \(a\)-coordinate differs by
\[
(F_Sx)_a-(F_Ty)_a=4\cdot\frac32-0=6.
\]
Thus the rational cross-support discrepancy system is feasible.

This already proves that \(h=1\) is insufficient at the cone level.

## 6. Scaling to integer Euler witnesses

The common denominator of the rational point is \(2\). Multiplying both circulations by \(2\) gives
\[
x_e=3\quad(e\in S),\qquad
y_e=6\quad(e\in T).
\]

These are integer balanced positive circulations. Their Euler lifts are literal cyclic sources
\[
X=(0011)^3=001100110011
\]
and
\[
Y=(01)^6=010101010101.
\]

Each \(S\)-edge appears exactly three times as a periodic five-window of \(X\), and each \(T\)-edge appears exactly six times as a periodic five-window of \(Y\).

Their source one-counts agree:
\[
C_1(X)=C_1(Y)=(6,6).
\]

Their outputs are
\[
T(X)=a^{12},\qquad T(Y)=b^{12},
\]
so
\[
C_1(T(X))\ne C_1(T(Y)).
\]

There is also a smaller integral witness obtained directly from
\[
\alpha=1,\qquad\beta=2:
\]
\[
X_{\min}=0011,\qquad Y_{\min}=0101.
\]
Both have source \(C_1=(2,2)\), while their outputs are \(aaaa\) and \(bbbb\).

The nonintegral point above is retained because it explicitly demonstrates the denominator-clearing step used by the general rational support-cone argument.

## 7. Exact h=2 infeasibility across supports

For one traversal of the \(S\)-cycle,
\[
C_2(0011)=
\{00:1,01:1,11:1,10:1\}.
\]
Therefore a positive \(S\)-circulation of scalar \(\alpha\) has
\[
P_{2,S}x(00)=\alpha.
\]

For one traversal of the \(T\)-cycle,
\[
C_2(01)=\{01:1,10:1\},
\]
so every \(T\)-circulation has
\[
P_{2,T}y(00)=0.
\]

A cross-support equality
\[
P_{2,S}x=P_{2,T}y
\]
would therefore force
\[
\alpha=0,
\]
contradicting the support condition \(\alpha\ge1\).

Hence every \(S,T\) and \(T,S\) support-pair discrepancy system is infeasible already from the single \(00\)-row. Equivalently, the \(11\)-row gives the same obstruction.

The same-support pairs are also harmless:

- For \(S,S\), equality of \(C_2\) forces the two circulation scalars to agree via the \(00\)-row, so the output histograms agree.
- For \(T,T\), equality of \(C_2\) forces the two scalars to agree via either the \(01\)- or \(10\)-row, so the output histograms agree.

Because \(S\) and \(T\) are the only Euler supports, these four ordered support pairs exhaust all cases.

Thus equal source \(C_2\) always implies equal output \(C_1\).

## 8. Exact horizon

Section 6 gives two sources with equal \(C_1\) and different output \(C_1\), so
\[
H_{T,\mathcal X}(1)>1.
\]

Section 7 proves that source \(C_2\) is sufficient globally, so
\[
H_{T,\mathcal X}(1)\le2.
\]

Therefore
\[
\boxed{H_{T,\mathcal X}(1)=2.}
\]

This is an exact theorem for the stated finite-type domain, not a conclusion from bounded enumeration.

## 9. Why independent per-SCC analysis fails

Inside \(S\), \(C_1\) already fixes \(\alpha\), so the output count is fixed. Inside \(T\), \(C_1\) already fixes \(\beta\), so the output count is fixed. Thus an analyst who checked only pairs of sources lying in the **same** recurrent SCC would conclude that \(h=1\) is sufficient in both components.

The global conclusion is nevertheless false because
\[
P_{1,S}(\alpha)=P_{1,T}(2\alpha)
\]
for every positive \(\alpha\), while the outputs live on different output symbols.

The missing condition is exactly the cross-support compatibility equation. SCC decomposition is useful for organizing supports; it does not remove the need to compare their projected source-count cones.

## 10. Proof versus executable evidence

The exact horizon proof is Sections 2–8. It uses only the explicit two-cycle presentation and scalar balance equations.

The executable artifact experiments/reducible_support_example.py checks, with standard-library Fraction arithmetic:

- the two disjoint recurrent cycles;
- the exact rational point \((3/2,3)\);
- incidence balance and source \(P_1\) equality;
- the output discrepancy;
- denominator clearing and literal Euler-source histograms;
- the minimal integer witness;
- the \(P_2(00)\) obstruction; and
- the reported exact horizon value.

Regression: tests/test_reducible_support_example.py

Reproduce from repository root:

    python experiments/reducible_support_example.py
    python -m unittest tests.test_reducible_support_example -v
    python -m unittest discover -s tests -v

Finite execution supports the arithmetic and guards the example against regression; it is not substituted for the proof.

## 11. Limitations

This example concerns:

- nonempty finite **cyclic** sources of unrestricted positive length;
- one finite-type presentation;
- raw periodic source counts;
- a total nonerasing radius-two local rule;
- the output statistic \(C_1\).

It does not establish a generic LP implementation, efficiency bound, fixed-length result, rooted/cut output theorem, inventory-constrained result, or statement for arbitrary partial/sofic domains.

The general support-pair theorem in PR #6 is cited only as a provisional candidate dependency. The worked example itself has been proved directly above and remains meaningful even if the general theorem is later revised.

## 12. Pinned inputs

At task start:

- main: private-history-omitted;
- candidate PR #6 pre-issue-#7 head: private-history-omitted;
- README blob: private-history-omitted;
- AGENTS blob: private-history-omitted;
- RESEARCH_STATE blob: private-history-omitted;
- TASK_BOARD blob: private-history-omitted;
- CONCURRENCY_PROTOCOL blob: private-history-omitted.

Issue #7's recurrent-core repair is a separate open review item on PR #6. This branch is based directly on main and does not import that unmerged branch.


## 13. Revalidation before review handoff

Main advanced during this task by merging the separately reviewed reset-gap PR #5. Before handoff the repository was re-read and pinned again:

- current main: private-history-omitted;
- current PR #6 head: private-history-omitted;
- issue #11 remains A-owned and active, with C as the requested nonauthor reviewer.

The main-branch advance adds only the reset-gap audit/theorem/test files and does not overlap the three files in this topic branch. GitHub reports PR #25 mergeable against the new base. The worked example remains self-contained and does not depend on the merged reset-gap result.
