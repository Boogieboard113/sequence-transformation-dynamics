# Independent audit: linear lower bound for nonconstant all-finite horizon spectra

**Date:** 2026-10-11  
**Researcher:** B, adversarial audit  
**Task:** issue #29  
**Pinned main:** `private-history-omitted`  
**Primary proof source:** `audits/archive/STD_Recovery_Spectrum_Status_2026-10-09.md`, blob `private-history-omitted`, Section 8  
**Inherited dependency:** `audits/archive/STD_Global_Closure_Audit_2026-10-09.md`, blob `private-history-omitted`

This current chat/session did not author the pinned October 9 proof source. The review below is an **internal nonauthor mathematical audit**, not external peer review or formal verification.

## Verdict

**SOUND UNDER THE STATED HYPOTHESES.**

For a complete finite-radius synchronous local emission rule on the full family of all nonempty finite cyclic sources, with raw periodic block counts, the October 9 theorem is correct:

> If every output order has a finite source horizon and the output family is not one common periodic orbit, then there are computable constants c,C > 0 and k0 such that
>
>     c k <= H_T(k) <= C k
>
> for all k >= k0.

Equivalently within this scoped model, every all-finite horizon spectrum is either constant or Theta(k). No mathematical correction is required. Two proof bridges that were terse in the archived note are expanded below.

## 1. Nonperiodic outputs really give two noncommuting same-base return words

The main potential dependency gap is that the older global-closure proof used a silent cycle only later, for its infinite-horizon padding construction. The **finite phase test itself does not require a silent cycle**.

Fix any source-context vertex q in the full de Bruijn graph. Section 5 of the global-closure source chooses finite paths from q to every vertex and back, and constructs finitely many closed test walks at q. Unless the rule is all-erasing, choose a nonempty test output u, let p be its primitive root, and test whether every test output lies in p*.

The source proves:

1. if all tests lie in p*, a graph phase assignment exists;
2. that phase assignment forces every closed walk to emit a power of the appropriate rotation of p;
3. consequently every cyclic transformed output lies on one common periodic orbit.

Therefore, by contrapositive, if the output family is **not** one common periodic orbit, the phase test fails. A failed test supplies a closed return walk Q at the same q whose nonempty output v is not in p*. If u and v commuted, the elementary word commutation theorem would force them to have the same primitive root, hence v would belong to p*, contradiction. Thus

    u v != v u.

Both u and v are outputs of finite nonempty return walks P,Q based at the same source context q.

This conclusion does not use a silent cycle. The silent-cycle hypothesis was required only by the older theorem's separate neutral-padding argument for proving an **infinite** horizon.

## 2. The noncommuting-word square lemma is correct

Let u,v be nonempty and noncommuting. For h >= 1 define

    a = floor(|v| / |u|) + 2
    m = h + a
    W = u^(m+a) v u^(m-a) v
    Z = (u^m v)^2
    L = m |u| + |v|.

Then |W| = |Z| = 2L and Z is a square.

Let p be the primitive root of u and d = |p|. The choice of a gives

    a |u| - |v| >= d,

indeed it is strictly larger than |u|. Hence the first L+d symbols of W lie inside its initial u-run.

Assume W were a square. Equality with its shift by L would make p-infinity agree with its L-shift over a full primitive period. Distinct rotations of a primitive word are distinct, so d divides L. Since d divides |u|, it follows that d divides |v|.

The first L symbols of W are p-periodic. If W is a square, its second half equals its first, so all of W follows the same p-periodic sequence. The first v starts at a multiple of |u| and therefore at phase zero of p; its length is a multiple of d. Hence v is a power of p. That makes u and v commute, contradiction. Thus W is not a square.

Every cyclic rotation of a square is again a square, so W and Z are not cyclic rotations of one another. For equal-length words of length 2L, equality of raw cyclic 2L-block histograms is equivalent to having the same multiset of complete rotations; in particular it would force W to be a rotation of Z. Therefore

    C_(2L)(W) != C_(2L)(Z).

No hidden primitivity, parity, or alphabet-size assumption is used.

## 3. The source-histogram identity is exact for every h

Let p and q now denote the finite **source words** read from the return walks P and Q. They are nonempty. The theorem constructs

    X_h = p^(m+a) q p^(m-a) q
    Y_h = (p^m q)^2,

with m = h+a. The short p-run in X_h has exactly h copies, so it contains at least h source symbols. Every p-run separating the two q-islands in either cyclic word therefore contains at least h source symbols.

A clean way to formalize the archived proof is an insertion-defect argument.

Start with the cyclic periodic background p^(2m). Insert q twice, always at a boundary between complete p copies. Inserting one q can change an h-block only when that block starts inside q or within the preceding h-1 source positions. Because the adjacent background consists of complete p copies, the multiset of changed/new h-blocks is a fixed local defect depending only on (p,q,h), not on which p-copy boundary was chosen.

When two q insertions are separated in both cyclic directions by at least h background source symbols, their affected start-position sets are disjoint, so the two identical local defects add independently.

Both X_h and Y_h:

- start from the same p^(2m) background count;
- insert exactly two copies of q at p-copy boundaries;
- keep the two insertion neighborhoods at least h source symbols apart.

Therefore they acquire exactly twice the same insertion defect and

    C_h(X_h) = C_h(Y_h).

This proof also covers source periods shorter than local-rule context windows, because P and Q are actual closed walks at one source-context vertex and their concatenations are valid periodic source walks.

## 4. The output discrepancy gives a linear sequence of lower-bound witnesses

Because P and Q are closed at the same context q, their output labels concatenate without introducing an invalid local-rule join. Up to an irrelevant cyclic cut, the transformed outputs of X_h and Y_h are exactly W and Z from Section 2.

Set

    k_h = 2L
        = 2 |u| h + (2 a |u| + 2 |v|).

The preceding sections give

    C_h(X_h) = C_h(Y_h)
    C_(k_h)(T X_h) != C_(k_h)(T Y_h).

Raw cyclic source histograms marginalize downward: equality of C_h implies equality of every C_j for j <= h. Hence no horizon j <= h can predict the k_h-output histogram, so

    H_T(k_h) > h.

Write

    A = 2 |u| > 0
    B = 2 a |u| + 2 |v|.

Then k_h = A h + B.

## 5. Monotonicity interpolates the sparse witnesses to every large k

Raw cyclic output histograms also marginalize downward, so predicting order k+1 predicts order k. Therefore

    H_T(k+1) >= H_T(k).

For any k >= A+B, choose

    h = floor((k-B)/A) >= 1.

Then k_h <= k, and monotonicity gives

    H_T(k) >= H_T(k_h) > h,

hence

    H_T(k) >= floor((k-B)/A) + 1.

For example, once k >= max(A+B, 2B),

    H_T(k) >= k/(2A).

Thus one may take the explicit computable lower constant c = 1/(2A) after a computable threshold.

## 6. The inherited upper bound applies in exactly this branch

Assume all H_T(k) are finite and the output family is not one common periodic orbit.

If the silent-edge graph contained a directed cycle, the global-closure theorem says all horizons could be finite only when the periodic phase condition holds. But that phase condition forces all cyclic outputs onto one common periodic orbit, contrary to the hypothesis.

Therefore the silent-edge graph is acyclic. Let z be its longest directed silent path length. The inherited bounded-silence argument gives

    H_T(k) <= (k-1)(z+1) + 2r + 1.

This is at most C k for a computable positive constant, for example

    C = z + 2r + 2

for every k >= 1.

Together with Section 5 this proves Theta(k).

## 7. Why the theorem title matches the stated hypothesis

If all nonempty cyclic outputs lie on one common periodic orbit, their raw block histograms are determined by output length, and the global proof gives the same finite source horizon H_len for every output order. The all-erasing rule is the trivial constant case.

If the output family is not one common periodic orbit and every horizon is finite, Sections 1-6 force an unbounded Theta(k) spectrum.

Thus, within this model, “all-finite but nonconstant” and the nonperiodic branch used by the theorem have the required relationship. The resulting structural trichotomy is:

- finite cutoff;
- constant all-finite;
- Theta(k) all-finite.

The theorem does **not** claim eventual affinity or existence of a limit H_T(k)/k.

## 8. Independent finite counterexample search

The companion standard-library script

    python audits/2026-10-11/check_horizon_growth_theta.py

does not import repository theorem/production code.

It checks:

1. **Word lemma:** all 3,738 noncommuting pairs of nonempty binary words of lengths 1 through 5, for h=1 through 6: **22,428 instances, zero failures**.
2. **Source insertion lemma:** all 900 ordered pairs of nonempty binary source words of lengths 1 through 4, for h=1 through 6 and a=1 through 5: **27,000 instances, zero failures**.
3. **Binary radius-one rule family:** all 3^8 = **6,561** rules with per-context emissions in {empty,0,1}, using an independently implemented de Bruijn graph, finite phase test, silent-cycle test, and P/Q construction.

The third check returns:

    phase-test pass                         525
    phase-test fail / nonperiodic          6,036
    acyclic silent graph                   2,432
    all-finite by the graph criterion      2,879
    nonperiodic all-finite                 2,354
    P/Q witnesses checked                  18,108

All 18,108 source-histogram equalities and output-histogram discrepancies pass for h in {1,2,5}. The 6,036 and 2,354 counts independently match the archived report.

These computations are supporting counterexample searches only. In particular, the label “all-finite by the graph criterion” uses the audited global graph theorem as a classifier; the finite census is not a proof over unbounded source lengths or arbitrary alphabets/radii.

## 9. Failure-mode separation and scope

- **Theorem:** no gap found. The same-base noncommuting-return bridge, word lemma, source-histogram construction, monotonic interpolation, and bounded-silence upper bound are all sound.
- **Arithmetic:** the proof is integer/combinatorial. The independent checker uses Python exact integers and Counters only.
- **Algorithm/evidence:** the finite checker is an independent small-case oracle, not a universal decision proof.
- **Scope:** full nonempty finite cyclic source family of arbitrary positive lengths; complete finite-radius synchronous local emissions; raw periodic block counts. No result here is asserted for restricted source languages, fixed-length-only domains, rooted output statistics, sorting/positional rules, or arbitrary nonlocal programs.

## Required correction

**None.**

A documentation strengthening would be useful, but is not mathematically required: the archived Section 8.2 sentence about the two Q neighborhoods can be expanded using the insertion-defect argument in Section 3 above, and the text can explicitly note that the finite phase test supplies noncommuting returns without any silent-cycle assumption. Those clarifications make the dependency structure easier to audit but do not change the theorem.
