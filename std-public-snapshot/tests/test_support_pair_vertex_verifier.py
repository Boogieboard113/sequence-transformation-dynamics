import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFIER_PATH = ROOT / "verification" / "support_pair_vertex_verifier.py"
FIXTURE_DIR = ROOT / "verification" / "support_pair_vertex_fixtures"
FIXTURE_PATH = FIXTURE_DIR / "pr81_fractional_vertex.json"
EXPECTED_PATH = FIXTURE_DIR / "pr81_fractional_vertex.expected.json"

SPEC = importlib.util.spec_from_file_location("support_pair_vertex_verifier", VERIFIER_PATH)
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def fixture():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


class SupportPairVertexVerifierTests(unittest.TestCase):
    def test_candidate_fractional_vertex_and_literal_witness(self):
        result = verifier.verify_certificate(fixture())
        expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        self.assertEqual(result, expected)
        self.assertEqual(result["basis_determinant"], "-2")
        self.assertEqual(result["common_denominator"], 2)
        self.assertEqual(result["integer_witness"]["source_length_s"], 22)
        self.assertEqual(result["integer_witness"]["source_length_t"], 22)

    def test_false_denominator_rejected(self):
        doc = fixture()
        doc["claimed_denominator"] = 1
        with self.assertRaisesRegex(ValueError, "minimal common"):
            verifier.verify_certificate(doc)

    def test_altered_rational_coordinate_rejected(self):
        doc = fixture()
        doc["point_s"]["001"] = "3"
        with self.assertRaises(ValueError):
            verifier.verify_certificate(doc)

    def test_feasible_scaled_interior_point_is_not_vertex(self):
        doc = fixture()
        for field in ("point_s", "point_t"):
            for edge, value in list(doc[field].items()):
                doc[field][edge] = str(2 * verifier.exact_rational(value))
        doc["claimed_denominator"] = 1
        doc.pop("active_basis")
        doc.pop("integer_witness")
        with self.assertRaisesRegex(ValueError, "not a vertex"):
            verifier.verify_certificate(doc)

    def test_nontight_active_basis_row_rejected(self):
        doc = fixture()
        doc["active_basis"][-2] = "lower_s:000"
        with self.assertRaisesRegex(ValueError, "not tight"):
            verifier.verify_certificate(doc)

    def test_wrong_integer_scale_rejected(self):
        doc = fixture()
        doc["integer_witness"]["scale"] = 4
        with self.assertRaisesRegex(ValueError, "minimal common denominator"):
            verifier.verify_certificate(doc)

    def test_bad_literal_source_rejected(self):
        doc = fixture()
        doc["integer_witness"]["source_s"] += "0"
        with self.assertRaisesRegex(ValueError, "wrapped edge histogram"):
            verifier.verify_certificate(doc)

    def test_malformed_rational_rejected(self):
        doc = fixture()
        doc["point_s"]["001"] = "5/0"
        with self.assertRaisesRegex(ValueError, "exact rational"):
            verifier.verify_certificate(doc)

    def test_float_and_bool_rejected(self):
        doc = fixture()
        doc["point_s"]["001"] = 2.5
        with self.assertRaisesRegex(ValueError, "exact rational"):
            verifier.verify_certificate(doc)

        doc = fixture()
        doc["sign"] = True
        with self.assertRaisesRegex(ValueError, "exact integer"):
            verifier.verify_certificate(doc)

    def test_unknown_target_edge_rejected(self):
        doc = fixture()
        doc["target_row"]["111"] = 1
        with self.assertRaisesRegex(ValueError, "unknown edge"):
            verifier.verify_certificate(doc)

    def test_no_solver_or_generator_import(self):
        tree = ast.parse(VERIFIER_PATH.read_text(encoding="utf-8"))
        imported = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.append(node.module)
        self.assertFalse(any(name.startswith("experiments") for name in imported))

    def test_normal_and_optimized_cli_are_identical(self):
        normal = subprocess.run(
            [sys.executable, str(VERIFIER_PATH), str(FIXTURE_PATH)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        optimized = subprocess.run(
            [sys.executable, "-O", str(VERIFIER_PATH), str(FIXTURE_PATH)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(normal.returncode, 0, normal.stderr.decode())
        self.assertEqual(optimized.returncode, 0, optimized.stderr.decode())
        self.assertEqual(normal.stdout, optimized.stdout)
        parsed = json.loads(normal.stdout)
        expected = json.loads(EXPECTED_PATH.read_text(encoding="utf-8"))
        self.assertEqual(parsed, expected)


if __name__ == "__main__":
    unittest.main()
