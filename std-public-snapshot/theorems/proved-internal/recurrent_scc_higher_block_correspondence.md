# Recurrent SCC correspondence under higher-block lifting

**Date:** 2026-10-11  
**Status:** proved-internal; finite graph theorem, pending nonauthor review.  
**Scope:** recurrent cyclic cores of finite-type higher-block presentations. This is a graph/source-domain theorem only; it does not prove the reducible support-pair LP criterion or implement its solver.

## 1. Setup

Fix a finite alphabet and a finite-type presentation by allowed length-m blocks. For every t >= m, let G_t be the usual directed higher-block graph: a linearly allowed length-t word is an edge from its length-(t-1) prefix to its length-(t-1) suffix.

Let G_t^circ be the recurrent cyclic core obtained by retaining exactly the edges that lie on a directed closed walk.

Every recurrent edge has endpoints in the same strongly connected component: if edge u -> v lies on a closed walk, that walk gives a path v -> u, while the edge itself gives u -> v. Thus G_t^circ is a disjoint union of its nonempty recurrent SCCs, with no recurrent edge running between distinct SCCs.

The recurrent-core theorem merged in PR #6 identifies these edges exactly with blocks occurring in finite cyclic sources.

PR #39 proved that when G_s^circ is one nonempty SCC, every recurrent higher-block lift G_L^circ is also one SCC. The result below removes the global irreducibility assumption and works component by component.

## 2. Higher blocks as base-edge paths

Fix m <= s <= L and set q = L - s + 1.

A linearly allowed length-L word determines its q consecutive length-s windows. These form a directed q-edge path in G_s.

Conversely, any directed q-edge path in G_s reconstructs one unique linearly allowed length-L word, because consecutive s-blocks overlap in s-1 symbols and s >= m.

So edges of G_L are exactly q-edge paths of G_s.

For L > s, vertices of G_L are exactly (q-1)-edge paths of G_s. The case L=s is the identity presentation.

## 3. Exact recurrent-edge characterization without irreducibility

**Theorem 1.** Let L >= s. A length-L edge e of G_L is recurrent if and only if every one of its consecutive length-s constituent edges is recurrent in G_s.

### Forward direction

Suppose e lies on a directed closed walk in G_L.

Project the successive lifted edges to their sliding length-s windows. Going once around the lifted closed walk produces a closed walk in G_s. Every constituent s-edge of e occurs on that projected closed walk.

Hence every constituent s-edge is recurrent.

### Reverse direction

Suppose every constituent s-edge e_0, e_1, ..., e_(q-1) is recurrent in G_s.

A recurrent edge has endpoints in one SCC. Since consecutive e_i share a vertex, recurrence forces e_i and e_(i+1) to lie in the same recurrent SCC. Inductively the entire q-edge path lies in one unique recurrent SCC K of G_s^circ.

Because K is strongly connected, there is a directed path inside K from the terminal vertex of e_(q-1) back to the initial vertex of e_0.

Appending this connector closes the prescribed q-edge path to a directed closed walk in K. Sliding a q-edge window around that closed walk gives a directed closed walk in G_L containing the original lifted edge.

Therefore e is recurrent. QED.

### Important consequence

Theorem 1 does not require G_s^circ itself to be strongly connected.

In particular, a raw linearly allowed length-L block that crosses a transient connector between two recurrent base SCCs is not recurrent upstairs, because that connector is one of its constituent nonrecurrent s-edges.

## 4. Recurrent paths cannot cross SCCs

**Lemma 2.** Every nonempty directed path consisting only of recurrent edges of G_s lies entirely in one unique recurrent SCC of G_s^circ.

**Proof.** Each recurrent edge has both endpoints in one SCC. Consecutive path edges share a vertex, and SCCs partition vertices. Therefore the SCC containing one path edge is the SCC containing the next. Induction gives one component for the whole path. Uniqueness follows from the SCC partition. QED.

## 5. Bijection of recurrent SCCs

Let the recurrent SCCs of G_s^circ be K_1, ..., K_c.

For each K_j and L >= s, define Lift_L(K_j) by taking as lifted edges the length-L blocks whose q constituent s-edges all lie in K_j, with their incident length-(L-1) vertices.

**Theorem 3 (componentwise higher-block correspondence).** For every L >= s:

1. each Lift_L(K_j) is nonempty and strongly connected;
2. the recurrent edge set of G_L is the disjoint union of the lifted edge sets Lift_L(K_j);
3. no recurrent lifted edge joins two different component lifts;
4. every recurrent SCC of G_L^circ is exactly one Lift_L(K_j).

Therefore base recurrent SCCs and lifted recurrent SCCs are in a canonical bijection.

### Proof

For item 1, each K_j is a nonempty strongly connected recurrent graph. Apply the irreducible higher-block theorem proved in PR #39 to K_j itself. Its recurrent q-path lift is nonempty and strongly connected.

For item 2, Theorem 1 says a lifted edge is recurrent exactly when all its constituent base edges are recurrent. Lemma 2 says those constituent edges then lie in one unique K_j. Thus every recurrent lifted edge belongs to exactly one Lift_L(K_j), and every edge in such a lift is recurrent.

For item 3, an edge in Lift_L(K_j) has every constituent base edge in K_j, so it cannot also belong to Lift_L(K_i) for i != j. Its incident lifted vertices inherit the same component path. Thus no recurrent lifted transition crosses between different lifts.

For item 4, each Lift_L(K_j) is strongly connected by item 1, and item 3 prevents any recurrent path from connecting distinct lifts in both directions. Hence each lift is one SCC of G_L^circ, and item 2 shows there are no other recurrent SCCs. QED.

## 6. Boundary cases

### L=s

Then q=1 and Lift_s(K_j)=K_j. The correspondence is the identity.

### Recurrent self-loops

A one-edge self-loop component lifts to the repeated periodic block family from that loop and remains one SCC at every higher order.

### Periodic components

No aperiodicity or mixing assumption is used. A directed d-cycle remains one strongly connected lifted component. The theorem is about SCC structure, not primitive period.

### Source periods shorter than L

A cyclic source of period n<L is represented by a repeated closed base walk. Its periodic length-L windows are q-edge segments of that repeated walk and therefore stay inside the same recurrent component. Short source periods need no separate hypothesis.

### Transient connectors between recurrent SCCs

Suppose a raw allowed graph contains two recurrent components and a one-way path from the first to the second with no return path.

Every edge on that connector is transient. Any linearly allowed higher block containing the connector may exist in the raw higher-block graph, but Theorem 1 removes it from the recurrent lifted core.

So higher-block lifting does not merge recurrent SCCs through transient admissible paths.

## 7. Consequence for cyclic-source and support bookkeeping

Every finite cyclic source traverses one closed walk. At base order s it therefore lies in one recurrent SCC K_j; at every lifted order L its edge histogram lies in the corresponding Lift_L(K_j).

This allows reducible analyses to attach a canonical base-component label to every recurrent lifted edge and every cyclic source.

However this does **not** collapse the accepted support-pair theorem to an SCC-only calculation.

Inside one recurrent SCC there may be many proper nonempty strongly connected positive edge supports. The support-pair criterion from merged PR #6 quantifies over such supports, not merely maximal SCCs.

Therefore:

- supports from different recurrent SCCs must still be compared when their source projections can agree;
- distinct proper supports inside the same recurrent SCC may also need comparison;
- per-SCC horizon checks still do not imply global sufficiency.

The worked PR #25 example remains the simplest cross-component illustration. Issue #31 separately audits the support-pair theorem itself, and issue #44 separately implements bounded exact certificates. Neither is proved by this note.

## 8. Finite regression plan

Supporting tests should check small presentations with:

1. multiple recurrent self-loop components;
2. a periodic component plus a self-loop component;
3. transient one-way connectors between recurrent components;
4. source periods shorter than the lifted block order.

For each tested s,L:

- compute the base recurrent SCC partition independently;
- compute the recurrent higher-block edge set;
- map each recurrent lifted edge to the unique base SCC containing its constituent s-windows;
- verify each component lift is strongly connected;
- verify the lifted SCC partition has exactly the same number of components and exactly the predicted edge partition.

Finite checks support the theorem but do not replace the proof.

## 9. Pinned provenance

Task start:

- main: private-history-omitted;
- accepted recurrent-core theorem: PR #6 merge private-history-omitted;
- accepted irreducible lift theorem: PR #39 merge private-history-omitted;
- reviewed PR #39 proposal head: private-history-omitted.

No claim from B issue #31 or C issue #44 is used as a premise beyond the already merged finite-type/recurrent-core graph definitions.