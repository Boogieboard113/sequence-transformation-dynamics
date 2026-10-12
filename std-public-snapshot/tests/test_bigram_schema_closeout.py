"""Issue #50: current-verifier schema checks; historical pinned artifacts unchanged.

The 55-case probe is exercised in normal and optimized Python, and the 11-case
corpus is checked *against the current patched verifier*, not against the old
SHA-pinned historical checkout required by run_corpus.py.
"""
import ast
from collections import UserDict
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from audits.verify_bigram_exact import verify
from verification.malformed_certificates.run_corpus import (
    classify, expected_matches,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "audits/2026-10-11/fixtures"
CORPUS = ROOT / "verification/malformed_certificates"
PROBE = ROOT / "verification/2026-10-11/pr9_schema_probe.py"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class BigramSchemaCloseoutTests(unittest.TestCase):
    def test_all_fourteen_required_key_paths_raise_value_error(self):
        cases = [
            ("positive", ("machine", "flip")),
            ("positive", ("machine", "output_words")),
            ("positive", ("answer", "status")),
            ("positive", ("answer", "zero_cycle_potential")),
            ("positive", ("answer", "coefficient_table")),
            ("negative", ("answer", "witness")),
            ("negative", ("answer", "witness", "source_word")),
            ("negative", ("answer", "witness", "start_state")),
            ("negative", ("answer", "witness", "output_from_start")),
            ("negative", ("answer", "witness", "output_from_other")),
            ("negative", ("answer", "witness", "histogram_difference")),
            ("positive", ("answer", "zero_cycle_potential", 1, 0, "weight")),
            ("positive", ("answer", "coefficient_table", "0", 0, "coefficient")),
            ("negative", ("answer", "witness", "histogram_difference", 0,
                          "count_difference")),
        ]
        self.assertEqual(len(cases), 14)
        for kind, path in cases:
            with self.subTest(kind=kind, path=path):
                machine = fixture("example_4letter_" +
                                  ("candidate" if kind == "positive" else "negative") +
                                  ".json")
                answer = fixture("example_4letter_" +
                                 ("result" if kind == "positive" else "negative_result") +
                                 ".json")
                values = {"machine": copy.deepcopy(machine),
                          "answer": copy.deepcopy(answer)}
                node = values
                for part in path[:-1]:
                    node = node[part]
                del node[path[-1]]
                with self.assertRaisesRegex(ValueError, "missing required field: " +
                                            str(path[-1])):
                    verify(values["machine"], values["answer"])

    def test_nonobject_required_container_fails_controlled(self):
        valid = fixture("example_4letter_candidate.json")
        answer = fixture("example_4letter_result.json")
        for value in (None, [], "wrong", 3):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    verify(value, answer)
                with self.assertRaises(ValueError):
                    verify(valid, value)

        negative = fixture("example_4letter_negative.json")
        neganswer = fixture("example_4letter_negative_result.json")
        for value in (None, [], "wrong", 3):
            with self.subTest(witness=value):
                altered = copy.deepcopy(neganswer)
                altered["witness"] = value
                with self.assertRaises(ValueError):
                    verify(negative, altered)

    def test_existing_mapping_inputs_still_accepted(self):
        positive_machine = fixture("example_4letter_candidate.json")
        positive_answer = fixture("example_4letter_result.json")
        negative_machine = fixture("example_4letter_negative.json")
        negative_answer = fixture("example_4letter_negative_result.json")
        self.assertEqual(
            verify(UserDict(positive_machine), UserDict(positive_answer))["kind"],
            "exact_H1",
        )
        negative_answer["witness"] = UserDict(negative_answer["witness"])
        self.assertEqual(
            verify(UserDict(negative_machine), UserDict(negative_answer))["kind"],
            "literal_infinite",
        )

    def test_existing_eleven_case_corpus_against_current_verifier(self):
        manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["cases"]), 11)
        count = {"PASS": 0, "REJECT": 0, "CRASH": 0}
        for entry in manifest["cases"]:
            with self.subTest(case=entry["id"]):
                case = json.loads((ROOT / entry["path"]).read_text(encoding="utf-8"))
                self.assertEqual(case["expected"], entry["expected"])
                actual = classify(verify, case["machine"], case["answer"])
                count[actual["outcome"]] += 1
                self.assertTrue(expected_matches(entry["expected"], actual), actual)
        self.assertEqual(count, {"PASS": 3, "REJECT": 8, "CRASH": 0})

    def test_fifty_five_case_probe_normal_and_optimized(self):
        outcomes = []
        for args in ([], ["-O"]):
            with self.subTest(optimize=bool(args)):
                cp = subprocess.run(
                    [sys.executable, *args, str(PROBE), str(ROOT)],
                    cwd=ROOT, capture_output=True, text=True, check=True,
                )
                self.assertEqual(cp.stderr, "")
                data = json.loads(cp.stdout)
                self.assertEqual(data["case_count"], 55)
                self.assertEqual(data["summary"],
                                 {"PASS": 9, "REJECT": 46, "CRASH": 0})
                outcomes.append(data["results"])
        self.assertEqual(outcomes[0], outcomes[1])

    def test_verifier_has_no_optimizer_removed_assert_statements(self):
        source = (ROOT / "audits/verify_bigram_exact.py").read_text(encoding="utf-8")
        self.assertFalse(any(isinstance(node, ast.Assert)
                             for node in ast.walk(ast.parse(source))))


if __name__ == "__main__":
    unittest.main()
