import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "verification/malformed_certificates"
MANIFEST = json.loads((CORPUS / "manifest.json").read_text())

SPEC = importlib.util.spec_from_file_location(
    "malformed_corpus_runner", CORPUS / "run_corpus.py"
)
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def case(case_id):
    entry = next(row for row in MANIFEST["cases"] if row["id"] == case_id)
    return entry, json.loads((ROOT / entry["path"]).read_text())


class MalformedCertificateCorpusTests(unittest.TestCase):
    def test_required_cases_present(self):
        ids = {row["id"] for row in MANIFEST["cases"]}
        required = {
            "accept_positive",
            "accept_negative",
            "accept_huge_exact_gauge",
            "reject_false_float_precision",
            "reject_bool_as_int",
            "reject_duplicate_coordinate",
            "reject_malformed_rational",
            "reject_invalid_source_index",
            "reject_silent_cycle",
            "reject_inconsistent_negative_metadata",
            "reject_missing_required_weight",
        }
        self.assertEqual(ids, required)

    def test_case_blob_hashes_and_metadata_match_manifest(self):
        for entry in MANIFEST["cases"]:
            with self.subTest(case=entry["id"]):
                data = (ROOT / entry["path"]).read_bytes()
                self.assertEqual(
                    runner.git_blob_sha1(data), entry["git_blob_sha1"]
                )
                doc = json.loads(data)
                self.assertEqual(doc["case_id"], entry["id"])
                self.assertEqual(doc["expected"], entry["expected"])

    def test_controls_prevent_universal_rejection(self):
        passes = [
            row for row in MANIFEST["cases"]
            if row["expected"]["outcome"] == "PASS"
        ]
        rejects = [
            row for row in MANIFEST["cases"]
            if row["expected"]["outcome"] == "REJECT"
        ]
        self.assertEqual(len(passes), 3)
        self.assertGreater(len(rejects), 0)

    def test_huge_gauge_is_exact_python_integer_10_pow_300(self):
        _, doc = case("accept_huge_exact_gauge")
        for rows in doc["answer"]["zero_cycle_potential"]:
            extras = [
                row for row in rows
                if row["pair"] == ["extra", "coordinate"]
            ]
            self.assertEqual(len(extras), 1)
            value = extras[0]["weight"]
            self.assertIs(type(value), int)
            self.assertEqual(value, 10**300)

    def test_false_float_case_contains_float_potential(self):
        _, doc = case("reject_false_float_precision")
        value = doc["answer"]["zero_cycle_potential"][0][0]["weight"]
        self.assertIs(type(value), float)
        self.assertEqual(value, 1e300)

    def test_bool_case_is_one_boolean_weight_mutation(self):
        _, doc = case("reject_bool_as_int")
        value = doc["answer"]["zero_cycle_potential"][1][0]["weight"]
        self.assertIs(type(value), bool)
        self.assertTrue(value)

    def test_duplicate_case_really_duplicates_coordinate(self):
        _, doc = case("reject_duplicate_coordinate")
        rows = doc["answer"]["coefficient_table"]["0"]
        pairs = [tuple(row["pair"]) for row in rows]
        self.assertLess(len(set(pairs)), len(pairs))

    def test_malformed_rational_case_uses_zero_denominator(self):
        _, doc = case("reject_malformed_rational")
        self.assertEqual(
            doc["answer"]["coefficient_table"]["0"][0]["coefficient"],
            "1/0",
        )

    def test_invalid_source_index_case_is_negative(self):
        _, doc = case("reject_invalid_source_index")
        self.assertEqual(doc["answer"]["witness"]["source_word"][0], -1)

    def test_silent_cycle_case_has_silence_from_both_states(self):
        _, doc = case("reject_silent_cycle")
        machine = doc["machine"]
        self.assertEqual(machine["output_words"][0][0], "")
        self.assertEqual(machine["output_words"][1][0], "")
        self.assertEqual(machine["flip"][0], 1)

    def test_negative_metadata_case_is_inconsistent(self):
        _, doc = case("reject_inconsistent_negative_metadata")
        witness = doc["answer"]["witness"]
        self.assertNotEqual(witness["source_length"], len(witness["source_word"]))

    def test_missing_weight_case_omits_required_key(self):
        _, doc = case("reject_missing_required_weight")
        self.assertNotIn(
            "weight", doc["answer"]["zero_cycle_potential"][1][0]
        )
        self.assertEqual(doc["expected"]["outcome"], "REJECT")

    def test_classifier_distinguishes_reject_from_crash(self):
        def reject(_machine, _answer):
            raise ValueError("bad input")

        def crash(_machine, _answer):
            raise KeyError("missing")

        self.assertEqual(
            runner.classify(reject, {}, {})["outcome"], "REJECT"
        )
        self.assertEqual(
            runner.classify(crash, {}, {})["outcome"], "CRASH"
        )

    def test_expected_reject_never_accepts_crash(self):
        expected = {"outcome": "REJECT"}
        actual = {"outcome": "CRASH", "exception": "KeyError"}
        self.assertFalse(runner.expected_matches(expected, actual))

    def test_output_path_inside_target_is_rejected_before_write(self):
        td = tempfile.TemporaryDirectory()
        try:
            target = Path(td.name).resolve()
            output = target / "corpus-result.json"
            with self.assertRaises(SystemExit):
                runner.reject_output_inside_target(output, target)
            self.assertFalse(output.exists())
        finally:
            td.cleanup()

    def test_output_path_outside_target_is_allowed(self):
        target_td = tempfile.TemporaryDirectory()
        output_td = tempfile.TemporaryDirectory()
        try:
            target = Path(target_td.name).resolve()
            output = Path(output_td.name).resolve() / "corpus-result.json"
            runner.reject_output_inside_target(output, target)
        finally:
            output_td.cleanup()
            target_td.cleanup()


if __name__ == "__main__":
    unittest.main()
