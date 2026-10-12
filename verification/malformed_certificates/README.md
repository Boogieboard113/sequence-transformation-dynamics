# Exact malformed-certificate corpus

Run `python verification/malformed_certificates/run_corpus.py` from the snapshot root.

The runner checks the SHA-256 of the included exact verifier and the content checksums of all eleven fixtures before import and execution. The fixture `git_blob_sha1` fields are content-only checksums; they contain no Git history or author metadata.

Three controls must pass. Eight malformed cases must raise `ValueError`: float and bool weights, duplicate coordinates, malformed rationals, invalid source indices, a silent cycle, inconsistent negative metadata, and a missing required weight. Unexpected exceptions are classified as crashes and fail the run.

This is a snapshot-local adapter of the historical corpus infrastructure. It validates the included repaired verifier; it does not claim reproduction of an omitted private commit or verification of a general mathematical theorem.
