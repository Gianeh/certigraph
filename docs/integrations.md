# Integrations

CertiGraph’s intended role is a verification layer next to existing graph tools.

## NetworkX

The optional adapter helpers in `certigraph/adapters/networkx.py` use duck typing and only require NetworkX when you call them with NetworkX graphs.

```python
import networkx as nx
from certigraph.adapters.networkx import directed_weighted_edges
from certigraph import bellman_ford_certificate, check_sssp_certificate

G = nx.DiGraph()
G.add_weighted_edges_from([("s", "a", 2), ("a", "b", -1), ("s", "b", 5)])

vertices = list(G.nodes)
edges = directed_weighted_edges(G)
distance, parent = bellman_ford_certificate(vertices, edges, "s")
assert check_sssp_certificate(vertices, edges, "s", distance, parent).ok
```

End-to-end scripts in this repository:

```bash
python examples/networkx_adapter_demo.py
python examples/networkx_components_demo.py
```

## Solver services

A remote solver can return JSON:

```json
{
  "result": {"value": 42},
  "certificate": {"...": "..."},
  "instance_sha256": "...",
  "producer": "optimizer-service-v17"
}
```

The client should verify the certificate before using the result.

## CI / data pipelines

Use the CLI exit code:

```bash
python -m certigraph verify maxflow artifact.json
```

A rejected certificate exits with code `2`, making it natural to fail builds, stop deployments, or quarantine pipeline outputs.

A ready-to-use workflow is included in `.github/workflows/verify-solver-output.yml`.
