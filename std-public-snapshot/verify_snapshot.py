#!/usr/bin/env python3
"""Verify the publication package against its content manifest."""
import hashlib
from pathlib import Path
import sys

root = Path(__file__).resolve().parent
failed = []
checked = 0
for line in (root / "SHA256SUMS").read_text().splitlines():
    expected, relative = line.split("  ", 1)
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        failed.append(relative)
        continue
    checked += 1
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failed.append(relative)
if failed:
    print("FAIL: " + ", ".join(failed))
    sys.exit(1)
print(f"PASS: {checked} file checksums")
