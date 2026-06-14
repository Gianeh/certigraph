"""Optional helpers for NetworkX-like graphs.

The functions are deliberately duck-typed: they work with objects exposing the
small subset of the NetworkX API that they need. NetworkX is not a runtime
dependency of CertiGraph.
"""

from __future__ import annotations

from typing import Any, Hashable, List, Tuple

Vertex = Hashable


def vertices(G: Any) -> List[Vertex]:
    """Return graph vertices as a list."""

    return list(G.nodes)


def directed_weighted_edges(G: Any, *, weight: str = "weight", default: float = 1.0) -> List[Tuple[Vertex, Vertex, float]]:
    """Extract directed weighted edges from a NetworkX-like graph."""

    return [(u, v, float(data.get(weight, default))) for u, v, data in G.edges(data=True)]


def undirected_weighted_edges(G: Any, *, weight: str = "weight", default: float = 1.0) -> List[Tuple[Vertex, Vertex, float]]:
    """Extract undirected weighted edges from a NetworkX-like graph."""

    return directed_weighted_edges(G, weight=weight, default=default)


def capacity_edges(G: Any, *, capacity: str = "capacity", default: float = 1.0) -> List[Tuple[Vertex, Vertex, float]]:
    """Extract directed capacity edges from a NetworkX-like graph."""

    return [(u, v, float(data.get(capacity, default))) for u, v, data in G.edges(data=True)]


def undirected_edges(G: Any) -> List[Tuple[Vertex, Vertex]]:
    """Extract undirected edges from a NetworkX-like graph."""

    return [(u, v) for u, v in G.edges()]
