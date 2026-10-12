"""Reproducible exact small certificates for the cyclic reduction theorem.

Run from repository root: python experiments/structural_reduction_certificates.py
Write: python experiments/structural_reduction_certificates.py --write FILE
Check: python experiments/structural_reduction_certificates.py --check FILE
All arithmetic and enumeration are exact. Standard library only.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

# A direct ``python experiments/...`` invocation puts only experiments/ on
# sys.path; make the documented repository-root command work without an
# environment variable or package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from std_tools.structural_reduction import (
    all_attainable, cyclic_class, erased_max_from_reduction,
    exact_pattern_bounds, lift_edges, raw_histogram, reduce_histogram,
    reduced_circuits, source_from_edges, emission_of_edges,
)


def serialize(red):
    return {
        'kind': red.kind,
        'histogram': dict(sorted(red.histogram.items())),
        'branches': list(red.branches),
        'macros': {
            k: {'start': v.start, 'end': v.end, 'path': list(v.path),
                'multiplicity': v.count}
            for k, v in sorted(red.macros.items())
        },
        'period': list(red.cycle),
        'period_repetitions': red.copies,
    }


def make_certificates():
    hist = {'00': 2, '01': 2, '10': 2}
    emission = {'00': '0', '01': '0', '10': '1'}
    red = reduce_histogram(hist)
    witnesses = {}
    circuits = list(reduced_circuits(red))
    for circuit in circuits:
        edges = lift_edges(red, circuit)
        word = source_from_edges(red, edges)
        output = emission_of_edges(edges, emission)
        key = cyclic_class(output)
        if key not in witnesses:
            witnesses[key] = {
                'macro_tour': list(circuit), 'source_word': word,
                'output_word': output,
                'C3_000': raw_histogram(output, 3)['000'],
                'C3_001': raw_histogram(output, 3)['001'],
            }
    assert set(witnesses) == {'000101', '001001'}
    assert exact_pattern_bounds(red, emission, ['000', '001']) == {
        '000': (0, 1), '001': (1, 2)}

    merge_hist = {'000': 2, '001': 1, '010': 2, '100': 1, '101': 1}
    merged = reduce_histogram(merge_hist)
    coverage = Counter()
    for macro in merged.macros.values():
        for e in macro.path:
            coverage[e] += macro.count
    assert coverage == merge_hist

    erase = reduce_histogram({'0': 2, '1': 2})
    silence = {'0': '', '1': 'x'}
    erase_witnesses = {}
    for c in reduced_circuits(erase):
        maximum = erased_max_from_reduction(erase, c, silence)
        erase_witnesses.setdefault(str(maximum), {
            'macro_tour': list(c), 'source_word': source_from_edges(erase, lift_edges(erase, c))})
    assert set(erase_witnesses) == {'1', '2'}
    assert all_attainable(erase, silence, erase_cap=1) == {'xx'}

    periodic = reduce_histogram({'01': 2, '10': 2})
    assert all_attainable(periodic, {'01': 'a', '10': 'b'}) == {'abab'}
    disconnected = reduce_histogram({'00': 1, '11': 1})
    assert disconnected.kind == 'infeasible'

    return {
        'version': 1,
        'date': '2026-10-11',
        'purpose': 'Exact executable witness certificates; not formal proof.',
        'different_exact_C3_bounds': {
            'reduction': serialize(red),
            'macro_circuits_with_fixed_anchor': len(circuits),
            'cyclic_output_witnesses': dict(sorted(witnesses.items())),
            'raw_output_pattern_bounds': {
                k: list(v) for k, v in exact_pattern_bounds(red, emission, ['000', '001']).items()
            },
            'cyclic_avoid_000': sorted(all_attainable(red, emission,
                                                     forbidden_blocks={'000'})),
        },
        'merge_shared_forced_type': {
            'reduction': serialize(merged),
            'original_edges': 7, 'reduced_macro_traversals': 5,
            'path_type_coverage': dict(sorted(coverage.items())),
            'shared_010_macros': ['001', '101'],
        },
        'erasure_cap': {
            'histogram': {'0': 2, '1': 2},
            'silence_run_witnesses': dict(sorted(erase_witnesses.items())),
            'cyclic_outputs_at_cap_1': sorted(all_attainable(erase, silence, 1)),
            'cyclic_outputs_at_cap_0': sorted(all_attainable(erase, silence, 0)),
        },
        'pure_cycle': {
            'reduction': serialize(periodic),
            'cyclic_outputs': sorted(all_attainable(periodic, {'01': 'a', '10': 'b'})),
        },
        'disconnected_balanced_support': serialize(disconnected),
        'rooted_cut_counterexample': {
            'rooted_outputs': sorted(all_attainable(reduce_histogram({'0': 1}),
                                                  {'0': 'ab'}, rooted=True)),
            'invalid_arbitrary_output_cut': 'ba',
        },
    }


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--write', metavar='PATH')
    group.add_argument('--check', metavar='PATH')
    args = parser.parse_args()
    content = json.dumps(make_certificates(), indent=2, sort_keys=True) + '\n'
    if args.write:
        Path(args.write).parent.mkdir(parents=True, exist_ok=True)
        Path(args.write).write_text(content, encoding='utf-8')
        print('wrote', args.write)
    elif args.check:
        actual = Path(args.check).read_text(encoding='utf-8')
        if content != actual:
            raise SystemExit('certificate mismatch: ' + args.check)
        print('exact certificate matches', args.check)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
