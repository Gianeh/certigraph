# Proof-Carrying Graph Results: a small useful building block for verifiable computation

## Abstract

This note proposes a compact engineering pattern: every nontrivial graph computation should be able to emit a result plus a certificate that can be checked by a much smaller, independently auditable program. The accompanying `certigraph` package implements five such checkers: single-source shortest paths, minimum spanning forest, maximum flow, topological order, and bipartition.

The immediate value is modest but real: results from optimized solvers, distributed jobs, notebooks, or AI-generated code can be accepted or rejected without trusting the producer. The larger thesis is that scientific and infrastructure software should move from "trust my implementation" toward "verify this result."

## Core object

A proof-carrying result has four parts:

```text
(instance, output, certificate, checker_id)
```

The producer may be a conventional algorithm, a GPU kernel, an HPC workflow, a cloud service, or a code-generating model. The checker should be deterministic, small, and boring. For an auditable deployment, add:

```text
instance_hash, certificate_hash, checker_version, checker_hash, numeric_domain
```

## Five concrete certificates

### 1. Single-source shortest paths

Input: directed weighted graph `G=(V,E,w)` and source `s`.

Output: claimed distances `D[v]`, with `None` for unreachable vertices.

Certificate: for every reachable `v != s`, one parent edge `(u,v)` that realizes `D[v] = D[u] + w(u,v)`.

Checker:

1. `D[s] = 0`.
2. Parent pointers form actual source-rooted paths.
3. For every edge `(u,v)`, if `u` is reachable then `v` is reachable and `D[v] <= D[u] + w(u,v)`.

Why it works: parent paths prove each finite distance is attainable; edge inequalities prove no path can be shorter. This supports negative and zero edges as long as shortest distances are well-defined.

### 2. Minimum spanning forest

Input: undirected weighted graph.

Output/certificate: selected edge indices.

Checker:

1. Selected edges are acyclic.
2. Selected edges connect every connected component of the input graph.
3. For every non-selected edge `(u,v,w)`, the maximum-weight selected edge on the unique selected path from `u` to `v` has weight at most `w`.

Why it works: if a non-tree edge were cheaper than a path edge, exchanging it would reduce the tree. If no such exchange exists, the forest satisfies the cycle-optimality condition.

### 3. Maximum flow

Input: directed capacitated graph, source `s`, sink `t`.

Output: edge flows.

Certificate: edge flows plus the source side `S` of an `s-t` cut.

Checker:

1. Capacity constraints hold.
2. Flow conservation holds at all non-terminal vertices.
3. `s in S`, `t not in S`.
4. Flow value equals capacity of the cut.

Why it works: every feasible flow is bounded above by every cut capacity; equality proves both optimality of the flow and minimality of the cut.

### 4. Topological order

Certificate: a vertex permutation. Check that every edge points forward.

### 5. Bipartition

Certificate: a color for every vertex. Check that every edge crosses colors.

## Design choices

### Small TCB

The package separates producers from checkers. The producer can be wrong; its output is accepted only if the checker accepts the certificate.

### No dependencies

The checker layer uses only the Python standard library. This makes the logic easier to inspect and port.

### Friendly failure

Every checker returns a structured `CheckResult` rather than raising on an invalid certificate. This is useful in pipelines where certificates may be adversarial or produced by unreliable tools.

### Numeric honesty

The default tolerance is `1e-9`, suitable for demos but not for adversarial floating-point settings. A hardened version should use exact integer/rational domains or fixed decimal semantics.

## Research and engineering roadmap

The next useful step is not adding hundreds of graph algorithms. The next useful step is a common certificate envelope:

```json
{
  "problem": "sssp",
  "instance_hash": "sha256:...",
  "output": {...},
  "certificate": {...},
  "checker": {
    "name": "certigraph",
    "version": "0.1.0",
    "hash": "sha256:..."
  },
  "numeric_domain": "int64"
}
```

Then build adapters for real tools:

- NetworkX and graph-tool exporters.
- Routing and scheduling pipelines.
- Compiler dataflow analyses.
- HPC workflow managers.
- LLM code-generation agents that must attach checkable witnesses to their answers.

## Success criterion

A tool like this succeeds when researchers stop publishing naked graph outputs and start publishing:

```text
answer + certificate + checker
```

That small cultural shift would make computational claims easier to audit, reproduce, cache, and compose.

## References

- R. M. McConnell, K. Mehlhorn, S. Naeher, P. Schweitzer, "Certifying Algorithms", 2010. https://people.mpi-inf.mpg.de/~mehlhorn/ftp/CertifyingAlgorithms.pdf
- G. C. Necula, "Proof-Carrying Code", POPL 1997. https://dl.acm.org/doi/10.1145/263699.263712
- A. Chiesa and E. Tromer, "Proof-Carrying Data and Hearsay Arguments from Signature Cards", 2010. https://ic-people.epfl.ch/~achiesa/docs/CT10.pdf
- A. Shokry, A. Elmasry, A. Khalafallah, A. Aly, "Verifying Shortest Paths in Linear Time", arXiv:2412.06121, 2024. https://arxiv.org/abs/2412.06121
- R. Sedgewick and K. Wayne, "Minimum Spanning Trees", Algorithms, 4th edition companion site. https://algs4.cs.princeton.edu/43mst/
- "Max-flow min-cut theorem", overview and theorem statement. https://en.wikipedia.org/wiki/Max-flow_min-cut_theorem
