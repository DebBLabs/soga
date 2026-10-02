"""Static-only checks for the D-118 recovery and portability package."""

import ast
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[1]
RESTORE = REPO / "tools/m02_aauth_fcf656d/restore_demo_runtime.py"
LOCALHOST = REPO / "tools/m02_aauth_fcf656d/run_localhost_gateway_tests.py"
MANIFEST = REPO / "knowledge/working/EXTERNAL_INPUT_MANIFEST.md"


class DemoRuntimeRecoveryStaticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.restore_text = RESTORE.read_text(encoding="utf-8")
        cls.localhost_text = LOCALHOST.read_text(encoding="utf-8")
        cls.manifest_text = MANIFEST.read_text(encoding="utf-8")
        cls.restore_tree = ast.parse(cls.restore_text)
        cls.localhost_tree = ast.parse(cls.localhost_text)

    def test_no_personal_or_private_tmp_runtime_paths(self):
        combined = self.restore_text + self.localhost_text + self.manifest_text
        self.assertNotIn("/Users/debb", combined)
        self.assertNotIn("/private/tmp", combined)

    def test_durable_root_is_repository_sibling(self):
        self.assertIn('EVIDENCE_PARENT = REPO.parent / "research-evidence"',
                      self.restore_text)
        self.assertIn('DURABLE_ROOT = EVIDENCE_PARENT / "soga"', self.restore_text)
        self.assertIn('DURABLE_ROOT = REPO.parent / "research-evidence/soga"',
                      self.localhost_text)

    def test_exact_four_wheels_and_no_dynamic_arguments(self):
        self.assertEqual(self.restore_text.count("https://files.pythonhosted.org/packages/"), 4)
        self.assertIn('require(len(sys.argv) == 1', self.restore_text)
        self.assertNotIn("argparse", self.restore_text)

    def test_zero_redirect_and_finite_network_controls(self):
        for required in ("redirect refused", "CONNECT_TIMEOUT = 15",
                         "ARTIFACT_TIMEOUT = 120", "READ_MARGIN = 65_536",
                         "network prohibited after acquisition"):
            self.assertIn(required, self.restore_text)

    def test_pinned_environment_and_install_controls(self):
        for required in ('EXPECTED_PYTHON = "3.9.6"', 'EXPECTED_PLATFORM = "darwin"',
                         'EXPECTED_MACHINE = "arm64"', 'EXPECTED_PIP = "21.2.4"',
                         'EXPECTED_EXECUTABLE = (',
                         '"--no-index"', '"--no-deps"', '"--only-binary=:all:"',
                         '"--no-cache-dir"', '"--no-compile"'):
            self.assertIn(required, self.restore_text)

    def test_runtime_target_must_not_preexist(self):
        self.assertIn('require(not WHEEL_ROOT.exists()', self.restore_text)
        self.assertIn('"recovery target already exists"', self.restore_text)

    def test_failure_evidence_and_symlink_ancestor_guards_present(self):
        for required in ("class RetrievalError", 'record["wheel_retrievals"].append(error.record)',
                         'filename + ".UNVERIFIED"', "durable path component is unsafe"):
            self.assertIn(required, self.restore_text)

    def test_record_symlink_and_scratch_guards_present(self):
        for required in ("verify_record", "unaccounted installed file",
                         "installed tree contains symlink", 'entries[0].name == "xcrun_db"',
                         'item["size"] <= 4096'):
            self.assertIn(required, self.restore_text)

    def test_localhost_claim_controls_retained(self):
        for required in ("EXPECTED_TEST_COUNT = 53", "TIMEOUT_SECONDS = 90",
                         "STREAM_LIMIT_BYTES = 2_000_000", 'address[0] != "127.0.0.1"',
                         'event == "socket.bind" and address[1] != 0',
                         "ALLOWED_STDERR_SHA256"):
            self.assertIn(required, self.localhost_text)

    def test_localhost_requires_verified_durable_manifest(self):
        self.assertIn("VERIFIED_DURABLE_RUNTIME", self.localhost_text)
        self.assertIn("provider is outside exact durable runtime root", self.localhost_text)
        self.assertIn("manifest_sha256", self.localhost_text)
        self.assertIn("provider RECORD mismatch", self.localhost_text)

    def test_manifest_carries_required_baseline_and_boundaries(self):
        for required in ("CPython `3.9.6`", "resolved interpreter", "`sys.platform=darwin`",
                         "`platform.machine()=arm64`", "pip `21.2.4`",
                         "Preservation evidence only; not an active runtime", "D-118"):
            self.assertIn(required, self.manifest_text)

    def test_scripts_remain_parseable_without_importing_them(self):
        self.assertIsInstance(self.restore_tree, ast.Module)
        self.assertIsInstance(self.localhost_tree, ast.Module)


if __name__ == "__main__":
    unittest.main()
