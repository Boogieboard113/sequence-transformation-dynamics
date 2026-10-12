# STD audit and useful bounds for interval defects

October 9, 2026

The audited finite-period prime-sieve results remain valid within their stated scope. The interval problem now has explicit uniform bounds, efficiently computed finite certificates, sharp certificates for small moduli, exact second-moment identities, and a growing-depth relative-error result obtained from established sieve theory. A square-root-cutoff counterexample proves that uniformly negligible relative error at every deletion step is an impossible target there.

No new bound on the distribution of actual primes, twin-prime theorem, or originality claim is established. The self-contained arguments below have been checked mathematically and computationally, but have not received independent review or proof-assistant verification.

## 1. Audit result

The current `STD_50_Prime_Problems_2026-10-09.md` was read in full. Its proof arguments and companion program were reviewed, and its 8,859 recorded exact comparisons were rerun successfully. This audit covers the latest prime branch and its use of the earlier closure framework. It is not a fresh proof-by-proof certification of every historical STD research package.

| Claim | Audit finding |
|---|---|
| Complete-period window update \(B_{qM}=K_qB_M\) | Valid. Coprimality \(q\nmid M\), lifting to the full period, and counting every starting residue are essential. |
| Diagonal update of constellation correlations | Valid by CRT and the invertible subset-summation transform. |
| Exact gap counts by inclusion-exclusion | Valid, including periodically extended windows, with the stated consecutive-gap convention. |
| Driving-term recurrence | Valid under its span restriction \(g<2q\) and even old modulus. It cannot be applied at equality without extra terms. |
| Fixed-gap wheel limits and singular-series convergence | The arguments survive. These are finite-sieve limits with substantial prior literature. |
| Erasure and external-phase counterexamples | Valid. They prevent an extension of the closure claims to arbitrary source families or fixed external alignments. |
| Interval defect identity | Valid, including its sign and telescoping weights. The previous report supplied an identity, not a useful general error bound. |
| Prime-indicator zero entropy | The given subword-complexity argument survives. Zero entropy does not provide a prime-counting error estimate. |
| Originality or prime-distribution breakthrough | Neither is established. |

An explicit boundary check reinforces the driving-term restriction. With old modulus 30, new prime 7, and span 14, applying the restricted recurrence incorrectly predicts 9 length-3 drivers and 4 length-4 drivers. Direct counts are 10 and 6. This is not a counterexample to the stated theorem; it is a counterexample to omitting its strict inequality.

Two qualifications matter for the next phase:

* A small error relative to the **current survivor count** is weaker than a small error relative to the **number expected to be deleted at this one step**. The latter scale is smaller by approximately \(q/|H|\).
* Mean-square bounds over uniformly sampled CRT phases are not pointwise bounds for the particular initial interval \([1,X]\).

The previous verifier uses Python `assert`, so its checks require an ordinary, nonoptimized invocation. The new verification guards raise explicitly and remain active under Python optimization. Neither program is a general formal theorem verifier.

## 2. Definitions and signs

Let \(H\) be a finite nonempty set of distinct integer offsets. For integer \(t\) and integer \(L\ge0\), write

\[
I_{t,L}=\{t+1,\ldots,t+L\}.
\]

Let \(M\) be a squarefree product of previously sieved primes, and let \(q\nmid M\) be a new prime. Put

\[
f_M(n)=\prod_{h\in H}\mathbf1_{\gcd(n+h,M)=1},
\qquad A_M(t,L)=\sum_{n\in I_{t,L}}f_M(n).
\]

For each prime \(p\), let \(F_p=-H\bmod p\) and \(\nu_p=|F_p|\). Define

\[
N_M=\prod_{p\mid M}(p-\nu_p),\qquad
V_M=\frac{N_M}{M}=\prod_{p\mid M}(1-\nu_p/p),
\qquad \mathcal W_M=\prod_{p\mid M}(1+\nu_p).
\]

Empty products are 1. The full-period expected count is \(LV_M\); the signed interval error is

\[
\Delta_M(t,L)=A_M(t,L)-LV_M.
\]

Let \(\alpha_q=\nu_q/q\), and let \(B_q(t,L)\) be the number of current survivors deleted by \(q\). The one-step defect is

\[
\epsilon_q(t,L)=B_q(t,L)-\alpha_q A_M(t,L).
\]

Thus positive defect means more deletions than uniform residue proportions predict. The exact identities are

\[
\boxed{A_{qM}=(1-\alpha_q)A_M-\epsilon_q},
\qquad
\boxed{\epsilon_q=(1-\alpha_q)\Delta_M-\Delta_{qM}.}
\]

For successive primes \(p_1,\ldots,p_J\), let \(M_j=\prod_{i\le j}p_i\), \(V_j=V_{M_j}\), and

\[
w_{j,J}=\prod_{i=j+1}^J(1-\alpha_{p_i}).
\]

Then, with \(A_0=L\),

\[
\boxed{\Delta_{M_J}=-\sum_{j=1}^J w_{j,J}\epsilon_{p_j}.}
\]

This product definition of the weights remains meaningful even when a pattern is locally obstructed. Expressions dividing by \(V_j\) below require positive survival density.

## 3. Explicit bounds valid for every interval

### Lemma 1. Discrepancy of a periodic mask

Suppose a binary sequence has period \(q\), with \(\nu\) ones per period. For any consecutive \(K\) positions, its one count \(C\) satisfies

\[
\boxed{|C-K\nu/q|\le\frac{\nu(q-\nu)}q.}
\]

**Proof.** Complete periods cancel. In a remaining segment of length \(r<q\), the one count lies between \(\max(0,r-q+\nu)\) and \(\min(r,\nu)\). Subtract \(r\nu/q\). Maximizing either possible deviation over \(r\) gives \(\nu(q-\nu)/q\). QED.

The same argument applies to an arithmetic progression with step coprime to \(q\), because its residue pattern is again periodic with \(\nu\) ones per period.

### Theorem 1. Uniform one-step defect bound

For every \(t,L\),

\[
\boxed{
|\epsilon_q(t,L)|\le
\frac{\nu_q(q-\nu_q)}q\,
\min\{N_M,\mathcal W_M\}.
}
\tag{1}
\]

This bound is independent of the interval location and length. It can be weak when many primes have already been sieved, but it has no hidden constant.

**Proof using surviving residues.** Partition old survivors by their \(N_M\) allowed residues modulo \(M\). Within the interval, each part is a consecutive segment of an arithmetic progression with step \(M\). Lemma 1 bounds its centered new-prime deletion count by \(\nu_q(q-\nu_q)/q\). Sum over the parts.

**Proof using inclusion-exclusion.** Let \(E_p(n)=\mathbf1_{n\bmod p\in F_p}\). Expand

\[
f_M(n)=\prod_{p\mid M}(1-E_p(n))
=\sum_{d\mid M}\mu(d)E_d(n),
\qquad E_d=\prod_{p\mid d}E_p.
\]

CRT expresses \(E_d\) as the disjoint union of \(\nu(d)=\prod_{p\mid d}\nu_p\) residue classes modulo \(d\). On every such class, apply Lemma 1 to the centered \(q\)-mask. The sum of the numbers of classes is

\[
\sum_{d\mid M}\nu(d)=\mathcal W_M.
\]

The triangle inequality gives the other bound in (1). QED.

The trivial asymmetric bound is also available:

\[
-\alpha_q A_M\le\epsilon_q\le(1-\alpha_q)A_M.
\]

Intersecting valid bounds is preferable to reporting a large symmetric bound when it exceeds the possible deletion count.

### Theorem 2. Uniform bound for the accumulated error

For every \(t,L\),

\[
\boxed{
|\Delta_M(t,L)|\le
\min\{\mathcal W_M-1,\ N_M(1-V_M)\}.
}
\tag{2}
\]

**Proof.** In the inclusion-exclusion expansion above, each residue-class count differs from \(L/d\) by at most 1. The \(d=1\) term is exactly \(L\), so its error is zero. Summing the other errors gives \(\sum_{d\mid M,d>1}\nu(d)=\mathcal W_M-1\). Alternatively, apply Lemma 1 to the binary period \(M\), with \(N_M\) ones. QED.

This improves the previous report's coarse bound \(|\Delta_M|\le N_M\). It controls the weighted sum of defects directly; it need not pay the much larger cost of separately summing every absolute one-step bound.

For a fixed \(k\)-element offset set, \(\mathcal W_{M_z}\le(k+1)^{\pi(z)}\). Together with standard prime asymptotics and \(V_{M_z}\asymp_H(\log z)^{-k}\), (2) is already relatively small for

\[
z\le c\log L\log\log L,
\qquad c<1/\log(k+1),
\]

as \(L,z\to\infty\). A new prime of comparable size also has relatively small one-step defect by (1). These are shallow-sieving results, not square-root-cutoff estimates.

## 4. Sharp finite certificates from one period

The previous bounds require only local residue counts. When \(qM\) is manageable, one can compute a much sharper bound.

Define the integer, zero-mean periodic signal

\[
u(n)=f_M(n)\bigl(q\mathbf1_{n\bmod q\in F_q}-\nu_q\bigr),
\qquad Q=qM.
\]

Its sum over one period is zero by CRT. Let

\[
P(0)=0,\qquad P(r)=\sum_{n=1}^r u(n),\quad0\le r\le Q,
\]

extended periodically, using \(P(Q)=0\). Then

\[
q\epsilon_q(t,L)=P(t+L)-P(t).
\]

Therefore

\[
\boxed{
\sup_{t,L}|\epsilon_q(t,L)|
=\frac{\max P-\min P}{q}.
}
\tag{3}
\]

This is an equality: the two extremizing prefix positions can be joined by a forward cyclic interval. For one fixed length, the sharp bound is instead

\[
\boxed{
\max_{0\le t<Q}\frac{|P(t+L)-P(t)|}{q}.
}
\tag{4}
\]

Computing (3) or (4) costs \(O(qM)\) once the signal is available. Full periods can be removed from \(L\), since they add zero defect. This is useful certification for small and moderate moduli; it is not a compact algorithm for arbitrarily large primorials.

### Certified example

Take \(M=13\#=30030\) and \(q=17\). Exhaustive integer prefix calculations over \(Q=510510\) give:

| Offsets | Formula (1) | Sharp bound for every location and every length | Sharp bound at length \(10^6\) |
|---|---:|---:|---:|
| \(\{0\}\) | \(1024/17\approx60.235\) | \(118/17\approx6.941\) | \(99/17\approx5.824\) |
| \(\{0,2\}\) | \(14580/17\approx857.647\) | \(230/17\approx13.529\) | \(140/17\approx8.235\) |
| \(\{0,2,6\}\) | \(26880/17\approx1581.176\) | \(271/17\approx15.941\) | \(196/17\approx11.529\) |

On the particular million-start interval \(1\le n\le10^6\):

| Offsets | Before 17 | After 17 | Actual one-step defect |
|---|---:|---:|---:|
| \(\{0\}\) | 191808 | 180524 | \(20/17\) |
| \(\{0,2\}\) | 49447 | 43627 | \(46/17\) |
| \(\{0,2,6\}\) | 21312 | 17550 | \(18/17\) |

For twins this means the model predicts \((15/17)49447=43629+12/17\) survivors; the true count is 43627. The discrepancy is exactly \(46/17\). Counts concern candidate **starts**; offsets may extend past the end of the starting interval.

## 5. Finite certificates without constructing a primorial

The full inclusion-exclusion bound can grow too quickly. A cheap alternative is a truncated, rigorously one-sided certificate.

For the selected primes, compute polynomial coefficients

\[
\prod_{p\mid M}(1+\nu_p x/p)=\sum_j a_jx^j,
\qquad
\prod_{p\mid M}(1+\nu_p x)=\sum_j b_jx^j.
\]

Let

\[
S_r=\sum_{j=0}^r(-1)^ja_j,
\qquad R_r=\sum_{j=1}^r b_j.
\]

Bonferroni inequalities and the same residue-class remainder bound imply

\[
A_M(t,L)\le LS_r+R_r\quad(r\text{ even}),
\]

\[
A_M(t,L)\ge LS_r-R_r\quad(r\text{ odd}).
\tag{5}
\]

At full degree both inequalities hold. Intersect all chosen bounds with \([0,L]\), round lower bounds upward and upper bounds downward, and obtain a certified integer interval containing \(A_M\) for **every** starting position.

**Proof.** At a point excluded by exactly \(m\) primes, truncated inclusion-exclusion is \(\sum_{j\le r}(-1)^j\binom mj\); it bounds the survivor indicator above for even \(r\) and below for odd \(r\). Summing over the interval gives the one-sided inequalities. Each intersection of \(j\) exclusion events has main term \(L\nu(d)/d\) and error at most \(\nu(d)\). Summing these errors gives \(R_r\). QED.

Up to degree \(r\), the coefficients cost \(O(r\pi(z))\) arithmetic operations, with exact rational arithmetic available. This computation does not enumerate the \(2^{\pi(z)}\) prime subsets or the period \(M_z\). It is a standard Bonferroni/Brun-type construction, not a new fundamental lemma.

### Explicit useful output

For twins \(H=\{0,2\}\), all primes through 97, and every interval containing exactly \(10^{12}\) consecutive starting integers, (5) proves

\[
\boxed{
17{,}856{,}272{,}319
\le A_{97}(t,10^{12})\le
20{,}611{,}537{,}508.
}
\]

Here \(A_{97}\) means sieving by primes at most 97. The lower certificate uses degree 9 and the upper degree 8. Relative to \(10^{12}V_{97}\), the interval is approximately

\[
[0.93251446,\ 1.07640365].
\]

The untruncated error bound \(\mathcal W_M-1=564859072961\) is too large to give this conclusion. The finite truncation gives a positive lower bound with all constants explicit.

For single candidates with the same parameters, the certified interval is

\[
120{,}313{,}182{,}158\le A_{97}(t,10^{12})
\le120{,}323{,}438{,}924,
\]

or approximately \([0.99996585,1.00005110]\) times the density main term.

At length \(10^{30}\), the same polynomial method handles all primes through 997. For twins, the certificate is approximately \([0.99878105,1.00033687]\) times the density prediction. Exact integers and rational main terms are in `results.json`.

Given bounds \(\ell_M\le A_M\le u_M\) and \(\ell_{qM}\le A_{qM}\le u_{qM}\), a valid one-step certificate follows:

\[
(1-\alpha_q)\ell_M-u_{qM}
\le\epsilon_q\le
(1-\alpha_q)u_M-\ell_{qM}.
\]

This conversion can lose precision. A good total-count certificate is not automatically a good relative certificate for the much smaller one-stage deletion count.

## 6. Exact second moments and accumulated cancellation

### Theorem 3. Exact mean square over interval positions

Choose \(t\) uniformly modulo \(Q=qM\). This is a precisely defined probability model on interval locations, not an assumption that prime numbers are random. Then \(\mathbb E\epsilon_q=0\).

Define

\[
C_M(d)=\frac{N_M(H\cup(H+d))}{M},
\qquad c_q(d)=|F_q\cap(F_q-d)|,
\]

and

\[
\Gamma_q(d)=C_M(d)\left(\frac{c_q(d)}q-\alpha_q^2\right).
\]

The exact variance is

\[
\boxed{
\sigma_q^2(L)=L\Gamma_q(0)
+2\sum_{d=1}^{L-1}(L-d)\Gamma_q(d).
}
\tag{6}
\]

**Proof.** Write \(\epsilon_q=\sum_{i=1}^L f_M(t+i)(\mathbf1_{t+i\bmod q\in F_q}-\alpha_q)\), square, and average. CRT makes the old-modulus and new-prime factors independent under uniform \(t\bmod qM\). Their two-point expectations are \(C_M(d)\) and \(c_q(d)/q-\alpha_q^2\). Group ordered pairs of positions by their separation. QED.

All \(N_M\) factors in (6) are exact CRT products. Thus the variance can be evaluated without enumerating the whole period. The direct formula costs \(O(L\pi(z)|H|)\) residue work for fixed small offset sets. One may first reduce \(L\) modulo \(qM\).

For any \(a>0\),

\[
\Pr(|\epsilon_q|\ge a)\le\frac{\sigma_q^2(L)}{a^2}.
\tag{7}
\]

For example, with \(M=2310\), \(q=13\), \(H=\{0,2\}\), and \(L=1000\),

\[
\sigma_q^2=\frac{301454}{195195},\qquad
\sigma_q\approx1.24272828.
\]

At least 99% of the 30030 possible interval phases therefore satisfy \(|\epsilon_q|\le10\sigma_q\approx12.4273\). Exhaustive checking actually gives the stronger all-phase maximum \(49/13\approx3.76923\). The variance method remains useful when direct period enumeration is unavailable, provided its correlation sum can still be evaluated or bounded.

No assertion that (6) is always bounded by an independent Bernoulli variance is made. Off-diagonal correlations must be retained.

### Theorem 4. Defects at different stages are orthogonal

Fix a final modulus \(M_J\), choose \(t\) uniformly modulo it, and let \(\mathcal F_j\) record \(t\bmod M_j\). The CRT makes the newly exposed prime phase uniform conditional on \(\mathcal F_{j-1}\). Hence

\[
\boxed{\mathbb E[\epsilon_{p_j}\mid\mathcal F_{j-1}]=0.}
\]

If every \(V_j>0\), then

\[
Z_j=\frac{A_{M_j}(t,L)}{V_j}
\]

is a martingale with increments \(-\epsilon_{p_j}/V_j\). In particular, for \(i<j\),

\[
\mathbb E[\epsilon_{p_i}\epsilon_{p_j}]=0.
\]

Using the exact telescoping identity gives

\[
\boxed{
\mathbb E[\Delta_{M_J}^2]
=\sum_{j=1}^J w_{j,J}^2\,
\mathbb E[\epsilon_{p_j}^2].
}
\tag{8}
\]

**Proof.** Conditional on the old phase, every old survivor at each of the fixed interval offsets is removed for exactly \(\nu_{p_j}\) of the \(p_j\) new phases. Linearity of conditional expectation proves the first assertion, without independence between positions. Earlier defects are measurable with respect to \(\mathcal F_{j-1}\), proving orthogonality. Expanding the square of the telescoping sum proves (8). QED.

This replaces a triangle inequality by an exact sum of squared contributions for the specified phase-average problem. It does not imply cancellation at an individually selected starting point.

For completeness, if deterministic bounds \(|\epsilon_{p_j}|\le b_j\) are available, the standard bounded-increment martingale argument also gives

\[
\Pr(|\Delta_{M_J}|\ge a)
\le2\exp\left(-\frac{a^2}{2\sum_jw_{j,J}^2b_j^2}\right).
\]

The elementary proof bounds the conditional exponential moment of each centered increment in \([-w_jb_j,w_jb_j]\) by \(\exp(\lambda^2w_j^2b_j^2/2)\), multiplies these bounds, and optimizes \(\lambda\). The result can be weaker than (7) when the worst-case \(b_j\) are large.

The random-CRT-phase organization is an application of standard sieve and martingale methods. No claim that this construction is new in the literature is made.

## 7. A useful growing-depth bound from classical sieve theory

Here the substantial external input is the fundamental lemma of the combinatorial sieve, not a new STD theorem. A suitable fixed-offset formulation is recorded in Lemma 1.4 of Gorodetsky [R2]; Tao's notes give a weaker exponential-rate version [R1]. For an admissible fixed \(k\)-element \(H\), interval length \(L\), cutoff \(z\), level \(D=z^s\), and sufficiently large \(s\), it implies, for every fixed \(0<\eta<1\),

\[
\boxed{
|\Delta_z(t,L)|
\le C_{H,\eta}LV_z e^{-(1-\eta)s\log s}
+C_{H,\eta}D(1+\log D)^{k-1}.
}
\tag{9}
\]

Constants in (9) are not made numerically explicit here. Thus (9) is a rigorous asymptotic range statement, whereas (1)–(5) give finite numerical certificates.

The displayed remainder follows from the usual sieve remainder sum and the elementary estimate

\[
\sum_{d\le D}\mu^2(d)k^{\omega(d)}
\le\sum_{d\le D}d_k(d)
\le D(1+\log D)^{k-1}.
\]

For the last inequality, count ordered factorizations into \(k\) positive integers and sum over the first \(k-1\) factors, bounding the last by \(D\) divided by their product. No assertion that an unspecified big-O constant equals 1 is used.

Take \(D=L^{1/2}\). For fixed \(H\), (9) proves

\[
A_z(t,L)=LV_z(1+o(1))
\]

uniformly over interval positions when \(z=L^{o(1)}\) and \(z\to\infty\). This is a classical rough-tuple counting regime, far beyond what the full inclusion-exclusion error alone provides.

### Corollary. A range with small relative one-step defect

Suppose the old sieve contains all primes less than \(q\). Fix an admissible \(H\), and fix \(c\) with \(0<c<1/2\). As \(L\to\infty\), uniformly over interval positions and primes \(q\to\infty\) satisfying

\[
q\le\exp\bigl(c\sqrt{\log L\log\log L}\bigr),
\]

we have

\[
\boxed{\epsilon_q(t,L)
=o\left(\frac{\nu_q}{q}A_{q^-}(t,L)\right).}
\tag{10}
\]

Here \(A_{q^-}\) means survival of primes strictly below \(q\). This genuinely controls the defect relative to the predicted deletion count, not just relative to all survivors.

**Derivation.** Apply (9) before and after adding \(q\), then use \(\epsilon_q=(1-\alpha_q)\Delta_{q^-}-\Delta_q\). Let \(T=\log L\), \(a=\log q\), and choose \(D=L^{1/2}\), so the smaller sieve ratio is \(s=T/(2a)\). Dividing by the expected deletion main term gives a bound of the form

\[
O_{H,\eta}\left(
q e^{-(1-\eta)s\log s}
+\frac{qL^{1/2}(1+\log L)^{k-1}}{LV_{q^-}}
\right).
\]

At the largest allowed \(a=c\sqrt{T\log T}\),

\[
s\log s=\left(\frac1{4c}+o(1)\right)\sqrt{T\log T}.
\]

Choose \(\eta\) small enough that \(c^2<(1-\eta)/4\). The first term tends to zero; smaller \(q\) only improve the eventual bound. The second tends to zero because \(V_{q^-}\asymp_H(\log q)^{-k}\). Finally (9) gives \(A_{q^-}\sim LV_{q^-}\), permitting replacement of its main term by its actual count. QED.

The range in (10) is subpower in \(L\). It does not include \(q\asymp\sqrt L\). The conclusion is a corollary of existing sieve theory; it is not presented as an improvement on that theory.

## 8. Why tiny relative defects fail at the square-root cutoff

### Theorem 5. An exact obstruction in the single-candidate problem

Let \(q\ge3\) be prime, let the old sieve remove all multiples of primes less than \(q\), and use the interval

\[
I=(q,q^2]\cap\mathbb Z.
\]

Its old survivors are precisely the primes in this interval together with \(q^2\). Indeed, any surviving composite has every prime factor at least \(q\), and a composite no larger than \(q^2\) can then only be \(q^2\).

Consequently,

\[
A=\pi(q^2)-\pi(q)+1,\qquad B_q=1,
\]

and

\[
\boxed{\epsilon_q=1-A/q.}
\]

The prime number theorem gives \(A/q\to\infty\), hence

\[
\boxed{\frac{\epsilon_q}{A/q}\longrightarrow-1.}
\tag{11}
\]

Thus a uniform claim \(\epsilon_q=o(A/q)\) at the square-root cutoff is false, already for single candidates. The defect is nevertheless small compared with \(A\), because \(|\epsilon_q|/A\sim1/q\). This is why the normalization distinction matters.

| New prime \(q\) | Interval | Before deletion | Actually deleted | Defect divided by expected deletions |
|---:|---|---:|---:|---:|
| 13 | \((13,169]\) | 34 | 1 | −0.617647 |
| 31 | \((31,961]\) | 152 | 1 | −0.796053 |
| 101 | \((101,10201]\) | 1227 | 1 | −0.917685 |
| 997 | \((997,994009]\) | 77893 | 1 | −0.987200 |

These finite rows were checked by a direct sieve as well as by the prime-counting expression.

There is also an exact late-stage formula that helps identify the proper replacement for the uniform-deletion model. If all earlier primes have been sieved, \(q^3>X\), and \(I\subseteq[1,X]\), the old survivors divisible by \(q\) are exactly

\[
\{q\}\cap I\quad\text{and}\quad
\{qr\in I:r\text{ prime},\ r\ge q\}.
\]

To prove this, write a surviving multiple as \(qm\). Then \(m<X/q<q^2\) has no prime factor below \(q\), so it is either 1 or a prime at least \(q\). At these depths, deletion counts reflect the allowed factorization types. Treating them as uniform residue fractions loses that information. This is the setting addressed by classical Buchstab-type decompositions.

The earlier report's total-error warning remains valid. At the square-root cutoff, Mertens' product predicts \(2e^{-\gamma}X/\log X\), while actual prime counts have leading coefficient 1. The total correction contributes at main-term scale. Nothing in the phase-average martingale removes this deterministic correction at the initial interval.

## 9. Reproducibility and verification

The new script `interval_defect.py` uses only the Python standard library and exact integer or rational arithmetic for every asserted identity and certificate. It completed **282,677 exact checks**. Displayed RMS values and ratios are rounded separately.

The checks include:

* Every interval phase for selected small moduli, offset sets, and lengths, comparing the pointwise analytic bounds and prefix certificates with direct sums.
* Exact covariance formulas against exhaustive squared-defect averages.
* 600 reproducible varied intervals, including negative starts and zero lengths, with direct counts compared against an independent CRT inclusion-exclusion implementation.
* Bonferroni certificate containment, including locally obstructed patterns.
* 3,735 conditional-mean checks, 150 cross-stage orthogonality checks, and 15 total-variance decompositions.
* Million-start examples checked against periodic certificates.
* Four square-root-cutoff cases, checking both the survivor formula and the single actual deletion.

The original 8,859-check program is also included, along with its rerun result. These finite tests support the implementations; they do not replace the proofs or independently validate the external fundamental lemma.

Run the new results with:

```bash
python3 interval_defect.py --output results.json
```

Run the previous audit checks with:

```bash
python3 prior_verify_std_primes.py --output prior_audit_results.json
```

## 10. Current research position

The interval defect is now more than an unspecified remainder:

1. Its worst-case size has elementary uniform bounds with explicit constants.
2. For manageable moduli, its sharp global bound is a finite prefix-range certificate.
3. Truncated polynomial calculations certify useful large-interval counts without constructing the primorial.
4. Its exact covariance and cross-stage orthogonality support rigorous phase-average estimates.
5. Existing sieve theory supplies a growing-depth regime with negligible relative stage error.
6. An explicit square-root-cutoff family proves where that target must fail.

The next substantive goal should be a controlled **factorization-aware interval model** at deeper sieve stages, starting with single candidates and the late-stage identity above. At shallow depths, the uniform-density model has proved error bounds. Near the primality cutoff, a correction that accounts for primes, semiprimes, and their restrictions is essential. For tuples, proving sufficiently sharp joint factorization estimates remains substantially harder.

A useful future result must either improve a computational certificate at a specified cost, improve a known analytic estimate, or prove a new compression theorem for these corrected observables. Rephrasing a classical estimate in STD notation alone does not establish novelty.

## Sources

The current STD source audited was `STD_50_Prime_Problems_2026-10-09.md`, together with its executable checks. Its distinctions between complete periods, fixed intervals, arbitrary cyclic sources, and actual prime counts are retained.

**R1.** Terence Tao, *254A Notes 4: Some sieve theory* (2015). Primary author exposition of inclusion-exclusion sieves, combinatorial sieve weights, and the fundamental lemma. Used to identify the classical status of the methods and verify the required sieve hypotheses. https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/

**R2.** Ofir Gorodetsky, *The variance of integers without small prime factors in short intervals*, Mathematische Zeitschrift 308, 59 (2024). Lemma 1.4 supplies the fixed-offset interval form of the fundamental lemma used in (9), including its stronger decay in the sieve ratio. The present interval-defect and martingale formulas are derived explicitly above; no claim to reproduce the paper's sharper variance results is made. https://doi.org/10.1007/s00209-024-03601-w

Standard inputs also include CRT, Bonferroni inequalities, the prime number theorem, Mertens' product theorem, and elementary martingale inequalities. The proofs of (1)–(8) and the exact obstruction in (11) require no prime-tuple conjecture. The limiting statement in (11) uses the prime number theorem.