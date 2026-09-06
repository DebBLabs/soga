import subprocess
import sys
import unittest
from pathlib import Path

from scripts.run_m01_physical import authorization_is_recorded


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_m01_physical.py"


class M01PhysicalRunnerTests(unittest.TestCase):
    def run_runner(self, authorization):
        return subprocess.run(
            [
                sys.executable,
                str(RUNNER),
                "--api-base-url",
                "http://127.0.0.1:1/api",
                "--authorization",
                authorization,
            ],
            cwd=ROOT,
            input="",
            text=True,
            capture_output=True,
            timeout=3,
            check=False,
        )

    def test_wrong_authorization_blocks_before_network(self):
        result = self.run_runner("NOT-AUTHORIZED")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("D-032 is required", result.stderr)

    def test_decision_record_check_is_independent_of_live_repository_state(self):
        self.assertFalse(authorization_is_recorded("## D-031 — prior decision only"))
        self.assertTrue(authorization_is_recorded("## D-032 — authorized test decision"))

    def test_recorded_authorization_still_requires_terminal_confirmation(self):
        result = self.run_runner("D-032")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("confirmation mismatch", result.stderr)
        self.assertIn("Type EXECUTE", result.stdout)


if __name__ == "__main__":
    unittest.main()
