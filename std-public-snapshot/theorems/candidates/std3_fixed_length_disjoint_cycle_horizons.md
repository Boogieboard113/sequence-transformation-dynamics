# Exact fixed-length horizon formula for disjoint recurrent cycles

**Status:** analytic author proof, candidate pending an independent exact-head review; **not** an accepted theorem.
**Base:** main private-history-omitted; the issue's older initial pin is private-history-omitted.
**Accepted motivating example:** PR #100, theorem blob private-history-omitted. This proof does not use the PR #100 checker or any conclusions of pending PRs #98/#99/#102.

## 1. Exact objects and conventions

Fix finite nonempty alphabets A and B, an integer m >= 1 and an allowed set F subset A^m. Let X_N be the **rooted**, nonempty, length-exactly-N cyclic source words x in A^N, N >= 1, for which *every* periodic length-m window belongs to F. There are N windows counted with multiplicity even when N < m: the window starting at site t is

    x_t x_(t+1 mod N) ... x_(t+m-1 mod N).

Let G_m be the **canonical** directed higher-block graph, with each allowed word a_1...a_m as one edge from its (m-1)-prefix to its (m-1)-suffix. At m=1 the vertex is the empty word. Let G_m^circ contain exactly the edges on some directed closed walk and their incident vertices. Nonrecurrent edges of the original presentation may exist but cannot appear in a cyclic source.

**Hypothesis:** the entire nonempty G_m^circ is a disjoint union of finitely many **vertex-disjoint directed simple cycles** Gamma_1,...,Gamma_s. Within the recurrent core there are no edges linking these cycles, no shared vertices and no branching. Denote their edge-lengths by d_i >= 1 and the cyclic source words read around them by w_i of length d_i, each defined up to cyclic rotation.

For any nonempty word z and integer h >= 1, write C_h(z) for the raw periodic vector of length-h block counts in A^h or B^h as appropriate. Thus sum of coordinates of C_h(z) is |z|, *not* the number of distinct windows.

Fix one deterministic **total** synchronous local word-emission rule

    phi : A^(2r+1) -> B^+,    r >= 0,

where B^+ excludes the empty emission. For a rooted source x of length N define

    e_t(x) = phi(x_(t-r)...x_t...x_(t+r)),
    T(x) = e_0(x) e_1(x) ... e_(N-1)(x),

all context indices understood modulo N. The target is the **raw cyclic** output statistic C_k(T(x)), with fixed k >= 1; it is not a rooted output or an output-rotation equivalence test. The output length may vary with the source. Nonerasure ensures it is positive.

For each N with X_N nonempty, define H_N(k) as the least **positive** h for which equal source C_h on X_N always implies equal output C_k. Leave H_N(k) **undefined** if X_N is empty (do not declare a vacuous horizon 1).

## 2. The theorem

Define

    I_N = {i : d_i divides N},
    P_(i,h) = C_h(w_i) / d_i  in Q^(A^h),  h >= 1,
    Q_(i,k) = C_k(T(w_i)) / d_i in Q^(B^k), k >= 1.

**Theorem.** Under Section 1's exact hypothesis:

1. Each w_i is a primitive cyclic word. The exact rooted source domain is

       X_N = union_(i in I_N) Rot(w_i^(N/d_i)).

   Consequently X_N is nonempty iff I_N is nonempty, and |X_N| = sum_(i in I_N) d_i.

2. Set b=max(1,m-1). For every N with I_N nonempty,

       H_N(k) =
       min {h in {1,...,b} :
              for all i,j in I_N,
              P_(i,h) = P_(j,h) implies Q_(i,k) = Q_(j,k)}.       (1)

   In particular, **H_N(k) <= max(1,m-1)**, with **no** requirement that k <= m or N >= m or N >= 2r+1. The improved bound uses the *vertex-disjoint* hypothesis, not merely edge disjointness. Comparisons are rational and exact; the output density denominator is d_i (source sites), **not** |T(w_i)|.

3. Equivalently, for distinct i,j put

       delta(i,j) = min {h in {1,...,b} : P_(i,h) != P_(j,h)}.

   Each such delta exists. With the convention max(empty set union {1}) = 1,

       H_N(k) = max( {1} union
                     {delta(i,j) : i,j in I_N, Q_(i,k) != Q_(j,k)} ).  (2)

   Thus a single active component, or identical Q_(i,k) across every active component, gives H_N(k)=1 even if some source density vectors tie.

4. Put L=lcm(d_1,...,d_s). The nonempty-domain indicator and the value of H_N(k) **where defined** depend only on N mod L. Equivalently, adjoining an "undefined" symbol for empty X_N makes an L-periodic sequence. **No claim that L is the least period** is made.

5. For every pair of **distinct** cycles put lambda(i,j)=lcm(d_i,d_j). For every nonempty X_N, the exact formula has the more explicit divisibility-threshold form

       H_N(k) = max({1} union
              {delta(i,j) : i<j, Q_(i,k) != Q_(j,k),
                            lambda(i,j) divides N}).             (8)

   In particular, if N divides M and X_N is nonempty, then X_M is nonempty and H_N(k) <= H_M(k). For each integer t>=2, the positive lengths with H_N(k)>=t are **exactly** the union of the sets of positive multiples of lambda(i,j) over pairs with different Q_(i,k) and delta(i,j)>=t. This gives a finite divisibility description of every nontrivial horizon threshold.

## 3. Analytic proof

### 3.1 Closed-walk classification and primitivity

For each x in X_N, form its successive periodic m-blocks, one from each source site. Adjacent m-blocks overlap in exactly m-1 symbols even for N < m, because indexing wraps modulo N. These edges form an N-step closed walk in G_m. Every traversed edge lies on a closed walk and is therefore in G_m^circ.

Every vertex of G_m^circ belongs to one of the stipulated pairwise disjoint simple cycles, and each such vertex has exactly one incoming and one outgoing **recurrent** edge. Hence this closed walk is forced to remain on a single Gamma_i and can return to its initial phase after N steps if and only if d_i divides N. Its edge-first symbols recover x, giving a rotation of w_i^(N/d_i). Conversely, any such power traverses Gamma_i repeatedly and all its periodic m-blocks belong to F, so is admitted. This proves the domain identity, including periods N smaller than the presentation order m.

The d_i consecutive edge-first symbols read around Gamma_i form a cyclic word w_i. If w_i had a smaller cyclic period p < d_i, the ordered (m-1)-block vertex at phase t would equal that at phase t+p. This contradicts the distinct-vertex property of a simple directed cycle. Thus w_i is primitive, its N-site power has exactly d_i distinct rooted rotations, and two distinct cycles cannot generate the same rooted source because its canonical m-block walk is unique. The cardinality formula follows. The m=1 self-loop case is covered: vertex simplicity forces each possible recurrent component to have length one.

### 3.2 Exact source/output scaling, including unequal emission lengths

For any nonempty z, q >= 1 and h >= 1, periodic windows at starts 0,...,q|z|-1 of z^q repeat the |z| phases q times, regardless of whether h exceeds |z| or q|z|. Therefore

       C_h(z^q) = q C_h(z).                                        (3)

Rotating a rooted source permutes its periodic source windows, leaving C_h unchanged.

Likewise, *every* radius-r context at site t of z^q equals the corresponding context at site t mod |z| of z: this is true even when 2r+1 exceeds the source period and wraps repeatedly. The emitted **site-block sequence** therefore repeats q times, so

       T(z^q) = T(z)^q,                                           (4)

where T on the right is computed using contexts of the primitive cyclic source z, not contexts of a truncated linear substring.

Rotating z^q by j source sites rotates its list of emitted site-blocks by j. After concatenation this is a **character** rotation by the sum of the lengths of the j skipped emission blocks. Those lengths need not be equal. The total output is nonempty because every site emits at least one character. Character rotations preserve raw cyclic C_k and (3) applies to the nonempty output word, proving

       C_k(T(Rot_j(w_i^(N/d_i)))) =
           (N/d_i) C_k(T(w_i)) = N Q_(i,k).                       (5)

Analogously, for the same source,

       C_h(Rot_j(w_i^(N/d_i))) =
           (N/d_i) C_h(w_i) = N P_(i,h).                          (6)

Equations (5) and (6) use **source-site normalization** and remain valid when output lengths differ across components.

### 3.3 Pair criterion, finite upper bound, and exact minimum

Fix N with I_N nonempty. By the domain identity, any x,y in X_N come from some i,j in I_N. Equations (5),(6) say

       C_h(x)=C_h(y)  iff  P_(i,h)=P_(j,h),
       C_k(T(x))=C_k(T(y))  iff  Q_(i,k)=Q_(j,k),

because the common positive source length N cancels. Conversely, the words w_i^(N/d_i) and w_j^(N/d_j) exist for *every* eligible pair i,j. Thus each pairwise implication in (1) is **both necessary and sufficient** for order h on the full X_N; this is not an unsupported per-component-only test.

In fact **one less source order is sufficient** when m>=2. A periodic (m-1)-block is exactly a vertex of the canonical higher-block graph. As Gamma_i is a directed **simple** cycle, its d_i successive (m-1)-blocks are its d_i distinct vertices, each appearing exactly once in C_(m-1)(w_i). Distinct cycles are **vertex-disjoint**, so their (m-1)-block supports are disjoint. Therefore P_(i,m-1) != P_(j,m-1) whenever i != j. When m=1, the canonical higher-block graph has just the empty-word vertex; the disjoint-simple-cycle hypothesis then permits **at most one** recurrent component, whose fixed-N outputs have one histogram value, giving H_N(k)=1. In both cases distinct active components cannot collide at b=max(1,m-1), proving the sharpened bound H_N(k)<=b. This does not rely on any restriction k<=m.

For completeness, periodic prefix marginalization gives for all h >= 1 and any u in A^h,

       C_h(z)(u) = sum_(a in A) C_(h+1)(z)(ua).                    (7)

This holds even for a source shorter than h. Thus equality of P_(i,h+1) implies equality of P_(i,h), and once two components are distinguished by some h they remain distinguished at every larger order. Their first distinguishing order delta(i,j) exists by the preceding **(m-1)-vertex argument** (or no such pair exists when m=1).

A pair with Q_(i,k)=Q_(j,k) imposes no restriction on h. For a pair with different Q-vectors, every h < delta(i,j) fails by its explicit equal-source-histogram witness, while every h >= delta(i,j) separates the sources. Taking the maximum over these pairwise thresholds (default 1 when none) proves (2), and hence the least-positive-order assertion in (1).

### 3.4 Divisibility-class periodicity

For any N >= 1, membership of i in I_N is exactly d_i | N. Since d_i | L, I_(N+L)=I_N. All P_(i,h), Q_(i,k) and delta(i,j) are independent of N, so formulas (1) or (2) yield identical H-values whenever both lengths are nonempty. Also X_N is empty iff I_N is empty. This proves L-periodicity of the partial horizon without asserting a least period.

There is also an explicit arithmetic refinement. A pair i,j is simultaneously eligible at length N exactly when d_i|N and d_j|N, equivalently lambda(i,j)|N. Applying this equivalence to (2) gives (8). For t>=2, its maximum is at least t precisely when one of the corresponding lambda(i,j) divides N; any such N is automatically admissible. If N|M, every lambda dividing N also divides M, so (8) gives H_N(k)<=H_M(k). These are *divisibility*, not ordinary numeric, monotonicity claims. They prove the threshold-union statement and conclude the theorem.

This completes the analytic proof.

## 4. Small adversarial fixtures / boundary calculations

### 4.1 Different primitive periods, short source, variable-length nonerasing emission

Take A=B={0,1}, m=4, with F the six periodic m-windows from

       u=0011 (d=4),    v=01 (d=2).

Explicitly F={0011,0110,1100,1001,0101,1010}. The directed edges on 3-block vertices form two vertex-disjoint directed simple cycles, one of length 4 (vertices 001,011,110,100), the other of length 2 (010,101). Hence all recurrent edges are exactly these six edges.

Let r=0, phi(0)=0, phi(1)=11, k=2. This is **nonerasing but unequal-length** emission. The primitive outputs are

       T(u)=001111,   T(v)=011.

Both source one-block densities are (1/2,1/2), while

       P_(u,2)(00,01,10,11)=(1/4,1/4,1/4,1/4);
       P_(v,2)(00,01,10,11)=(0,1/2,1/2,0).

Output two-block counts, in the same coordinate order, are

       C_2(T(u)) = (1,1,1,3),   Q_(u,2)=(1/4,1/4,1/4,3/4);
       C_2(T(v)) = (0,1,1,1),   Q_(v,2)=(0,1/2,1/2,1/2).

Thus delta(u,v)=2 and the outputs disagree. At N=4, admitted words include u and v^2=0101; their C_1 vectors coincide at (2,2), but their outputs 001111 and 011011 have different C_2, so H_4(2)=2. At N=2 < m only the two rotations of v occur; H_2(2)=1. At odd N the source domain is empty and H_N(2) is undefined. The full partial spectrum repeats modulo 4 (no minimal-period claim).

This example also checks why dividing Q by **source period** rather than output length is necessary.

### 4.2 Radius exceeds the shortest source period

Keep F, u, v, and m from 4.1 but let r=2 and set

       phi(01010)=01,    phi(10101)=1,
       phi(c)=0 for every other five-symbol binary context c.

This is total and nonerasing. The length-two source v=01 has cyclic radius-two contexts 01010 and 10101, despite 2r+1=5 > N=2, and T(v)=011. The length-four source u=0011 has none of these alternating contexts, so T(u)=0000. For k=1, their output source-site densities differ while their C_1 source densities still tie, so H_4(1)=2; H_2(1)=1 since only v is admissible. This excludes the tempting but false assumption that short source words have truncated rather than periodic contexts.

### 4.3 Sharpness of the improved bound at m=3 and m=4

For **m=3**, use alphabet A={0,1,2,3}, primitive words

       w=0123,    v=0321

and let F be the union of their periodic **3-block** sets. Both words have the same C_1: each of 0,1,2,3 occurs exactly once. Their periodic **2-block** supports, however, are

       supp C_2(w)={01,12,23,30};
       supp C_2(v)={03,32,21,10},

which are disjoint. Consequently the order-3 canonical higher-block graph is exactly two vertex-disjoint simple directed cycles, each of length four. Under the identity rule and target k=2, at N=4 the two sources have equal C_1 and different C_2, so **H_4(2)=2=m-1**.

For **m=4**, use alphabet A={0,1,2}, primitive words

       w=001021122,    v=002212011

and let F be the union of their periodic **4-block** sets. Both words have exactly the same C_2: every one of the nine ordered **two-symbol words** over this ternary alphabet occurs **once**. Their periodic **3-block** supports are respectively

       supp C_3(w)={001,010,102,021,211,112,122,220,200};
       supp C_3(v)={002,022,221,212,120,201,011,110,100},

which are disjoint. Each component traverses nine distinct length-3 vertices with indegree and outdegree one in their allowed union, so the recurrent graph is exactly two vertex-disjoint directed simple cycles. Under the identity rule, k=3, N=9, the two words have equal C_2 but unequal C_3; lower-h equality follows by prefix marginalization. Therefore **H_9(3)=3=m-1**.

These explicit examples show that replacing the general bound m-1 by m-2 is false for m=3 and m=4. They do **not** assert sharpness for every presentation order or a minimal-period result. All displayed set claims are literal finite combinatorial checks, not universal computational induction.

### 4.4 Why vertex-disjointness cannot be silently dropped

For m=2 and F={00,01,10}, the recurrent graph has a self-loop at vertex 0 and a two-edge 0->1->0 cycle **sharing vertex 0**. The length-three rooted cyclic source 001 has periodic windows {00,01,10} and is admissible. But it is neither a power/rotation of the one-cycle word 0 (which would give 000) nor a power/rotation of the two-cycle word 01 (whose period does not divide 3). It is a concatenation of the two returning walks. Thus the source classification, and hence this theorem's pair reduction, cannot be applied to branching/shared-vertex recurrent graphs.

### 4.5 Degenerate cases

- If the recurrent core has one simple cycle, X_N consists of one output-histogram class at every eligible N, hence H_N(k)=1 for every k, independent of the source-symbol histogram.
- Different active cycles can tie at some source order without restricting the horizon if their Q_(i,k) also tie; output-discrepant pairs alone govern (2).
- Source periods of 1 (self-loops), N<m, N<2r+1, any k including k larger than output length, and nonprimitive fixed-length powers are covered by cyclic indexing in (3)–(7).
- For m=1 there can be at most one recurrent simple-cycle component because there is only the empty-word vertex; the valid bound is b=1 rather than the meaningless histogram order zero.
- The bound m-1 is sharp for m=3 and m=4 in Section 4.3; no all-m sharpness theorem is asserted.
- As N grows by divisibility, H_N(k) cannot decrease; **no** monotonicity is implied for successive integers N and N+1.
- No assertion is made for an empty exact-N source domain; a vacuous 1 would change the statement's domain and must be declared as a separate convention.

## 5. Dependencies, evidence grade, limitations and handoff

**Premises imported from accepted STD work:** finite-type cyclic-word / canonical higher-block closed-walk conventions, raw periodic block counts, and the legality of dropping nonrecurrent edges. The proof of the special disjoint-cycle classification, emission covariance/scaling, exact horizon criterion, upper bound and divisibility period is given above; it does **not** import unrestricted-length support-pair rational scaling, PR #97 denominators, or any unresolved historical source.

**Evidence classification:** Sections 2–3 constitute an **author analytic proof**. Section 4 supplies explicit manually checkable counterexamples/fixtures. A bounded author-side Python 3.13.5 spot check confirmed the Section 4.1 m=4 F graph, the N=1..8 literal-domain sizes (0,2,0,6,0,2,0,6), the displayed variable-emission and radius-two outputs, plus the Section 4.3 m=3/m=4 pairwise (m-1)-vertex disjointness, shared (m-2)-histograms, distinct higher histograms, and degree-one graph checks. Separate literal rooted-word filtering over all 4^4 and 3^9 strings at N=4 and N=9 respectively admitted exactly 8 and 18 rooted sources and gave H_4(2)=2 and H_9(3)=3 under identity, matching the stated sharpness fixtures. This is **supporting finite computation only**, not an independent oracle, complete test suite, formal proof, or acceptance review. A distinct STD3-Engineering oracle (#108) and independent STD3-Audit mathematical review (#107) remain separate obligations.

**Limitations:** the recurrent core must be a union of vertex-disjoint *simple* cycles; branching graphs, overlapping cycles, rooted-output observables, erasing/possibly empty output, noncanonical duplicate-edge presentations, fixed inventory constraints other than length, and arbitrary non-finite-type source predicates are excluded. No claim is made about optimal computational complexity, a minimal period, or general unrestricted-length STD horizons.

**Review/integration gate:** freeze the exact committed head for STD3-Audit's independent nonauthor mathematical review when authorized. This revised analytic packet strengthens the bound and incorporates the independent Audit #107 preflight's possible (m-1)-vertex improvement; Audit has **not** yet reviewed this source, and author-side revisions do not count as nonauthor review. As of writing, historical PRs #98, #99, and #102 are pending distinct reviews, and #104/#106 prohibit opening a fourth substantive research PR until an integration slot opens. Only STD3-Lead may integrate or update consolidated accepted-state documentation. READY fallback for this worker: **none**. Next owner: **STD3-Audit** for independent proof review after the coordinator releases a review slot; **STD3-Lead** for review-slot scheduling and eventual integration.
