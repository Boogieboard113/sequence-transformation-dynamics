"""Acceptance and adversarial tests; calls remain active under python -O."""
import copy
import json
from pathlib import Path
import unittest

from audits.verify_bigram_exact import raw2, verify

FIXTURES = Path(__file__).resolve().parents[1] / 'audits/2026-10-11/fixtures'


def read(name):
    return json.loads((FIXTURES / name).read_text())


class BigramCertificateAudit(unittest.TestCase):
    def setUp(self):
        self.machine = read('example_4letter_candidate.json')
        self.answer = read('example_4letter_result.json')
        self.negative = read('example_4letter_negative.json')
        self.witness = read('example_4letter_negative_result.json')
        self.false = read('false_float_certificate.json')

    def test_valid_positive_direct_H1(self):
        result = verify(self.machine, self.answer)
        self.assertEqual(result['kind'], 'exact_H1')
        self.assertEqual(result['checked_hidden_edges'], 128)
        self.assertEqual(result['checked_source_edges'], 64)

    def test_valid_negative(self):
        self.assertEqual(verify(self.negative, self.witness)['kind'], 'literal_infinite')

    def test_float_false_positive_rejected(self):
        with self.assertRaisesRegex(ValueError, 'exact integer'):
            verify(self.false['machine'], self.false['answer'])

    def test_false_machine_has_actual_same_source_disagreement(self):
        machine = self.false['machine']
        outputs = []
        for start in (0, 1):
            q, output = start, ''
            for letter in (0, 1):
                output += machine['output_words'][q][letter]
                q ^= machine['flip'][letter]
            self.assertEqual(q, start)
            outputs.append(output)
        self.assertEqual(outputs, ['1', '00'])
        self.assertNotEqual(raw2(outputs[0]), raw2(outputs[1]))

    def test_huge_integer_false_certificate_rejected(self):
        for rows in self.false['answer']['zero_cycle_potential']:
            for row in rows:
                row['weight'] = 10**300
        with self.assertRaisesRegex(ValueError, 'hidden-state edge residual'):
            verify(self.false['machine'], self.false['answer'])

    def test_huge_integer_valid_gauge_shift_accepted(self):
        for rows in self.answer['zero_cycle_potential']:
            rows.append({'pair': ['extra', 'coordinate'], 'weight': 10**300})
        self.assertEqual(verify(self.machine, self.answer)['kind'], 'exact_H1')

    def test_inexact_potentials_rejected(self):
        for number in (1.0, True, float('inf'), float('nan')):
            with self.subTest(number=number):
                answer = copy.deepcopy(self.answer)
                answer['zero_cycle_potential'][0].append({'pair': ['X', 'X'], 'weight': number})
                with self.assertRaises(ValueError):
                    verify(self.machine, answer)

    def test_wrong_exact_potential_rejected(self):
        self.answer['zero_cycle_potential'][0].append({'pair': ['X', 'X'], 'weight': 1})
        with self.assertRaisesRegex(ValueError, 'hidden-state edge residual'):
            verify(self.machine, self.answer)

    def test_coefficients_require_exact_values(self):
        for value in (1.0, True, '999'):
            with self.subTest(value=value):
                answer = copy.deepcopy(self.answer)
                answer['coefficient_table']['0'][0]['coefficient'] = value
                with self.assertRaises(ValueError):
                    verify(self.machine, answer)

    def test_duplicate_coordinate_rejected(self):
        self.answer['coefficient_table']['0'] *= 2
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            verify(self.machine, self.answer)

    def test_machine_schema_rejected(self):
        for flips in ([], [2, 1, 0, 1], [True, 1, 0, 1], [1.0, 1, 0, 1]):
            with self.subTest(flips=flips):
                machine = copy.deepcopy(self.machine)
                machine['flip'] = flips
                with self.assertRaises(ValueError):
                    verify(machine, self.answer)

    def test_silent_cycle_rejected(self):
        self.machine['output_words'][1][0] = ''
        with self.assertRaisesRegex(ValueError, 'acyclic silent graph'):
            verify(self.machine, self.answer)

    def test_false_negative_header_rejected(self):
        self.witness['H_T(2)'] = 1
        with self.assertRaisesRegex(ValueError, 'header'):
            verify(self.negative, self.witness)

    def test_false_witness_metadata_rejected(self):
        for field in ('source_length', 'length_bound'):
            answer = copy.deepcopy(self.witness)
            answer['witness'][field] += 1
            with self.assertRaisesRegex(ValueError, field):
                verify(self.negative, answer)

    def test_negative_source_indices_rejected(self):
        self.witness['witness']['source_word'][0] = -1
        with self.assertRaisesRegex(ValueError, 'invalid source'):
            verify(self.negative, self.witness)

    def test_false_output_rejected(self):
        self.witness['witness']['output_from_start'] = []
        with self.assertRaisesRegex(ValueError, 'output mismatch'):
            verify(self.negative, self.witness)

    def test_false_histogram_rejected(self):
        self.witness['witness']['histogram_difference'][0]['count_difference'] += 1
        with self.assertRaisesRegex(ValueError, 'histogram discrepancy'):
            verify(self.negative, self.witness)


if __name__ == '__main__':
    unittest.main()
