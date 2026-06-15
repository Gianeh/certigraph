"""Small, dependency-free checkers for proof-carrying graph results.

The functions in this module are intended to be part of the trusted computing
base (TCB): they are deliberately simple, deterministic, and independent from
heavy graph packages.  Producers may be buggy, optimized, parallel, or generated
by an LLM; the checker should remain boring.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from math import isfinite, inf
from numbers import Real
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Optional, Sequence, Tuple

Vertex = Hashable
WeightedDiEdge = Tuple[Vertex, Vertex, float]
WeightedUnEdge = Tuple[Vertex, Vertex, float]
CapacityEdge = Tuple[Vertex, Vertex, float]


@dataclass(frozen=True)
class CheckResult:
    """Outcome of a verifier.

    Attributes:
        ok: True iff the certificate was accepted.
        message: Human-readable explanation.
        details: Machine-readable metadata useful for logs or debugging.
    """

    ok: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def __bool__(self) -> bool:  # pragma: no cover - trivial convenience
        return self.ok


def _pass(message: str = "accepted", **details: Any) -> CheckResult:
    return CheckResult(True, message, dict(details))


def _fail(message: str, **details: Any) -> CheckResult:
    return CheckResult(False, message, dict(details))


def _is_number(x: Any) -> bool:
    return isinstance(x, Real) and not isinstance(x, bool) and isfinite(float(x))


def _is_int_number(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _eq(a: float, b: float, abs_tol: float) -> bool:
    return abs(float(a) - float(b)) <= abs_tol


def _leq(a: float, b: float, abs_tol: float) -> bool:
    return float(a) <= float(b) + abs_tol


def _vertex_list(vertices: Iterable[Vertex]) -> Tuple[Optional[List[Vertex]], Optional[CheckResult]]:
    try:
        vs = list(vertices)
    except TypeError:
        return None, _fail("vertices must be iterable")
    seen = set()
    for v in vs:
        try:
            hash(v)
        except TypeError:
            return None, _fail("vertices must be hashable", vertex=repr(v))
        if v in seen:
            return None, _fail("duplicate vertex", vertex=v)
        seen.add(v)
    return vs, None


def _validate_weighted_edges(
    vertices: Sequence[Vertex], edges: Sequence[Tuple[Any, Any, Any]], *, field: str = "w"
) -> Tuple[Optional[List[Tuple[Vertex, Vertex, float]]], Optional[CheckResult]]:
    V = set(vertices)
    out: List[Tuple[Vertex, Vertex, float]] = []
    try:
        iterator = enumerate(edges)
    except TypeError:
        return None, _fail("edges must be iterable")
    for i, e in iterator:
        try:
            u, v, w = e
        except (TypeError, ValueError):
            return None, _fail("edge must have three fields", edge_index=i, edge=repr(e))
        if u not in V or v not in V:
            return None, _fail("edge endpoint not in vertices", edge_index=i, edge=(u, v))
        if not _is_number(w):
            return None, _fail(f"edge {field} must be a finite number", edge_index=i, value=repr(w))
        out.append((u, v, float(w)))
    return out, None


def _validate_weighted_edges_int(
    vertices: Sequence[Vertex], edges: Sequence[Tuple[Any, Any, Any]], *, field: str = "w"
) -> Tuple[Optional[List[Tuple[Vertex, Vertex, int]]], Optional[CheckResult]]:
    V = set(vertices)
    out: List[Tuple[Vertex, Vertex, int]] = []
    try:
        iterator = enumerate(edges)
    except TypeError:
        return None, _fail("edges must be iterable")
    for i, e in iterator:
        try:
            u, v, w = e
        except (TypeError, ValueError):
            return None, _fail("edge must have three fields", edge_index=i, edge=repr(e))
        if u not in V or v not in V:
            return None, _fail("edge endpoint not in vertices", edge_index=i, edge=(u, v))
        if not _is_int_number(w):
            return None, _fail(f"edge {field} must be an integer in exact mode", edge_index=i, value=repr(w))
        out.append((u, v, int(w)))
    return out, None


class _UnionFind:
    def __init__(self, vertices: Iterable[Vertex]) -> None:
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, x: Vertex) -> Vertex:
        p = self.parent[x]
        if p != x:
            self.parent[x] = self.find(p)
        return self.parent[x]

    def union(self, a: Vertex, b: Vertex) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def check_topological_order(
    vertices: Iterable[Vertex], edges: Sequence[Tuple[Vertex, Vertex]], order: Sequence[Vertex]
) -> CheckResult:
    """Verify that ``order`` is a topological ordering of a directed graph.

    Certificate: a permutation of all vertices.
    Check: every directed edge points forward in that permutation.
    """

    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    V = set(vs)
    try:
        order_list = list(order)
    except TypeError:
        return _fail("order must be iterable")
    if len(order_list) != len(vs):
        return _fail("order length differs from number of vertices", order_len=len(order_list), vertices=len(vs))
    try:
        order_set = set(order_list)
    except TypeError as exc:
        return _fail("order contains unhashable vertex", error=str(exc))
    if order_set != V or len(order_set) != len(order_list):
        return _fail("order is not a permutation of vertices")
    pos = {v: i for i, v in enumerate(order_list)}
    for i, (u, v) in enumerate(edges):
        if u not in V or v not in V:
            return _fail("edge endpoint not in vertices", edge_index=i, edge=(u, v))
        if pos[u] >= pos[v]:
            return _fail("edge violates topological order", edge_index=i, edge=(u, v), pos_u=pos[u], pos_v=pos[v])
    return _pass("valid topological order", vertices=len(vs), edges=len(edges))


def check_bipartition(
    vertices: Iterable[Vertex], edges: Sequence[Tuple[Vertex, Vertex]], color: Mapping[Vertex, Any]
) -> CheckResult:
    """Verify a bipartition certificate for an undirected graph.

    Certificate: a color/side for each vertex. The actual color values are arbitrary;
    only equality/inequality matters.
    """

    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    V = set(vs)
    missing = [v for v in vs if v not in color]
    if missing:
        return _fail("color missing for vertex", vertex=missing[0])
    for i, (u, v) in enumerate(edges):
        if u not in V or v not in V:
            return _fail("edge endpoint not in vertices", edge_index=i, edge=(u, v))
        if color[u] == color[v]:
            return _fail("edge has equal endpoint colors", edge_index=i, edge=(u, v), color=color[u])
    return _pass("valid bipartition", vertices=len(vs), edges=len(edges))


def check_connected_components(
    vertices: Iterable[Vertex], edges: Sequence[Tuple[Vertex, Vertex]], component: Mapping[Vertex, Any]
) -> CheckResult:
    """Verify an undirected connected-components certificate.

    Certificate: one component label for each vertex.

    Verification idea:
      1. Every edge must stay inside one claimed component.
      2. Vertices that are graph-connected must have the same label.
      3. Vertices in different graph components must not share a label.
    """

    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    V = set(vs)
    missing = [v for v in vs if v not in component]
    if missing:
        return _fail("component label missing for vertex", vertex=missing[0])

    parsed_edges: List[Tuple[Vertex, Vertex]] = []
    uf = _UnionFind(vs)
    for i, e in enumerate(edges):
        try:
            u, v = e
        except (TypeError, ValueError):
            return _fail("edge must have two fields", edge_index=i, edge=repr(e))
        if u not in V or v not in V:
            return _fail("edge endpoint not in vertices", edge_index=i, edge=(u, v))
        if component[u] != component[v]:
            return _fail("edge crosses claimed components", edge_index=i, edge=(u, v), component_u=component[u], component_v=component[v])
        parsed_edges.append((u, v))
        if u != v:
            uf.union(u, v)

    root_to_label: Dict[Vertex, Any] = {}
    label_to_root: Dict[Any, Vertex] = {}
    for v in vs:
        label = component[v]
        try:
            hash(label)
        except TypeError:
            return _fail("component label must be hashable", vertex=v, label=repr(label))
        root = uf.find(v)
        if root in root_to_label and root_to_label[root] != label:
            return _fail("connected vertices assigned different labels", vertex=v, expected=root_to_label[root], actual=label)
        root_to_label[root] = label
        if label in label_to_root and label_to_root[label] != root:
            return _fail("disconnected components merged under one label", vertex=v, label=label)
        label_to_root[label] = root

    components = len({uf.find(v) for v in vs})
    return _pass("valid connected-components certificate", vertices=len(vs), edges=len(parsed_edges), components=components)


def _distance_value(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, str) and x.lower() in {"inf", "+inf", "infinity", "unreachable", "none", "null"}:
        return None
    if _is_number(x):
        return float(x)
    return None  # caller distinguishes by checking raw value when needed


def _parse_edge_index(raw: Any) -> Optional[int]:
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, str):
        text = raw.strip()
        if text.startswith(("+", "-")):
            sign, rest = text[0], text[1:]
            if rest.isdigit():
                return int(sign + rest)
        elif text.isdigit():
            return int(text)
    return None


def _parse_parent_entry(entry: Any) -> Optional[Tuple[Vertex, int]]:
    if entry is None:
        return None
    if isinstance(entry, Mapping):
        if "u" not in entry or "edge" not in entry:
            return None
        edge_idx = _parse_edge_index(entry["edge"])
        if edge_idx is None:
            return None
        return (entry["u"], edge_idx)
    if isinstance(entry, (tuple, list)) and len(entry) == 2:
        edge_idx = _parse_edge_index(entry[1])
        if edge_idx is None:
            return None
        return (entry[0], edge_idx)
    return None


def check_sssp_certificate(
    vertices: Iterable[Vertex],
    edges: Sequence[WeightedDiEdge],
    source: Vertex,
    distance: Mapping[Vertex, Any],
    parent: Mapping[Vertex, Any],
    *,
    abs_tol: float = 1e-9,
    exact: bool = False,
) -> CheckResult:
    """Verify a single-source shortest-path certificate.

    This checker accepts directed graphs with positive, zero, or negative finite
    weights, provided no reachable negative cycle makes the requested distances
    undefined.

    Certificate:
      - ``distance[v]`` is the claimed shortest-path distance, or ``None`` for
        unreachable vertices.
      - ``parent[v]`` is ``None`` for the source/unreachable vertices, otherwise
        either ``(u, edge_index)`` or ``{"u": u, "edge": edge_index}`` naming
        an incoming edge that realizes ``distance[v]``.

    Verification idea:
      1. Parent pointers form actual source-to-v paths whose lengths equal the
         claimed distances, so every finite claim is attainable.
      2. Every edge satisfies the Bellman-Ford inequality D[v] <= D[u] + w(u,v),
         so no path can beat the claim.
      3. No edge leaves the finite-distance region toward an unreachable vertex,
         so all reachable vertices are finite.

    Numeric modes:
      - default: finite real numbers with absolute tolerance ``abs_tol``;
      - ``exact=True``: integer-only validation with exact equality/inequality
        checks and ``abs_tol=0``.
    """

    if abs_tol < 0:
        return _fail("abs_tol must be non-negative", abs_tol=abs_tol)
    if exact and abs_tol != 0:
        return _fail("exact mode requires abs_tol=0", abs_tol=abs_tol)
    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    V = set(vs)
    if source not in V:
        return _fail("source not in vertices", source=source)
    if exact:
        es, err = _validate_weighted_edges_int(vs, edges)
    else:
        es, err = _validate_weighted_edges(vs, edges)
    if err is not None:
        return err
    assert es is not None

    D: Dict[Vertex, Optional[Any]] = {}
    for v in vs:
        if v not in distance:
            return _fail("distance missing for vertex", vertex=v)
        raw = distance[v]
        if exact:
            if raw is None or (isinstance(raw, str) and raw.lower() in {"inf", "+inf", "infinity", "unreachable", "none", "null"}):
                d = None
            elif _is_int_number(raw):
                d = int(raw)
            else:
                return _fail("distance must be integer or unreachable marker in exact mode", vertex=v, value=repr(raw))
        else:
            d = _distance_value(raw)
            if d is None and raw is not None and not (
                isinstance(raw, str) and raw.lower() in {"inf", "+inf", "infinity", "unreachable", "none", "null"}
            ):
                return _fail("distance must be finite number or unreachable marker", vertex=v, value=repr(raw))
        D[v] = d

    if D[source] is None:
        return _fail("source distance must be zero", source=source, distance=D[source])
    if exact:
        if D[source] != 0:
            return _fail("source distance must be zero", source=source, distance=D[source])
    elif not _eq(float(D[source]), 0.0, abs_tol):
        return _fail("source distance must be zero", source=source, distance=D[source])

    # Parent entries must identify real edges and realize equality.
    parent_edge: Dict[Vertex, Optional[Tuple[Vertex, int]]] = {v: None for v in vs}
    for v in vs:
        p_raw = parent.get(v, None)
        p = _parse_parent_entry(p_raw)
        if v == source:
            if p is not None:
                return _fail("source must not have a parent", source=source)
            continue
        if D[v] is None:
            if p_raw is not None:
                return _fail("unreachable vertex must not have a parent", vertex=v)
            continue
        if p is None:
            return _fail("reachable non-source vertex needs a parent edge", vertex=v)
        u, edge_idx = p
        if edge_idx < 0 or edge_idx >= len(es):
            return _fail("parent edge index out of range", vertex=v, edge_index=edge_idx)
        eu, ev, w = es[edge_idx]
        if eu != u or ev != v:
            return _fail("parent edge does not match vertex", vertex=v, parent=p, actual_edge=(eu, ev, w))
        if D[u] is None:
            return _fail("parent vertex is unreachable", vertex=v, parent=u)
        assert D[v] is not None and D[u] is not None
        if exact:
            if D[v] != D[u] + w:
                return _fail(
                    "parent edge does not realize claimed distance",
                    vertex=v,
                    distance=D[v],
                    parent_distance=D[u],
                    edge_weight=w,
                )
        elif not _eq(float(D[v]), float(D[u]) + float(w), abs_tol):
            return _fail(
                "parent edge does not realize claimed distance",
                vertex=v,
                distance=D[v],
                parent_distance=D[u],
                edge_weight=w,
            )
        parent_edge[v] = (u, edge_idx)

    # Parent chains must terminate at source; otherwise they do not witness paths.
    state: Dict[Vertex, int] = {v: 0 for v in vs}  # 0 unseen, 1 active, 2 proven
    state[source] = 2

    def prove_chain(v: Vertex) -> Optional[CheckResult]:
        stack: List[Vertex] = []
        cur = v
        while state[cur] != 2:
            if state[cur] == 1:
                return _fail("parent pointers contain a cycle", vertex=cur)
            state[cur] = 1
            stack.append(cur)
            pe = parent_edge[cur]
            if pe is None:
                return _fail("parent chain does not reach source", vertex=cur)
            cur = pe[0]
        for x in stack:
            state[x] = 2
        return None

    for v in vs:
        if D[v] is not None:
            err2 = prove_chain(v)
            if err2 is not None:
                return err2

    # Bellman-Ford inequalities and reachability closure.
    for i, (u, v, w) in enumerate(es):
        du, dv = D[u], D[v]
        if du is None:
            continue
        if dv is None:
            return _fail("edge leaves reachable region toward vertex marked unreachable", edge_index=i, edge=(u, v, w))
        candidate = du + w
        if exact:
            if dv > candidate:
                return _fail(
                    "edge relaxation would improve claimed distance",
                    edge_index=i,
                    edge=(u, v, w),
                    distance_u=du,
                    distance_v=dv,
                    candidate=candidate,
                )
        elif not _leq(float(dv), float(candidate), abs_tol):
            return _fail(
                "edge relaxation would improve claimed distance",
                edge_index=i,
                edge=(u, v, w),
                distance_u=du,
                distance_v=dv,
                candidate=candidate,
            )

    reachable = sum(1 for d in D.values() if d is not None)
    return _pass("valid SSSP certificate", vertices=len(vs), edges=len(es), reachable=reachable)


def check_minimum_spanning_forest_certificate(
    vertices: Iterable[Vertex],
    edges: Sequence[WeightedUnEdge],
    chosen: Iterable[int],
    *,
    abs_tol: float = 1e-9,
) -> CheckResult:
    """Verify a minimum-spanning-forest certificate for an undirected graph.

    Certificate: indices of the selected forest edges.

    Verification idea:
      1. The selected edges are acyclic and span every connected component.
      2. For every non-selected edge e=(u,v), the maximum-weight edge on the
         unique selected u-v path has weight <= w(e). Replacing a heavier path
         edge by e can never improve the forest, which is the cycle-optimality
         condition for MST/MSF.

    Self-loops are allowed in the input but cannot be selected; they are ignored
    by the optimality check because they cannot participate in a spanning forest.
    """

    if abs_tol < 0:
        return _fail("abs_tol must be non-negative", abs_tol=abs_tol)
    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    es, err = _validate_weighted_edges(vs, edges)
    if err is not None:
        return err
    assert es is not None
    n = len(vs)

    try:
        chosen_list = list(chosen)
    except TypeError:
        return _fail("chosen must be iterable")
    if len(set(chosen_list)) != len(chosen_list):
        return _fail("chosen edge list contains duplicates")
    for idx in chosen_list:
        if not isinstance(idx, int) or isinstance(idx, bool) or idx < 0 or idx >= len(es):
            return _fail("chosen edge index out of range", edge_index=idx)

    chosen_set = set(chosen_list)
    uf = _UnionFind(vs)
    adjacency: Dict[Vertex, List[Tuple[Vertex, float, int]]] = {v: [] for v in vs}
    total_weight = 0.0
    for idx in chosen_list:
        u, v, w = es[idx]
        if u == v:
            return _fail("self-loop cannot be selected in a spanning forest", edge_index=idx)
        if not uf.union(u, v):
            return _fail("chosen edges contain a cycle", edge_index=idx, edge=(u, v, w))
        adjacency[u].append((v, w, idx))
        adjacency[v].append((u, w, idx))
        total_weight += w

    # Spanning check: every original non-loop edge must lie inside one selected component.
    for i, (u, v, w) in enumerate(es):
        if u == v:
            continue
        if uf.find(u) != uf.find(v):
            return _fail("chosen forest does not span an input connected component", edge_index=i, edge=(u, v, w))

    # Binary lifting over the selected forest for max-edge-on-path queries.
    index = {v: i for i, v in enumerate(vs)}
    depth = [0] * n
    comp = [-1] * n
    parent0 = [-1] * n
    max0 = [-inf] * n
    cid = 0
    for root in vs:
        ri = index[root]
        if comp[ri] != -1:
            continue
        comp[ri] = cid
        q = deque([root])
        while q:
            u = q.popleft()
            ui = index[u]
            for v, w, _edge_idx in adjacency[u]:
                vi = index[v]
                if vi == parent0[ui]:
                    continue
                if comp[vi] != -1:
                    continue
                comp[vi] = cid
                parent0[vi] = ui
                max0[vi] = w
                depth[vi] = depth[ui] + 1
                q.append(v)
        cid += 1

    K = max(1, n.bit_length())
    up = [parent0]
    mx = [max0]
    for k in range(1, K):
        prev_up, prev_mx = up[-1], mx[-1]
        cur_up = [-1] * n
        cur_mx = [-inf] * n
        for i in range(n):
            mid = prev_up[i]
            if mid == -1:
                cur_up[i] = -1
                cur_mx[i] = prev_mx[i]
            else:
                cur_up[i] = prev_up[mid]
                cur_mx[i] = max(prev_mx[i], prev_mx[mid])
        up.append(cur_up)
        mx.append(cur_mx)

    def path_max(a: Vertex, b: Vertex) -> Optional[float]:
        ia, ib = index[a], index[b]
        if comp[ia] != comp[ib]:
            return None
        if ia == ib:
            return -inf
        best = -inf
        if depth[ia] < depth[ib]:
            ia, ib = ib, ia
        diff = depth[ia] - depth[ib]
        bit = 0
        while diff:
            if diff & 1:
                best = max(best, mx[bit][ia])
                ia = up[bit][ia]
            diff >>= 1
            bit += 1
        if ia == ib:
            return best
        for k in range(K - 1, -1, -1):
            if up[k][ia] != up[k][ib]:
                best = max(best, mx[k][ia], mx[k][ib])
                ia = up[k][ia]
                ib = up[k][ib]
        best = max(best, mx[0][ia], mx[0][ib])
        return best

    for i, (u, v, w) in enumerate(es):
        if i in chosen_set or u == v:
            continue
        pm = path_max(u, v)
        if pm is None:
            return _fail("internal error: non-tree edge endpoints disconnected after spanning check", edge_index=i)
        if not _leq(pm, w, abs_tol):
            return _fail("cycle optimality violated by non-tree edge", edge_index=i, edge=(u, v, w), path_max=pm)

    return _pass("valid minimum spanning forest certificate", vertices=n, edges=len(es), chosen=len(chosen_list), total_weight=total_weight)


def check_max_flow_certificate(
    vertices: Iterable[Vertex],
    edges: Sequence[CapacityEdge],
    source: Vertex,
    sink: Vertex,
    flow: Sequence[Any],
    cut: Iterable[Vertex],
    *,
    abs_tol: float = 1e-9,
) -> CheckResult:
    """Verify a maximum-flow certificate.

    Certificate:
      - a flow value for each directed edge, by edge index;
      - an s-side vertex set of a cut.

    Verification idea: capacity constraints + conservation make the flow feasible;
    source in cut and sink outside make the cut feasible; if flow value equals cut
    capacity, weak duality plus max-flow/min-cut proves simultaneous optimality.
    """

    if abs_tol < 0:
        return _fail("abs_tol must be non-negative", abs_tol=abs_tol)
    vs, err = _vertex_list(vertices)
    if err is not None:
        return err
    assert vs is not None
    V = set(vs)
    if source not in V or sink not in V or source == sink:
        return _fail("source and sink must be distinct vertices", source=source, sink=sink)
    es, err = _validate_weighted_edges(vs, edges, field="capacity")
    if err is not None:
        return err
    assert es is not None
    if len(flow) != len(es):
        return _fail("flow length differs from edge count", flow_len=len(flow), edges=len(es))

    F: List[float] = []
    excess = {v: 0.0 for v in vs}  # outflow minus inflow
    for i, ((u, v, cap), f_raw) in enumerate(zip(es, flow)):
        if cap < -abs_tol:
            return _fail("capacity must be non-negative", edge_index=i, capacity=cap)
        if not _is_number(f_raw):
            return _fail("flow value must be a finite number", edge_index=i, value=repr(f_raw))
        f = float(f_raw)
        if f < -abs_tol:
            return _fail("flow value is negative", edge_index=i, flow=f)
        if f > cap + abs_tol:
            return _fail("flow exceeds capacity", edge_index=i, flow=f, capacity=cap)
        F.append(f)
        excess[u] += f
        excess[v] -= f

    value = excess[source]
    if value < -abs_tol:
        return _fail("flow has negative source value", value=value)
    if not _eq(excess[sink], -value, abs_tol):
        return _fail("sink imbalance does not match source value", source_value=value, sink_excess=excess[sink])
    for v in vs:
        if v in {source, sink}:
            continue
        if not _eq(excess[v], 0.0, abs_tol):
            return _fail("flow conservation violated", vertex=v, excess=excess[v])

    try:
        S = set(cut)
    except TypeError:
        return _fail("cut must be iterable")
    if not S <= V:
        return _fail("cut contains vertices outside graph", extra=sorted(map(repr, S - V)))
    if source not in S or sink in S:
        return _fail("cut must contain source and exclude sink", source_in=source in S, sink_in=sink in S)
    cut_capacity = sum(cap for (u, v, cap) in es if u in S and v not in S)
    if not _eq(value, cut_capacity, abs_tol):
        return _fail("flow value does not equal cut capacity", value=value, cut_capacity=cut_capacity)

    return _pass("valid maximum-flow/min-cut certificate", vertices=len(vs), edges=len(es), value=value, cut_capacity=cut_capacity)
