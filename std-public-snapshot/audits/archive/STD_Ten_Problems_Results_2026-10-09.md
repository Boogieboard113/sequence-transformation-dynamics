# STD: ten foundational problems, one forward-and-inverse framework

**Date:** October 9, 2026  
**Status:** Explicit definitions, self-contained derivations, and newly executed exact computations. No independent peer review, formal proof-assistant verification, or originality claim. Existing automata, linear-algebra, conservation-law, and information-theory results are identified as background rather than renamed as discoveries.

## Executive result

The work treats all ten requested problems, with different scopes made explicit. The main additions are an exact inverse-counting construction for arbitrary finite-radius contextual erasure, a finite-versus-infinite preimage test, a complete algorithm for rational additive invariants of any prescribed block order, and a minimum-counter theorem for forward prediction.

A concrete output-triple predictor that formerly retained 32 source counters needs exactly **four rational additive counters**, uniformly over all source lengths. A second result connects forward and backward questions: **every output has finitely many preimages across all source lengths exactly when the silent source graph is acyclic**. This property implies global statistical closure, but not reversibility.

The ten problems are not asserted solved for arbitrary programs, nonlocal rearrangements, every infinite alphabet, or every infinite-time question. In particular, the local-emission class is not closed under composition when the first transformation can erase arbitrarily long gaps.

## 0. The common setting and a necessary root convention

Let A and B be finite nonempty alphabets. A rule is an explicit table

    phi: A^(2r+1) -> B*,  r >= 0.

At source position i, evaluate phi on the original cyclic context X[i-r:i+r+1], with periodic wrapping, and emit its word. All positions update synchronously. Images may be empty, short, or variable-length. Empty output has zero block counts.

For a nonempty source word X, raw cyclic C_h(X) counts blocks starting at every position, including repeated wrapping when h exceeds |X|. The coordinate sum is |X|.

Forward closure uses cyclic histograms, so the cut is irrelevant. **Inverse counting is different:** its default source and output words are rooted. The output cut is immediately before the emission of source position zero, even if that emission is empty. No automatic quotient by rotation is performed. The software separately handles forgetting the output cut and, through Burnside's lemma, quotienting source rotations at a specified source length.

This distinction prevents counting the same periodic word multiple times, or mistakenly identifying genuinely different rooted inputs.

Encode phi as a de Bruijn graph G with vertices A^(2r) and one edge for each context c in A^(2r+1), from its prefix to its suffix of length 2r. The edge emits phi(c) and has input label equal to the center symbol c[r]. At r=0, G has one vertex and one edge per source symbol.

Rooted sources X of length n are in bijection with length-n closed walks in G, with a specified starting state and center-label word X. Even if n<2r, consistency of the closed walk forces the contexts to be the periodic contexts of X. Thus the emitted edge-label word is precisely the rooted T(X), not merely a rotation chosen afterwards.

Throughout, statements inherited from the earlier `STD_Global_Closure_Audit_2026-10-09.md` and `STD_Comprehensive_Advance_2026-10-09.md` retain those notes' self-contained-research status. This work does not claim to have independently peer-reviewed their entire proof packages.

## 1. Direct transformation: more than constructing the output

### 1.1 Evaluation and length

A direct implementation takes O(n(2r+1)+|T(X)|) operations using explicit context construction, hence O(n+|T(X)|) for a fixed rule. Materializing an output requires at least its number of symbol writes.

Length is a local additive statistic:

    |T(X)| = sum_c |phi(c)| C_(2r+1)(X)[c].

This holds with arbitrary contextual erasure.

### 1.2 Exact distribution of output lengths

Put a polynomial weight z^|phi(c)| on each source-graph edge, and let W(z) be the resulting adjacency matrix; sum weights for parallel edges. Then

    tr(W(z)^n) = sum_(X in A^n) z^|T(X)|.

**Proof.** Matrix multiplication enumerates length-n walks and multiplies their edge weights. Taking the trace selects closed walks. Each closed walk is one rooted source, and the exponent is the total emitted length. The closed-walk/source bijection proves exact counting, including short periods. QED.

The code computes coefficients by dynamic programming without symbolic polynomial expansion. This answers questions such as how many length-n inputs shrink to a specified output length.

### 1.3 Sharp expansion and contraction ratios

If lambda_min and lambda_max are the minimum and maximum mean emitted lengths over simple directed cycles of G, then for every source

    lambda_min |X| <= |T(X)| <= lambda_max |X|.

Every closed walk decomposes into directed cycles, so its mean is a weighted average of cycle means. Conversely, repeating a cycle attains its ratio. These extrema are rational and finitely computable. Their computation is a separate graph problem; it is not needed by the supplied inverse dynamic program.

### 1.4 Operations outside the main class

For a finite **linear** integer word, inserting each adjacent sum between its neighbors is exactly inverted by selecting positions 1,3,5,... in one-based numbering. A known positional permutation is inverted by the inverse permutation. These statements use their own boundary and positional conventions; they are not applications of the unrooted cyclic closure theorem.

Phase-labelled pair merging is treated in Section 6.4.

## 2. The inverse transformation problem

### 2.1 Exact inverse counting for a fixed rooted output

Fix Y=y_0...y_(m-1). Construct a product graph with states

    (v,j),  v in vertices(G),  0 <= j <= m.

For every source edge e:v->w with emitted word u, add a product edge

    (v,j) -> (w,j+|u|)

exactly when Y[j:j+|u|]=u and j+|u|<=m. Label it with the source center symbol of e. Empty images leave j unchanged; they are not omitted.

Let B_Y be the integer adjacency matrix, counting parallel edges. For positive n,

    N_n(Y) = #{X in A^n : T(X)=Y}
           = sum_v (B_Y^n)[(v,0),(v,m)].

**Proof.** A successful product path reads exactly Y and has a closed source-state projection. The source label is consequently a valid rooted cyclic input, and every such input supplies exactly one path and starting context. Each product edge consumes exactly one source position, including an empty-emission edge. QED.

Dynamic programming computes N_n(Y) and backtracking constructs an actual preimage. It can return zero, one, or many preimages at the specified length.

### 2.2 A rational inverse generating function

As a formal power series,

    F_Y(z) = sum_(n>=1) N_n(Y) z^n
           = sum_v ((I-z B_Y)^(-1))[(v,0),(v,m)]
             - |vertices(G)| * 1_(m=0).

The subtraction removes zero-length source paths when Y is empty. The domain excludes empty sources.

Thus every fixed-output preimage-count sequence satisfies an effectively obtainable integer linear recurrence, by the characteristic polynomial of B_Y. The code implements dynamic programming, not symbolic matrix inversion. It does not claim a logarithmic bit-time algorithm for printing an exponentially large count.

### 2.3 Is the all-length inverse fiber infinite?

For each source base v, retain product states reachable from (v,0) that can also reach (v,m). The inverse fiber is infinite exactly when one of these retained graphs contains a directed cycle.

**Proof.** A cycle on a successful path can be repeated, producing distinct source lengths with the same output. Conversely, arbitrarily long successful paths in a finite graph must repeat a state. Since output progress never decreases, every cycle is silent. If there is no such cycle, successful paths lie in a DAG and their total number is finitely computable. QED.

It matters that the start and finish have the **same source base**. Reachability from one base and returnability to another must not be mixed.

The supplied `inverse_status` returns empty, unique, finite_multiple, or infinite. A resource failure is not interpreted as infinity.

### 2.4 Rotation handling

To forget only the output cut, sum N_n(Z) over **distinct** rotations Z of Y. Inputs remain rooted.

To count source necklaces, use Burnside rather than dividing by n. A rotation by j fixes exactly words X=Z^(n/d), where d=gcd(n,j). Repetition of the source repeats the output, so

    necklace_count_n([Y])
      = (1/n) sum_(d|n) EulerPhi(n/d) N_d^cyclic(root_(n/d)(Y)).

A summand is zero if nonempty Y is not the required exact power. For Y empty, the root is empty. N_d^cyclic forgets the output cut but still counts rooted length-d inputs. The implementation verifies the final result is an integer.

### 2.5 Uniform injectivity

For one-symbol emission rules, form the synchronized pair graph G x G. Pair two edges only if they emit the same symbol. Mark a paired edge if its two input center symbols differ.

**Theorem.** The transformation is injective on rooted cyclic sources of every length if and only if no marked edge belongs to a directed cycle of the pair graph.

A marked edge on a closed walk supplies two unequal rooted inputs with the same output. Conversely, any collision supplies such a closed walk and must use a marked edge. This is an all-length test, not a bounded search.

The code performs this test and returns collision words for negative answers. For equal finite input/output alphabets, injectivity on each length also gives bijectivity on that length.

For arbitrary word emissions, a theoretical all-length rooted injectivity reduction is available: construct the finite transducer of closed source walks, storing the chosen starting context in its state, and exclude empty inputs. Its relation is exactly {(X,T(X))}. Swap input and output labels. The original transformation is injective precisely when this inverse transducer is functional. Functionality of finite transducers is an established decidable problem. The package implements the simpler synchronized-pair test for one-symbol images, **not** a general transducer-functionality engine. It does implement arbitrary-word-emission inverse counting and fixed-output uniqueness.

## 3. Statistical closure: forward information is a different question

For any summary S and output observable O,

    S(X)=S(Y) => O(TX)=O(TY)

holds exactly when O composed with T factors through S. This is statistical sufficiency, not reversibility.

For STD's block summaries, the condition is

    C_h(X)=C_h(Y) => C_k(TX)=C_k(TY).

The inherited additive rank theorem applies once

    C_k(TX)=F C_L(X)

has been established. With D_L the source incidence matrix and P_h the projection to shorter counts, sufficiency at h<=L is equivalent to

    rank([D_L;P_h]) = rank([D_L;P_h;F]).

A reconstruction identity is F=U D_L+G P_h. This is an exact rational linear-algebra test. The earlier general fixed-k theorem supplies a local representation or an infinity obstruction for finite-radius rules on the full cyclic family. These are inherited results, not newly rerun full classifications in this package.

Closure and reconstruction are complementary: closure asks what can be predicted from an input summary; the inverse asks what can be recovered from an output. One cannot substitute an answer to one question for an answer to the other.

## 4. The minimum horizon and the minimum number of counters

### 4.1 These are different optimization problems

The horizon minimizes the length of source patterns one must inspect. The number of retained counters minimizes the dimension of the summary after those patterns have been read. A rule may require length-5 source information but only four aggregate counters.

### 4.2 Minimum-counter theorem

Suppose Q(X)=F C_L(X) is a known rational additive observable. Allow summaries consisting of fixed rational linear combinations of C_L(X), with the same coefficients for **all source lengths**. Their minimum number is

    d_min = rank([D_L;F]) - rank(D_L).

If an existing summary A_0 C_L is already supplied, the minimum number of additional counters is

    rank([D_L;A_0;F]) - rank([D_L;A_0]).

**Proof.** Source histograms lie in the circulation space K=ker D_L. The displayed rank difference is the dimension of the output row functionals restricted to K. A basis of these functionals attains the bound. For the lower bound, if rational counters A C_L determine F C_L, then ker(D_L) intersect ker(A) is contained in ker(F). Otherwise multiply a rational separating vector to make it integral, add a sufficiently large positive integral circulation, and obtain two realizable positive histograms with equal summaries and different outputs. Thus F restricted to K factors through A restricted to K and cannot have larger rank. The same argument works with prescribed additional rows A_0. QED.

This is not a minimum-bit theorem, and it does not restrict arbitrary nonlinear integer encodings. At one bounded source length, coefficients depending on that bound could pack multiple counters into one integer. That is not the uniform rational-additive model of this theorem.

### 4.3 An exact four-counter predictor

Use alphabet {e,a}, erase every e-center, and emit

    eae -> 0, eaa -> 0, aae -> 0, aaa -> 1.

Retain only

    n_a = C_1(X)[a],
    p   = C_5(X)[eaaae],
    q   = C_5(X)[eaaaa],
    t   = C_5(X)[aaaaa].

Then, in output order 000,001,010,011,100,101,110,111,

    C_3(TX) = (n_a-3p-4q-t, p+q, p, q, p+q, 0, q, t).

A source run of m a's emits 0 for m=1, 00 for m=2, and 0 1^(m-2) 0 for m>=3. Counting triples in these runs and at their zero-to-zero joins proves the formula. All-a and all-e circles satisfy it with periodic wrapping.

Four is minimal: the output histograms of sources ea, eaaa, eaaaa, and a are linearly independent, supplying respectively independent 000,010,011,111 coordinates. The minimum-counter theorem supplies the lower bound uniformly over lengths.

The horizon is still exactly 5. The sources

    X=eaaaeaaaaa,  Y=eaaaaeaaaa

have equal C_4, but their outputs 01001110 and 01100110 have different 111 counts. The new exact rank calculation independently finds horizons 1,2,3,4 insufficient and 5 sufficient.

This reduces the counter count from 32 to 4, not the required input-pattern horizon. The four counters are nonnegative integers at most the source length; the reconstructed histogram is nonnegative on actual sources.

## 5. Global closure and a new forward/backward connection

### 5.1 Inherited global classification

The saved global theorem states that every output size has a finite horizon if and only if the silent source graph is acyclic, or all nonempty cyclic outputs follow one common periodic orbit. The all-erasing rule is a trivial constant case. It also provides a finite cutoff test bound and distinguishes constant finite spectra, unbounded all-finite spectra, and finite cutoffs.

This report uses that existing result with its explicit full-source scope. It does not represent those entire historical computations as newly executed.

### 5.2 Finite-preimage theorem

For the local rules considered here, the following are equivalent:

1. Every rooted output has finitely many source preimages across all positive lengths.
2. The empty output has only finitely many source preimages.
3. The silent source graph has no directed cycle.
4. There is a constant d such that |X|<=d |T(X)| for every source X.

**Proof.** If a silent cycle exists, take its source word U. Every U^j is nonempty, has a different length, and emits nothing. Therefore the empty fiber is infinite, disproving 1,2,4.

Conversely, if the silent graph is acyclic, let z be its longest path length. On every source circle there is a nonempty emission, and between successive nonempty emissions there are at most z silent centers. If p centers emit, then

    |X| <= (z+1)p <= (z+1)|T(X)|.

Thus d=z+1 works. A fixed output of length m has preimages only among the finitely many words of lengths at most dm. No nonempty source emits the empty word. QED.

This theorem is independent of the harder necessity direction of global closure. The same gap bound gives an additive formula for each output k-histogram, with

    H_T(k) <= (k-1)(z+1)+2r+1.

Hence all-output finite fibers imply global closure. The converse fails: mapping each 111 context to 01 and everything else to empty has completely predictable periodic outputs but infinitely many sources mapping to empty.

Injectivity across all positive source lengths also implies acyclic silence, and therefore global closure in this local cyclic class. It is not a theorem about arbitrary positional transformations: those may require an origin or phase data.

## 6. Information loss and reversible augmentation

### 6.1 Exact fiber ambiguity

Fix the input length n and assume the source is uniform on A^n. Conditional on observing Y, all N_n(Y) preimages are equally likely. Therefore, when N_n(Y)>0,

    H(X | T(X)=Y) = log_2 N_n(Y).

The average lost information is

    H(X | T(X)) = sum_Y (N_n(Y)/|A|^n) log_2 N_n(Y).

No probability distribution on unknown source lengths is silently introduced. An infinite all-length fiber is a counting fact; an entropy statement for that domain needs a specified probability law.

Conditional entropy and its deterministic-function interpretation are standard information theory, not an STD invention.

### 6.2 Minimal additional data for exact recovery

Suppose the output Y and source length n are known. Any fixed-length binary tag that makes recovery unique within that fiber requires at least

    ceil(log_2 N_n(Y))

bits. This is attainable in principle by assigning distinct indices to the preimages in a fixed order. A single tag length valid for every output requires

    ceil(log_2 max_Y N_n(Y)).

This is a zero-error counting theorem, not an efficient ranking/unranking algorithm. The output and n are side information; the tag is a separate component with known framing.

### 6.3 Deletion example

For 0->empty and 1->1, observing 1^m from a length-n source gives

    N_n(1^m)=binomial(n,m).

Choose the m surviving positions; every other position is zero. For m>=1,

    sum_(n>=1) N_n(1^m) z^n = z^m/(1-z)^(m+1).

For m=0, excluding the empty source gives z/(1-z).

At n=100,m=50 there are exactly

    100891344545564193334812497256

preimages, corresponding to approximately 96.34871716287934 conditional bits. A fiber-specific fixed-length tag needs 97 bits. The transformation's symbol statistics are simple, but this says almost nothing about recovering the original arrangement.

By contrast, rooted symbol duplication 0->00,1->11 has a unique preimage on its image and loses no source information, despite increasing length.

### 6.4 Phase-labelled merging

Let n be even and work over a finite field F_q. With a specified root and pairing phase, define

    Y_j = X_(2j)+X_(2j+1).

Each output coordinate has q input pairs, independently. Every output therefore has q^(n/2) preimages and loses (n/2) log_2(q) bits for uniform input. The total sum is conserved in F_q. After merging a length-2^s word down to its one total sum, each sum has q^(2^s-1) preimages.

This example belongs to a phase-labelled merging model, not the unlabelled local-emission setting. The code tests q=2,3,5 and lengths 2,4,6.

## 7. Repeated transformations and periodic points

### 7.1 General finite-state conclusions with explicit assumptions

A length-preserving rule T:A^n->A^n acts on |A|^n states. Every orbit is eventually periodic, with tail length plus cycle length at most |A|^n, by the pigeonhole principle. A cycle-finding algorithm determines the orbit for a specified input without storing all states.

If length never increases and T(empty)=empty, there are at most sum_(j=0)^n |A|^j available rooted states from a length-n start, so eventual periodicity still follows. Unbounded growth does not have this finite-state guarantee. If every active source position always emits at least two letters, length at least doubles on each iteration, ruling out any nonempty finite cycle.

For a one-symbol rule, fixed points are counted by the source graph retaining only edges for which emitted symbol equals input center. If its adjacency matrix is A_fix, the number of rooted length-n fixed points is tr(A_fix^n). For fixed t, T^t has finite radius at most tr, so the same construction counts points fixed by T^t. Exact period counts follow by divisor inversion.

These are fixed-rule/fixed-length algorithms, not a uniform small summary for all lengths and times. The earlier AND example H_(T^t)(1)=t+1 remains a counterexample to unconditional horizon stabilization.

### 7.2 Exact information dynamics for a binary local rule

Consider

    (F X)_i = X_i XOR X_(i+1).

Let n be the cyclic input length. Write n=2^s m with m odd. After t>=0 iterations,

    dim ker(F^t) = min(t,2^s).

Consequently every reachable rooted output has exactly

    2^min(t,2^s)

preimages of length n. For uniform input, the lost information is exactly min(t,2^s) bits.

**Proof.** Represent a binary source in the vector space F_2[z]/(z^n-1). Up to an invertible cyclic shift depending on the polynomial-index convention, F^t is multiplication by (1+z)^t. Multiplication by f modulo a monic polynomial P has kernel dimension deg gcd(f,P): if d=gcd(f,P), then P divides f x exactly when P/d divides x. In characteristic two,

    z^n-1 = (z^m-1)^(2^s),

and z=1 is a simple root of z^m-1 because m is odd. Thus the common-factor degree is min(t,2^s). A linear map has equal-sized fibers over its image, proving the count. QED.

For odd n, loss saturates at one bit. For n a power of two, F^n sends every input to all zeros. The growth in loss is not determined solely by the number of iterations; the arithmetic of the cycle length matters.

With the convention choosing the cyclic shift represented by z, the number fixed by F^t is

    2^deg gcd((1+z)^t-1, z^n-1).

Using the opposite shift convention gives the reciprocal operator; the fixed-point counts agree by reversal conjugacy. The code chooses a consistent convention and verifies the counts directly. If Fix(t) is the count fixed by F^t, the number of points of exact period t is sum_(d|t) mu(t/d) Fix(d).

## 8. Composition: exact laws and a limitation

### 8.1 Closure, fibers, and information

For compatible domains and empty-word conventions,

    H_(S composed T)(k) <= H_T(H_S(k))

whenever the right side is finite. This follows by chaining sufficiency.

For fixed source length n,

    N_(S composed T),n(Z) = sum_(Y:S(Y)=Z) N_T,n(Y).

Only finitely many intermediate Y arise from A^n, even when S has an infinite all-length fiber.

For any finite-entropy source distribution and deterministic Y=T(X), Z=S(Y),

    H(X|Z) = H(X|Y) + H(Y|Z).

The first term measures information lost at T, the second additional information lost at S using the actual induced intermediate distribution. This is the conditional-entropy chain rule, not a new entropy axiom.

### 8.2 Locality need not survive composition

Let T delete e and retain 0,1. Let

    (S Y)_i = Y_i AND Y_(i+1).

Then the number of ones in S(TX) is C_2(TX)[11]. For every h, pad 0011 and 0101 by e^h after each symbol. The padded inputs have equal C_h, but their final outputs have respectively one and zero ones.

Therefore

    H_(S composed T)(1)=infinity.

Every finite-radius local-emission rule has finite H(1), since its output symbol counts are local. Thus this composition has **no finite-radius local-emission representation** on the full cyclic source family.

This is a structural obstruction, not an inability to execute the composition.

### 8.3 A positive locality bound

Suppose the first rule T has radius r, emits at least one symbol somewhere on each source circle, and successive nonempty emissions are at distance at most d. If S has output-context radius s, group the S-emissions according to their starting symbol in each T-image. To evaluate that group requires at most s nonempty images on either side, whose centers lie within sd positions. Their T-contexts require r more positions.

Thus S composed T has a finite local-emission representation with radius at most

    r+sd.

In particular, when T is non-erasing, d=1 and the radius is at most r+s. Cyclic wrapping and short periods are interpreted as before.

For symbolwise morphisms on rooted words, commutation can be decided by checking S(T(a))=T(S(a)) for each source symbol a. For positional or cyclic-up-to-rotation equality, the equality convention must again be specified.

## 9. Invariant discovery

### 9.1 All symbol-additive invariants, including contextual erasure

Assume the same source and output alphabet. Seek weights lambda_a such that

    I_lambda(X)=sum_a lambda_a C_1(X)[a]

satisfies I_lambda(TX)=I_lambda(X). On each source context c define

    delta_lambda(c)=sum_a lambda_a N_a(phi(c))-lambda_(center(c)).

The invariant condition is exactly

    delta_lambda in rowspace(D_(2r+1)).

Equivalently, delta_lambda is a graph-potential difference on every edge. Its sum around each source cycle vanishes. The converse follows because cycles span the circulation space. This is a finite linear system in lambda and the potential.

The code computes the full rational solution space, rather than searching for a few named quantities.

### 9.2 Complete fixed-order invariants without assuming histogram closure

For prescribed h>=1, seek all rational c such that

    I_c(X)=c . C_h(X),
    I_c(TX)=I_c(X) for every source X.

This remains decidable even when H_T(h)=infinity. Cancellation in one scalar invariant can succeed while the full output vector is not finitely sufficient.

Choose a source guard s containing at least h output symbols protected against exterior contexts. If a context c0 has nonempty image, s=c0^h works. If everything erases, only identically zero cyclic observables are invariant.

Construct finite weighted representations of

    q_T(w)=C_h(T(s w s)),
    q_I(w)=C_h(s w s),

using the SAME source guard. Their direct-sum difference has a rational representation

    q_T(w)-q_I(w)=alpha M_w beta.

Compute the reachable row space

    R=span{alpha M_w : w in A*}.

It stabilizes by ordinary finite-dimensional reachability. Let E have rows r beta for a basis r of R. Then

    c is an invariant coefficient vector iff E c=0.

**Proof.** Invariance gives equality on every guarded word. Conversely, if equality holds on every guarded word, apply it to w=X^t. Inserting the fixed guards changes only a bounded number of source contexts, emitted symbols, and output h-blocks. Therefore

    I_c(T(sX^ts))-I_c(sX^ts)
      = t (I_c(TX)-I_c(X)) + O(1).

Divide by t. The guarded equality forces the invariant identity on every cyclic source. The reachable-space test is exactly equivalence of the two scalar weighted series for the unknown c. QED.

Coefficients in rowspace(D_h) describe identically zero cyclic sums, such as C_2[01]-C_2[10]. The software quotients these out. Reported dimensions count independent nonzero observables, not redundant descriptions.

This is a complete algorithm for a **specified finite order h**. It does not assert a finite list of invariants covering every possible block order at once; the identity preserves arbitrarily high-order information.

### 9.3 A transparent current law

For elementary traffic rule 184,

    T(X)_i = X_i + J(X_(i-1),X_i)-J(X_i,X_(i+1)),
    J(a,b)=a(1-b).

The current terms telescope on a circle, proving that the number of ones is conserved. The number of zeros is also conserved because length is fixed. This belongs to the established theory of additive conservation laws in cellular automata; the code reproduces it as a check.

### 9.4 Exact classifications completed

For all 3^8=6,561 binary radius-one rules with images in {empty,0,1}, the dimensions of the symbol-additive invariant spaces are:

| Dimension | Rules |
|---|---:|
| 0 | 6,142 |
| 1 | 414 |
| 2 | 5 |

The five dimension-two rules, in conventional elementary numbering, are 170,184,204,226,240.

For all 256 one-symbol-output elementary rules, the numbers of independent order-two additive invariants, after removing identically zero cyclic sums, are:

| Dimension | Rules |
|---|---:|
| 1 | 218 |
| 2 | 35 |
| 3 | 3 |

The three dimension-three rules are 170,204,240: two shifts and the identity. The six all-length rooted reversible elementary rules found by the separate pair-graph method are 15,51,85,170,204,240. The classical subclasses are validation benchmarks, not originality claims.

### 9.5 All invariants at a fixed finite length

For a length-preserving rule on A^n, every connected component of its directed functional graph contains one directed cycle with a basin of states feeding into it. A real-valued observable I satisfies I(TX)=I(X) on A^n exactly when it is constant on each such basin. Thus the space of **all** real-valued invariants on that finite state set has dimension equal to the number of cycle basins.

This is a complete characterization of arbitrary observables at that n, not just additive ones. It generally requires enumerating |A|^n states. The new finite-dynamics routine returns all cycles, basin sizes, and maximal transient length. It is distinct from a local formula valid uniformly over all n.

## 10. Prediction complexity and what 'efficient' means

The constructions distinguish four costs: compiling the rule, reading the source, retaining a summary, and answering later queries.

For a fixed rooted output of length m, the inverse product graph has at most

    |A|^(2r)(m+1)

states and at most (m+1)|A|^(2r+1) edges. Running an n-step dynamic program separately for each source base takes O(n |V| (m+1)|E|) arithmetic operations after graph construction. Integer counts can need O(n log |A|) bits, so arithmetic operations are not constant-cost bit operations.

For forward prediction, the four-counter example reduces retained counters by a factor of eight compared with its full 32-entry source histogram. It still needs source-window length 5. An initial exact pass must inspect the input; basic tasks such as counting ones have a worst-case linear inspection lower bound. No speedup is claimed for a constant observable that requires no input inspection, nor for all transformations indiscriminately.

The invariant algorithm is finite but its control state and observable dimension can grow exponentially with h and radius. An explicit resource limit reports that no classification was computed. The code never labels a memory limit as infinite horizon or infinite ambiguity.

The examples show concrete information and storage reductions. They are not a production-performance benchmark against optimized third-party libraries.

## 11. A useful warning about positional rules

Let a rooted length-four permutation swap the first two positions. This is invertible. The inputs

    X=0011,  Y=0110

are rotations, so every unlabelled cyclic C_h agrees. Their outputs are 0011 and 1010, whose pair histograms differ. Therefore no unlabelled cyclic input-block histogram suffices for those output pair counts.

There is no conflict with the implication from local injectivity to global closure: this fixed-origin permutation is not a rotation-equivariant finite-radius rule on the full unrooted cyclic family. Root and phase are part of the model, not information that block counts magically contain.

## 12. Computational record: checks actually run

Every listed computation was executed for this package. No historical regression totals have been added to these new totals.

### Core forward and inverse suite

- 4,536 directly transformed source words across 36 rules, including radii 0,1,2 and variable-length erasure.
- 216 complete output-length distributions matched against direct enumeration.
- 2,934 target inverse-count sequences through source length 6 matched direct enumeration.
- 2,934 actual inverse witnesses constructed and validated.
- 707 source-necklace fiber counts matched direct enumeration with rotation quotienting.
- 200 deletion/binomial identities and 26 exact finite all-length fiber totals checked.
- 130 XOR-iteration fiber/fixed-point cases, n=1,...,10 and t=0,...,12.
- 8,190 direct checks of the four-counter triple formula, covering every binary source of lengths 1,...,12.
- Exact rational minimum-counter value 4 and exact horizon 5 computed.
- 24 parameterized nonlocal-composition witness instances and 8 traffic-current local identities checked.

### Reversibility and symbol invariants

- All 256 elementary rules classified for all-length rooted injectivity, with 250 explicit collision certificates and 6 positive pair-graph results.
- All 6,561 ternary-output-choice rule tables classified for symbol-additive invariants.
- 26,288 additional direct invariant evaluations passed.

### General fixed-order invariants

- All 256 elementary rules classified at observable order 2.
- 37,422 direct checks of the returned invariant bases.
- 36 additional variable-length/context-erasing cases at orders 1 and 2, including radius 2.
- 558 direct checks in those erasing cases, plus guarded-model checks; order-1 results agree with the independent incidence method.
- Eight additional order-3 elementary-rule cases.
- Separator deletion at order 2 has exactly two nonzero additive invariants, although its complete output pair histogram has infinite horizon.

### Forward/backward graph connection

- All 6,561 rule tables checked: 2,432 have finite fibers for every output across all lengths; 4,129 have an infinite empty-output fiber.
- All 6,561 empty-fiber answers cross-checked with the target-product inverse algorithm.
- 72,960 direct checks of the source-length/output-length inequality in the acyclic-silence class.
- Nine phase-labelled pair-merging cases and 20 positional-permutation witness instances checked.
- Complete finite orbit decompositions for all 256 elementary rules at lengths 1 through 6: 1,536 cases, with 12,336 cycle edges verified and fixed-point counts checked directly.

Finite checks support the implementations. The all-length claims and complete fixed-order classifications rely on the finite graph/linear-algebra criteria proved above, not on extrapolating the direct checks.

## 13. Deliverables and execution

The package uses Python's standard library only. It includes:

- `std_core.py`: direct transformation, length distributions, inverse counting, fiber status, witness recovery, source-necklace counts, single-symbol injectivity, symbol invariants, rational ranks, four-counter prediction, XOR formulas, and complete finite orbit decompositions.
- `std_invariants.py`: the independent same-guard weighted-series method for all fixed-order additive invariants, including erasure.
- `std_analyze.py`: a command-line interface with validated full rule tables and explicit errors.
- Four reproducible test scripts, recorded JSON outputs, example rules, this report, and a SHA-256 manifest.

Examples:

    python3 std_analyze.py examples/delete_zero.json inverse 111 --max-n 8
    python3 std_analyze.py examples/traffic_184.json invariants 2
    python3 std_analyze.py examples/xor_102.json injectivity
    python3 std_analyze.py examples/bounded_erasure.json finite-fibers
    python3 std_analyze.py examples/traffic_184.json dynamics 6
    python3 test_std.py core
    python3 test_std.py classification
    python3 test_invariants.py
    python3 test_bridge.py
    python3 test_dynamics.py

The general inverse-transducer functionality reduction, symbolic generating-function inversion, and arbitrary-time symbolic classification of nonlinear growing rules are theoretical statements or explicit remaining scope boundaries, not features silently attributed to the executable package.

## 14. Sources and status

### Inherited STD sources

- `STD_Global_Closure_Audit_2026-10-09.md`: full-cyclic conventions, additive rank theorem, global closure graph criterion, and previously identified verifier limitation.
- `STD_Comprehensive_Advance_2026-10-09.md`: fixed-k protected-guard theorem, earlier 0001 formulas, and the AND iteration counterexample.

Their complete relevant text was read for this task. The four-counter reduction, inverse product-graph code, invariant code, and newly reported computational totals were developed or executed here.

### Established neighboring mathematics

- Mehryar Mohri, **Weighted Transducer Algorithms**, author-maintained reference page: https://cs.nyu.edu/~mohri/transducer-algorithms.html . Finite transducers, inversion, composition, and weighted algorithms are established tools.
- Stefan Kiefer, **Notes on Equivalence and Minimization of Weighted Automata**, arXiv:2009.01217: https://arxiv.org/abs/2009.01217 . The reachability/equivalence linear algebra is existing theory.
- **Approximate Problems for Finite Transducers**, ICALP 2025, article 155: https://drops.dagstuhl.de/storage/00lipics/lipics-vol334-icalp2025/html/LIPIcs.ICALP.2025.155/LIPIcs.ICALP.2025.155.html . Its introduction records the established decidability of finite-transducer functionality; the STD use requires the explicit closed-walk relation construction described above.
- Tetsuya Hattori and Shinji Takesue, **Additive conserved quantities in discrete-time lattice dynamical systems**, Physica D 49 (1991), 295-322, DOI 10.1016/0167-2789(91)90150-8. Existing necessary-and-sufficient local conservation-law methods.
- Nino Boccara and Henryk Fuks, **Number-conserving cellular automaton rules**, arXiv:adap-org/9905004: https://arxiv.org/abs/adap-org/9905004 . The number-conservation examples are not newly discovered classes.
- John C. Baez, Tobias Fritz, and Tom Leinster, **A Characterization of Entropy in Terms of Information Loss**, arXiv:1106.1791: https://arxiv.org/abs/1106.1791 . Deterministic information loss as conditional entropy and its compositional interpretation are established mathematics.

This is a focused comparison, not an exhaustive priority investigation. No proof is certified merely because a related paper exists.

## Bottom line

STD now has complementary exact treatments of forward sufficient statistics, inverse fibers, loss of information, and additive invariants. All ten foundational questions have concrete results within stated scopes. The central new relationship is that erased-run structure controls both finite-window prediction and finiteness of inverse fibers, while quantitative information loss and reversibility remain genuinely different questions.

What remains broader than this work includes arbitrary nonlocal programs, all source restrictions, a universal finite list of invariants across all orders, optimal bit encodings under unrestricted models, and complete symbolic long-time dynamics for arbitrary nonlinear length-changing rules.