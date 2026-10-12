# Exact bigram verifier integration scope

**Date:** 2026-10-11  
**Integration task:** #35  
**Source audit:** PR #9 at `private-history-omitted`

This focused integration carries only the exact per-instance verifier, its five pinned fixtures, and its adversarial unittest file from draft PR #9. Those files are copied byte-for-byte; their Git blob IDs are recorded below.

## Integrated claim

For the verifier's stated scope — total two-state permutation machines, at least one erasure, acyclic silence, all nonempty closed cyclic runs, and raw cyclic output-bigram counts — an accepted positive certificate directly proves the H=1 predictor through two exact telescoping identities, and an accepted negative certificate supplies a literal same-source infinity witness.

This direct verifier implication was independently reviewed by Researcher B on the original PR #9 head. Researcher D independently reproduced the replacement suite under normal and optimized Python and found no hostile arithmetic/type mutation accepted.

## Explicit exclusions

This integration does **not** accept or import:

- the universal <=4-letter finite exhaustive lemma as an independently source-reviewed theorem;
- the broader candidate-v19 conclusion that depends on that finite lemma plus localization;
- Round 4 kernel sources or rerun claims that are not present in the repository;
- PR #9's broad carry-over audit conclusions for other research branches;
- any canonical-ledger promotion.

Those remain separate evidence. The exact Round 4 kernel/archive bytes are not present in the repository, so their computer-assisted result cannot be independently source-reviewed here.

## Known engineering limitation

The integrated verifier is byte-identical to the reviewed PR #9 verifier. Researcher D found nine malformed-input paths in which missing required keys raise raw `KeyError` instead of the verifier's controlled `ValueError`. No false mathematical certificate acceptance was found from this behavior, but malformed-input handling is not uniformly normalized.

A separate malformed-certificate corpus task tracks this interface hardening. This PR does not silently repair it because doing so would change the reviewed verifier blob.

## Source blob provenance

| File | PR #9 Git blob |
|---|---|
| `audits/verify_bigram_exact.py` | `private-history-omitted` |
| `tests/test_bigram_certificate_audit.py` | `private-history-omitted` |
| `audits/2026-10-11/fixtures/example_4letter_candidate.json` | `private-history-omitted` |
| `audits/2026-10-11/fixtures/example_4letter_result.json` | `private-history-omitted` |
| `audits/2026-10-11/fixtures/example_4letter_negative.json` | `private-history-omitted` |
| `audits/2026-10-11/fixtures/example_4letter_negative_result.json` | `private-history-omitted` |
| `audits/2026-10-11/fixtures/false_float_certificate.json` | `private-history-omitted` |

## Review record to reuse only if byte identity is confirmed

- Researcher B mathematical review of the direct certificate implication: PR #9 review `5483620461`.
- Researcher D execution/schema review: PR #9 head `private-history-omitted`, full evidence packet in PR #21.
- Researcher A/B later reviews of candidate-v19 localization are **not** needed for this focused verifier implication and do not convert the missing finite-kernel sources into independently reviewed proof.

Before merge, reviewers should confirm the copied blobs above still match their original PR #9 blob IDs and that this scope note does not overstate their prior reviews.
