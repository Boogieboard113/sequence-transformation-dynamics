# STD: optimal recovery, linear horizon growth, and current standing

**Date:** October 9, 2026.  
**Status:** Self-contained derivations, established-method applications, executable algorithms, and finite tests. This is not independent peer review, proof-assistant verification, or an established originality claim. “Solved” always refers to the specified mathematical class, not to every question expressible as a sequence transformation.

## Executive result

The newest contributions are:

1. An optimal fixed-width recovery record for any specified finite-radius local rule, fixed original length, and final output, with a constructive encoder and decoder that do not enumerate all possible originals.
2. A direct two-stage recovery construction, including cases where the composite is not itself a finite-radius rule. The saved record need not contain the intermediate sequence.
3. Exact all-length recovery when the complete target fiber is finite, with a decision distinguishing an infinite fiber from a computation limit.
4. Explicit table/recomputation memory tradeoffs, an online chunked deletion codec with a redundancy bound, and a precisely scoped memory lower bound.
5. A positive linear lower bound for every nonperiodic output family. Together with the preceding global theorem, this strengthens every unbounded all-finite horizon spectrum to **Theta(k)**.
6. An exact bounded-degree polynomial-invariant algorithm for substitution count maps, and a complete polynomial-invariant ring for the Fibonacci substitution counts.

The central current status is a connected research framework with proofs and tested tools for prediction, reconstruction, information loss, invariants, and composition in a sharply defined class. It is not a completed theory of arbitrary programs or all nonlocal operations.

## 1. Scope and evidence reviewed

The complete `STD_Ten_Problems_2026-10-09.md` and `STD_Global_Closure_Audit_2026-10-09.md` were read. Relevant source code from the ten-problem archive was inspected. The inherited global classifier was run again on all 6,561 binary radius-one rules as part of the new growth-witness suite. Earlier large fixed-k, reversibility, and invariant suites were **not** all rerun in this step; their recorded results remain inherited evidence.

Retain finite alphabets A,B and a complete synchronous rule

    phi: A^(2r+1) -> B*.

Every center reads its context from the original periodically extended source and emits a word, possibly empty. Closure uses every nonempty finite cyclic source, raw block counts, repeated wrapping on short periods, and zero counts for empty outputs.

    H_T(k) = min{h>=1: C_h(X)=C_h(Y) implies C_k(TX)=C_k(TY) for all sources}.

It is infinity when no finite horizon works. Raw cyclic counts recover source length, but not an origin or residue alignment.

Recovery retains an origin. The rooted output is the concatenation beginning at source position zero; initial empty emissions simply contribute nothing. T(empty)=empty. Rooted recovery is not necklace recovery.

For the primary coding theorem, the decoder is given the rule, original source length n, and complete transformed output y. Their storage is not counted as recovery payload. Later sections remove the known-length assumption when possible and charge for it otherwise.

## 2. Minimum recovery information

For n>=1 define the finite inverse fiber

    F_T(n,y) = {x in A^n: T(x)=y},    N_T(n,y)=|F_T(n,y)|.

If N=0, y is not an output of a source of this length. If N>0, the minimum binary record width, fixed within this fiber, is

    b_T(n,y) = ceil(log2 N_T(n,y)).

### Proof

A b-bit record distinguishes at most 2^b candidates. Exact recovery requires distinct records for distinct members of the same fiber, proving the lower bound. Enumerate the fiber in a fixed order and encode an index from 0 to N-1 in exactly ceil(log2 N) bits. This proves achievability. For N=1, the record is empty.

This counting/indexing principle is classical enumerative coding. Cover's 1973 paper gives ranking and inverse algorithms based on counts of completions. The STD-specific construction below supplies those counts for contextual, variable-length, cyclic transformations. It is not an invention of enumerative coding.

Every unused binary string representing an index >=N is rejected. This is not error correction or authentication: changing one valid record into another valid record need not be detectable.

### Actual example

For 0->empty and 1->1, with n=8 and y=111, the fiber size is binomial(8,3)=56. Six bits are optimal. The new lexicographic codec returns

    original: 00101001
    output:   111
    rank:     13
    record:   001101
    decoded:  00101001.

This is six **extra** bits. The output, rule, source length, and framing remain part of the decoder's side information.

## 3. Exact ranking without listing the originals

### 3.1 Output-matching automaton

The source de Bruijn graph has vertices A^(2r). An edge e of length 2r+1 runs from its prefix to its suffix, emits phi(e), and carries its **center source letter** e[r]. The center label is essential for the chosen root convention.

For target y of length m, matching states are

    (b,v,j),

where b is the initial source context, v the current context, and j the number of matched output symbols. An edge is permitted precisely when its emitted word matches y at j. It updates v and advances j by the emitted length. It consumes one original source symbol even when its output is empty.

Initial states are (b,b,0). Accepting states satisfy v=b and j=m. For every positive source length, accepting paths are in bijection with rooted source strings mapping to y. Periodic overlap determines the initial context even when n<2r; it must not be transmitted separately.

### 3.2 Completion counts

For a matching state s let D_t(s) count accepting paths using exactly t further original source symbols. Then

    D_0(s) = 1 if s is accepting, else 0,
    D_(t+1)(s) = sum_(s --a--> s') multiplicity(s,a,s') D_t(s').

The desired fiber cardinality is the sum of D_n over initial states.

Silent cycles cause no termination problem here because t decreases at every source transition. This is fixed original length, not a search over all lengths.

### 3.3 Lexicographic rank and inverse rank

Maintain the finite vector of partial matching paths compatible with the already selected source prefix. For each possible next source letter a, multiply those path counts by the appropriate completion counts. Their sum is exactly the number of fiber members beginning with that extended prefix.

To rank x, add the sizes of all smaller-letter branches before following x's actual next letter. To unrank an integer, locate the branch containing it, subtract preceding branch sizes, and continue.

At the end, exactly one complete accepting path remains. This is a check of the source/path bijection, not an assumption that the matching machine must be deterministic at every intermediate step.

This constructs

    decode(y,n,encode(x)) = x

with the optimal fixed-width payload. Source contexts and their phases are incorporated into the global rank; they are not extra hidden side information.

### Complexity

Let Q and E be the numbers of states and weighted transitions of the compiled matching machine. A full completion table takes O(nE) arithmetic operations and O(nQ) integer slots. Ranking or unranking uses O(nE) further arithmetic operations.

For a single local rule, before trimming Q is at most |A|^(4r)(m+1). The radius and alphabet dependence is substantial. Rule validation, output-word matching, graph construction, and input/output storage are separate costs.

Counts may be exponentially large in n; for a fixed rule they can require O(n) bits. Arithmetic-operation bounds and integer-slot bounds are not bit-complexity bounds.

## 4. Memory tradeoffs and streaming

### 4.1 Table versus recomputation

The supplied codec has two exact modes:

| Mode | Completion arithmetic | Completion storage |
|---|---:|---:|
| Full table | O(nE) | O(nQ) integer slots |
| Recompute layers when needed | O(n^2 E) | O(Q) integer slots |

The second mode repeatedly reconstructs suffix-completion layers. It is slower but retains fewer counts. The Python ranking API receives an input string; these figures describe additional completion storage, not a claim that the implementation never retains the source or target.

The optimal general rank normally depends on the final output y. A practical encoder must retain or reread the source after y is known, or use a different online code. Offline optimality does not automatically imply an online optimum.

### 4.2 A rigorous delayed-output memory obstruction

Consider a transformation erasing every binary input. Suppose an encoder reads the input once, cannot reread it, and is forbidden to emit any recovery bits before the input ends. For inputs of known length n, its final internal state must distinguish 2^n originals. It therefore needs at least n bits of distinguishable state.

This lower bound is specific to that delayed-output model. If recovery bits may be emitted as input arrives, the encoder can write each erased bit immediately and use small working memory. The theorem does not rule that out.

### 4.3 A genuinely streaming deletion codec

For 0->empty, 1->1, divide the source into blocks of size at most q. A block of length ell with t ones is represented by:

* t, using ceil(log2(ell+1)) header bits;
* its fixed-weight rank, using ceil(log2 binomial(ell,t)) bits.

A generator yields the transformed block and record as soon as that source block has been read. It buffers only one block. Original length and q are decoder metadata. Without the per-block count header, one cannot silently assume the decoder knows how to split the transformed stream.

For B=ceil(n/q) blocks and total m ones, the record length L satisfies

    L <= ceil(log2 binomial(n,m)) + B[ceil(log2(q+1))+1].

Proof: for the actual vector of block weights, product_i binomial(ell_i,t_i) is at most binomial(n,m). Taking logarithms bounds the sum of ideal rank lengths. Rounding costs less than one bit per block, and each header has at most ceil(log2(q+1)) bits.

Thus finite-memory streaming is available with an explicit redundancy budget. Exact offline optimum and bounded-memory online coding are separate objectives.

This adds a mathematically injective recovery interface; it does not make the implementation physically reversible. Bennett's time/space tradeoff results concern reversible computation with stronger machine-level requirements.

## 5. Unknown original length

Let F_T(y) be the union of inverse fibers over all finite source lengths, including empty when appropriate.

### Finite complete fibers

If F_T(y) is finite, source length need not be supplied separately. Rank the entire fiber in length-then-lexicographic order. The optimal fixed record width is

    ceil(log2 |F_T(y)|).

The matching automaton is trimmed to states reachable from an initial state and able to reach an accepting state with the same retained base context. A productive cycle means arbitrarily many source transitions can be added without changing y. Because the output position never decreases, that cycle is silent.

If there is no productive cycle, the productive graph is acyclic. Its longest accepting path bounds the source lengths; dynamic programming counts every length. The record identifies the length interval and then the word's rank within that interval.

Empty paths at different guessed source contexts are **not** counted as different empty sources. There is exactly one empty source when allowed. The implementation handles that separately.

Example: erase a center only at context 010 and otherwise emit the center. For target 0, the entire rooted fiber is {0,01,10}. Two bits suffice even with original length unknown.

### Infinite complete fibers

An infinite fiber cannot have a uniformly bounded binary recovery record: finitely many bounded-width records cannot distinguish infinitely many sources.

Each individual finite source can still be recovered using a variable-length record. For example, prepend a self-delimiting gamma code for n+1, followed by the optimal fixed-n payload. The length header uses

    2 floor(log2(n+1))+1

bits. This is a constructive upper bound, not a claim of global optimality among all variable-length schemes or all source priors.

The supplied all-length finite-fiber codec distinguishes `InfiniteFiber` from `ResourceLimit`. A failed computation cap never proves an infinite mathematical fiber.

## 6. Optimal recovery through composition

Let Y=T(X) and Z=S(Y), with original length n fixed. Define

    N_T(n,y)=|{x in A^n:T(x)=y}|.

Then

    N_(S o T)(n,z) = sum_(y:S(y)=z) N_T(n,y).

Only intermediate words reachable from length-n inputs contribute, so the sum is finite. It is a **weighted sum**, not a product of two unweighted inverse-fiber sizes.

Order the possible intermediate words and assign each y an interval of length N_T(n,y). Inside that interval use x's rank in T's y-fiber. This directly proves an optimal joint payload of

    ceil(log2 N_(S o T)(n,z)).

It need not save the intermediate sequence. Computing the record can still require intermediate information or working storage.

### Direct two-stage compiler

The implementation does not enumerate all intermediate words. Along each source transition of T, feed its emitted word through S's source-context graph, matching S's emissions against z. Retain both initial contexts, both current contexts, target position, and whether any intermediate symbol has been emitted.

Each original step advances the source-length counter. Summing over intermediate graph paths is safe because a complete nonempty intermediate rooted circle determines a unique cyclic source-context path for S. Empty intermediate words are handled once in a separate branch; otherwise arbitrary second-stage root guesses would overcount them.

The resulting finite matching machine is unambiguous on accepted original strings and uses the same rank/unrank algorithm. The construction works even if S o T is not itself a local rule. It is polynomial in n for a fixed compiled machine, but machine size and compilation cost can grow rapidly with rule radii, output labels, and number of stages.

The same finite-context idea extends mathematically to a fixed finite pipeline, with separate handling of the first stage whose full output is empty. The shipped direct compiler is for **two stages**, not an arbitrary-pipeline implementation.

### Why separate logs may waste bits

Let n=4, T delete zero, and S erase the surviving ones. The intermediate outputs empty,1,11,111,1111 have source-fiber sizes

    1,4,6,4,1.

The final fiber has size 16, so the optimal joint record has four bits. Separately recording the intermediate weight among five choices takes three bits, and an original of weight two needs three further rank bits: six bits in that staged format.

The identity for Shannon conditional entropy under deterministic composition remains additive. It does not imply that independently rounded worst-case binary record lengths add optimally.

### New contextual example actually run

Delete separators e and then XOR consecutive surviving bits. For original

    0e1ee0e1

the final output is 1111. At original length 8 there are exactly 140 originals over {0,1,e} producing this output. The joint codec uses eight bits and decodes exactly. It does not save the intermediate 0101 as part of the record.

## 7. Information loss and statistics

For uniformly random X in A^n, the posterior on each output fiber is uniform. Therefore

    H_Sh(X|Y,n)=E[log2 N_T(n,Y)].

The fixed-width-per-fiber record obeys

    H_Sh(X|Y,n) <= E[payload length] < H_Sh(X|Y,n)+1.

The output, source length, and rule are conditioned on. A Shannon entropy is not defined solely by saying a fiber is infinite; a prior must be specified.

If only a statistic R(X) must be recovered, rather than the whole source, replace fiber size by

    |{R(x):x in F_T(n,y)}|.

Its logarithm gives the corresponding fixed-width recovery bound. Counting distinct statistic values can be a different algorithmic problem from counting original strings.

The earlier additive reconstruction theorem remains useful: if source histogram c obeys Dc=0, retained data are Fc, and desired statistics Rc, exact recoverability on the full cyclic family is equivalent to

    rank([D;F;R])=rank([D;F]).

A conserved statistic I already satisfies I(X)=I(TX), so it needs no extra recovery bits. This is the connection between reconstruction and invariants; the complete string can remain ambiguous even when some desired statistics are recovered perfectly.

## 8. A stronger horizon-growth theorem

The preceding global theorem proved a trichotomy: a finite cutoff, a constant finite spectrum, or an unbounded all-finite spectrum with a linear upper bound. It explicitly did not establish a positive linear lower bound. The following argument supplies one.

### Theorem: every nonconstant all-finite spectrum is Theta(k)

For a finite-radius synchronous local emission rule on the full cyclic source family, if all horizons are finite and the output family is not one common periodic orbit, there are computable constants c,C>0 and k0 such that

    c k <= H_T(k) <= C k    for k>=k0.

Constants depend on the rule. This does not assert that H_T(k)/k has a limit or that H_T is eventually affine.

### 8.1 A word lemma

Let u,v be nonempty words with uv != vu. Put

    a=floor(|v|/|u|)+2,   m=h+a,   h>=1,
    W=u^(m+a) v u^(m-a) v,
    Z=(u^m v)^2,
    L=m|u|+|v|.

Both words have length 2L. Z is a square. W is **not** a square.

Proof: let p be u's primitive root and d=|p|. The initial u-run in W has length

    (m+a)|u| >= L+d.

Suppose W were a square. Its shift by L would agree with itself. Comparing the first d symbols with the d symbols starting at L occurs entirely inside that initial u-run. Thus p^infinity agrees with its shift by L for a whole primitive period. Distinct rotations of a primitive word are distinct, so d divides L, and consequently d divides |v|.

The first L symbols of W follow p^infinity. Because L is a multiple of d and W is a square, the entire word follows that same periodic sequence. The first occurrence of v begins at a multiple of |u| and hence at phase zero. Its length is a multiple of d, forcing v to be a power of p. Then u and v commute, a contradiction.

Rotation of a square is again a square. Hence W and Z are not cyclic rotations of one another. Their raw cyclic blocks of length 2L differ: such blocks are complete rotations of the words themselves. QED.

### 8.2 Realize the words as source transformations

For a nonperiodic output family, the preceding finite graph periodicity test supplies two return walks P,Q at one source-context vertex whose output labels are noncommuting u,v. They are nonempty and have finite lengths.

For every h>=1 form source walks

    X_h=P^(m+a) Q P^(m-a) Q,
    Y_h=(P^m Q)^2,
    m=h+a.

The shorter P-run has h copies and therefore source length at least h. A source h-block cannot meet both Q pieces. Each Q has the same surrounding periodic P fragments; the total number of P copies is 2m in each source. Therefore

    C_h(X_h)=C_h(Y_h).

This uses closed walks based at the same source context, so all neighborhood emissions are actually realizable. Read edge center letters for exact rooted alignment; rotations would not affect the histogram argument.

Outputs are W and Z from the word lemma. Consequently, at

    k_h=2|u|h + (2a|u|+2|v|),

    H_T(k_h)>h.

Set A0=2|u| and B0=2a|u|+2|v|. Monotonicity gives, for k>=A0+B0,

    H_T(k) >= floor((k-B0)/A0)+1.

This is a positive linear lower bound, with explicit witnesses.

### 8.3 Combine with the inherited upper bound

In the nonperiodic globally closed case, the earlier theorem forces the silent-edge graph to be acyclic. If z is its longest path length, the inherited upper bound is

    H_T(k) <= (k-1)(z+1)+2r+1.

Together, the two inequalities prove Theta(k).

The strengthened structural trichotomy is now:

| Type | Behavior |
|---|---|
| Finite cutoff | Finite through K_T, infinite afterward |
| Constant finite | H_T(k)=H_len for every k |
| Linear order | H_T(k)=Theta(k), every horizon finite |

No sublinear unbounded all-finite spectrum exists in this class. No claim is made for sorting, arbitrary positional rules, restricted source languages, or nonlocal programs.

### Completed checks

The word lemma was checked on 11,214 noncommuting word-pair/horizon instances. The new source construction was checked on all 6,036 nonperiodic rules among the 6,561 binary radius-one {empty,0,1}-emission rules, at h=1,2,5: 18,108 equal-input-histogram/unequal-output-histogram witnesses passed.

Of these rules, the inherited global certificate identifies 2,354 as all-finite. The new lower bound strengthens their classification from unbounded-at-most-linear to Theta(k). The numerical class counts are reproduced, not newly discovered counts.

## 9. Nonlinear invariants: a complete subclass and a degree-bounded algorithm

The prior additive invariant solver does not classify arbitrary nonlinear invariants. Nevertheless an important part of the nonlinear problem can be solved exactly.

For a symbolwise substitution with count matrix M,

    c(TX)=M c(X).

Fix degree d. List all monomials in c of total degree at most d. Substitute Mc into each and expand exactly. If Sym_(<=d)(M) is the resulting coefficient action, polynomial invariants are precisely the nullspace of

    Sym_(<=d)(M)-I.

There are binomial(s+d,d) monomials for s source symbols. This is a finite rational linear-algebra computation. The set of nonnegative integer count vectors over all source lengths is Zariski dense: a polynomial vanishing on all such vectors is identically zero, by repeated application of the elementary fact that a nonzero one-variable polynomial has only finitely many roots. Thus coefficient equality is both necessary and sufficient.

This covers polynomial statistics of a proved closed count map. It is not a solver for every nonlinear invariant on arbitrary sequence spaces.

### Complete invariant ring for Fibonacci substitution counts

For 0->01 and 1->0,

    (a,b) -> (a+b,a).

Let

    Q(a,b)=a^2-ab-b^2.

Then Q changes sign, so every polynomial in Q^2 is invariant. Conversely, these are **all** rational polynomial invariants:

    Q[a,b]^(M) = Q[(a^2-ab-b^2)^2].

Proof: over R the matrix has eigenvalues phi=(1+sqrt(5))/2 and -1/phi, and independent eigen-coordinates. A monomial with exponents i,j has eigenvalue (-1)^j phi^(i-j). It equals 1 exactly when i=j and j is even. Their product is proportional to Q, so every invariant polynomial is a polynomial in Q^2. If the original polynomial has rational coefficients, comparison of its highest-degree pure-a term, followed by descent in degree, forces the coefficients of that polynomial in Q^2 to be rational.

For degree at most d the dimension is therefore floor(d/4)+1, including constants. The exact solver independently matches this dimension for every d=0,...,12 and its bases pass 1,372 direct rational evaluations.

This solves the entire polynomial-invariant ring for one important expanding example, not every possible word-level invariant of that substitution.

## 10. All ten foundational problems: status register

| Problem | Current result | Important remaining boundary |
|---|---|---|
| Forward transformation | Exact local evaluation and output-length formula; substitution count matrices; exact adjacent-sum insertion growth | No universal fast shortcut for every requested output |
| Inverse transformation | Inverse graph; fixed-/all-length counts; local-rule injectivity and surjectivity reductions; now optimal constructive recovery records | Rooted and rotation-quotiented recovery differ; unrestricted programs have undecidability obstructions |
| Statistical closure | Additive rank criterion; inherited fixed-k decision; exact reverse recovery criterion | Depends on explicit domain and observable hypotheses |
| Minimum horizon | Exact finite minimum through local-table/rank machinery; finite/infinite certificates | Expanding all tables can be expensive; exact asymptotic coefficients not determined generally |
| Global closure | Inherited silent-cycle/common-periodic criterion; computable cutoff; now constant/Theta(k)/cutoff trichotomy | Full-cyclic local-rule scope, not arbitrary nonlocal transformations |
| Information loss | Fiber counts, conditional entropy, exact minimum side records, finite/infinite unknown-length distinction | No prior-free Shannon entropy; optimum payload not optimum total metadata or runtime |
| Repeated transformation | Finite-universe attractors and minimal predictive partitions; substitution count powers; AND lower-bound example | General expanding dynamics not classified uniformly in time/size |
| Composition | Inherited downstream-locality criterion; now direct optimal two-stage recovery even for nonlocal composites | Full arbitrary-pipeline compiler not shipped; individual locality remains a separate problem |
| Invariants | Fixed-k additive solver; finite-universe invariants; now bounded-degree polynomial solver and a complete invariant ring | Arbitrary nonlinear invariants of arbitrary expanding rules are not classified |
| Prediction/complexity | Minimal rational counter dimension, exact bit minimum, table/recompute tradeoff, bounded-memory chunk code | No unproved broad speedup or universal constant-memory optimum |

All rows have substantive results. Their scope boundaries are not erased by calling the ten headings “solved.”

## 11. Why an unrestricted all-programs solver cannot exist

This is a decidability boundary, not an appeal to an unsolved problem.

Given any program P, define the total computable string transformation

    T_P(x) = 1 if P halts within |x| steps, else 0.

Every individual forward computation terminates: it performs a bounded simulation. There exists any source mapping to 1 exactly when P eventually halts. Therefore a universal algorithm deciding inverse existence for arbitrary total computable sequence transformations would decide the halting problem.

Classical computability theory rules this out. Individual cases, restricted subclasses, and bounded-source-length recovery remain tractable. The finite local-table restriction is a meaningful mathematical condition, not an arbitrary inconvenience.

## 12. Newly completed computational evidence

The following were actually completed in this step:

| Suite | Completed outcome |
|---|---:|
| All 6,561 binary radius-one rules, n=1,...,4 | 112,674 fibers counted; 196,830 exact lexicographic optimal-width round trips |
| 120 seeded varied alphabet/radius/image-length rules | 9,835 fibers; 15,012 round trips |
| Recompute-memory mode vs table mode | 1,495 round trips agree |
| Longer selected inputs at n=16,32,80 | 15 round trips |
| Two-stage rules, including nonlocal composition | 80 pairs; 1,905 final fibers; 5,261 joint round trips |
| Unknown source length, finite complete fibers | 155 target problems; 152 round trips |
| Unknown source length, productive silent cycles | 3 infinite fibers correctly detected |
| Fixed-weight combinatorial index | 4,094 round trips |
| Chunk-streaming format | 16,376 round trips and redundancy checks |
| New horizon-growth word lemma | 11,214 instances |
| New source-histogram horizon witnesses | 18,108 instances on all 6,036 nonperiodic small rules |
| Polynomial invariant spaces | Exact degrees 0 through 12; 1,372 basis evaluations |
| Invalid records/ranks | 10 deliberately invalid records/ranks rejected |
| Other edge checks | Impossible fixed-length target and separate resource-limit outcome checked |

These numbers are not confidence percentages. Proofs justify general claims; finite exhaustive/random tests check implementations and catch errors. No exhaustive test over unbounded source lengths was performed or claimed.

## 13. Where STD stands

The strongest supported description is:

> An internally developed, mathematically explicit research framework for statistical sufficiency and information flow under finite-state sequence transformations, with constructive algorithms and reproducible examples.

The full-source cyclic local branch now connects closure, inverse ambiguity, minimum recovery records, invariants, composition and spectrum growth. This is considerably more than a collection of ad hoc sequence experiments.

Three distinctions remain necessary:

* **Proof versus validation:** the project contains derivations and executable checks, not independent peer review or formal verification.
* **Integration versus novelty:** enumerative coding, de Bruijn methods, weighted automata, transfer matrices, invariant linear algebra and entropy identities are established mathematics. The particular STD combinations and new lower-bound argument require a focused priority comparison before claiming novelty.
* **A theory for a class versus a theory of everything:** arbitrary algorithms, all restricted languages, all nonlocal rearrangements, arbitrary nonlinear invariants and all infinite dynamical limits are not covered.

The most valuable next consolidation is a short canonical manuscript containing the precise closure theorem, the Theta(k) refinement, and the optimal recovery construction, with independently checked implementations. Further theorem targets include exact asymptotic horizon coefficients, more efficient minimum-horizon computation, rotation-quotiented recovery and broader constrained source families.

## 14. Reproducibility and literature

See the accompanying README and scripts. The new recovery compiler uses only the standard library. `std_global_closure.py` is an unchanged inherited implementation; this provenance is not concealed. The polynomial solver uses exact Fraction arithmetic. Metadata and framing are explicitly excluded from payload-optimality statements and charged when introduced.

Established primary sources consulted:

1. T. M. Cover, *Enumerative Source Encoding*, IEEE Transactions on Information Theory 19(1), 73–77 (1973), DOI 10.1109/TIT.1973.1054929. Primary author-hosted scan: https://isl.stanford.edu/~cover/papers/transIT/0073cove.pdf
2. C. H. Bennett, *Time/Space Trade-Offs for Reversible Computation*, SIAM Journal on Computing (1989). Author institution summary: https://research.ibm.com/publications/timespace-trade-offs-for-reversible-computation
3. S. Kiefer, *Notes on Equivalence and Minimization of Weighted Automata* (2020), https://arxiv.org/abs/2009.01217
4. J. Karhumaki, S. Puzynina, M. Rao, M. A. Whiteland, *On Cardinalities of k-Abelian Equivalence Classes* (2016), https://arxiv.org/abs/1605.03319
5. MIT OpenCourseWare, 6.441 Information Theory, conditional entropy and source coding lecture notes: https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/pages/lecture-notes/
6. A. M. Turing, *On Computable Numbers, with an Application to the Entscheidungsproblem*, Proceedings of the London Mathematical Society. Primary publication DOI: https://doi.org/10.1112/plms/s2-42.1.230. The bounded-simulation inverse reduction above is given explicitly rather than attributed verbatim to that paper.

Prior project sources are the supplied ten-problem and global-closure reports. The new results are not attributed to the literature sources merely because related machinery appears there.