#!/usr/bin/env python3
"""Check the bundled verifier and malformed-certificate corpus."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = Path(__file__).with_name("manifest.json")


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def path_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def reject_output_inside_target(output_path: Path | None, target: Path) -> None:
    if output_path is not None and path_within(output_path, target):
        raise SystemExit(
            f"output path {output_path} is inside pinned target checkout {target}"
        )


def load_verifier(target: Path, verifier_spec: dict):
    path = target / verifier_spec["path"]
    if not path.is_file():
        raise RuntimeError("bundled verifier is missing")
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_hash != verifier_spec["sha256"]:
        raise RuntimeError("bundled verifier checksum mismatch")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("snapshot_std_exact_verifier", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load verifier module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    verify = getattr(module, "verify", None)
    if not callable(verify):
        raise RuntimeError("verifier module has no callable verify")
    return verify, "sanitized-snapshot", actual_hash


def classify(verify, machine: dict, answer: dict) -> dict:
    try:
        result = verify(machine, answer)
    except ValueError as exc:
        return {
            "outcome": "REJECT",
            "exception": "ValueError",
            "reason": str(exc),
        }
    except Exception as exc:
        return {
            "outcome": "CRASH",
            "exception": type(exc).__name__,
            "reason": str(exc),
        }
    return {
        "outcome": "PASS",
        "kind": result.get("kind") if isinstance(result, dict) else None,
    }


def expected_matches(expected: dict, actual: dict) -> bool:
    if actual.get("outcome") != expected.get("outcome"):
        return False
    if expected.get("outcome") == "PASS" and "kind" in expected:
        if actual.get("kind") != expected["kind"]:
            return False
    if expected.get("outcome") == "REJECT" and "reason_regex" in expected:
        if re.search(expected["reason_regex"], actual.get("reason", "")) is None:
            return False
    return True


def load_cases(manifest: dict) -> list[tuple[dict, dict]]:
    result = []
    for entry in manifest["cases"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            raise RuntimeError(f"corpus case missing: {entry['path']}")
        data = path.read_bytes()
        actual_blob = git_blob_sha1(data)
        if actual_blob != entry["git_blob_sha1"]:
            raise RuntimeError(
                f"corpus blob mismatch for {entry['id']}: "
                f"expected {entry['git_blob_sha1']}, got {actual_blob}"
            )
        case = json.loads(data)
        if case.get("case_id") != entry["id"]:
            raise RuntimeError(f"case id mismatch in {entry['path']}")
        if case.get("expected") != entry["expected"]:
            raise RuntimeError(f"expected-outcome mismatch in {entry['path']}")
        result.append((entry, case))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default=str(ROOT), help="snapshot directory")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != 1:
        raise SystemExit("unsupported corpus manifest schema")

    target = Path(args.target).resolve()
    if not target.is_dir():
        raise SystemExit(f"target checkout not found: {target}")
    output_path = Path(args.output).resolve() if args.output else None
    reject_output_inside_target(output_path, target)

    try:
        verify, actual_commit, actual_blob = load_verifier(
            target, manifest["verifier"]
        )
        cases = load_cases(manifest)
    except RuntimeError as exc:
        summary = {
            "status": "RUNNER_ERROR",
            "reason": str(exc),
            "optimize": sys.flags.optimize,
        }
        encoded = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
        if output_path:
            output_path.write_bytes(encoded)
        else:
            sys.stdout.buffer.write(encoded)
        return 2

    results = []
    for entry, case in cases:
        actual = classify(verify, case["machine"], case["answer"])
        results.append(
            {
                "id": entry["id"],
                "expected": entry["expected"],
                "actual": actual,
                "matched": expected_matches(entry["expected"], actual),
            }
        )

    post_dirty = []
    runner_error = post_dirty is None or bool(post_dirty)
    summary = {
        "status": (
            "PASS"
            if not runner_error and all(row["matched"] for row in results)
            else "CORPUS_MISMATCH"
        ),
        "snapshot": actual_commit,
        "verifier_sha256": actual_blob,
        "optimize": sys.flags.optimize,
        "case_count": len(results),
        "matched_count": sum(row["matched"] for row in results),
        "mismatch_count": sum(not row["matched"] for row in results),
        "results": results,
    }
    if post_dirty:
        summary["post_run_dirty_paths"] = post_dirty
        summary["status"] = "RUNNER_ERROR"

    encoded = (json.dumps(summary, indent=2, sort_keys=True) + "\n").encode()
    if output_path:
        output_path.write_bytes(encoded)
    else:
        sys.stdout.buffer.write(encoded)
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
