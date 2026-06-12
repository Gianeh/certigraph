"""Optional NetworkX demo.

Run after installing the optional extra:

    python -m pip install -e .[networkx]
    python examples/networkx_adapter_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from certigraph import bellman_ford_certificate, check_sssp_certificate
from certigraph.adapters.networkx import directed_weighted_edges, vertices

try:
    import networkx as nx
except ImportError:  # pragma: no cover - depends on optional dependency
    print("NetworkX is not installed. Try: python -m pip install -e .[networkx]")
    raise SystemExit(0)

G = nx.DiGraph()
G.add_weighted_edges_from([("s", "a", 2), ("a", "b", -1), ("s", "b", 5), ("b", "c", 2)])

vs = vertices(G)
edges = directed_weighted_edges(G)
distance, parent = bellman_ford_certificate(vs, edges, "s")
result = check_sssp_certificate(vs, edges, "s", distance, parent)
print(json.dumps({"verified": result.ok, "distance": distance}, indent=2, sort_keys=True))
