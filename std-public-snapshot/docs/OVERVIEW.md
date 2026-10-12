# STD: a reader's introduction

## The question

Suppose a rule transforms a sequence, but you retain only counts of short patterns. Can those counts determine the transformed sequence's pattern counts exactly?

STD asks this over an explicitly specified family of finite **cyclic** words. It seeks the smallest sufficient source-window length, or two sources showing that a proposed length fails. This concerns sufficient statistics for a transformation, not reconstruction of the whole source.

## Definitions

Let A and B be finite alphabets. A source x has positive length N. Indices wrap modulo N, including when a window is longer than the source. For h ≥ 1,

$$C_h(x)(u)=\#\{i\in\{0,\ldots,N-1\}:x_i\cdots x_{i+h-1}=u\},\qquad u\in A^h.$$

These are **raw counts**: their sum is N. The length-three cyclic windows of `01` are `010` and `101`, each once. Rotating a source leaves C_h unchanged. Rooted words and rotation classes still differ when counting sources or inverse images.

A total synchronous radius-r rule assigns an output word to each centered context:

$$\phi:A^{2r+1}\to B^*.$$

Concatenating the emissions in source-site order gives T(x). Empty emissions mean erasure. An empty total output has zero raw block counts. Transformations outside this model require separate arguments.

For a domain D and output order k ≥ 1, define

$$H_{T,D}(k)=\min\{h\ge1:\ \forall x,y\in D,\ C_h(x)=C_h(y)\Rightarrow C_k(T(x))=C_k(T(y))\}.$$

If no finite h works, the horizon is infinity. The fixed-length disjoint-cycle theorem leaves empty length domains **undefined**. Unrestricted positive lengths, exact length N, and fixed inventories are different domains.

## Identity output

On all nonempty binary cyclic words, take T(x)=x and k=2. The sources `0011` and `0101` share C_1=(2,2), but have different pair counts. Thus h=1 fails. At h=2 the source and output statistics are identical, proving **H(2)=2** for the whole domain.

A found collision disproves sufficiency. A finite search finding no collision does not prove sufficiency over all lengths.

## Why components must be compared

Allow exactly the following periodic length-five source windows:

```text
00110  01100  11001  10011  01010  10101
```

The recurrent graph consists of the `0011` orbit and the `01` orbit. Use a total radius-two rule emitting `b` on `01010` and `10101`, and `a` on every other binary five-symbol context.

| Source | Source symbol counts | Output | Output symbol counts |
|---|---|---|---|
| `0011` | 0: 2, 1: 2 | `aaaa` | a: 4 |
| `0101` | 0: 2, 1: 2 | `bbbb` | b: 4 |

Within each component, source length determines the output counts. Across components, h=1 fails. At h=2, the `00` coordinate separates the components, and within each component total count determines length. Therefore **H(1)=2** on the stated domain.

This is the reviewed [PR #25 example](../theorems/proved-internal/reducible_support_worked_example.md), with [executable code](../experiments/reducible_support_example.py). Testing components separately would miss the collision.

## The finite-type method

A finite-type restriction specifies allowed windows of order m. Represent each allowed m-word by an edge from its (m−1)-prefix to its (m−1)-suffix. Cyclic sources are closed walks. Remove edges on no closed walk: no finite cyclic source uses them.

If R bounds consecutive silent emissions in the recurrent emission graph, then for k>1 the accepted local-additivity theorem uses

$$L=\max(m,2r+1)+(k-1)(R+1).$$

Charge each output k-window to the site emitting its first character. Bounded silence supplies its remaining characters within the stated lookahead, making C_k(T(x)) a linear function F of source L-block counts. For k=1 no lookahead across silent runs is needed.

On a strongly connected recurrent L-block graph, let D be the incidence matrix and P_h the h-prefix-count matrix. For 1≤h≤L, h is sufficient exactly when every row of F lies in the rational row span of D and P_h. Positive results yield linear identities; rank failure yields a balanced difference that lifts to two genuine Euler source words.

On a reducible graph, a circulation can combine disconnected components without representing a single cyclic source. The theorem instead compares **pairs of strongly connected positive supports** through rational feasibility. Scaling a rational point to integer Euler walks is legitimate because lengths are unrestricted; it does not preserve a fixed length or inventory.

These are summaries of the [finite-type theorem](../theorems/proved-internal/finite_type_exact_horizon.md). Its full hypotheses and proof govern use of the method.

## Fixed length

One reviewed theorem covers a special case: the entire recurrent canonical graph is a union of vertex-disjoint simple cycles, and the rule never erases. If component i has primitive source word w_i of period d_i, it occurs at length N precisely when d_i divides N.

Define P_(i,h)=C_h(w_i)/d_i and Q_(i,k)=C_k(T(w_i))/d_i. The horizon is the first h such that every eligible pair with equal P_(i,h) also has equal Q_(i,k). For nonempty exact-length domains,

$$1\le H_N(k)\le\max(1,m-1).$$

The Q denominator is the **source period**, not output length. Adjoining an undefined value for empty length classes gives a profile with period lcm(d_i). Its least period is a separate pending candidate, not part of the accepted theorem.

The [proof](../theorems/candidates/std3_fixed_length_disjoint_cycle_horizons.md), [acceptance ledger](RESULTS.md), and [finite oracle](../experiments/std3_cycle_spectrum_oracle_README.md) have distinct evidentiary roles.

## Use and limits

The immediate use is exact reasoning about which pattern summaries a local transformation requires, with inspectable counterexamples when a summary loses relevant information. Particular data-processing applications remain proposed uses until their rules and domains are modeled and tested.

There is no current total solver for arbitrary programs, general unbounded erasure, arbitrary rooted observables, or every fixed-length/inventory constraint. The project records internal AI-assisted nonauthor review separately from external peer review and formal proof.
