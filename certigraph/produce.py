"""Reference certificate producers for certigraph.

These functions are intentionally ordinary algorithms.  They are useful for demos,
tests, and bootstrapping, but they are *not* the trusted part of the system.  The
trusted part is in certigraph.verify.
"""

from __future__ import annotations

from collections import deque
from math import inf
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Optional, Sequence, Tuple

from .verify import CapacityEdge, Vertex, WeightedDiEdge, WeightedUnEdge, _UnionFind


def bellman_ford_certificate(
    vertices: Iterable[Vertex], edges: Sequence[WeightedDiEdge], source: Vertex
) -> Tuple[Dict[Vertex, Optional[float]], Dict[Vertex, Optional[Dict[str, Any]]]]:
    """Produce an SSSP certificate using Bellman-Ford.

    Raises ValueError if a negative cycle is reachable from the source.
    """

    vs = list(vertices)
    if source not in set(vs):
        raise ValueError("source not in vertices")
    dist = {v: inf for v in vs}
    parent: Dict[Vertex, Optional[Dict[str, Any]]] = {v: None for v in vs}
    dist[source] = 0.0
    for _ in range(max(0, len(vs) - 1)):
        changed = False
        for i, (u, v, w) in enumerate(edges):
            if dist[u] != inf and dist[u] + float(w) < dist[v]:
                dist[v] = dist[u] + float(w)
                parent[v] = {"u": u, "edge": i}
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + float(w) < dist[v]:
            raise ValueError("negative cycle reachable from source")
    out_dist = {v: (None if dist[v] == inf else dist[v]) for v in vs}
    return out_dist, parent


def kruskal_msf_certificate(vertices: Iterable[Vertex], edges: Sequence[WeightedUnEdge]) -> List[int]:
    """Produce minimum-spanning-forest edge indices using Kruskal's algorithm."""

    vs = list(vertices)
    uf = _UnionFind(vs)
    chosen: List[int] = []
    for idx, (u, v, w) in sorted(enumerate(edges), key=lambda item: (float(item[1][2]), item[0])):
        if u == v:
            continue
        if uf.union(u, v):
            chosen.append(idx)
    return chosen


def edmonds_karp_certificate(
    vertices: Iterable[Vertex], edges: Sequence[CapacityEdge], source: Vertex, sink: Vertex
) -> Tuple[List[float], List[Vertex]]:
    """Produce a max-flow/min-cut certificate with Edmonds-Karp."""

    vs = list(vertices)
    V = set(vs)
    if source not in V or sink not in V or source == sink:
        raise ValueError("source and sink must be distinct vertices")

    # Residual edge: [to, residual_capacity, rev_index, original_edge_index, sign]
    adj: Dict[Vertex, List[List[Any]]] = {v: [] for v in vs}

    def add_edge(u: Vertex, v: Vertex, cap: float, original: int) -> None:
        fwd = [v, float(cap), len(adj[v]), original, +1]
        rev = [u, 0.0, len(adj[u]), original, -1]
        adj[u].append(fwd)
        adj[v].append(rev)

    for i, (u, v, c) in enumerate(edges):
        if u not in V or v not in V:
            raise ValueError(f"edge {i} endpoint not in vertices")
        if float(c) < 0:
            raise ValueError(f"edge {i} has negative capacity")
        add_edge(u, v, float(c), i)

    flow = [0.0] * len(edges)

    while True:
        parent: Dict[Vertex, Tuple[Vertex, int]] = {}
        q = deque([source])
        seen = {source}
        while q and sink not in seen:
            u = q.popleft()
            for ei, e in enumerate(adj[u]):
                v, cap = e[0], e[1]
                if cap > 1e-12 and v not in seen:
                    seen.add(v)
                    parent[v] = (u, ei)
                    q.append(v)
                    if v == sink:
                        break
        if sink not in seen:
            break

        aug = inf
        v = sink
        while v != source:
            u, ei = parent[v]
            aug = min(aug, adj[u][ei][1])
            v = u
        v = sink
        while v != source:
            u, ei = parent[v]
            e = adj[u][ei]
            rev_index = e[2]
            original = e[3]
            sign = e[4]
            e[1] -= aug
            adj[v][rev_index][1] += aug
            flow[original] += sign * aug
            v = u

    # Residual-reachable set from source gives an s-side min cut.
    S = {source}
    q = deque([source])
    while q:
        u = q.popleft()
        for e in adj[u]:
            v, cap = e[0], e[1]
            if cap > 1e-12 and v not in S:
                S.add(v)
                q.append(v)
    return flow, list(S)


def topological_order_certificate(vertices: Iterable[Vertex], edges: Sequence[Tuple[Vertex, Vertex]]) -> List[Vertex]:
    """Produce a topological-order certificate with Kahn's algorithm."""

    vs = list(vertices)
    indeg = {v: 0 for v in vs}
    out = {v: [] for v in vs}
    for u, v in edges:
        if u not in indeg or v not in indeg:
            raise ValueError("edge endpoint not in vertices")
        indeg[v] += 1
        out[u].append(v)
    q = deque([v for v in vs if indeg[v] == 0])
    order: List[Vertex] = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in out[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) != len(vs):
        raise ValueError("graph is not acyclic")
    return order


def bipartition_certificate(vertices: Iterable[Vertex], edges: Sequence[Tuple[Vertex, Vertex]]) -> Dict[Vertex, int]:
    """Produce a bipartition coloring, or raise ValueError if not bipartite."""

    vs = list(vertices)
    V = set(vs)
    adj = {v: [] for v in vs}
    for u, v in edges:
        if u not in V or v not in V:
            raise ValueError("edge endpoint not in vertices")
        adj[u].append(v)
        adj[v].append(u)
    color: Dict[Vertex, int] = {}
    for start in vs:
        if start in color:
            continue
        color[start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    q.append(v)
                elif color[v] == color[u]:
                    raise ValueError("graph is not bipartite")
    return color
