# Recurrent higher-block irreducibility is invariant

**Date:** 2026-10-11  
**Status:** proved-internal; finite graph theorem with supporting regression checks; not externally peer reviewed or formally verified.  
**Scope:** finite directed higher-block presentations of finite-type cyclic source languages. This theorem is purely graph/source-domain mathematics; no emission rule, output alphabet, erasure assumption, or horizon statistic is needed for the theorem itself.

## 1. Setup

Let A be a finite alphabet. Fix allowed m-blocks W_m.

For every t >= m, let G_t be the directed higher-block graph:

- edges are linearly allowed words w in A^t, meaning every internal length-m factor of w belongs to W_m;
- w goes from its length-(t-1) prefix to its length-(t-1) suffix.

Let G_t^circ be the recurrent cyclic core, obtained by keeping exactly those edges that lie on a directed closed walk, together with their incident vertices.

Equivalently, an edge belongs to G_t^circ exactly when it occurs as a periodic t-window of some nonempty finite cyclic source in the stated finite-type domain. This is the recurrent-core theorem already merged in PR #6.

We say the cyclic presentation is irreducible at length t when G_t^circ is nonempty and strongly connected.

No rooted source convention is needed here. The theorem concerns cyclic admissibility and graph connectivity only.

## 2. Path model for higher blocks

Fix m <= s <= L and put

q = L - s + 1.

Every linearly allowed length-L word

w = w_0 ... w_(L-1)

determines the consecutive length-s blocks

e_i = w_i ... w_(i+s-1),  0 <= i < q.

These are edges of G_s, and consecutive e_i,e_(i+1) overlap in exactly s-1 symbols. Hence

(e_0,...,e_(q-1))

is a directed q-edge path in G_s.

Conversely, any directed q-edge path in G_s has the required s-1 overlaps and reconstructs one unique length-L word. Since s >= m, every length-m factor of that reconstructed word is contained in one of its consecutive allowed s-blocks, so the word is linearly allowed.

Thus edges of G_L are in bijection with directed q-edge paths in G_s.

Likewise, vertices of G_L correspond to directed (q-1)-edge paths in G_s when q > 1. For q = 1, G_L = G_s.

## 3. Recurrent-edge characterization under an irreducible base core

**Theorem 1.** Assume G_s^circ is nonempty and strongly connected. Let L >= s, and identify a length-L edge with its q = L-s+1 consecutive s-edges

(e_0,...,e_(q-1)).

Then the length-L edge belongs to G_L^circ if and only if every e_i belongs to G_s^circ.

### Recurrent lift implies recurrent constituents

Suppose the length-L edge lies on a directed closed walk in G_L.

Project every length-L edge on that closed walk to its consecutive length-s windows. Sliding one source symbol at a time around the closed G_L-walk produces a periodic closed walk in G_s. In particular, every constituent e_i of the original length-L edge occurs on this projected closed walk.

Therefore every e_i is recurrent in G_s.

### A path in the base core is recurrent upstairs

Conversely, suppose every constituent e_i lies in G_s^circ.

Because G_s^circ is strongly connected, there is a directed connector path in G_s^circ from the terminal vertex of e_(q-1) back to the initial vertex of e_0. Appending that connector to

e_0 e_1 ... e_(q-1)

produces a directed closed walk in G_s^circ containing the entire prescribed q-edge path consecutively.

Slide a window of q consecutive G_s-edges around this closed walk. By the path correspondence, those windows form a directed closed walk in G_L, and one edge is exactly the original length-L block.

Hence the original edge lies in G_L^circ. QED.

## 4. Strong connectivity survives every higher-block lift

**Theorem 2.** If G_s^circ is nonempty and strongly connected, then for every L >= s, G_L^circ is also nonempty and strongly connected.

### Proof

Nonemptiness follows from Theorem 1: choose a directed cycle in the nonempty strongly connected graph G_s^circ, repeat it if necessary, and take q consecutive edges. This gives a recurrent length-L edge.

For strong connectivity, L=s is immediate. Assume L>s, so a vertex of G_L^circ corresponds to a directed path of q-1 edges in G_s^circ.

Take arbitrary vertices U,V of G_L^circ. Let u_plus be the terminal base vertex of the G_s^circ-path represented by U, and let v_minus be the initial base vertex of the path represented by V.

Since G_s^circ is strongly connected, choose a directed connector path R from u_plus to v_minus.

Concatenate

U-path ; R ; V-path.

Slide a window of q-1 base edges along this concatenation. It starts at U and eventually reaches V.

Every transition between consecutive lifted vertices uses a q-edge path lying entirely in G_s^circ. By Theorem 1, every such transition edge lies in G_L^circ.

Therefore there is a directed path in G_L^circ from U to V. Since U,V were arbitrary, G_L^circ is strongly connected. QED.

## 5. Boundary cases

### L=s

Then q=1 and the lifted graph is the base graph itself.

### Self-loops

A single recurrent self-loop is a strongly connected recurrent core. Every higher-block lift consists of one recurrent self-loop labeled by the corresponding repeated periodic word.

### Periodic strongly connected graphs

The theorem does not require aperiodicity or mixing.

For example, a directed d-cycle is strongly connected but has period d. Its higher-block presentation remains a directed d-cycle up to the natural path labeling. The theorem preserves irreducibility, not graph period.

### Source periods shorter than L

The recurrent-core definition uses directed closed walks and periodic windows, not distinct linear positions.

A cyclic source of period n<L contributes a length-L edge by repeated periodic wrapping. In graph language this is a q-edge segment of a repeated closed base walk. The proof above already covers n<L.

## 6. Exact API consequence for the merged finite-type solver

At current main, exact_horizon_irreducible performs:

1. recurrent-core trimming at s=max(m,2r+1);
2. an explicit check that the recurrent base core is strongly connected;
3. bounded-silence analysis on that recurrent core;
4. construction of L=s+(k-1)(R+1);
5. recurrent-core trimming again at length L;
6. a second strong-connectivity check.

Theorems 1-2 show:

> Once step 2 succeeds, step 6 cannot fail for mathematical reasons.

The second check may still be retained as a defensive implementation invariant. If it ever fails, that indicates an inconsistency in allowed-block enumeration, recurrent-core extraction, or the path-lift assumptions, not a newly discovered reducible cyclic source domain.

Therefore the higher-block check is not an additional source-domain hypothesis after the base recurrent core is known irreducible.

A clean API distinction is:

- base recurrent core reducible: user-domain condition; route to cross-support analysis;
- higher lifted recurrent core reducible after an irreducible base core: internal invariant violation.

This theorem does not remove the need to trim recurrent edges at length L. A linearly allowed length-L word can contain transient base edges and must still be excluded. Theorem 1 identifies exactly which lifted edges survive.

## 7. Relation to reducible support analysis

This result applies only after the recurrent base core is one SCC.

If G_s^circ has multiple recurrent SCCs, one cyclic source lies in one SCC while two compared sources may lie in different SCCs. The cross-support compatibility problem from merged PR #6 remains genuine.

The present theorem does not say higher-block lifting merges those SCCs or that per-SCC horizon checks solve the reducible problem.

## 8. Evidence plan and limitations

A regression/property test should enumerate small binary finite-type presentations and, whenever a base recurrent core is nonempty and strongly connected, verify for several L>=s:

1. the recurrent length-L edge set equals the linearly allowed length-L words whose consecutive length-s windows all lie in the base recurrent core;
2. the recurrent length-L core is strongly connected.

Finite checks are supporting evidence only. The universal result is the path/closed-walk proof.

This theorem does not address reducible recurrent cores, fixed-length-only populations, rooted output conventions, emission/erasure semantics, support-pair LP correctness, or complexity of large higher-block enumeration.

## 9. Pinned inputs

Task start:

- main: private-history-omitted;
- std_tools/sft_closure.py blob: private-history-omitted;
- merged PR #6: private-history-omitted;
- recurrent-core issue #7: complete and merged.

No claim from B's active reducible support-pair audit (issue #31) is used to prove this theorem.
