import unittest

from certigraph.envelope import check_envelope, make_envelope, sha256_json


class TestEnvelope(unittest.TestCase):
    def test_sha256_json_is_canonical(self):
        a = {"b": [2, 3], "a": 1}
        b = {"a": 1, "b": [2, 3]}
        self.assertEqual(sha256_json(a), sha256_json(b))

    def test_envelope_detects_payload_tampering(self):
        envelope = make_envelope("topo", {"vertices": ["a"], "edges": [], "order": ["a"]}, producer="test")
        self.assertTrue(check_envelope(envelope))
        envelope["payload"]["order"] = []
        self.assertFalse(check_envelope(envelope))


if __name__ == "__main__":
    unittest.main()
