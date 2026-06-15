"""Optional NetworkX end-to-end connected-components verification demo.

Run after installing the optional extra:

    python -m pip install -e .[networkx]
    python examples/networkx_components_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json

from certigraph import check_connected_components, connected_components_certificate
from certigraph.adapters.networkx import undirected_edges, vertices

try:
    import networkx as nx
except ImportError:  # pragma: no cover - depends on optional dependency
    print("NetworkX is not installed. Try: python -m pip install -e .[networkx]")
    raise SystemExit(0)

G = nx.Graph()
G.add_edges_from([("warehouse", "hub-a"), ("hub-a", "store-a"), ("hub-b", "store-b")])
G.add_node("island")

vs = vertices(G)
es = undirected_edges(G)
component = connected_components_certificate(vs, es)
result = check_connected_components(vs, es, component)
print(json.dumps({"verified": result.ok, "components": component, "details": result.details}, indent=2, sort_keys=True))
