"""Validate all bundled JSON examples with the CLI-facing Python API."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
from pathlib import Path

from certigraph.cli import verify

ROOT = Path(__file__).resolve().parents[1]
VALID = {
    "sssp": ROOT / "examples" / "sssp_valid.json",
    "msf": ROOT / "examples" / "msf_valid.json",
    "maxflow": ROOT / "examples" / "maxflow_valid.json",
    "topo": ROOT / "examples" / "topo_valid.json",
    "bipartition": ROOT / "examples" / "bipartition_valid.json",
}
INVALID = {
    "sssp": ROOT / "examples" / "invalid" / "sssp_tampered_distance.json",
    "maxflow": ROOT / "examples" / "invalid" / "maxflow_bad_cut.json",
    "topo": ROOT / "examples" / "invalid" / "topo_reversed_order.json",
    "bipartition": ROOT / "examples" / "invalid" / "bipartition_odd_cycle.json",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    for kind, path in VALID.items():
        result = verify(kind, load(path), 1e-9)
        print(f"valid   {kind:12s} {result.ok} {path.relative_to(ROOT)}")
        if not result.ok:
            return 1
    for kind, path in INVALID.items():
        result = verify(kind, load(path), 1e-9)
        print(f"invalid {kind:12s} {result.ok} {path.relative_to(ROOT)}")
        if result.ok:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
