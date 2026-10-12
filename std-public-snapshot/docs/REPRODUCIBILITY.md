# Reproduce this snapshot

Extract the ZIP and open a terminal in `std-public-snapshot`. Use Python 3.12; the core uses only the standard library.

```bash
python verify_snapshot.py
python examples/quickstart.py
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
```

`verify_snapshot.py` checks every packaged file against `SHA256SUMS`. This manifest identifies this export's bytes, not a private Git commit. Run it before generating extra output files inside the snapshot.

The quickstart demonstrates identity H(2)=2, literal source histograms, and the cross-component H(1)=2 example. See [validation results](VALIDATION.json) for checks actually executed on this sanitized export. The suite excludes only tests of the omitted historical Git-checkout runner and recovered-archive provenance checker.

Additional demonstrations:

```bash
python experiments/reducible_support_example.py
python experiments/support_pair_certificate_experiment.py
python experiments/structural_reduction_certificates.py --check experiments/certificates/forced_continuation_2026-10-11.json
python verification/malformed_certificates/run_corpus.py
```

The corpus runner checks the bundled verifier and fixture integrity, then requires three accepted controls and eight controlled rejections. Its public-snapshot adapter does not require a private checkout. A crash is not a successful rejection. The support-pair reference solver has an eight-edge cap.

Execution evidence is not a universal theorem or independent mathematical review. A resource limit is not infeasibility. No collision within a finite bound does not establish sufficiency. Report the snapshot checksum, command, interpreter, exact input, observed output, and failed obligation when reporting an error.
