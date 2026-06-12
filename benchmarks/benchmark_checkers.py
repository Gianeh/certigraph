"""Tiny benchmark script for CertiGraph checkers.

This is intentionally simple and dependency-free. It is not a rigorous benchmark
suite; it is a smoke test for asymptotic regressions and demo numbers.

Run:
    python benchmarks/benchmark_checkers.py
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import random
import time
from typing import Callable

from certigraph import (
    bellman_ford_certificate,
    check_max_flow_certificate,
    check_minimum_spanning_forest_certificate,
    check_sssp_certificate,
    edmonds_karp_certificate,
    kruskal_msf_certificate,
)


def timed(label: str, fn: Callable[[], object]) -> None:
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    print(f"{label:28s} {elapsed * 1000:9.2f} ms  {result}")


def sssp_case(n: int = 600, m: int = 2500):
    rng = random.Random(1)
    vertices = list(range(n))
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 20)) for _ in range(m)]
    edges.extend((i, i + 1, 1) for i in range(n - 1))
    distance, parent = bellman_ford_certificate(vertices, edges, 0)
    return lambda: check_sssp_certificate(vertices, edges, 0, distance, parent).ok


def msf_case(n: int = 1500, m: int = 5000):
    rng = random.Random(2)
    vertices = list(range(n))
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 1000)) for _ in range(m)]
    edges.extend((i, i + 1, 1) for i in range(n - 1))
    chosen = kruskal_msf_certificate(vertices, edges)
    return lambda: check_minimum_spanning_forest_certificate(vertices, edges, chosen).ok


def maxflow_case(n: int = 80, m: int = 450):
    rng = random.Random(3)
    vertices = list(range(n))
    edges = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 20)) for _ in range(m)]
    edges.extend((i, i + 1, rng.randint(1, 10)) for i in range(n - 1))
    flow, cut = edmonds_karp_certificate(vertices, edges, 0, n - 1)
    return lambda: check_max_flow_certificate(vertices, edges, 0, n - 1, flow, cut).ok


if __name__ == "__main__":
    timed("SSSP checker", sssp_case())
    timed("MSF checker", msf_case())
    timed("max-flow checker", maxflow_case())
