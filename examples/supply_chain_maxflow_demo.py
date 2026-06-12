"""Demo: certify a tiny supply-chain max-flow/min-cut result."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from certigraph import check_max_flow_certificate, edmonds_karp_certificate

vertices = ["factory", "rail", "port", "warehouse", "retail"]
edges = [
    ("factory", "rail", 8),
    ("factory", "port", 5),
    ("rail", "warehouse", 4),
    ("rail", "port", 3),
    ("port", "warehouse", 6),
    ("warehouse", "retail", 9),
]

flow, cut = edmonds_karp_certificate(vertices, edges, "factory", "retail")
result = check_max_flow_certificate(vertices, edges, "factory", "retail", flow, cut)

print(json.dumps({"flow": flow, "cut": cut, "verified": result.ok, "details": result.details}, indent=2, sort_keys=True))
