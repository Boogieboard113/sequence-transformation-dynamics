#!/usr/bin/env python3
"""Exact per-instance checker for Round 4 two-state bigram certificates.

Scope: total permutation machines, at least one erasure, acyclic silent graph,
all nonempty closed cyclic runs, and raw cyclic output bigram counts. Words
are strings or lists of string tokens. Potentials are integers; coefficients
are integers or rational strings. No classifier or enumeration is imported.

Unlike the original Round 4 verifier, positive answers are checked against a
source telescoping identity as well as hidden-state invariance. Acceptance
therefore does not depend on the exhaustive four-letter structural lemma.
See audits/2026-10-11/STD_Audit_2026-10-11.md for the argument and original defect.
"""
from collections import Counter
from collections.abc import Mapping
from fractions import Fraction
from itertools import product
import json
import re
import sys


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def required(mapping, field):
    """Read a required object key with a controlled schema rejection."""
    require(isinstance(mapping, Mapping), 'required field belongs to an object')
    require(field in mapping, 'missing required field: ' + field)
    return mapping[field]


def combine(*terms):
    """Signed sparse vector sum, preserving negative coordinates exactly."""
    result = Counter()
    for scale, vector in terms:
        for pair, value in vector.items():
            result[pair] += scale * value
    return {pair: value for pair, value in result.items() if value}


def raw2(word):
    return Counter((word[i], word[(i + 1) % len(word)])
                   for i in range(len(word)))


def integer(value):
    require(type(value) is int, 'expected an exact integer, not float or bool')
    return value


def rational(value):
    if type(value) is int:
        return Fraction(value)
    require(type(value) is str and
            re.fullmatch(r'[+-]?\d+(?:/[1-9]\d*)?', value) is not None,
            'expected an integer or exact rational string')
    return Fraction(value)


def vector(rows, field, parse):
    require(type(rows) is list, 'coordinate rows must be a list')
    result = {}
    seen = set()
    for row in rows:
        require(type(row) is dict, 'coordinate row must be an object')
        pair = row.get('pair')
        require(type(pair) is list and len(pair) == 2 and
                all(type(token) is str for token in pair), 'invalid output pair')
        pair = tuple(pair)
        require(pair not in seen, 'duplicate output pair')
        seen.add(pair)
        value = parse(required(row, field))
        if value:
            result[pair] = value
    return result


def verify(machine, answer):
    flip = required(machine, 'flip')
    words = required(machine, 'output_words')
    require(type(flip) is list and len(flip) > 0 and
            all(type(x) is int and x in (0, 1) for x in flip), 'invalid flips')
    n = len(flip)
    require(type(words) is list and len(words) == 2 and
            all(type(row) is list and len(row) == n for row in words),
            'expected two emission rows of alphabet size')
    W = {}
    for q, x in product(range(2), range(n)):
        word = words[q][x]
        require(type(word) in (str, list) and
                all(type(token) is str for token in word), 'invalid emission word')
        W[q, x] = tuple(word)
    silent = [(q, x) for q, x in W if not W[q, x]]
    require(len({q for q, x in silent}) == 1 and
            all(flip[x] == 1 for q, x in silent),
            'requires at least one erasure and an acyclic silent graph')

    def emit(source, q):
        start, output = q, []
        for x in source:
            output.extend(W[q, x])
            q ^= flip[x]
        require(q == start, 'source word does not close')
        return output

    status = required(answer, 'status')
    if status == 'infinite':
        require(answer.get('H_T(2)') == 'infinity', 'bad infinite claim header')
        witness = required(answer, 'witness')
        source, q = required(witness, 'source_word'), required(witness, 'start_state')
        require(type(source) is list and 0 < len(source) <= 2*n*n and
                all(type(x) is int and 0 <= x < n for x in source),
                'invalid source word or length outside certified bound')
        require(type(q) is int and q in (0, 1), 'invalid starting state')
        for field, expected in [('source_length', len(source)), ('length_bound', 2*n*n)]:
            if field in witness:
                require(integer(witness[field]) == expected, 'wrong ' + field)
        U, V = emit(source, q), emit(source, 1-q)
        require(U == required(witness, 'output_from_start') and
                V == required(witness, 'output_from_other'),
                'claimed output mismatch')
        delta = combine((1, raw2(U)), (-1, raw2(V)))
        reported = vector(required(witness, 'histogram_difference'), 'count_difference', integer)
        require(bool(delta) and delta == reported, 'claimed histogram discrepancy mismatch or zero')
        return {'result': 'PASS', 'kind': 'literal_infinite', 'witness_length': len(source)}

    require(status == 'finite' and type(answer.get('H_T(2)')) is int and
            answer['H_T(2)'] == 1, 'bad finite claim header')
    rows = required(answer, 'zero_cycle_potential')
    require(type(rows) is list and len(rows) == 2*n*n, 'wrong potential vertex count')
    potential = [vector(row, 'weight', integer) for row in rows]
    table = required(answer, 'coefficient_table')
    require(type(table) is dict and set(table) == {str(x) for x in range(n)},
            'wrong coefficient table source alphabet')
    twice = {}
    for x in range(n):
        if flip[x]:
            expected = {pair: Fraction(count, 2)
                        for pair, count in raw2(W[0, x] + W[1, x]).items()}
        else:
            require(raw2(W[0, x]) == raw2(W[1, x]), 'identity letter outputs disagree')
            expected = {pair: Fraction(count) for pair, count in raw2(W[0, x]).items()}
        reported = vector(table[str(x)], 'coefficient', rational)
        require(reported == expected, 'source-one coefficient table incorrect')
        twice[x] = {pair: int(2*count) for pair, count in expected.items()}

    local = {}
    for q, x, y, z in product(range(2), range(n), range(n), range(n)):
        word = W[q, x]
        counts = Counter(zip(word, word[1:]))
        if word:
            q1 = q ^ flip[x]
            nxt = W[q1, y] or W[q1 ^ flip[y], z]
            require(bool(nxt), 'consecutive erasures outside scope')
            counts[word[-1], nxt[0]] += 1
        local[q, x, y, z] = counts
    for q, x, y, z in local:
        u, v = q*n*n+x*n+y, (q ^ flip[x])*n*n+y*n+z
        residual = combine((1, potential[u]), (1, local[q, x, y, z]),
                           (-1, local[1-q, x, y, z]), (-1, potential[v]))
        require(not residual, 'nonzero hidden-state edge residual')

    total = {(x, y, z): combine((1, local[0, x, y, z]), (1, local[1, x, y, z]))
             for x, y, z in product(range(n), repeat=3)}
    # Integrate the path (a,a) -> (a,x) -> (x,y), choosing a=0.
    phi = {(x, y): combine((1, total[0, 0, x]), (1, total[0, x, y]), (-2, twice[0]))
           for x, y in product(range(n), repeat=2)}
    for x, y, z in total:
        residual = combine((1, phi[x, y]), (1, total[x, y, z]),
                           (-1, twice[x]), (-1, phi[y, z]))
        require(not residual, 'nonzero source H=1 edge residual')
    return {'result': 'PASS', 'kind': 'exact_H1', 'checked_hidden_edges': 2*n**3,
            'checked_source_edges': n**3, 'verified_coefficients': n,
            'H1_dependency': 'directly checked telescoping identities'}


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('python audits/verify_bigram_exact.py machine.json result.json')
    with open(sys.argv[1], encoding='utf-8') as file:
        machine = json.load(file)
    with open(sys.argv[2], encoding='utf-8') as file:
        answer = json.load(file)
    print(json.dumps(verify(machine, answer), indent=2))
