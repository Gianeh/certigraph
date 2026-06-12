"""Demo: verify a build-pipeline topological order."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from certigraph import check_topological_order, topological_order_certificate

vertices = ["fetch", "parse", "typecheck", "test", "package", "deploy"]
edges = [
    ("fetch", "parse"),
    ("parse", "typecheck"),
    ("typecheck", "test"),
    ("test", "package"),
    ("package", "deploy"),
]

order = topological_order_certificate(vertices, edges)
result = check_topological_order(vertices, edges, order)
print(json.dumps({"order": order, "verified": result.ok, "message": result.message}, indent=2))
