# Adversarial reset-gap audit: scope erratum and exact horizon theorem

**Date:** 2026-10-11. **Research track:** B, audit/adversarial.
**Mathematical scope:** deterministic, integer-weighted binary finite-state closed runs; NOT an unrestricted STD transformation theorem.
**Proof status:** internally proved under explicit hypotheses, not peer-reviewed or formally verified.

**Provenance:** Reviewed README.md, AGENTS.md, docs/RESEARCH_STATE.md, docs/TASK_BOARD.md, Issue #1, and audits/archive/STD_Audit_2026-10-10.txt. Also inspected recent commits and open PRs (none at the start of this audit). The original reset-gap manuscript/program is NOT present in the repository; this note reconstructs the precise model needed for a valid result rather than claiming line-by-line verification of that absent source.

## 1. Precise weighted closed-run model

Fix a finite nonempty state set Q with distinguished state q0. From each q there are deterministic transitions a(q), b(q), with integer weights u(q), v(q), respectively. A closed run consists of a nonempty binary source word X and initial state s returning to s after X; its total weight is W(s,X). The source observable C_h(X) is the RAW cyclic h-block count with periodic wraparound, even when h>|X|. All arguments also apply coordinatewise to integer-vector weights.

Write O={a^n(q0):n>=0} for the a-orbit of q0. The orbit-reset hypothesis is b(q)=q0 for every q in O. The **free-gap orbit domain** D_O contains all b-containing closed runs entirely within O. Under these hypotheses every binary cyclic word containing b has one such closed run: after any b the state is q0, fixing all subsequent states including the rooted start state.

Let q_n=a^n(q0), and define the gap weight

    F(n)=v(q_n)+sum_{i=0}^{n-1} u(q_i),  n>=0.

For X=a^(n1)b ... a^(nr)b, with r>=1 and freely chosen nonnegative gaps, W(X)=sum_i F(ni). The horizon H(D) is the least h>=1 such that equal C_h on any two admissible runs implies equal weights, or infinity otherwise. For unrestricted multi-state closed-run domains, W need not be a function of the source word alone: that is an immediate obstruction to finite horizon. This statistic is **not automatically H_T(k)** for a word-valued transformation T.

## 2. Counterexample: the literal broad domain is false

Take Q={0,1}, q0=0:

| state | a next | a weight | b next | b weight |
|---|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 |

The q0 a-orbit is O={0}; the reset assumption holds on O, and F(n)=0 for every n. Thus the orbit theorem predicts H(D_O)=1. However the same one-letter source X=b gives two unrestricted closed runs, with respective weights 0 and 1. As the source word is identical, C_h agrees at **every** h, including h>|X|, while the weights differ. The horizon over **all** b-containing closed runs is infinity. This mechanism needs at least two states, and length one is the shortest nonempty source.

Required repair: either explicitly quantify only over b-containing closed runs within O, or impose **global reset** b(q)=q0 for every q and quantify over b-containing closed runs. Under global reset every b-bearing closed run is forced into O. Do NOT silently extend either conclusion to b-free runs.

**Classification:** FALSE under the broader literal hypothesis, reproducible with the two-state chart in tests/test_reset_gap_adversarial.py.

## 3. Exact affine-tail theorem

**Theorem A (verified internally).** Under the orbit reset assumption and the full free-gap b-containing domain D_O, define

    D2F(n)=F(n+2)-2F(n+1)+F(n).

For every integer h>=1, the following are equivalent:

1. Equal raw cyclic C_h implies equal W for all pairs of admissible runs.
2. D2F(n)=0 for every n>=h-1.

Therefore

    H(D_O)=min{h>=1: D2F(n)=0 for every n>=h-1},

with H=infinity if no such h exists. In particular H is finite iff F is *eventually affine*.

**Sufficiency proof.** If D2F(n)=0 for n>=h-1 then there are integers A,B with F(n)=An+B for all n>=h-1. Let N_j(X) count cyclic gaps containing exactly j a's between successive b's. For 0<=j<=h-2, raw cyclic counts give

    N_j(X)=C_(j+2)(X)[b a^j b].

This is still true for periods shorter than j+2 because wrapping is part of the definition. By marginalizing h-blocks, C_h determines every C_t for t<=h and hence all these N_j, as well as the numbers of a and b symbols. Now

    W(X)=A*(#a)+B*(#b)
          +sum_{j=0}^{h-2}(F(j)-Aj-B)*N_j(X).

Everything on the right is determined by C_h, proving sufficiency.

**Necessity proof and adversarial certificate.** If D2F(n) differs from zero for any n>=h-1, take the two valid free-gap sources

    X=b a^n b a^(n+2),
    Y=b a^(n+1) b a^(n+1).

They each have two b's, length 2n+4, and all gaps have at least h-1 a's. Thus an h-window contains at most one b. In both words each a^i b a^(h-1-i), for i=0,...,h-1, occurs exactly twice, and a^h occurs 2n+4-2h times; all other h-block counts vanish. Consequently C_h(X)=C_h(Y). But

    W(X)-W(Y)=F(n)+F(n+2)-2F(n+1)=D2F(n) != 0.

This supplies a finite, explicit counterexample to any insufficient proposed h. Both directions are independent of the October 10 archived assertion.

## 4. Exact finite-state criterion and bound

The finite a-orbit has a preperiod mu>=0 and period d>=1, with mu+d=|O|<=|Q|. Set q_n=a^n(q0). Direct subtraction yields

    DF(n)=F(n+1)-F(n)
         =u(q_n)+v(q_(n+1))-v(q_n).

For n>=mu, DF(n+d)=DF(n). Theorem A and periodicity imply:

- If DF(mu),...,DF(mu+d-1) are not all equal, H(D_O)=infinity.
- Otherwise D2F(n)=0 for all n>=mu. Define
  J={n:0<=n<mu and D2F(n)!=0}.
  If J is empty H(D_O)=1; otherwise H(D_O)=max(J)+2.

The finite-horizon bound follows: H<=mu+1<=|Q|. All calculations are exact integer operations; no sampling is used to decide infinity.

This is equivalent to the archived eventual-phase residual formulation F(n)=An+B_r: take A as the mean a-weight per step on the eventual a-cycle and demand equality of every eventual-phase B_r. Comparing residuals using inconsistent phase origins is invalid.

## 5. A second boundary defect: a-only cycles

**Theorem B (verified internally).** Suppose **every** b-transition globally resets to q0. Let D_all contain **all** nonempty closed runs, including b-free ones. For each a-cycle Gamma_i in the a-transition functional graph, let its length be ell_i and its total a-weight be U_i. Then

    H(D_all)=H(D_O)

if every pair i,j satisfies ell_j*U_i=ell_i*U_j; otherwise H(D_all)=infinity.

**Proof.** Global reset forces all b-bearing cycles into O; apply Theorem A. An a-only closed run of length L traces a directed a-cycle repeatedly and has weight L*U_i/ell_i. If mean weights differ, let L be a common multiple of ell_i and ell_j. Then the same input word a^L yields two closed runs with unequal weights, defeating every h. If mean weights all agree, a-only run weight is determined solely by L, which is already given by C_1. Moreover a-only and b-bearing input words cannot have identical C_h because their b-counts differ. Hence the b-bearing minimum is also the all-run minimum.

For example, choose a self-loops at both states, weights 0 and 1; choose both b-edges to reset to q0 with weight 0. The b-bearing orbit horizon is H=1 but the two a-only runs labelled a differ in weight, so H(D_all)=infinity. **Global b-reset alone is insufficient if a-only runs are in scope.**

## 6. Arbitrary source restrictions break the converse

Theorem A requires the full freely concatenable gap domain. On the restricted language with **exactly one b** per cycle, the word is a^n b up to rotation and its weight is F(n), determined by the a count in C_1; so H=1 even for non-affine F. For example, take two states, a swapping them with weights u=(0,1), and b resetting both to q0 with weights v=(0,0). Here F(n)=floor(n/2) has nonzero D2F(n) infinitely often; H on free-gap cycles is infinite, but H on one-b cycles is 1. Do not transfer the free-gap necessity to regular/sofic restrictions or finite-length populations without additional arguments.

## 7. Independently executed regression corpus

New code: audits/reset_gap_adversarial.py.
New tests: tests/test_reset_gap_adversarial.py.
Reproduce from the repository root:

    python -m unittest discover -s tests -v

The checker directly enumerates finite closed runs and computes raw cyclic histograms independently from std_tools/cyclic.py. Ten new tests passed in a local Python run. They cover the identical-source two-state defect; exact finite H=2 and H=3; long-gap periodic nonclosure certificates through h=8; source restriction to one b; exclusion of a-only cycles; and two exhaustive small-model surveys.

Surveys use every deterministic a-map, globally resetting b-map, and every assignment of weights 0 or 1 on a and b. Counts are **computed evidence**; the general theorems are proved separately.

| States | Charts | Orbit H=1 | Orbit H=2 | Orbit H=3 | Orbit infinite | All-run H=1 | All-run H=2 | All-run H=3 | All-run infinite |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 64 | 42 | 10 | 0 | 12 | 34 | 10 | 0 | 20 |
| 3 | 1728 | 852 | 292 | 80 | 504 | 588 | 252 | 80 | 808 |

For two-state charts, finite b-containing horizon predictions were compared with every closed run through length seven. For all 1,728 three-state charts, finite **all-run** predictions were compared with every closed run through length six. Failure to find a short collision alone is never called proof of infinity or sufficiency.

## 8. Status classification and limitations

- **FALSE:** Original all-b-containing-run claim when only q0-orbit b-edges are assumed to reset. Explicit two-state, one-letter counterexample.
- **VERIFIED UNDER EXPLICIT ASSUMPTIONS (internal proofs):** Exact affine-tail / second-difference criterion and finite-state H<=|Q| bound on freely concatenable b-containing orbit cycles.
- **VERIFIED UNDER EXPLICIT ASSUMPTIONS (internal proof):** Extension to every closed run under global b reset plus equal mean a-cycle weights.
- **COMPUTATIONALLY SUPPORTED ONLY:** The finite-size 64- and 1,728-chart census and bounded brute-force cross-checks.
- **UNRESOLVED / NOT COVERED:** The absent original reset-gap manuscript's exact wording, its original implementation, partial transition models, arbitrary sofic source languages, output-word statistics H_T(k), and general STD finite-radius nonlocal transformations.

The repository should not promote any broader reset-gap claim to verified status. Import the original October 10 note/program before a literal line-by-line audit. Another researcher should review these proofs independently before the coordinating chat merges them.
