# Exact vertices and shortest witnesses in the exponential-minor family

**Date:** 2026-10-11.  
**Task:** issue #73.  
**Status at authorship:** analytic proof submitted for independent nonauthor review; not yet an accepted-state claim.  
**Task-start main:** `private-history-omitted`.  
**Inputs:** PR #67 family in `support_pair_sparse_sharpness.md`, blob `private-history-omitted`; PR #6 Euler lifting and support-pair conventions in `finite_type_exact_horizon.md`, blob `private-history-omitted`; PR #59 distinction between Cramer determinants and common denominator clearing in `support_pair_witness_size_bounds.md`, blob `private-history-omitted`.

## 1. Scope and result

This note concerns **only** the explicit family from Section 4 of PR #67. For every integer `t >= 3`, it proves:

1. The normalized LP with both positive supports equal to all `4t` edges and signed target discrepancy at least one has exactly **one vertex when t is odd** and exactly **two vertices when t is even**. All of these vertices are integral.
2. The shortest equal-source-`C_1`, target-discrepant cyclic sources having those full positive supports have individual length **exactly `6t`**.
3. When their positive supports may vary over all admissible individual cyclic sources, the shortest such pair has individual length **exactly `4t`**.
4. The nonerasing local-emission system below has exact horizon **`H_T(1)=2`**.

The family therefore has the accepted exponential structural minors `2^t`, but denominator-one vertices and linear shortest actual witnesses for this selected target. This resolves the behavior of this particular family. It neither proves nor disproves a general polynomial witness-size bound or a general worst-case lower bound for STD.

All counts are raw periodic cyclic counts. Sources have unrestricted positive integer length; rotations do not affect any claim here. A rooted inverse count, a fixed population, or a prescribed inventory is not being studied. A witness pair always means **two individually realizable nonempty cyclic words**, not two arbitrary possibly disconnected nonnegative circulations.

## 2. The domain, graph, and target

Let `A_t={a_0,...,a_(t-1)}`, with indices modulo `t`. Allow exactly the following length-three windows:

\[
s_i=a_i a_i a_{i+1},\qquad
t_i=a_i a_{i+1}a_i,\qquad
u_i=a_{i+1}a_i a_{i+1},\qquad
v_i=a_i a_{i+1}a_{i+1}.
\]

The repeated notation `t_i` denotes an edge label, while `t` is the alphabet size. The `4t` edges are distinct for `t>=3`. The domain consists of all nonempty finite cyclic words whose periodic length-three windows are among these edges, including the convention that windows wrap when the period is shorter than three.

Write the length-two vertices as

\[
p_i=a_i a_i,\quad w_i=a_i a_{i+1},\quad z_i=a_{i+1}a_i.
\]

They are pairwise distinct for `t>=3`. The edges are

\[
p_i\xrightarrow{s_i}w_i\xrightarrow{v_i}p_{i+1},
\qquad
w_i\xrightarrow{t_i}z_i\xrightarrow{u_i}w_i.
\]

The first edges form a directed ring through all `p_i,w_i`; each `w_i` has an attached two-edge excursion through `z_i`. This description also verifies strong connectivity and recurrence of all edges.

Use a total radius-one local rule with output alphabet `{0,1}`: emit `1` on context `s_0` and emit `0` on every other context in `A_t^3`. Thus the rule is nonerasing, emits one output symbol per source site, and is defined even on contexts outside the restricted domain. Its output-one count is the target

\[
F(X)=C_3(X)(s_0).
\]

Centered emission rather than forward-window labeling only shifts the enumeration of sites, leaving this raw cyclic count unchanged. In particular `|T(X)|=|X|` and the output-zero count is `|X|-F(X)`.

## 3. Complete circulation parameterization

**Lemma 1.** Every nonnegative real balanced edge vector on this graph, and only such a vector, has the form

\[
n(s_i)=n(v_i)=a,\qquad
n(t_i)=n(u_i)=b_i\qquad(0\le i<t),
\tag{1}
\]

where `a>=0` and every `b_i>=0`. Its prefix-one counts and total mass are

\[
C_1(a_i)=2a+b_i+b_{i-1},\qquad
M=2ta+2\sum_i b_i.
\tag{2}
\]

Here `C_1` means the linear prefix projection; it is the actual raw source histogram whenever the vector is realized by a cyclic word.

**Proof.** Balance at `z_i` gives `n(t_i)=n(u_i)=b_i`. Balance at `w_i` then gives `n(s_i)=n(v_i)`. Balance at `p_i` gives `n(s_i)=n(v_(i-1))`. Going around the ring shows these ring counts all equal one number `a`. Conversely these equations make every vertex balanced. The edges starting with `a_i` are exactly `s_i,t_i,v_i,u_(i-1)`, giving the first formula in (2); summing edge counts gives the second. The target is `F=a`. QED.

For an integer vector in (1), actual one-word realizability is especially simple:

- If `a>0`, all ring edges occur, and every positive excursion is attached to that ring. The positive support is strongly connected, so the accepted Euler-lifting lemma realizes the vector by one cyclic word.
- If `a=0` and the vector is nonzero, its positive edges are a union of excursion two-cycles. These cycles have disjoint vertex sets for `t>=3`. Consequently the vector is realizable by one cyclic word **if and only if exactly one `b_i` is positive**. That word uses only the two source symbols `a_i,a_(i+1)`.
- The zero vector is excluded by the nonempty-source convention.

This last restriction will be essential to the global minimum. Symbol overlap between excursions does not connect their length-two graph vertices.

## 4. The full-support normalized LP

Fix `S=T` equal to the entire `4t`-edge set, source order `h=1`, target `F=1_(s_0)`, and sign chosen so `F(x)-F(y)>=1`. These are exactly the accepted normalized support-pair constraints: both vectors balanced, identical prefix-one projection, every edge coordinate at least one, and one target discrepancy at least one.

Parameterize the `x` circulation by `(a+d,b_i)` and the `y` circulation by `(a,c_i)`. Balance and positivity imply

\[
a\ge1,\quad d\ge1,\quad b_i\ge1,\quad c_i\ge1.
\tag{3}
\]

The `x` ring positivity is automatic since `a+d>=2`. By (2), the matching source counts become

\[
e_i+e_{i-1}=-2d,\qquad e_i=b_i-c_i.
\tag{4}
\]

These equations completely describe the LP in reduced coordinates; the correspondence with the original `8t` edge variables is affine and one-to-one. Hence it preserves vertices. Indeed a nontrivial convex decomposition in either coordinate system maps bijectively to a nontrivial decomposition in the other.

Put `f_i=e_i+d`. Then (4) reads `f_i=-f_(i-1)`. Going around the ring proves:

- For odd `t`, `f_i=0`, so `c_i=b_i+d`.
- For even `t`, there is one real parameter `q` such that
  \[
  c_i=b_i+d-(-1)^i q.
  \tag{5}
  \]

This is an exact parity classification, including all feasible real points, not just integer or symmetric choices.

## 5. All vertices are integral

**Theorem 2.** For the full-support LP of Section 4:

- If `t` is odd, its only vertex is
  \[
  a=d=1,\quad b_i=1,\quad c_i=2.
  \tag{6}
  \]
- If `t` is even, its only vertices are
  \[
  a=d=1,\quad b_i=1,\quad q=+1\ \text{or}\ -1,
  \qquad c_i=2-(-1)^i q.
  \tag{7}
  \]

Thus the odd vertex has `x` ring/excursion counts `(2,1)` and `y` counts `(1,2)`. The even vertices have `x` counts `(2,1)` and `y` ring count one with excursion counts alternating between one and three. All original edge coordinates at these vertices are integers.

**Proof for odd t.** The reduced feasible set is exactly

\[
a\ge1,\quad d\ge1,\quad b_i\ge1,
\]

because `c_i=b_i+d>=2` is automatic. A coordinate strictly above its lower bound can be varied in both directions, so no such point is a vertex. Conversely the point where all coordinates equal their lower bounds is a vertex: a convex decomposition into feasible points forces equality in every lower bound in both components. This proves (6).

**Proof for even t: exhaustion.** By (3) and (5), the reduced feasible set is

\[
a\ge1,\qquad d\ge1,\qquad
b_i\ge\max\{1,\ 1-d+(-1)^i q\}.
\tag{8}
\]

Every vertex must have `a=1`, since otherwise `a` alone can be moved slightly in both directions. For the same reason every `b_i` must equal its displayed lower bound at a vertex: if it exceeds both lower bounds, changing only that `b_i` slightly preserves all constraints in both directions.

Every vertex also has `d=1`. To prove this without an assumption on which inequalities are active, suppose `d>1` and put `u_i=b_i-1>=0`. Positivity of `c_i` is the homogeneous inequality

\[
u_i+d-(-1)^i q\ge0.
\]

Scale `(d,q,u_0,...,u_(t-1))` by `1+epsilon` and `1-epsilon`, leaving `a` fixed. For sufficiently small positive `epsilon`, both new values of `d` remain at least one; all the homogeneous inequalities remain true. Returning to `b_i=1+u_i`, these are two distinct feasible points whose midpoint is the original point. Thus it is not a vertex.

Now let `a=d=1` and each `b_i` be minimal. Formula (8) reduces to

\[
b_i=\max\{1,(-1)^i q\}.
\tag{9}
\]

On each of the three open intervals `q<-1`, `-1<q<1`, and `q>1`, all expressions in (9) are affine in `q`. A sufficiently small positive and negative change in `q`, with `b_i` changed by those affine formulas, therefore expresses the point as the midpoint of two distinct feasible points. The only possible vertices are `q=-1,+1`. At either endpoint, (9) gives all `b_i=1`, yielding (7).

**Proof for even t: the two remaining points are vertices.** At either candidate, `a=d=b_i=1`. Any convex decomposition into feasible points forces those values in both components because they are individual lower bounds. With these values fixed, (8) forces `-1<=q<=1`. A convex combination giving `q=+1` forces `q=+1` in both components, and similarly for `q=-1`. Thus both candidates are vertices. QED.

**Denominator interpretation.** Every vertex has minimal common clearing denominator one. This does not say every rational feasible point is integral: for even `t`, the midpoint `q=0` of the two vertices is a different feasible point, and arbitrary rational `q` between the endpoints can give nonintegral `c_i`. For odd `t`, taking `d=3/2`, `a=b_i=1` is a rational nonintegral feasible point. Nor is a selected nonsingular active-basis determinant required to be one at an integral vertex: Cramer's numerators may share factors with that determinant. The accepted exponential structural-minor result and this vertex theorem concern different quantities.

## 6. Exact minimum with both supports full

**Theorem 3.** Among actual cyclic witness pairs with both positive edge supports equal to all `4t` edges, equal `C_1`, and differing `F`, the minimum common individual source length is `6t`.

**Proof.** Reverse the names of the witnesses if necessary so `F(x)>F(y)`. Their integer target difference is then `d>=1`. Full support forces `a>=1` and every `b_i>=1`, so (2) applied to `x` gives

\[
|X|=2t(a+d)+2\sum_i b_i\ge4t+2t=6t.
\]

Equal `C_1` forces the two lengths to be equal. This lower bound is attained by

\[
x:\ a_x=2,\ b_i=1;
\qquad
y:\ a_y=1,\ c_i=2.
\tag{10}
\]

Both are positive balanced integer vectors on the full strongly connected graph. Their source count of every `a_i` is six, and their target counts are two and one. Euler lifting, or the explicit words below, realizes them. QED.

For real normalized full-support feasible points `(x,y)`, the minimum edge mass of each circulation is `6t`, and the minimum combined edge mass of the pair is `12t`. For even `t`, the symmetric choice in (10) is the midpoint of the two LP vertices, not an additional vertex; either actual vertex also attains individual mass `6t` and combined mass `12t`.

## 7. Exact minimum over all admissible cyclic sources

**Theorem 4.** Among all nonempty admissible cyclic sources with equal `C_1` and different `F`, allowing their positive supports to vary, the minimum common individual source length is `4t`.

**Proof of the lower bound.** As before name the sources so `a_x>a_y`. Since these are actual integer edge counts, `a_x>=1`. A positive ring count forces `X` to contain every source symbol: by (2), `C_1(X)(a_i)>=2a_x>0` for every `i`.

If `a_y=0`, the one-word realizability classification after Lemma 1 says that `Y` is confined to a single excursion two-cycle. Such a word uses only two alphabet symbols, whereas `X` uses all `t>=3` symbols. This contradicts equal `C_1`. Hence `a_y>=1` and `a_x>=2`.

Applying the nonnegative version of (2) gives

\[
|X|=2ta_x+2\sum_i b_i\ge4t.
\]

**Attainment.** Choose

\[
x:\ a_x=2,\ b_i=0;
\qquad
y:\ a_y=1,\ c_i=1.
\tag{11}
\]

The `x` positive support is the ring and the `y` positive support is the entire graph. Each is strongly connected. Both vectors are balanced integers, have source count four of every symbol, length `4t`, and target counts two and one. Euler lifting realizes both. QED.

In particular, dropping full-support positivity legitimately reduces the minimum from `6t` to `4t`; dropping individual cyclic realizability would create a different problem and would invalidate the crucial obstruction when `a_y=0`.

## 8. Explicit cyclic words and exact horizon

In the following concatenations each `a_i` is one abstract alphabet symbol. For example, an index larger than nine does not mean a string of decimal digit symbols. All `i+1` subscripts are reduced modulo `t`.

Define three rooted representatives of cyclic words:

\[
W=\prod_{i=0}^{t-1}(a_i a_i),\qquad
V=\prod_{i=0}^{t-1}(a_i a_i a_{i+1} a_i),\qquad
Z=\prod_{i=0}^{t-1}(a_i a_i a_{i+1} a_i a_{i+1} a_i).
\tag{12}
\]

These are read by recording the first symbol of successive edges in tours based at `p_0`:

- `W` traverses `s_i,v_i` in index order.
- `V` traverses `s_i,t_i,u_i,v_i` in index order.
- `Z` traverses `s_i,t_i,u_i,t_i,u_i,v_i` in index order.

Each tour returns to `p_0`; reading first edge symbols gives the stated cyclic length-three windows, including across the last-to-first boundary. Concatenating these tours at `p_0` just adds their edge histograms. Therefore:

| Scope | X | Y | Individual length | Source count per symbol | Target counts `(F(X),F(Y))` |
|---|---|---|---:|---:|---|
| All admissible positive supports | `WW` | `V` | `4t` | 4 | `(2,1)` |
| Both positive supports full | `VW` | `Z` | `6t` | 6 | `(2,1)` |

**Corollary 5.** The local-emission rule from Section 2 has `H_T(1)=2` on the stated cyclic finite-type domain.

**Proof.** The explicit pair `WW,V` proves failure of source-order-one sufficiency. Conversely a periodic length-two window `a_0a_0` can be followed only by `a_1` in the allowed domain: the only edge leaving `p_0` is `s_0`. Hence

\[
F(X)=C_3(X)(s_0)=C_2(X)(a_0a_0).
\]

Equal source `C_2` determines this output-one count and also determines source length by summing its coordinates. Since the local rule emits exactly one symbol per source position, the output-zero count is then determined too. Thus all output `C_1` coordinates are determined by source `C_2`, proving sufficiency at order two and the exact minimum. QED.

## 9. Evidence classification and remaining question

The parameterization, vertex exhaustion, exact minimum lengths, and horizon statements above are analytic arguments. A separate exact computational companion may check finite parameter values, actual periodic windows, supports, and vertices; such checks support these proofs and do not establish their universal quantifiers. Acceptance requires an independent nonauthor review tied to the published exact theorem commit.

The inherited PR #67 structural minor is still `2^t` in a family with `N=8t` full-support variables. The new result gives denominator one for every vertex of the selected full-support LP, shortest full-support witnesses of length `6t`, and shortest witnesses over all allowed individual sources of length `4t`. It therefore supplies an explicit separation between large structural minors and these two witness quantities **for this family and this target**.

No claim is made about the size of determinants of all feasible active bases, arbitrary rational feasible-point denominators, other targets on the same family, other support pairs' vertex denominators, or a uniform worst-case lower bound across STD presentations. The general question of minimum required feasible denominators and shortest-witness growth remains open. There is no proof-assistant verification, external peer review, or originality claim in this packet.
