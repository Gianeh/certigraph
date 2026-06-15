# Research notes

CertiGraph is a software artifact inspired by two related traditions.

## Certifying algorithms

A certifying algorithm returns an output plus a witness that can be checked independently. This shifts the user’s trust from the producer to a smaller checker.

Useful entry points:

- R. M. McConnell, K. Mehlhorn, S. Näher, P. Schweitzer, **Certifying Algorithms**, 2011.
- M. Abdulaziz, et al., **Trustworthy Graph Algorithms**, MFCS 2019.

## Proof-carrying code and proof-carrying data

Proof-carrying code asks a producer to ship code with a machine-checkable proof of safety. CertiGraph applies the same broad spirit to graph results: ship the answer with evidence.

Useful entry point:

- G. C. Necula, **Proof-Carrying Code**, POPL 1997.

## Proof sketches for current checkers

### Single-source shortest paths

The certificate gives a distance for every vertex and a parent edge for every reachable non-source vertex.

The checker verifies:

1. parent chains form actual source-to-vertex paths with the claimed lengths;
2. every edge `(u, v, w)` satisfies `D[v] <= D[u] + w` when `u` is reachable;
3. no edge leaves the reachable region toward a vertex marked unreachable.

The parent paths prove the claimed distances are attainable. The edge inequalities prove no path can be shorter, by induction over path length.

### Minimum spanning forest

The certificate is the selected forest edge set.

The checker verifies:

1. selected edges are acyclic;
2. selected edges span every connected component of the input graph;
3. for every non-tree edge `(u, v)`, the maximum-weight edge on the selected `u-v` path is no heavier than `(u, v)`.

The third condition is the cycle optimality condition for MST/MSF.

### Maximum flow

The certificate is a flow value per edge plus an s-t cut.

The checker verifies:

1. capacity constraints;
2. flow conservation;
3. source is inside the cut and sink outside;
4. flow value equals cut capacity.

Weak duality says every feasible flow is at most every feasible cut. Equality certifies both maximum flow and minimum cut.

### Topological order

The certificate is a permutation of vertices. Every directed edge must go from earlier to later. This is exactly the definition of a topological ordering.

### Bipartition

The certificate assigns a color/side to every vertex. Every edge must connect unequal colors. This is exactly the definition of a bipartite graph.

### Connected components

The certificate assigns one label to each vertex.

The checker verifies:

1. every edge endpoint pair has the same claimed label;
2. graph-connected vertices are never split into different labels;
3. vertices from different graph components are never merged into one label.

These conditions are equivalent to partition equality between the claimed labeling and the graph's true connected components.

## Current limits

- Numeric checks currently use finite Python numbers with absolute tolerance.
- For adversarial numeric settings, exact integer/rational verification modes are still a roadmap item.
