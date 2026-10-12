import subprocess
import sys
import unittest
from pathlib import Path


class SupportPairPacketReproduction(unittest.TestCase):
    def test_committed_packet_regenerates_byte_for_byte(self):
        root = Path(__file__).resolve().parents[1]
        experiment = root / "experiments" / "support_pair_certificate_experiment.py"
        expected = root / "experiments" / "data" / "support_pair_certificates_2026-10-11.json"
        completed = subprocess.run(
            [sys.executable, str(experiment)],
            cwd=root,
            check=True,
            capture_output=True,
        )
        self.assertEqual(completed.stderr, b"")
        self.assertEqual(completed.stdout, expected.read_bytes())


if __name__ == "__main__":
    unittest.main()
