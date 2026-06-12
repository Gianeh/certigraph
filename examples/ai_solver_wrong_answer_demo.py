"""Demo: reject a plausible but wrong AI-generated shortest-path result."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from certigraph import bellman_ford_certificate, check_sssp_certificate

vertices = ["s", "a", "b", "c"]
edges = [
    ("s", "a", 2),
    ("s", "b", 5),
    ("a", "b", -1),
    ("b", "c", 2),
    ("a", "c", 5),
]

# Imagine this came from an untrusted LLM-generated solver. It looks plausible,
# but misses the cheaper s -> a -> b -> c path of length 3.
bad_distance = {"s": 0, "a": 2, "b": 5, "c": 7}
bad_parent = {
    "s": None,
    "a": {"u": "s", "edge": 0},
    "b": {"u": "s", "edge": 1},
    "c": {"u": "b", "edge": 3},
}

bad = check_sssp_certificate(vertices, edges, "s", bad_distance, bad_parent)
print("Untrusted solver result:")
print(json.dumps({"ok": bad.ok, "message": bad.message, "details": bad.details}, indent=2, sort_keys=True))

print("\nReference producer result:")
distance, parent = bellman_ford_certificate(vertices, edges, "s")
good = check_sssp_certificate(vertices, edges, "s", distance, parent)
print(json.dumps({"ok": good.ok, "message": good.message, "distance": distance}, indent=2, sort_keys=True))
