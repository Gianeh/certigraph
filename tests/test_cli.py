import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCLI(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "certigraph", *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_verify_valid_example(self):
        proc = self.run_cli("verify", "sssp", "examples/sssp_valid.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["ok"])

    def test_verify_invalid_example_exit_code_2(self):
        proc = self.run_cli("verify", "sssp", "examples/invalid/sssp_tampered_distance.json")
        self.assertEqual(proc.returncode, 2)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])

    def test_produce_then_verify(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "msf.cert.json"
            produced = self.run_cli("produce", "msf", "examples/msf_graph_only.json", "--out", str(out))
            self.assertEqual(produced.returncode, 0, produced.stderr)
            verified = self.run_cli("verify", "msf", str(out))
            self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_hash_outputs_digest_or_envelope(self):
        digest = self.run_cli("hash", "examples/sssp_valid.json")
        self.assertEqual(digest.returncode, 0, digest.stderr)
        self.assertIn("sha256", json.loads(digest.stdout))

        envelope = self.run_cli("hash", "examples/sssp_valid.json", "--envelope-kind", "sssp")
        self.assertEqual(envelope.returncode, 0, envelope.stderr)
        payload = json.loads(envelope.stdout)
        self.assertEqual(payload["kind"], "sssp")
        self.assertIn("payload_sha256", payload)


if __name__ == "__main__":
    unittest.main()
