# Reviewed results and their limits

This index summarizes the internally reviewed mathematical core selected for this sanitized research snapshot. Internal review is reported from private development records; those records are not included here for independent public inspection. The proofs, implementations, tests, and explicit limitations are included. See [snapshot notes](SNAPSHOT.md).

## Core results

| Result and source | What it establishes | Boundary / evidence |
|---|---|---|
| [Finite-type exact horizons](../theorems/proved-internal/finite_type_exact_horizon.md) | Recurrent trimming; local additivity; irreducible rank criterion; reducible support-pair criterion | Analytic proof, internal nonauthor review. Arbitrary positive lengths; for k>1 the finite-lookahead part requires bounded silence |
| [Higher-block irreducibility](../theorems/proved-internal/recurrent_higher_block_irreducibility.md) and [SCC correspondence](../theorems/proved-internal/recurrent_scc_higher_block_correspondence.md) | Recurrent components are preserved under higher-block lifting | Analytic graph results. Do not eliminate cross-support comparisons |
| [Forced-continuation reduction](../theorems/proved-internal/forced_continuation_cyclic_reduction_2026-10-11.md) | Exact contraction/lifting within one fixed feasible histogram fiber | Analytic bijection plus code. Not a global finite-horizon algorithm |
| [Horizon growth audit](../audits/2026-10-11/HORIZON_GROWTH_THETA_AUDIT.md); [primary proof](../audits/archive/STD_Recovery_Spectrum_Status_2026-10-09.md) | A nonconstant all-finite spectrum grows as Theta(k) | Full cyclic source family and complete finite-radius rules; constrained domains need separate results |
| [Witness-size bounds](../theorems/proved-internal/support_pair_witness_size_bounds.md) and [sparse refinement](../theorems/proved-internal/support_pair_sparse_sharpness.md) | Explicit finite bounds for Euler witnesses obtained from rational support-pair systems | Bounds are not practical runtime guarantees, and do not bound source histogram order |
| [Disjoint-cycle fixed-length horizons](../theorems/candidates/std3_fixed_length_disjoint_cycle_horizons.md) | Exact density/pair formula; H_N(k)≤max(1,m−1); divisibility structure | Entire recurrent canonical graph must be vertex-disjoint simple cycles; total nonerasing rule; empty length classes undefined |
| [Scoped reset-gap repair](../theorems/errata/reset_gap_scope_and_exact_horizon_2026-10-11.md) | Exact gap criterion for the specified total weighted closed-run charts | Not a general local word-emission or arbitrary sofic theorem; broader historical claim remains false |

## Denominators and witnesses are different

| Reviewed example | Conclusion | What it does not imply |
|---|---|---|
| [Coprime-orbit family](../theorems/candidates/coprime_orbit_witness_and_vertex_lower_bounds.md) | Reducible family with growing vertex denominators and quadratic shortest-witness growth in recurrent edge count | A superlinear lower bound in serialized input length |
| [Exponential-minor family](../theorems/proved-internal/exponential_minor_family_exact_witnesses.md) | The selected full-support vertices are integral despite exponential structural minors; exact linear witness minima | Exponential feasible-vertex denominators or universally hard witnesses |
| [Irreducible binary family](../theorems/candidates/irreducible_binary_vertex_denominator_family.md) | Unique specified full-support vertex has denominator p=(E−2)/2; exact shortest individual full-support witness length 4p+2 | Fixed output order for the identity-rule family, or the arbitrary-support minimum |
| [Six-edge search](../experiments/IRREDUCIBLE_FRACTIONAL_VERTEX_SEARCH_2026-10-11.md) | Declared finite search: 1,594 LP instances, 244 vertices, denominators one or two | An asymptotic theorem beyond the searched class |

## Executable surfaces

| Surface | Current status |
|---|---|
| `std_tools/sft_closure.py` | Reviewed exact rational solver for irreducible recurrent finite-type domains; scope exceptions are explicit |
| `experiments/support_pair_certificates.py` | Reviewed exact reference generator with an **eight recurrent-edge cap**; integer input validation included |
| `std_tools/structural_reduction.py` | Reviewed fixed-fiber contraction and lifting |
| `audits/verify_bigram_exact.py` | Reviewed focused exact certificate checker; does not accept the broader candidate-v19 classification by itself |
| `experiments/rooted_inverse_oracle.py` | Bounded rooted inverse oracle; no accepted production inverse counter is supplied |
| Practical JSON analyzer | Draft; independent review pending; excluded from the reviewed-core quickstart |

## Reading historical files

Historical directory names and headers are retained for navigation, not as an automatic certification system. The scope in this index controls the snapshot. A historical claim to have completed a theorem does not override a later erratum or unresolved dependency.

CI and finite enumeration are execution evidence. They do not replace mathematical proof or independent review, and none of these labels means external peer review or formal verification.
