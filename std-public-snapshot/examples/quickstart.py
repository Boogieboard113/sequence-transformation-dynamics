"""Run from repository root: python examples/quickstart.py.

Literal examples are witnesses, not a substitute for the cited sufficiency proof.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from std_tools.cyclic import cyclic_block_counts
from std_tools.sft_closure import exact_horizon_irreducible
from experiments.reducible_support_example import verify_example


def readable_counts(word, order):
    return {"".join(k): v for k, v in sorted(cyclic_block_counts(word, order).items())}


def main():
    x, y = "0011", "0101"
    if cyclic_block_counts(x, 1) != cyclic_block_counts(y, 1):
        raise RuntimeError("source-symbol collision failed")
    if cyclic_block_counts(x, 2) == cyclic_block_counts(y, 2):
        raise RuntimeError("output-pair discrepancy failed")
    horizon = exact_horizon_irreducible(
        alphabet="01", allowed_m={"0", "1"}, m=1,
        radius=0, emit=lambda context: context, k=2,
    )
    if horizon != 2:
        raise RuntimeError("identity horizon must be two")
    print("Identity rule; all nonempty binary cyclic sources")
    for word in (x, y):
        print(f"  {word}: C1={readable_counts(word, 1)}; C2={readable_counts(word, 2)}")
    print(f"  Exact H(2) = {horizon}")
    cross = verify_example()
    if cross["exact_horizon_k1"] != 2:
        raise RuntimeError("cross-component example changed")
    print("Reviewed two-component radius-2 emission example")
    print("  0011 -> aaaa; 0101 -> bbbb; equal source C1, different output C1")
    print("  Exact H(1) = 2; source C2(00) separates the components")


if __name__ == "__main__":
    main()
