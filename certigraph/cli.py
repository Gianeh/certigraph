"""Command-line interface for certigraph.

Examples:
    python -m certigraph verify sssp examples/sssp_valid.json
    python -m certigraph produce msf graph.json --out graph.cert.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .envelope import make_envelope, sha256_json
from .produce import (
    bellman_ford_certificate,
    bipartition_certificate,
    edmonds_karp_certificate,
    kruskal_msf_certificate,
    topological_order_certificate,
)
from .verify import (
    CheckResult,
    check_bipartition,
    check_max_flow_certificate,
    check_minimum_spanning_forest_certificate,
    check_sssp_certificate,
    check_topological_order,
)


def _read(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(path: Optional[str], data: Dict[str, Any]) -> None:
    text = json.dumps(data, indent=2, sort_keys=True)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def _edges_w(data: Dict[str, Any], *, cap: bool = False) -> List[Tuple[Any, Any, float]]:
    field = "capacity" if cap else "w"
    edges = []
    for i, e in enumerate(data.get("edges", [])):
        if isinstance(e, dict):
            if "u" not in e or "v" not in e or field not in e:
                raise ValueError(f"edge {i} must contain u, v, {field}")
            edges.append((e["u"], e["v"], e[field]))
        elif isinstance(e, list) and len(e) == 3:
            edges.append((e[0], e[1], e[2]))
        else:
            raise ValueError(f"edge {i} must be dict or [u,v,{field}]")
    return edges


def _edges_unweighted(data: Dict[str, Any]) -> List[Tuple[Any, Any]]:
    edges = []
    for i, e in enumerate(data.get("edges", [])):
        if isinstance(e, dict):
            if "u" not in e or "v" not in e:
                raise ValueError(f"edge {i} must contain u and v")
            edges.append((e["u"], e["v"]))
        elif isinstance(e, list) and len(e) == 2:
            edges.append((e[0], e[1]))
        else:
            raise ValueError(f"edge {i} must be dict or [u,v]")
    return edges


def _result_to_json(result: CheckResult) -> Dict[str, Any]:
    return {"ok": result.ok, "message": result.message, "details": result.details}


def verify(kind: str, data: Dict[str, Any], abs_tol: float) -> CheckResult:
    vertices = data["vertices"]
    if kind == "sssp":
        return check_sssp_certificate(vertices, _edges_w(data), data["source"], data["distance"], data.get("parent", {}), abs_tol=abs_tol)
    if kind in {"msf", "mst"}:
        return check_minimum_spanning_forest_certificate(vertices, _edges_w(data), data["chosen"], abs_tol=abs_tol)
    if kind == "maxflow":
        return check_max_flow_certificate(vertices, _edges_w(data, cap=True), data["source"], data["sink"], data["flow"], data["cut"], abs_tol=abs_tol)
    if kind in {"topo", "topological"}:
        return check_topological_order(vertices, _edges_unweighted(data), data["order"])
    if kind in {"bipartition", "bipartite"}:
        return check_bipartition(vertices, _edges_unweighted(data), data["color"])
    raise ValueError(f"unknown kind: {kind}")


def produce(kind: str, data: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(data)
    vertices = data["vertices"]
    if kind == "sssp":
        dist, parent = bellman_ford_certificate(vertices, _edges_w(data), data["source"])
        out["distance"] = dist
        out["parent"] = parent
    elif kind in {"msf", "mst"}:
        out["chosen"] = kruskal_msf_certificate(vertices, _edges_w(data))
    elif kind == "maxflow":
        flow, cut = edmonds_karp_certificate(vertices, _edges_w(data, cap=True), data["source"], data["sink"])
        out["flow"] = flow
        out["cut"] = cut
    elif kind in {"topo", "topological"}:
        out["order"] = topological_order_certificate(vertices, _edges_unweighted(data))
    elif kind in {"bipartition", "bipartite"}:
        out["color"] = bipartition_certificate(vertices, _edges_unweighted(data))
    else:
        raise ValueError(f"unknown kind: {kind}")
    return out


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="certigraph", description="Verify or produce proof-carrying graph results.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_verify = sub.add_parser("verify", help="verify a certificate JSON file")
    p_verify.add_argument("kind", choices=["sssp", "msf", "mst", "maxflow", "topo", "topological", "bipartition", "bipartite"])
    p_verify.add_argument("json_file")
    p_verify.add_argument("--abs-tol", type=float, default=1e-9)

    p_produce = sub.add_parser("produce", help="produce a certificate JSON file using reference algorithms")
    p_produce.add_argument("kind", choices=["sssp", "msf", "mst", "maxflow", "topo", "topological", "bipartition", "bipartite"])
    p_produce.add_argument("json_file")
    p_produce.add_argument("--out", default=None)

    p_hash = sub.add_parser("hash", help="print a canonical SHA-256 digest for a JSON file")
    p_hash.add_argument("json_file")
    p_hash.add_argument("--envelope-kind", default=None, help="wrap the JSON payload in a CertiGraph envelope of this kind")
    p_hash.add_argument("--producer", default="certigraph-cli", help="producer metadata for --envelope-kind")

    args = parser.parse_args(argv)
    try:
        data = _read(args.json_file)
        if args.cmd == "verify":
            result = verify(args.kind, data, args.abs_tol)
            print(json.dumps(_result_to_json(result), indent=2, sort_keys=True))
            return 0 if result.ok else 2
        if args.cmd == "produce":
            out = produce(args.kind, data)
            _write(args.out, out)
            return 0
        if args.cmd == "hash":
            if args.envelope_kind:
                envelope = make_envelope(args.envelope_kind, data, producer=args.producer)
                print(json.dumps(envelope, indent=2, sort_keys=True))
            else:
                print(json.dumps({"sha256": sha256_json(data)}, indent=2, sort_keys=True))
            return 0
    except Exception as exc:  # CLI boundary: report, do not traceback by default.
        print(json.dumps({"ok": False, "message": str(exc), "details": {"exception": type(exc).__name__}}, indent=2), file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
